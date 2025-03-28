from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

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
            'event_speed',
            'probability_residual',
            'krm_activity_affected',
            'krm_main_events',
            'krm_exposed_staff',
            'krm_main_elements'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["id"] = "risk_description"
        self.fields["krm_activity_affected"].widget.attrs["id"] = "krm_activity_affected"
        self.fields["krm_main_events"].widget.attrs["id"] = "krm_main_events"
        self.fields["krm_exposed_staff"].widget.attrs["id"] = "krm_exposed_staff"
        self.fields["krm_main_elements"].widget.attrs["id"] = "krm_main_elements"

        self.fields["risk_master"].widget.attrs["class"] = "form-select"
        self.fields["risk_master"].widget.attrs["data-control"] = "select2"
        self.fields["impact_inherent"].widget.attrs["class"] = "form-select"
        self.fields["probability_inherent"].widget.attrs["class"] = "form-select"
        self.fields["impact_residual"].widget.attrs["class"] = "form-select"
        self.fields["probability_residual"].widget.attrs["class"] = "form-select"
        self.fields["event_speed"].widget.attrs["class"]= "form-select"
