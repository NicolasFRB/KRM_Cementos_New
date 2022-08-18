from django import forms
from django.forms import ModelForm

from krm.controls.models import Control


class ControlCreateForm(ModelForm):
    class Meta:
        model = Control
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["id"] = "control_name"
        self.fields["description"].widget.attrs["id"] = "control_description"
        self.fields["testing_procedure"].widget.attrs["id"] = "control_testing_procedure"

        self.fields["risk"].widget.attrs["class"] = "form-select"
        self.fields["control_type"].widget.attrs["class"] = "form-select"
        self.fields["automation"].widget.attrs["class"] = "form-select"
        self.fields["control_frequency"].widget.attrs["class"] = "form-select"

        self.fields["is_gap"].widget.attrs["class"] = "form-select"
        self.fields["assert_existence"].widget.attrs["class"] = "form-select"
        self.fields["assert_completeness"].widget.attrs["class"] = "form-select"
        self.fields["assert_valuation"].widget.attrs["class"] = "form-select"
        self.fields["assert_rights"].widget.attrs["class"] = "form-select"
        self.fields["assert_disclosure"].widget.attrs["class"] = "form-select"
        self.fields["assert_accurancy"].widget.attrs["class"] = "form-select"
        self.fields["assert_froud"].widget.attrs["class"] = "form-select"
