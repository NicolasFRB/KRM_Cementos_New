from cProfile import label
from django.contrib.postgres.forms import SimpleArrayField
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, HiddenInput

from krm.evaluations_krm.models import EvaluationKrmResidual
from django.core.validators import FileExtensionValidator


class EvaluationResidualCreateForm(ModelForm):

    risk_companies = forms.CharField(
        max_length=1000,
        label=_('Riesgos Compañía')
    )

    class Meta:
        model = EvaluationKrmResidual
        fields = [
            'ref',
            'date_begin',
            'date_end',
            'description',
            'certification_year',
            'certification_period',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ref"].widget.attrs["id"] = "e_ref"
        self.fields["date_begin"].widget.attrs["id"] = "e_date_begin"
        self.fields["date_end"].widget.attrs["id"] = "e_date_end"
        self.fields["description"].widget.attrs["id"] = "e_description"

        self.fields["date_begin"].widget.attrs["class"] = "datepicker"
        self.fields["date_end"].widget.attrs["class"] = "datepicker"

        self.fields["certification_year"].widget.attrs["class"] = "form-select"


class EvaluationResidualCompleteForm(forms.Form):

    ref = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ref'].widget = HiddenInput()
