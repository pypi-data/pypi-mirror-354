import logging

from aldryn_forms.action_backends_base import BaseAction
from django.utils.translation import gettext_lazy as _
from djangocms_oidc.helpers import get_user_info

logger = logging.getLogger(__name__)


class DefaultAction(BaseAction):

    verbose_name = _('OIDC - Send email with handovered data and save to the site')

    def form_valid(self, cmsplugin, instance, request, form):
        user_info = get_user_info(request)
        recipients = cmsplugin.send_notifications(instance, form, user_info)
        form.instance.set_recipients(recipients)
        form.save(user_info=user_info)
        cmsplugin.send_success_message(instance, request)


class EmailAction(BaseAction):

    verbose_name = _('OIDC - Only send email with handovered data')

    def form_valid(self, cmsplugin, instance, request, form):
        recipients = cmsplugin.send_notifications(instance, form, get_user_info(request))
        logger.info(f'Sent email notifications to {len(recipients)} recipients.')
        cmsplugin.send_success_message(instance, request)
