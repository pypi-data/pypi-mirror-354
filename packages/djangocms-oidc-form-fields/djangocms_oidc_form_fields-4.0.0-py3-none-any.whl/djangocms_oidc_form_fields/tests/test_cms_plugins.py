from aldryn_forms.models import FormPlugin
from cms.api import add_plugin, create_page
from cms.models import Placeholder
from cms.plugin_rendering import ContentRenderer
from cms.test_utils.testcases import CMSTestCase
from django.test import RequestFactory
from djangocms_oidc.constants import DJANGOCMS_USER_SESSION_KEY

from djangocms_oidc_form_fields.cms_plugins import OIDCSpanElement


class TestOIDCFormPlugin(CMSTestCase):

    def setUp(self):
        self.page = create_page('test page', 'test_page.html', 'en', apphook='FormsApp')
        self.placeholder = self.page.get_placeholders("en")[0]

    def test_get_with_session(self):
        form_plugin = add_plugin(self.placeholder, 'OIDCFormPlugin', 'en')
        add_plugin(self.placeholder, 'OIDCTextField', 'en', name='name', target=form_plugin,
                   unmodifiable=False, oidc_attributes='name')
        add_plugin(self.placeholder, 'OIDCEmailField', 'en', name='email', oidc_attributes='email', required=True,
                   target=form_plugin)
        add_plugin(self.placeholder, 'BooleanField', 'en', name='student', target=form_plugin)
        add_plugin(self.placeholder, 'OIDCBooleanField', 'en', name='validated', target=form_plugin,
                   oidc_attributes='validated')
        add_plugin(self.placeholder, 'OIDCTextAreaField', 'en', name='address', target=form_plugin,
                   oidc_attributes='address')

        session = self.client.session
        session[DJANGOCMS_USER_SESSION_KEY] = {
            'email': 'mail@foo.foo',
            'name': 'Tester',
            'validated': True,
            'address': {'formatted': 'Street 42\n123 00 City'}
        }
        session.save()

        response = self.client.get(self.page.get_absolute_url('en'))

        self.assertContains(
            response,
            """<input type="email" name="email" value="mail@foo.foo" class="" required disabled id="id_email">""",
            html=True)
        self.assertContains(
            response,
            """<input type="text" name="name" value="Tester" class="" id="id_name">""",
            html=True)
        self.assertContains(
            response, """<input type="checkbox" name="student" class="" id="id_student">""", html=True)
        self.assertContains(
            response,
            """<input type="checkbox" name="validated" value="True" class="" disabled id="id_validated" checked>""",
            html=True)
        self.assertContains(
            response, """
                <textarea name="address" type="text" class="" disabled id="id_address">
                    Street 42
                    123 00 City
                </textarea>""", html=True)

    def test_get_without_session(self):
        form_plugin = add_plugin(self.placeholder, 'OIDCFormPlugin', 'en')
        add_plugin(self.placeholder, 'OIDCTextField', 'en', name='name', required=True, target=form_plugin)
        add_plugin(self.placeholder, 'OIDCEmailField', 'en', name='email', required=True, target=form_plugin,
                   oidc_attributes='email')
        response = self.client.get(self.page.get_absolute_url('en'))
        self.assertContains(
            response, """<input type="text" name="name" class="" required disabled id="id_name">""", html=True)
        self.assertContains(
            response, """<input type="email" name="email" class="" required disabled id="id_email">""", html=True)

    def test_post(self):
        form_plugin = add_plugin(self.placeholder, 'OIDCFormPlugin', 'en')
        add_plugin(self.placeholder, 'OIDCEmailField', 'en', name='email', required=True, target=form_plugin,
                   oidc_attributes='email')

        aldryn_form = FormPlugin.objects.last()
        session = self.client.session
        session[DJANGOCMS_USER_SESSION_KEY] = {
            'email': 'mail@foo.foo',
        }
        session.save()

        response = self.client.post(self.page.get_absolute_url('en'), {
            "form_plugin_id": aldryn_form.pk,
            "email": "tester@foo.foo"
        })
        self.assertContains(response, "Thank you for submitting your information.")

    def test_post_invalid(self):
        form_plugin = add_plugin(self.placeholder, 'OIDCFormPlugin', 'en')
        add_plugin(self.placeholder, 'OIDCEmailField', 'en', name='email', required=True, target=form_plugin,
                   oidc_attributes='email')

        aldryn_form = FormPlugin.objects.last()

        response = self.client.post(self.page.get_absolute_url('en'), {
            "form_plugin_id": aldryn_form.pk,
            "email": "tester@foo.foo"
        })
        self.assertEqual(response.context['form'].errors, {'email': ['This field is required.']})


class TestOIDCElementPlugin(CMSTestCase):

    def _create_model(self, plugin_class, **kwargs):
        placeholder = Placeholder.objects.create(slot='test')
        model_instance = add_plugin(
            placeholder,
            plugin_class,
            'en',
            **kwargs
        )
        return model_instance

    def _create_request(self, data=None):
        request = RequestFactory().request()
        request.session = {}
        if data is not None:
            request.session[DJANGOCMS_USER_SESSION_KEY] = data
        return request

    def test_no_attrs(self):
        model_instance = self._create_model(OIDCSpanElement, oidc_attributes="given_name")
        request = self._create_request()
        renderer = ContentRenderer(request=request)
        html = renderer.render_plugin(model_instance, {'request': request})
        self.assertHTMLEqual(html, """<span class="oidc-data given_name"></span>""")

    def test_with_attrs(self):
        model_instance = self._create_model(OIDCSpanElement, oidc_attributes="given_name")
        request = self._create_request({"given_name": "The Tester"})
        renderer = ContentRenderer(request=request)
        html = renderer.render_plugin(model_instance, {'request': request})
        self.assertHTMLEqual(html, """<span class="oidc-data given_name">The Tester</span>""")

    def test_with_formatted_attrs(self):
        model_instance = self._create_model(OIDCSpanElement, oidc_attributes="address")
        request = self._create_request({'address': {'formatted': 'Street 42\n123 00 City'}})
        renderer = ContentRenderer(request=request)
        html = renderer.render_plugin(model_instance, {'request': request})
        self.assertHTMLEqual(html, """<span class="oidc-data address">Street 42\n123 00 City</span>""")

    def test_with_multilevel_attrs(self):
        model_instance = self._create_model(OIDCSpanElement, oidc_attributes="address.location.city")
        request = self._create_request({"address": {"location": {"city": "Prague"}}})
        renderer = ContentRenderer(request=request)
        html = renderer.render_plugin(model_instance, {'request': request})
        self.assertHTMLEqual(html, """<span class="oidc-data addresslocationcity">Prague</span>""")
