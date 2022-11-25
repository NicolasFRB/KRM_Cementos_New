from cProfile import label
from django.contrib.postgres.forms import SimpleArrayField
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, HiddenInput

from django.core.validators import FileExtensionValidator

from krm.evaluations_krm.models import EvaluationKrmInherent
from django.core.validators import FileExtensionValidator

from krm.questionnaires.models import EvaluationQuestionnaire


class EvaluationQuestionnaireCreateForm(ModelForm):

    questions_to_evaluate = forms.CharField(
        max_length=1000,
        label=_('Preguntas')
    )

    class Meta:
        model = EvaluationQuestionnaire
        fields = [
            'ref',
            'questionnaire',
            'date_begin',
            'date_end',
            'questionnaire',
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

        self.fields["certification_year"].widget.attrs["data-control"] = "select2"
        self.fields["certification_year"].widget.attrs["class"] = "form-select"
        self.fields["questionnaire"].widget.attrs["class"] = "form-select"
        self.fields["questionnaire"].widget.attrs["data-control"] = "select2"


class EvaluationQuestionnaireCompleteForm(forms.Form):

    ref = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ref'].widget = HiddenInput()
