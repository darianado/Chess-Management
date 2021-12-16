from django import forms
from django.test import TestCase
from clubs.models import User
from clubs.helpers import Status
from clubs.forms import SetMatchResultForm

class SetMatchResultFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            'match_status': Status.WON_A.value
        }

    def test_form_has_necessary_fields(self):
        form = SetMatchResultForm()
        self.assertIn('match_status', form.fields)

    def test_form_match_status_field_is_using_select_widget(self):
        form = SetMatchResultForm()
        self.assertTrue(isinstance(form.fields["match_status"].widget, forms.Select))

    def test_valid_form(self):
        form = SetMatchResultForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_with_invalid_status_5(self):
        self.form_input["match_status"] = 5
        form = SetMatchResultForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_with_invalid_status_0(self):
        self.form_input["match_status"] = 0
        form = SetMatchResultForm(data=self.form_input)
        self.assertFalse(form.is_valid())
