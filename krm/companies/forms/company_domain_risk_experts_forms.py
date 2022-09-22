from django import forms
from django.forms import ModelForm

from krm.companies.models import CompanyDomainRiskExperts


class CompanyDomainRiskExpertsForm(ModelForm):
    class Meta:
        model = CompanyDomainRiskExperts
        fields = ['expert', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["expert"].widget.attrs["class"] = "form-select"
