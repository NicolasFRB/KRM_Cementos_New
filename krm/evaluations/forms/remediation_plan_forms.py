from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import NON_FIELD_ERRORS

from krm.evaluations.models import RemediationPlan

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Field


class RemediationPlanCreateForm(ModelForm):
    class Meta:
        model = RemediationPlan
        fields = [
            "description",
            "date_end",
            "attachment"
        ]

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) == 0:
            raise forms.ValidationError("Campo obligatorio")        
        elif len(description) < 20:
            raise forms.ValidationError("Debe proporcionar información suficiente para finalizar la evaluación")
        elif len(description) < 5000:
            return description
        else:
            raise forms.ValidationError("Muy largo")

    def __init__(self, *argv, **kwargs):
        super(RemediationPlanCreateForm, self).__init__(*argv, **kwargs)
        self.fields["date_end"].widget.attrs["class"] = "datepicker"
        self.fields["description"].widget.attrs["id"] = "cta_description"


class RemediationPlanUpdateForm(ModelForm):
    class Meta:
        model = RemediationPlan
        fields = [
            "date_end",
            "status",
            "description"
        ]

    def __init__(self, *argv, **kwargs):
        super(RemediationPlanUpdateForm, self).__init__(*argv, **kwargs)
        self.fields["date_end"].widget.attrs["class"] = "datepicker"
        self.fields["description"].widget.attrs["id"] = "e_description"
