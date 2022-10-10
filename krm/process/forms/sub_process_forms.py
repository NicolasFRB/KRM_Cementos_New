from django import forms
from django.forms import ModelForm

from django.utils.translation import gettext_lazy as _
from krm.process.models import SubProcess


class SubProcessCreateForm(ModelForm):
    class Meta:
        model = SubProcess
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["id"] = "subprocess_description"
        self.fields["process"].widget.attrs["class"] = "form-select"
        self.fields["process"].widget.attrs["data-control"] = "select2"
