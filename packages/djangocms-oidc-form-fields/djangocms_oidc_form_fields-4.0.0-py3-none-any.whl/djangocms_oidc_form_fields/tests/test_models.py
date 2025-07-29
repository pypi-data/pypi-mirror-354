from django.test import TestCase

from djangocms_oidc_form_fields.models import (
    OIDCElementPlugin,
    OIDCEmailFieldPlugin,
    OIDCFieldPlugin,
    OIDCTextAreaFieldPlugin,
)


class TestOIDCFieldPlugin(TestCase):

    def test_field_save(self):
        obj = OIDCFieldPlugin()
        obj.save()
        self.assertEqual(obj.pk, obj.cmsplugin_ptr_id)
        self.assertTrue(obj.FIELD_TYPE_OIDC)
        self.assertTrue(obj.unmodifiable)
        self.assertIsNone(obj.oidc_attributes)

    def test_field_save_with_params(self):
        obj = OIDCFieldPlugin(unmodifiable=False, oidc_attributes='{}')
        obj.save()
        self.assertEqual(obj.pk, obj.cmsplugin_ptr_id)
        self.assertFalse(obj.unmodifiable)
        self.assertEqual(obj.oidc_attributes, '{}')

    def test_copy_relations_no_option_set(self):
        field1 = OIDCFieldPlugin.objects.create()
        field2 = OIDCFieldPlugin.objects.create()
        field2.copy_relations(field1)

    def test_textarea_field_save(self):
        obj = OIDCTextAreaFieldPlugin()
        obj.save()
        self.assertEqual(obj.pk, obj.cmsplugin_ptr_id)
        self.assertTrue(obj.unmodifiable)
        self.assertIsNone(obj.oidc_attributes)
        self.assertIsNone(obj.text_area_columns)
        self.assertIsNone(obj.text_area_rows)

    def test_email_field_save(self):
        obj = OIDCEmailFieldPlugin()
        obj.save()
        self.assertEqual(obj.pk, obj.cmsplugin_ptr_id)
        self.assertTrue(obj.unmodifiable)
        self.assertIsNone(obj.oidc_attributes)
        self.assertFalse(obj.email_send_notification)
        self.assertEqual(obj.email_subject, "")
        self.assertEqual(obj.email_body, "")


class TestOIDCElementPlugin(TestCase):

    def test_field(self):
        obj = OIDCElementPlugin(oidc_attributes='given_name family_name')
        obj.save()
        self.assertEqual(obj.pk, obj.cmsplugin_ptr_id)
        self.assertEqual(obj.oidc_attributes, 'given_name family_name')
        self.assertEqual(str(obj), 'given_name family_name')
