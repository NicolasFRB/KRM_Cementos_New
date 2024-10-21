from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _

from krm.remediation_plans.models import RemediationPlan


class RemediationPlanCreateForm(ModelForm):
    class Meta:
        model = RemediationPlan
        fields = '__all__'
        exclude = ['status', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["control"].widget.attrs["class"] = "form-select"
        self.fields["control"].widget.attrs["data-control"] = "select2"

        self.fields["responsible"].widget.attrs["class"] = "form-select"
        self.fields["responsible"].widget.attrs["data-control"] = "select2"

        self.fields["supervisor"].widget.attrs["class"] = "form-select"
        self.fields["supervisor"].widget.attrs["data-control"] = "select2"

        self.fields["additional_users"].widget.attrs["class"] = "form-select"
        self.fields["additional_users"].widget.attrs["data-control"] = "select2"

        self.fields["date_begin"].widget.attrs["id"] = "e_date_begin"
        self.fields["date_end"].widget.attrs["id"] = "e_date_end"

        self.fields["date_begin"].widget.attrs["class"] = "datepicker"
        self.fields["date_end"].widget.attrs["class"] = "datepicker"


class RemediationPlanUpdateForm(ModelForm):
    class Meta:
        model = RemediationPlan
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["control"].widget.attrs["class"] = "form-select"
        self.fields["control"].widget.attrs["data-control"] = "select2"

        self.fields["responsible"].widget.attrs["class"] = "form-select"
        self.fields["responsible"].widget.attrs["data-control"] = "select2"

        self.fields["supervisor"].widget.attrs["class"] = "form-select"
        self.fields["supervisor"].widget.attrs["data-control"] = "select2"

        self.fields["additional_users"].widget.attrs["class"] = "form-select"
        self.fields["additional_users"].widget.attrs["data-control"] = "select2"

        self.fields["status"].widget.attrs["class"] = "form-select"
        self.fields["status"].widget.attrs["data-control"] = "select2"

        self.fields["next_to_reply"].widget.attrs["class"] = "form-select"
        self.fields["next_to_reply"].widget.attrs["data-control"] = "select2"

        self.fields["date_begin"].widget.attrs["id"] = "e_date_begin"
        self.fields["date_end"].widget.attrs["id"] = "e_date_end"

        self.fields["date_begin"].widget.attrs["class"] = "datepicker"
        self.fields["date_end"].widget.attrs["class"] = "datepicker"
