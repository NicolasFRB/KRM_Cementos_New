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
