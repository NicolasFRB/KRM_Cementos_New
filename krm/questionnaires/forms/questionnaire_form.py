from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.translation import gettext as _
from django.contrib.postgres.forms import SimpleArrayField

from django.forms.widgets import CheckboxSelectMultiple


from krm.questionnaires.models import Questionnaire


class QuestionnaireCreateForm(ModelForm):
    class Meta:
        model = Questionnaire
        fields = '__all__'
