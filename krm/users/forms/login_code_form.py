from django import forms
from django.forms import HiddenInput
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404
from krm.users.models import User


class LoginCodeForm(forms.Form):
    login_code = forms.CharField(
        max_length=140,
        label='Código de inicio de sesión'
    )
