from django.utils.translation import gettext as _
from django import forms
from django.forms import ModelForm

from krm.configuration.models.configuration import Configuration


class ConfigurationUpdateForm(ModelForm):
    class Meta:
        model = Configuration
        fields = [
            'app_name',
            'main_email',
        ]


class ImportForm(forms.Form):
    data_file = forms.FileField(
        label=_('Archivo de excel a importar')
    )
