from django import forms
from django.forms import ModelForm

from krm.companies.models import CompanyDomainRiskEvaluator


class CompanyDomainRiskEvaluatorsForm(ModelForm):
    class Meta:
        model = CompanyDomainRiskEvaluator
        fields = ['evaluator', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["evaluator"].widget.attrs["class"] = "form-select"
        self.fields["evaluator"].widget.attrs["data-control"] = "select2"
