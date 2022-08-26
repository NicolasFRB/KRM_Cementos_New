from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from krc.business_group.models import BusinessGroup

from crispy_forms.helper import FormHelper
from crispy_forms.layout import(
    Layout, Fieldset,
    HTML, Field)


class BusinessGroupCreateForm(ModelForm):
    class Meta:
        model = BusinessGroup
        fields = [
            'name',
            'vat',
            'address',
            'state',
            'cp',
            'country',
            'email'
        ]

    def __init__(self, *argv, **kwargs):
        super(BusinessGroupCreateForm, self).__init__(*argv, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'

