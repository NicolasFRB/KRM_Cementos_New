from django import forms
from django.forms import ModelForm

from krm.risks.models import RiskCompany


class CompanyRiskExpertsForm(ModelForm):
    class Meta:
        model = RiskCompany
        fields = ['expert', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["expert"].widget.attrs["class"] = "form-select"
        self.fields["expert"].widget.attrs["data-control"] = "select2"
        self.fields["expert"].label= ""
