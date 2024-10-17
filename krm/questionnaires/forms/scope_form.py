
from django import forms
from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.translation import gettext as _
from django.contrib.postgres.forms import SimpleArrayField

from django.forms.widgets import CheckboxSelectMultiple


from krm.questionnaires.models import Scope


class ScopeCreateForm(ModelForm):
    class Meta:
        model = Scope
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["questionnaire"].widget.attrs["class"] = "form-select"
        self.fields["questionnaire"].widget.attrs["data-control"] = "select2"
        self.fields["user_to_assign"].widget.attrs["class"] = "form-select"
        self.fields["user_to_assign"].widget.attrs["data-control"] = "select2"


class ScopeUpdateForm(ModelForm):
    class Meta:
        model = Scope
        fields = ['ref', 'name', 'user_to_assign']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_to_assign"].widget.attrs["class"] = "form-select"
        self.fields["user_to_assign"].widget.attrs["data-control"] = "select2"
