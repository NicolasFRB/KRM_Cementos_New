import datetime
from cProfile import label
from django.contrib.postgres.forms import SimpleArrayField
from django import forms
from django.forms import ModelForm, HiddenInput
from django.utils.translation import gettext_lazy as _

from django.core.validators import FileExtensionValidator

from krm.evaluations.models import Evaluation
from krm.evaluations_krm.models.evaluation_krm_inherent_model import EvaluationKrmInherent
from krm.evaluations_krm.models.evaluation_krm_residual_model import EvaluationKrmResidual
from django.core.validators import FileExtensionValidator

from krm.companies.models.company_model import Company
from krm.risks.models.domain_risk_model import DomainRisk


class EvaluationCreateForm(ModelForm):

    controls_companies_to_evaluate = forms.JSONField(
	label=_('Controles a evaluar')
    )

    class Meta:
        model = Evaluation
        fields = [
            'ref',
            'date_begin',
            'date_intermediate',
            'date_end',
            'description',
            'notification_text',
            'certification_year',
            'certification_period',
            'allow_self_autosupervision',
            'notification_text'
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
            'notification_text',
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

    def clean_ref(self):
        ref = self.cleaned_data.get("ref").upper()
        if Evaluation.objects.filter(ref=ref).count() > 0:
            raise forms.ValidationError(
                _('Ya existe una evaluación con esa REF'))
        return ref


class EvaluationActionForm(forms.Form):
    evaluation_pk = forms.IntegerField()
    action = forms.CharField(required=False)


class EvaluationTemplateAssignDownload(forms.Form):
    evaluation = forms.IntegerField()

    def __init__(self, *argv, **kwargs):
        super(EvaluationTemplateAssignDownload,
              self).__init__(*argv, **kwargs)


class EvaluationDownload(forms.Form):
    process_test = forms.IntegerField()

    def __init__(self, *argv, **kwargs):
        super(EvaluationDownload, self).__init__(*argv, **kwargs)

class DownloadEvaluationActionForm(forms.Form):

    action = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['action'].widget = HiddenInput()


class EvaluationAssignImportForm(forms.Form):
    evaluation_assign_file = forms.FileField(
        label=_('Plantilla de asignación en excel a importar'),
        validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls'])]
    )


class EvaluationNotificationForm(forms.Form):
    notification_text = forms.CharField(
        label=_('Texto personalizado de notificación'),
        max_length=5000,
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False
    )
    notification_pk = SimpleArrayField(forms.CharField(
        max_length=1000),
        label=_('Notificar')
    )

class EvaluationDashboardForm(forms.Form):

    def year_choices():
        return [(r, r) for r in range(2000, datetime.date.today().year + 1)]

    def current_year():
        return datetime.date.today().year

    def certification_period_choices():
        choices= Evaluation.objects.all().values_list("certification_period", flat=True).order_by("certification_period").distinct()
        return [(cp, cp) for cp in choices if cp]

    evaluation = forms.ModelMultipleChoiceField(
        label=_("Evaluaciones"),
        required=False,
        queryset=Evaluation.objects.all(),
    )

    company = forms.ModelMultipleChoiceField(
        label=_("Compañías"),
        required=False,
        queryset=Company.objects.all(),
    )

    date_evaluation_begin = forms.DateField(
        label=_('Desde'),
        required=False,
        widget=forms.DateInput(attrs={'class': 'datepicker'})
    )

    date_evaluation_end = forms.DateField(
        label=_('Hasta'),
        required=False,
        widget=forms.DateInput(attrs={'class': 'datepicker'})
    )

    certification_year = forms.MultipleChoiceField(
        label=_("Año de certificación"),
        required=False,
        choices=year_choices(),
    )

    certification_period = forms.MultipleChoiceField(
        label=_("Periodo de certificación"),
        required=False,
        choices=(),
    )

    PROCESS_STATUS_CHOICES = (
        ("SI", _("Sin iniciar")),
        ("EP", _("En proceso")),
        ("FI", _("Finalizado")),
    )

    process_status = forms.MultipleChoiceField(
        label=_("Estado"),
        required=False,
        choices=PROCESS_STATUS_CHOICES,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["evaluation"].widget.attrs["class"] = "form-select"
        self.fields["evaluation"].widget.attrs["data-control"] = "select2"
        self.fields["company"].widget.attrs["class"] = "form-select"
        self.fields["company"].widget.attrs["data-control"] = "select2"
        self.fields["certification_year"].widget.attrs["class"] = "form-select"
        self.fields["certification_year"].widget.attrs["data-control"] = "select2"
        self.fields["certification_period"].choices = EvaluationDashboardForm.certification_period_choices()
        self.fields["certification_period"].widget.attrs["class"] = "form-select"
        self.fields["certification_period"].widget.attrs["data-control"] = "select2"
        self.fields["process_status"].widget.attrs["class"] = "form-select"
        self.fields["process_status"].widget.attrs["data-control"] = "select2"

class EvaluationKrmDashboardForm(forms.Form):
    def year_choices():
        return [(r, r) for r in range(2000, datetime.date.today().year + 1)]

    def current_year():
        return datetime.date.today().year

    def certification_period_choices():
        choices=EvaluationKrmInherent.objects.all().values_list("certification_period", flat=True).distinct().union(
            EvaluationKrmResidual.objects.all().values_list("certification_period", flat=True).distinct()
        ).order_by("certification_period")
        return [(cp, cp) for cp in choices if cp]

    evaluation_inherent = forms.ModelMultipleChoiceField(
        label=_("Evaluaciones Inherentes"),
        required=False,
        queryset= EvaluationKrmInherent.objects.all(),
    )

    evaluation_residual =  forms.ModelMultipleChoiceField(
        label=_("Evaluaciones Residuales"),
        required=False,
        queryset= EvaluationKrmResidual.objects.all(),
    )

    company = forms.ModelMultipleChoiceField(
        label=_("Compañías"),
        required=False,
        queryset=Company.objects.all(),
    )

    date_evaluation_begin = forms.DateField(
        label=_('Desde'),
        required=False,
        widget=forms.DateInput(attrs={'class': 'datepicker'})
    )

    date_evaluation_end = forms.DateField(
        label=_('Hasta'),
        required=False,
        widget=forms.DateInput(attrs={'class': 'datepicker'})
    )

    certification_year = forms.MultipleChoiceField(
        label=_("Año de certificación"),
        required=False,
        choices=year_choices(),
    )

    certification_period = forms.MultipleChoiceField(
        label=_("Periodo de certificación"),
        required=False,
        choices=(),
    )

    PROCESS_STATUS_CHOICES = (
        ("EP", _("En proceso")),
        ("FI", _("Finalizado")),
    )

    process_status = forms.MultipleChoiceField(
        label=_("Estado"),
        required=False,
        choices=PROCESS_STATUS_CHOICES,
    )

    domain_risk = forms.ModelMultipleChoiceField(
        label=_("Dominios de Riesgo"),
        required=False,
        queryset= DomainRisk.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["evaluation_inherent"].widget.attrs["class"] = "form-select"
        self.fields["evaluation_inherent"].widget.attrs["data-control"] = "select2"
        self.fields["evaluation_residual"].widget.attrs["class"] = "form-select"
        self.fields["evaluation_residual"].widget.attrs["data-control"] = "select2"
        self.fields["company"].widget.attrs["class"] = "form-select"
        self.fields["company"].widget.attrs["data-control"] = "select2"
        self.fields["certification_year"].widget.attrs["class"] = "form-select"
        self.fields["certification_year"].widget.attrs["data-control"] = "select2"
        self.fields["certification_period"].choices = EvaluationKrmDashboardForm.certification_period_choices()
        self.fields["certification_period"].widget.attrs["class"] = "form-select"
        self.fields["certification_period"].widget.attrs["data-control"] = "select2"
        self.fields["process_status"].widget.attrs["class"] = "form-select"
        self.fields["process_status"].widget.attrs["data-control"] = "select2"
        self.fields["domain_risk"].widget.attrs["class"] = "form-select"
        self.fields["domain_risk"].widget.attrs["data-control"]= "select2"

from krm.risks.models import DomainRisk
from krm.evaluations.models import Evaluation
class EvaluationFilterForm(forms.Form):

    domain_risk = forms.ModelMultipleChoiceField(
        label=_("Dominio de riesgo"),
        required=False,
        queryset=DomainRisk.objects.all().values_list("ref", flat=True).distinct(),
    )


    certification_period = forms.ModelMultipleChoiceField(
        label=_("Periodo de certificación"),
        required=False,
        # choices=[],
        queryset=Evaluation.objects.filter()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        posible_values = [
            (evaluation.certification_period_with_year,
             evaluation.certification_period_with_year)
            for evaluation in Evaluation.objects.all().order_by("certification_year")
        ]

        # Quitar duplicados
        posible_values = list(set(posible_values))

        # Configurar las opciones dinámicas para certification_period
        self.fields["certification_period"].choices = posible_values

        # Agregar clases y atributos personalizados a los widgets
        self.fields["domain_risk"].widget.attrs["class"] = "form-select"
        self.fields["domain_risk"].widget.attrs["data-control"] = "select2"

        self.fields["certification_period"].widget.attrs["class"] = "form-select"
        self.fields["certification_period"].widget.attrs["data-control"] = "select2"
