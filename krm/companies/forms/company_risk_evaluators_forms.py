from django import forms
from django.forms import ModelForm

from krm.risks.models import RiskCompany


class CompanyRiskEvaluatorsForm(ModelForm):
    class Meta:
        model = RiskCompany
        fields = ['evaluator', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["evaluator"].widget.attrs["class"] = "form-select"
        self.fields["evaluator"].widget.attrs["data-control"] = "select2"
        self.fields["evaluator"].label= ""
