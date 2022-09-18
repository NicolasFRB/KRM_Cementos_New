from django import forms
from django.forms import HiddenInput
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from krm.users.models import User


class PasswordForm(forms.Form):
    remember_key = forms.CharField(max_length=32)
    password1 = forms.CharField(
        label=_('Nuevo password'),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_('Nuevo password (confirmación)'),
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.fields['remember_key'].widget = HiddenInput()

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data['password2']
        if not password1 == password2:
            raise forms.ValidationError(_('Los passwords no coinciden'))
        user = get_object_or_404(
            User, remember_key=self.cleaned_data['remember_key'])
        validate_password(
            self.cleaned_data['password2'],
            user
        )
        return password2
