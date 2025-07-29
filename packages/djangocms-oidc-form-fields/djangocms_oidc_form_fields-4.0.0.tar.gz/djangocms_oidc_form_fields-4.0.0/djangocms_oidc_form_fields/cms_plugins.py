import logging
import re
from typing import Optional

from aldryn_forms.cms_plugins import (
    BooleanField,
    EmailField,
    FormPlugin,
    HiddenField,
    NumberField,
    PhoneField,
    TextAreaField,
    TextField,
)
from aldryn_forms.helpers import get_user_name
from aldryn_forms.signals import form_post_save, form_pre_save
from aldryn_forms.validators import is_valid_recipient
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django import forms
from django.conf import settings
from django.utils.encoding import force_str
from django.utils.translation import get_language, gettext_lazy as _
from djangocms_oidc.helpers import get_user_info
from emailit.api import send_mail
from emailit.utils import get_template_names

from .forms import OIDCFormSubmissionBaseForm
from .models import OIDCElementPlugin, OIDCEmailFieldPlugin, OIDCFieldPlugin, OIDCTextAreaFieldPlugin

logger = logging.getLogger(__name__)


@plugin_pool.register_plugin
class OIDCFormPlugin(FormPlugin):
    name = _('OIDC Form')
    module = _('OpenID Connect Form')

    def process_form(self, instance, request):
        form_class = self.get_form_class(instance, request)
        form_kwargs = self.get_form_kwargs(instance, request)
        form = form_class(**form_kwargs)

        if request.POST.get('form_plugin_id') == str(instance.id) and form.is_valid():
            fields = [field for field in form.base_fields.values()
                      if hasattr(field, '_plugin_instance')]

            # pre save field hooks
            for field in fields:
                field._plugin_instance.form_pre_save(
                    instance=field._model_instance,
                    form=form,
                    request=request,
                )

            form_pre_save.send(
                sender=FormPlugin,
                instance=instance,
                form=form,
                request=request,
            )

            self.form_valid(instance, request, form)

            # post save field hooks
            for field in fields:
                field._plugin_instance.form_post_save(
                    instance=field._model_instance,
                    form=form,
                    request=request,
                )

            form_post_save.send(
                sender=FormPlugin,
                instance=instance,
                form=form,
                request=request,
            )
        elif request.POST.get('form_plugin_id') == str(instance.id) and request.method == 'POST':
            # only call form_invalid if request is POST and form is not valid
            self.form_invalid(instance, request, form)
        return form

    def get_form_class(self, instance, request=None):
        """
        Constructs form class basing on children plugin instances.
        """
        fields = self.get_form_fields(instance, request)
        formClass = (
            type(OIDCFormSubmissionBaseForm)
            ('OIDCAldrynDynamicForm', (OIDCFormSubmissionBaseForm,), fields)
        )
        return formClass

    def get_form_fields(self, instance, request=None):
        form_fields = {}
        fields = instance.get_form_fields()
        for field in fields:
            plugin_instance = field.plugin_instance
            field_plugin = plugin_instance.get_plugin_class_instance()
            if hasattr(plugin_instance, 'FIELD_TYPE_OIDC'):
                form_fields[field.name] = field_plugin.get_form_field(plugin_instance, request)
            else:
                form_fields[field.name] = field_plugin.get_form_field(plugin_instance)
        return form_fields

    def send_notifications(self, instance, form, user_info=None):
        users = instance.recipients.exclude(email='')

        recipients = [user for user in users.iterator()
                      if is_valid_recipient(user.email)]

        formatters = getattr(settings, 'DJANGOCMS_OIDC_FORM_FIELDS_ADMIN_USER_INFO', {})
        user_info_data = []
        if user_info is not None:
            for key in sorted(user_info.keys()):
                value = formatters.get(key, lambda v: v)(user_info[key])
                user_info_data.append((key.replace('_', ' '), value))
        context = {
            'form_name': instance.name,
            'form_data': form.get_serialized_field_choices(),
            'form_plugin': instance,
            'user_info_data': user_info_data,
        }

        reply_to = None
        for field_name, field_instance in form.fields.items():
            if hasattr(field_instance, '_model_instance') and \
                    field_instance._model_instance.plugin_type == 'EmailField':
                if form.cleaned_data.get(field_name):
                    reply_to = [form.cleaned_data[field_name]]
                    break

        subject_template_base = getattr(
            settings, 'ALDRYN_FORMS_EMAIL_SUBJECT_TEMPLATES_BASE',
            getattr(settings, 'ALDRYN_FORMS_EMAIL_TEMPLATES_BASE', None))
        if subject_template_base:
            language = instance.language or get_language()
            subject_templates = get_template_names(language, subject_template_base, 'subject', 'txt')
        else:
            subject_templates = None

        send_mail(
            recipients=[user.email for user in recipients],
            context=context,
            template_base=getattr(
                settings, 'DJANGOCMS_OIDC_FORM_FIELDS_EMAIL_TEMPLATES_BASE',
                'djangocms_oidc_form_fields/emails/notification'
            ),
            subject_templates=subject_templates,
            language=instance.language,
            reply_to=reply_to,
        )

        users_notified = [
            (get_user_name(user), user.email) for user in recipients]
        return users_notified


class OIDCGetValueMixin:

    def get_oidc_values(self, user_info: Optional[dict[str, str]], attributes: str) -> list[str]:
        """Get OIDC values."""
        values = []
        if user_info is None:
            return values
        for key in re.split(r'\s+', attributes):
            if "." in key:
                chunks = key.split(".")
                values.extend(self.get_oidc_values(user_info.get(chunks[0]), ".".join(chunks[1:])))
            else:
                value = user_info.get(key)
                if isinstance(value, dict) and value.get('formatted'):
                    value = value['formatted']
                values.append("" if value is None else force_str(value))
        return values

    def get_oidc_attribute_value(self, user_info: dict[str, str], attributes: str) -> str:
        """Get OIDC attribute value."""
        return " ".join(self.get_oidc_values(user_info, attributes))


class OIDCFieldMixin(OIDCGetValueMixin):
    module = _('OpenID Connect Form Field')
    model = OIDCFieldPlugin

    form_field_enabled_options = [
        'unmodifiable',
        'oidc_attributes',
    ] + TextField.form_field_enabled_options
    fieldset_general_fields = [
        'unmodifiable',
        'oidc_attributes',
    ] + TextField.fieldset_general_fields

    def get_form_field(self, instance, request=None):
        form_field_class = self.get_form_field_class(instance)
        form_field_kwargs = self.get_form_field_kwargs(instance, request)
        if issubclass(form_field_class, forms.fields.BooleanField) and 'max_length' in form_field_kwargs:
            form_field_kwargs.pop('max_length')
        field = form_field_class(**form_field_kwargs)
        # allow fields access to their model plugin class instance
        field._model_instance = instance
        # and also to the plugin class instance
        field._plugin_instance = self
        return field

    def get_form_field_kwargs(self, instance, request=None):
        kwargs = super().get_form_field_kwargs(instance)
        if instance.unmodifiable:
            kwargs['disabled'] = True
        if request is not None and instance.oidc_attributes:
            user_info = get_user_info(request)
            if user_info is not None:
                kwargs['initial'] = self.get_oidc_attribute_value(user_info, instance.oidc_attributes)
        return kwargs


@plugin_pool.register_plugin
class OIDCTextField(OIDCFieldMixin, TextField):
    name = _('OIDC Text Field')


@plugin_pool.register_plugin
class OIDCTextAreaField(OIDCFieldMixin, TextAreaField):
    name = _('OIDC Text Area Field')
    model = OIDCTextAreaFieldPlugin


@plugin_pool.register_plugin
class OIDCHiddenField(OIDCFieldMixin, HiddenField):
    name = _('OIDC Hidden Field')


@plugin_pool.register_plugin
class OIDCPhoneField(OIDCFieldMixin, PhoneField):
    name = _('OIDC Phone Field')


@plugin_pool.register_plugin
class OIDCNumberField(OIDCFieldMixin, NumberField):
    name = _('OIDC Number Field')


@plugin_pool.register_plugin
class OIDCEmailField(OIDCFieldMixin, EmailField):
    name = _('OIDC Email Field')
    model = OIDCEmailFieldPlugin


@plugin_pool.register_plugin
class OIDCBooleanField(OIDCFieldMixin, BooleanField):
    name = _('OIDC Yes/No Field')


@plugin_pool.register_plugin
class OIDCSpanElement(OIDCGetValueMixin, CMSPluginBase):
    name = _('OIDC Span element')
    module = _('OpenID Connect Elements')
    model = OIDCElementPlugin
    render_template = "djangocms_oidc_form_fields/span.html"
    cache = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        request = context["request"]
        user_info = get_user_info(request)
        if user_info is not None:
            context["oidc_hangovered_value"] = self.get_oidc_attribute_value(user_info, instance.oidc_attributes)
        elif hasattr(request, 'toolbar') and request.toolbar.edit_mode_active:
            context["oidc_hangovered_value"] = instance.oidc_attributes
        return context
