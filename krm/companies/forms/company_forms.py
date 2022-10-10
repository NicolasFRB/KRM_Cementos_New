from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.translation import gettext as _
from django.contrib.postgres.forms import SimpleArrayField

from krm.companies.models import Company
from krm.risks.models import RiskCompany


class CompanyCreateForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["country"].widget.attrs["class"] = "form-select"


class CompanyKrmRiskSelectForm(forms.Form):
    risk_pk = SimpleArrayField(forms.CharField(
        max_length=1000),  label=_('Riesgos-Compañías'))


class CompanyImportForm(forms.Form):
    companies_file = forms.FileField(
        label=_('Archivo de excel a importar')
    )
