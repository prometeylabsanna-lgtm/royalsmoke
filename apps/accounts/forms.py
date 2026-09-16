from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from apps.core.validation import EmailField, NameField, PasswordField, PhoneField, RequiredCheckboxField
from apps.core.validation.rules import validate_password


class EmailAuthenticationForm(AuthenticationForm):
    username = EmailField(label=_('Email'))


class RegisterForm(UserCreationForm):
    email = EmailField(label=_('Email'))
    first_name = NameField(label=_('Імʼя'), optional=True)
    last_name = NameField(label=_('Прізвище'), optional=True)
    phone = PhoneField(label=_('Телефон'), optional=True)
    age_confirm = RequiredCheckboxField(label=_('Підтвердження віку'))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'] = PasswordField(label=_('Пароль'))
        self.fields['password2'] = forms.CharField(
            label=_('Повторіть пароль'),
            widget=forms.PasswordInput(attrs={'data-rs-rule': 'password', 'autocomplete': 'new-password'}),
            strip=False,
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError(_('Паролі не збігаються'))
        if password2:
            err = validate_password(password2)
            if err:
                raise ValidationError(err)
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
