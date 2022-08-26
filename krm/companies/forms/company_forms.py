from django import forms
from django.forms import ModelForm

from krm.companies.models import Company


class CompanyCreateForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["country"].widget.attrs["class"] = "form-select"
