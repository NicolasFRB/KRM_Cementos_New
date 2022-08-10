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
        # self.helper = FormHelper()
        # self.helper.form_class = 'login-form kt-form'
        # self.helper.form_show_labels = False
        self.fields['remember_key'].widget = HiddenInput()
        # self.helper.layout = Layout(
        #     Field('remember_key'),
        #     Field('password1', required="true",
        #           placeholder=_("Nueva contraseña *")),
        #     Field('password2', required="true", placeholder=_(
        #         "Repite tu nueva contraseña *")),
        #     HTML("""
        #         <div class="row kt-login__actions">
        #             <button class="btn btn-primary btn-sm">%(enter_text)s</button>
        #             <a href="%(cancel_link_url)s" class="kt-link">%(cancel_link_text)s</a>
        #         </div>
        #     """ % {
        #         'cancel_link_url': reverse('users:login'),
        #         'cancel_link_text': _('Cancelar'),
        #         'enter_text': _('Guardar')
        #     })
        # )

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
