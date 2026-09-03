"""Тести правил валідації."""

from django.test import SimpleTestCase

from apps.core.validation.rules import (
    run_rule,
    validate_email,
    validate_name,
    validate_password,
    validate_phone,
    validate_url,
)
from apps.leads.views import CallbackForm


class ValidationRulesTests(SimpleTestCase):
    def test_name(self):
        self.assertIsNone(validate_name('Олег'))
        self.assertIsNotNone(validate_name('A'))
        self.assertIsNotNone(validate_name('Oleg123'))

    def test_email(self):
        self.assertIsNone(validate_email('user@example.com'))
        self.assertIsNotNone(validate_email('bad@'))
        self.assertIsNotNone(validate_email('no-at'))

    def test_password(self):
        self.assertIsNone(validate_password('Secret1!'))
        self.assertIsNotNone(validate_password('short1!'))
        self.assertIsNotNone(validate_password('alllowercase1!'))
        self.assertIsNotNone(validate_password('ALLUPPERCASE1!'))
        self.assertIsNotNone(validate_password('NoDigits!'))
        self.assertIsNotNone(validate_password('NoSpecial1'))

    def test_phone_international(self):
        self.assertIsNone(validate_phone('+380 44 000 00 00'))
        self.assertIsNone(validate_phone('+1 (202) 555-0123'))
        self.assertIsNone(validate_phone('380441112233'))
        self.assertIsNotNone(validate_phone('123'))
        self.assertIsNotNone(validate_phone('abcdefghi'))

    def test_url(self):
        self.assertIsNone(validate_url('https://example.com/x'))
        self.assertIsNone(validate_url('/catalog/'))
        self.assertIsNotNone(validate_url('not a url'))

    def test_optional_empty(self):
        self.assertIsNone(run_rule('email', '', optional=True))
        self.assertIsNone(run_rule('phone', '  ', optional=True))
        self.assertIsNotNone(run_rule('email', 'bad', optional=True))

    def test_callback_form(self):
        form = CallbackForm(data={'name': '', 'phone': '+380501112233'})
        self.assertTrue(form.is_valid())
        form_bad = CallbackForm(data={'name': 'A1', 'phone': '12'})
        self.assertFalse(form_bad.is_valid())
        self.assertIn('phone', form_bad.errors)
