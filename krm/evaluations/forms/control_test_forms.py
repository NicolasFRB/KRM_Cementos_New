from cProfile import label
from django.contrib.postgres.forms import SimpleArrayField
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from django.core.validators import FileExtensionValidator

from krm.evaluations.models import ControlTest


class ControlTestAssignForm(ModelForm):

    class Meta:
        model = ControlTest
        fields = [
            'control_test_supervisor',
            'control_test_owner'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["control_test_supervisor"].widget.attrs["class"] = "form-select"
        self.fields["control_test_owner"].widget.attrs["class"] = "form-select"

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.evaluation.allow_self_autosupervision:
            control_test_supervisor = cleaned_data.get(
                "control_test_supervisor")
            control_test_owner = cleaned_data.get("control_test_owner")
            if control_test_supervisor is not None and control_test_supervisor is not None:
                if control_test_supervisor == control_test_owner:
                    raise forms.ValidationError(
                        _('El Control Supervisor del control debe ser diferente del Control Owner'))


class ControlTestUpdateForm(ModelForm):

    send_notification = forms.BooleanField(
        required=False,
        label=_('Enviar notificación'),
        help_text=_(
            'Si marca esta opción se enviará un email de notificación al Control Owner o al Control Supervisor según el estado indicado')
    )

    class Meta:
        model = ControlTest
        fields = [
            'date_begin',
            'control_test_owner',
            'control_test_supervisor',
            'status',
            'result',
            'remediation_plan_needed'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["control_test_supervisor"].widget.attrs["class"] = "form-select"
        self.fields["control_test_owner"].widget.attrs["class"] = "form-select"
        self.fields["status"].widget.attrs["class"] = "form-select"
        self.fields["result"].widget.attrs["class"] = "form-select"
        self.fields["date_begin"].widget.attrs["class"] = "datepicker"

    def clean(self):
        cleaned_data = super().clean()
        if not self.instance.evaluation.allow_self_autosupervision:
            control_test_supervisor = cleaned_data.get(
                "control_test_supervisor")
            control_test_owner = cleaned_data.get("control_test_owner")
            if control_test_supervisor is not None and control_test_supervisor is not None:
                if control_test_supervisor == control_test_owner:
                    raise forms.ValidationError(
                        _('El Control Supervisor del control debe ser diferente del Control Owner'))

# class ControlTestUpdateForm(ModelForm):

#     class Meta:
#         model = ControlTest
#         fields = [
#             'ref',
#             'date_begin',
#             'date_intermediate',
#             'date_end',
#             'description',
#             'certification_year',
#             'certification_period',
#             'allow_self_autosupervision'
#         ]

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["ref"].widget.attrs["id"] = "e_ref"
#         self.fields["date_begin"].widget.attrs["id"] = "e_date_begin"
#         self.fields["date_intermediate"].widget.attrs["id"] = "e_date_intermediate"
#         self.fields["date_end"].widget.attrs["id"] = "e_date_end"
#         self.fields["description"].widget.attrs["id"] = "e_description"

#         self.fields["date_begin"].widget.attrs["class"] = "datepicker"
#         self.fields["date_end"].widget.attrs["class"] = "datepicker"
#         self.fields["date_intermediate"].widget.attrs["class"] = "datepicker"

#         self.fields["certification_year"].widget.attrs["class"] = "form-select"


# class ControlTestInitForm(forms.Form):
#     pk = forms.IntegerField()


# class ControlTestTemplateAssignDownload(forms.Form):
#     evaluation = forms.IntegerField()

#     def __init__(self, *argv, **kwargs):
#         super(ControlTestTemplateAssignDownload,
#               self).__init__(*argv, **kwargs)


# class ControlTestDownload(forms.Form):
#     process_test = forms.IntegerField()

#     def __init__(self, *argv, **kwargs):
#         super(ControlTestDownload, self).__init__(*argv, **kwargs)


# class ControlTestAssignImportForm(forms.Form):
#     process_test = forms.IntegerField()
#     process_assign_file = forms.FileField(
#         label=_(u'Plantilla de asignación en excel a importar'),
#         validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])]
#     )


class ControlTestCaForm(ModelForm):

    CONTROL_RESULT_CHOICES = (
        ("", _("-")),
        ("EF", _("Efectivo")),
        ("NE", _("No efectivo")),
    )
    control_result = forms.ChoiceField(
        required=True,
        choices=CONTROL_RESULT_CHOICES,
        label=_("Resultado del control")
    )
    CONTROL_STATUS_CHOICES = (
        ("SI", _("Sin iniciar")),
        ("WO", _("En espera de respuesta del Control Owner")),
        ("WS", _("En espera de respuesta del Control Supervisor")),
        ("WA", _("En espera de respuesta del Control Administrator")),
        ("FI", _("Finalizado")),
    )
    control_status = forms.ChoiceField(
        required=True,
        choices=CONTROL_STATUS_CHOICES,
        label=_("Estado del control")
    )
    description = forms.CharField(
        widget=forms.Textarea,
        label=_("Descripción del seguimiento del control"),
        max_length=10000,
        required=False
    )

    class Meta:
        model = ControlTest
        fields = [
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["control_result"].widget.attrs["class"] = "form-select"
        self.fields["control_status"].widget.attrs["class"] = "form-select"
        self.fields["description"].widget.attrs["id"] = "cta_description"

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("status") == self.instance.status:
            raise forms.ValidationError(
                _('Debe establecer un nuevo estado del control para finalizar la revisión del control test'))
