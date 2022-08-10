from django import forms
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, HTML


class RememberForm(forms.Form):
    email = forms.CharField(max_length=140, label=_(u'Email'))

    # def __init__(self, *args, **kwargs):
    #     super(RememberForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.form_class = 'login-form kt-form'
    #     self.helper.form_show_labels = False
    #     self.helper.layout = Layout(
    #         Field('email', placeholder=_("Introduzca su email *"), required="true"),
    #         HTML(u"""
    #             <div class="row kt-login__actions">
    #                 <button class="btn btn-primary btn-sm">"""), HTML(_("Recordar contraseña")), HTML("""</button>
    #             </div>
    #         </form>
    #         """)
    #     )
