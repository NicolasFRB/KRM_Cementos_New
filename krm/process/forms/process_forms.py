from django import forms
from django.forms import ModelForm

from krm.process.models import Process


class ProcessCreateForm(ModelForm):
    class Meta:
        model = Process
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["id"] = "process_description"
