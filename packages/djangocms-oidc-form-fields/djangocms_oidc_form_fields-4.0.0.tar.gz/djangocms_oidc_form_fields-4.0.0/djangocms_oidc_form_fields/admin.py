import json

from aldryn_forms.admin import FormSubmissionAdmin
from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import OIDCFormSubmission


class OIDCFormSubmissionAdmin(FormSubmissionAdmin):

    readonly_fields = FormSubmissionAdmin.readonly_fields + ['get_user_info_for_display']
    export_fields = FormSubmissionAdmin.export_fields + (
        ('user_info', _('user info'), True),
    )
    change_list_template = "admin/aldryn_forms/formsubmission/change_list.html"

    class Media:
        css = {
             'all': ('djangocms_oidc_form_fields/admin/form_submission.css', )
        }

    def get_user_info_for_display(self, obj):
        content = []
        if obj.user_info is not None:
            formatters = getattr(settings, 'DJANGOCMS_OIDC_FORM_FIELDS_ADMIN_USER_INFO', {})
            data = json.loads(obj.user_info)
            for key in sorted(data.keys()):
                value = formatters.get(key, lambda v: v)(data[key])
                content.append("<div><span>{}:</span> <span>{}</span></div>".format(key.replace('_', ' '), value))
        return mark_safe("<div class='admin-user-info'>{}</div>".format("\n".join(content)))
    get_user_info_for_display.allow_tags = True
    get_user_info_for_display.short_description = _('Handovered data')

    def export_field_parse_user_info(self, submission):
        """Parse export form field user_info."""
        fields, values = {}, {}
        values = json.loads(submission.user_info)
        for name in values.keys():
            fields[name] = name.replace("_", " ")
        return fields, values


admin.site.register(OIDCFormSubmission, OIDCFormSubmissionAdmin)
