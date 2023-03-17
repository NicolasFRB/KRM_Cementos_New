from django import forms
from django.utils.translation import gettext as _
from django.forms import ModelForm

from krm.companies.models import CompanyControls


class ControlCompanySelectForm(forms.Form):
    company_pk = forms.IntegerField(
        label=_('Compañía')
    )


class ControlCompanyUpdateForm(ModelForm):
    class Meta:
        model = CompanyControls
        fields = ['active', 'control_test_owners', 'control_test_supervisors']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["control_test_owners"].widget.attrs["class"] = "form-select"
        self.fields["control_test_owners"].widget.attrs["data-control"] = "select2"
        self.fields["control_test_supervisors"].widget.attrs["class"] = "form-select"
        self.fields["control_test_supervisors"].widget.attrs["data-control"] = "select2"
