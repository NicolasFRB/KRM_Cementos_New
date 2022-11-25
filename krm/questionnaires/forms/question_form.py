
from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.translation import gettext as _
from django.contrib.postgres.forms import SimpleArrayField

from django.forms.widgets import CheckboxSelectMultiple


from krm.questionnaires.models import Question


class QuestionCreateForm(ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["questionnaire"].widget.attrs["class"] = "form-select"
        self.fields["questionnaire"].widget.attrs["data-control"] = "select2"
