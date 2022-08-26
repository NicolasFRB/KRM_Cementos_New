from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from krc.business_group.models import Company

from crispy_forms.helper import FormHelper
from crispy_forms.layout import(
    Layout, Fieldset,
    HTML, Field)

from django_countries.data import COUNTRIES


class CompanyCreateForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

        widgets = {'business_group': forms.HiddenInput()}

    # def __init__(self, *argv, **kwargs):
    #     super(CompanyCreateForm, self).__init__(*argv, **kwargs)
        # self.fields['countries'].widget.attrs['class'] = 'kt-select2'


class CompanyImportForm(forms.Form):
    companies_file = forms.FileField(label=_(u'Archivo de excel a importar'))
