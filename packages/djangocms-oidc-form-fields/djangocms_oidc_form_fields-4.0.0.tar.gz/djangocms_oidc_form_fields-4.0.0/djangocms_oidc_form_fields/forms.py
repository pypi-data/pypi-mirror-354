import json

from aldryn_forms.forms import FormSubmissionBaseForm

from .models import OIDCFormSubmission


class OIDCFormSubmissionBaseForm(FormSubmissionBaseForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = OIDCFormSubmission(
            name=self.form_plugin.name,
            language=self.form_plugin.language,
            form_url=self.request.build_absolute_uri(self.request.path),
        )

    def save(self, commit=False, user_info=None):
        self.instance.set_form_data(self)
        if user_info is not None:
            self.instance.user_info = json.dumps(user_info)
        self.instance.save()
