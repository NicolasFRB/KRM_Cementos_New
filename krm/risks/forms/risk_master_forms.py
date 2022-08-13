from django import forms
from django.forms import ModelForm

from krm.risks.models import RiskMaster


class RiskMasterCreateForm(ModelForm):
    class Meta:
        model = RiskMaster
        fields = [
            'ref',
            'name',
            'description',
            'domain_risk',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["id"] = "risk_master_description"
        self.fields["domain_risk"].widget.attrs["class"] = "form-select"
        self.fields["domain_risk"].widget.attrs["data-control"] = "select2"
