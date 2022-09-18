from cProfile import label
from django.contrib.postgres.forms import SimpleArrayField
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from django.core.validators import FileExtensionValidator

from krm.evaluations.models import Evaluation


class EvaluationCreateForm(ModelForm):

    companies = SimpleArrayField(forms.CharField(
        max_length=200), label=_('Compañías'))
    controls = SimpleArrayField(forms.CharField(
        max_length=1000),  label=_('Controles'))

    class Meta:
        model = Evaluation
        fields = [
            'ref',
            'date_begin',
            'date_intermediate',
            'date_end',
            'description',
            'certification_year',
            'certification_period',
            'allow_self_autosupervision'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ref"].widget.attrs["id"] = "e_ref"
        self.fields["date_begin"].widget.attrs["id"] = "e_date_begin"
        self.fields["date_intermediate"].widget.attrs["id"] = "e_date_intermediate"
        self.fields["date_end"].widget.attrs["id"] = "e_date_end"
        self.fields["description"].widget.attrs["id"] = "e_description"

        self.fields["date_begin"].widget.attrs["class"] = "datepicker"
        self.fields["date_end"].widget.attrs["class"] = "datepicker"
        self.fields["date_intermediate"].widget.attrs["class"] = "datepicker"

        self.fields["certification_year"].widget.attrs["class"] = "form-select"


class EvaluationUpdateForm(ModelForm):

    class Meta:
        model = Evaluation
        fields = [
            'ref',
            'date_begin',
            'date_intermediate',
            'date_end',
            'description',
            'certification_year',
            'certification_period',
            'allow_self_autosupervision'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ref"].widget.attrs["id"] = "e_ref"
        self.fields["date_begin"].widget.attrs["id"] = "e_date_begin"
        self.fields["date_intermediate"].widget.attrs["id"] = "e_date_intermediate"
        self.fields["date_end"].widget.attrs["id"] = "e_date_end"
        self.fields["description"].widget.attrs["id"] = "e_description"

        self.fields["date_begin"].widget.attrs["class"] = "datepicker"
        self.fields["date_end"].widget.attrs["class"] = "datepicker"
        self.fields["date_intermediate"].widget.attrs["class"] = "datepicker"

        self.fields["certification_year"].widget.attrs["class"] = "form-select"


class EvaluationInitForm(forms.Form):
    evaluation_pk = forms.IntegerField()


class EvaluationTemplateAssignDownload(forms.Form):
    evaluation = forms.IntegerField()

    def __init__(self, *argv, **kwargs):
        super(EvaluationTemplateAssignDownload,
              self).__init__(*argv, **kwargs)


class EvaluationDownload(forms.Form):
    process_test = forms.IntegerField()

    def __init__(self, *argv, **kwargs):
        super(EvaluationDownload, self).__init__(*argv, **kwargs)


class EvaluationAssignImportForm(forms.Form):
    process_test = forms.IntegerField()
    process_assign_file = forms.FileField(
        label=_(u'Plantilla de asignación en excel a importar'),
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])]
    )
