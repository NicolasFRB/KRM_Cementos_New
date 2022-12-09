from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.translation import gettext as _
from django.contrib.postgres.forms import SimpleArrayField

from django.core.validators import FileExtensionValidator

from django.forms.widgets import CheckboxSelectMultiple


from krm.questionnaires.models import Questionnaire


class QuestionnaireCreateForm(ModelForm):
    class Meta:
        model = Questionnaire
        fields = '__all__'


class QuestionnaireImportForm(forms.Form):
    ref = forms.CharField(
        label=_("REF"),
        max_length=200,
        required=True,
    )
    name = forms.CharField(
        label=_("Nombre"),
        max_length=500,
        required=True,
    )
    questionnaire_file = forms.FileField(
        label=_("Archivo de excel a importar"),
        required=True,
        validators=[FileExtensionValidator(
            allowed_extensions=["xlsx", "xls"])],
    )

    class Meta:
        model = Questionnaire
        fields = []

    def __init__(self, *args, **kwargs):
        super(QuestionnaireImportForm, self).__init__(*args, **kwargs)
