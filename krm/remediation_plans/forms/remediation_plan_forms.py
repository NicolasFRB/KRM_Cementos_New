from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _

from krm.remediation_plans.models import RemediationPlan
from krm.companies.models import Company


class RemediationPlanCreateForm(ModelForm):
    class Meta:
        model = RemediationPlan
        fields = '__all__'
        exclude = ["status", "next_to_reply", "company"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["control"].widget.attrs["class"] = "form-select"
        self.fields["control"].widget.attrs["data-control"] = "select2"

        self.fields["responsible"].widget.attrs["class"] = "form-select"
        self.fields["responsible"].widget.attrs["data-control"] = "select2"

        self.fields["supervisor"].widget.attrs["class"] = "form-select"
        self.fields["supervisor"].widget.attrs["data-control"] = "select2"

        self.fields["additional_users"].widget.attrs["class"] = "form-select"
        self.fields["additional_users"].widget.attrs["data-control"] = "select2"

        # self.fields["status"].widget.attrs["class"] = "form-select"
        # self.fields["status"].widget.attrs["data-control"] = "select2"
        # self.fields["status"].choices = [("", "Seleccionar")] + list(self.fields["status"].choices)[0:]
        # self.fields["status"].initial = "EP"

        # self.fields["next_to_reply"].widget.attrs["class"] = "form-select"
        # self.fields["next_to_reply"].widget.attrs["data-control"] = "select2"
        # self.fields["next_to_reply"].choices = [("", "Seleccionar")] + list(self.fields["next_to_reply"].choices)[0:]
        # # poner por defecto la nueva opción
        # self.fields["next_to_reply"].initial = "WR"

        self.fields["date_begin"].widget.attrs["id"] = "e_date_begin"
        self.fields["date_end"].widget.attrs["id"] = "e_date_end"

        self.fields["date_begin"].widget.attrs["class"] = "datepicker"
        self.fields["date_end"].widget.attrs["class"] = "datepicker"

        # Añadir requerido el responsible
        self.fields["responsible"].required = True
        self.fields["supervisor"].required = True
        self.fields["description"].required = True


class RemediationPlanUpdateForm(ModelForm):
    class Meta:
        model = RemediationPlan
        fields = '__all__'
        exclude = ["company" ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["control"].widget.attrs["class"] = "form-select"
        self.fields["control"].widget.attrs["data-control"] = "select2"

        self.fields["responsible"].widget.attrs["class"] = "form-select"
        self.fields["responsible"].widget.attrs["data-control"] = "select2"

        self.fields["supervisor"].widget.attrs["class"] = "form-select"
        self.fields["supervisor"].widget.attrs["data-control"] = "select2"

        self.fields["additional_users"].widget.attrs["class"] = "form-select"
        self.fields["additional_users"].widget.attrs["data-control"] = "select2"

        self.fields["status"].widget.attrs["class"] = "form-select"
        self.fields["status"].widget.attrs["data-control"] = "select2"

        self.fields["next_to_reply"].widget.attrs["class"] = "form-select"
        self.fields["next_to_reply"].widget.attrs["data-control"] = "select2"

        self.fields["date_begin"].widget.attrs["id"] = "e_date_begin"
        self.fields["date_end"].widget.attrs["id"] = "e_date_end"

        self.fields["date_begin"].widget.attrs["class"] = "datepicker"
        self.fields["date_end"].widget.attrs["class"] = "datepicker"




class RuRemediationPlanCreateForm(ModelForm):
    class Meta:
        model = RemediationPlan
        fields = '__all__'
        exclude = ["status", "next_to_reply", "responsible", "supervisor", "company" ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["additional_users"].widget.attrs["class"] = "form-select"
        self.fields["additional_users"].widget.attrs["data-control"] = "select2"

        self.fields["date_begin"].widget.attrs["id"] = "e_date_begin"
        self.fields["date_end"].widget.attrs["id"] = "e_date_end"

        self.fields["date_begin"].widget.attrs["class"] = "datepicker"
        self.fields["date_end"].widget.attrs["class"] = "datepicker"


class RemediationPlanCreateSelectCompany(forms.Form):
    company = forms.ChoiceField(
        label=_("Seleccione la Compañía"),
        choices=[],
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "data-control": "select2",
            }
        ),
    )

    # def __init__(self, *args, **kwargs):
    #     super(RemediationPlanCreateSelectCompany, self).__init__(*args, **kwargs)
    #     # self.fields["company"].choices = kwargs.get("companies", [])
    #     # self.fields["company"].initial = kwargs.get("company", None)
    #     # Quiero llenar el campo company con todas las compañias de la base de datos
    #     self.fields["company"].choices = [(c.pk, c.name) for c in Company.objects.all()]
    #     # Añadir una opción vacía al principio
    #     self.fields["company"].choices = [("", _("-"))] + self.fields["company"].choices
