from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

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
        self.fields["description"].widget.attrs["id"] = "risk_description"
