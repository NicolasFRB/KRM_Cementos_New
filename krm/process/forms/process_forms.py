from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from krm.process.models import Process


class ProcessCreateForm(ModelForm):
    class Meta:
        model = Process
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["id"] = "process_description"

    def clean_ref(self):
        ref = self.cleaned_data.get("ref").upper()
        if Process.objects.filter(ref=ref).count() > 0:
            raise forms.ValidationError(
                _('Ya existe un proceso con esa REF'))
        return ref
