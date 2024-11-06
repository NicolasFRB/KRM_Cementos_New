from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import NON_FIELD_ERRORS

from krm.evaluations.models import ControlTestAnswer

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Field


class ControlTestAnswerCreateForm(ModelForm):
    CONTROL_RESULT_CHOICES = (
        ("", _("-")),
        ("EF", _("Efectivo")),
        ("NE", _("No efectivo")),
        ("NA", _("No aplica en el periodo certificado")),
    )
    control_result = forms.ChoiceField(
        required=True, choices=CONTROL_RESULT_CHOICES, label=_("Resultado del control")
    )

    class Meta:
        model = ControlTestAnswer
        fields = [
            "description",
            "attachment_1",
            "attachment_2",
            "attachment_3"
        ]

    def __init__(self, *args, **kwargs):
        super(ControlTestAnswerCreateForm, self).__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["id"] = "cta_description"
        self.fields["attachment_1"].widget.attrs.update(
            {"class": "custom-file-input", "id": "customFile1"}
        )
        self.fields["attachment_2"].widget.attrs.update(
            {"class": "custom-file-input", "id": "customFile2"}
        )
        self.fields["attachment_3"].widget.attrs.update(
            {"class": "custom-file-input", "id": "customFile3"}
        )
        self.fields["description"].error_messages = {
            "max_length": _(
                "Longitud de la descripción demasiado larga. En caso de estar pegando desde el portapapales asegúrese que ha copiado solo texto. Si el tamaño del texto es mayor a 10000 caracteres considere incluirlo como una evidencia. Caracteres introducidos %(show_value)d."
            )
        }
        self.fields["control_result"].widget.attrs["class"] = "form-select"


class ControlTestAnswerUpdateForm(ModelForm):
    class Meta:
        model = ControlTestAnswer
        fields = [
            "description",
            "attachment_1",
            "attachment_2",
            "attachment_3"
        ]

class ControlTestAnswerOwnerCreateForm(ModelForm):
    CONTROL_RESULT_CHOICES = (
        ("", _("-")),
        ("EF", _("Efectivo")),
        ("NE", _("No efectivo")),
        ("NA", _("No aplica en el periodo certificado")),
    )
    control_result = forms.ChoiceField(
        required=True,
        choices=CONTROL_RESULT_CHOICES,
        label=_("Resultado del control")
    )

    class Meta:
        model = ControlTestAnswer
        fields = [
            "description",
            "attachment_1",
            "attachment_2",
            "attachment_3"
        ]

    def __init__(self, *args, **kwargs):
        super(ControlTestAnswerOwnerCreateForm, self).__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["id"] = "cta_description"
        self.fields["description"].error_messages = {
            "max_length": _(
                "Longitud de la descripción demasiado larga. En caso de estar pegando desde el portapapales asegúrese que ha copiado solo texto. Si el tamaño del texto es mayor a 10000 caracteres considere incluirlo como una evidencia. Caracteres introducidos %(show_value)d."
            )
        }
        self.fields["control_result"].widget.attrs["class"] = "form-select"
        self.fields["control_result"].widget.attrs["data-control"] = "select2"

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) == 0:
            raise forms.ValidationError("Campo obligatorio")
        elif len(description) < 3:
            raise forms.ValidationError("Debe proporcionar información suficiente para finalizar la evaluación")
        elif len(description) < 5000:
            return description
        else:
            raise forms.ValidationError("Muy largo")


class ControlTestAnswerSupervisorCreateForm(ModelForm):
    more_information = forms.BooleanField(
        label=_("Solicitar más información al responsable de cumplimentar el control"),
        required=False,
    )

    class Meta:
        model = ControlTestAnswer
        fields = [
            "description",
            "attachment_1",
            "attachment_2",
            "attachment_3"
        ]

    def __init__(self, *args, **kwargs):
        super(ControlTestAnswerSupervisorCreateForm,
              self).__init__(*args, **kwargs)
        self.fields["description"].widget.attrs["id"] = "cta_description"
        self.fields["description"].error_messages = {
            "max_length": _(
                "Longitud de la descripción demasiado larga. En caso de estar pegando desde el portapapales asegúrese que ha copiado solo texto. Si el tamaño del texto es mayor a 10000 caracteres considere incluirlo como una evidencia. Caracteres introducidos %(show_value)d."
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        more_information = cleaned_data.get("more_information")
        if more_information:
            if len(description) < 20:
                raise forms.ValidationError(
                    _('Debe especificar la información necesaria que necesita del Control Owner'))
        else:
            if len(description) < 3:
                raise forms.ValidationError(
                _('Debe proporcionar información suficiente para finalizar la evaluación'))
