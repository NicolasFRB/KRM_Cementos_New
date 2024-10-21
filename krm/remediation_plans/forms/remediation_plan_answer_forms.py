from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import NON_FIELD_ERRORS

from krm.remediation_plans.models import RemediationPlanAnswer

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Field


class RemediationPlanAnswerCreateForm(ModelForm):
    class Meta:
        model = RemediationPlanAnswer
        fields = [
            "status",
            "description",
            "next_to_reply",
            "attachment_1",
        ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RemediationPlanAnswerCreateForm, self).__init__(*args, **kwargs)

        self.fields["description"].error_messages = {
            "max_length": _(
                "Longitud de la descripción demasiado larga. En caso de estar pegando desde el portapapales asegúrese que ha copiado solo texto. Si el tamaño del texto es mayor a 8000 caracteres considere incluirlo como una evidencia. Caracteres introducidos %(show_value)d."
            )
        }
        self.fields["status"].widget.attrs["class"] = "form-select"
        self.fields["next_to_reply"].widget.attrs["class"] = "form-select"
        self.fields["description"].widget.attrs["required"] = "required"
