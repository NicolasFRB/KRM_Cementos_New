from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from django.core.validators import FileExtensionValidator

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

        self.fields["risks"].widget.attrs["class"] = "form-select"
        self.fields["sub_processes"].widget.attrs["class"] = "form-select"
        self.fields["risks"].widget.attrs["data-control"] = "select2"
        self.fields["sub_processes"].widget.attrs["data-control"] = "select2"

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


class ControlImportForm(ModelForm):
    controls_file = forms.FileField(
        label=_("Archivo de excel a importar"),
        validators=[FileExtensionValidator(
            allowed_extensions=["xlsx", "xls"])],
    )

    class Meta:
        model = Control
        fields = []

    def __init__(self, *args, **kwargs):
        super(ControlImportForm, self).__init__(*args, **kwargs)
