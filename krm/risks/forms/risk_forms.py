from django import forms
from django.forms import ModelForm

from krm.risks.models import Risk


class RiskCreateForm(ModelForm):
    class Meta:
        model = Risk
        fields = [
            'ref',
            'name',
            'description',
            'risk_master',
            'impact_inherent',
            'probability_inherent',
            'impact_residual',
            'probability_residual',

        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["id"] = "risk_description"
        self.fields["risk_master"].widget.attrs["class"] = "form-select"
        self.fields["risk_master"].widget.attrs["data-control"] = "select2"
        self.fields["impact_inherent"].widget.attrs["class"] = "form-select"
        self.fields["probability_inherent"].widget.attrs["class"] = "form-select"
        self.fields["impact_residual"].widget.attrs["class"] = "form-select"
        self.fields["probability_residual"].widget.attrs["class"] = "form-select"
