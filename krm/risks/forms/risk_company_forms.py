from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from krm.risks.models import RiskCompany


class RiskCompanyUpdateForm(ModelForm):
    class Meta:
        model = RiskCompany
        fields = [
            'name',
            'description',
            'krm_activity_affected',
            'krm_main_events',
            'krm_exposed_staff',
            'krm_main_elements',
            'evaluator',
            'expert'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["id"] = "risk_description"
        self.fields["evaluator"].widget.attrs["id"] = "risk_evaluator"
        self.fields["expert"].widget.attrs["id"] = "risk_expert"
        self.fields["krm_activity_affected"].widget.attrs["id"] = "krm_activity_affected"
        self.fields["krm_main_events"].widget.attrs["id"] = "krm_main_events"
        self.fields["krm_exposed_staff"].widget.attrs["id"] = "krm_exposed_staff"
        self.fields["krm_main_elements"].widget.attrs["id"] = "krm_main_elements"
