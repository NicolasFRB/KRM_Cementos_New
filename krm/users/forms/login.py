from django import forms
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML

from django.conf import settings


class LoginForm(forms.Form):
    username = forms.CharField(label=_("Email"))
    password = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput())

    # def __init__(self, *args, **kwargs):
    #     super(LoginForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_class = 'form'
    #     self.helper.form_show_labels = True
    #     # injected_html =
    #     self.helper.layout = Layout(
    #         Field('username', placeholder=_(u"Correo electrónico *"),
    #               css_class='form-control'),
    #         Field('password', placeholder="Password *",
    #               css_class='form-control'),
    #         HTML("""
    #             <div class="row kt-login__actions">
    #                 <a href="%(remember_link_url)s" class="kt-link kt-login__link-forgot">%(remember_link_text)s</a>
    #                 <button class="btn btn-sm btn-primary btn-elevate">%(enter_text)s</button>
    #             </div>
    #         """ % {
    #             'remember_link_url': reverse('users:remember_password_form'),
    #             'remember_link_text': _('¿Ha olvidado su contraseña?'),
    #             'enter_text': _('Entrar')
    #         })
    #     )
