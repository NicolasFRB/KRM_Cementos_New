from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from krm.risks.models import DomainRisk


class DomainRiskCreateForm(ModelForm):
    class Meta:
        model = DomainRisk
        fields = [
            'ref',
            'name',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["id"] = "domain_risk_description"
