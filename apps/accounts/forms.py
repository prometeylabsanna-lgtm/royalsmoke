from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from apps.accounts.models import User


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Імʼя', max_length=150, required=False)
    last_name = forms.CharField(label='Прізвище', max_length=150, required=False)
    phone = forms.CharField(label='Телефон', max_length=30, required=False)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
