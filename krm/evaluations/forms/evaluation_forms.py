import datetime
from cProfile import label
from django.contrib.postgres.forms import SimpleArrayField
from django import forms
from django.forms import ModelForm, HiddenInput
from django.utils.translation import gettext_lazy as _

from django.core.validators import FileExtensionValidator

from krm.evaluations.models import Evaluation
from django.core.validators import FileExtensionValidator

from krm.companies.models.company_model import Company


class EvaluationCreateForm(ModelForm):

    controls_companies_to_evaluate = forms.CharField(
        max_length=200000,
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

    notification_pk = SimpleArrayField(forms.CharField(
        max_length=1000),  label=_('Notificar'))

class EvaluationDashboardForm(forms.Form):

    def year_choices():
        return [(r, r) for r in range(2000, datetime.date.today().year + 1)]

    def current_year():
        return datetime.date.today().year

    evaluation = forms.ModelMultipleChoiceField(
        label=_("Evaluations"),
        required=False,
        queryset=Evaluation.objects.all(),
    )
    
    company = forms.ModelMultipleChoiceField(
        label=_("Companies"),
        required=False,
        queryset=Company.objects.all(),
    )

    date_evaluation_begin = forms.DateField(
        label=_('From'),
        required=False,
        widget=forms.DateInput(attrs={'class': 'datepicker'})
    )

    date_evaluation_end = forms.DateField(
        label=_('To'),
        required=False,
        widget=forms.DateInput(attrs={'class': 'datepicker'})
    )

    certification_year = forms.MultipleChoiceField(
        label=_("Certification year"),
        required=False,
        choices=year_choices(),
    )
    
    certification_period = forms.ModelMultipleChoiceField(
        label=_("Certification period"),
        required=False,
        queryset=Evaluation.objects.all().values_list("certification_period", flat=True).distinct(),
    )

    PROCESS_STATUS_CHOICES = (
        ("SI", _("Sin iniciar")),
        ("EP", _("En proceso")),
        ("FI", _("Finalizado")),
    )

    process_status = forms.MultipleChoiceField(
        label=_("Status"),
        required=False,
        choices=PROCESS_STATUS_CHOICES,
    )

    CONTROL_STATUS_CHOICES = (
        ("SI", _("Sin iniciar")),
        ("WO", _("En espera de respuesta del Control Owner")),
        ("WS", _("En espera de respuesta del Control Supervisor")),
        ("WA", _("En espera de respuesta del Control Administrator")),
        ("FI", _("Finalizado")),
    )

    control_status = forms.MultipleChoiceField(
        label=_("Control Status"),
        required=False,
        choices=CONTROL_STATUS_CHOICES,
    )

    # DIVISION_CHOICES = (
    #     ("CRM", _("Rhythm management")),
    #     ("EP", _("Endoscopy")),
    #     ("PI", _("Peripheral Interventions")),
    #     ("NMOD", _("Neuromodulation")),
    #     ("IC/W", _("Interventional cardiology")),
    # )

    # INT_TYPE_CHOICES = (
    #     ("1", _("Educational Grant to HCO")),
    #     ("2", _("Fellowship/Scholarship Grant to HCO")),
    #     ("3", _("Charitable Donations")),
    #     ("4", _("Financial Support to PCO")),
    #     ("5", _("Service agreements")),
    #     ("6", _("Advertisement & Promotional opportunities")),        
    #     ("7", _("Customer-organized BSC product training and education")),        
    #     ("8", _("Complementary research grant")),        
    #     ("9", _("Market research")),        
    #     ("10", _("Advisory boards")),        
    #     ("11", _("Practical training event organized by third parties")),        
    #     ("11", _("Contracting with speaker")),        
    # )

    # interaction_type = forms.MultipleChoiceField(
    #     label=_("Interaction type"),
    #     required=False,
    #     choices=INT_TYPE_CHOICES,
    # )

    # company = forms.ModelMultipleChoiceField(
    #     label=_("Agents"),
    #     required=False,
    #     queryset=Company.objects.all(),
    # )

    # PHS_CHOICES = (
    #     ('sol', _('Request')),
    #     ('apr', _('Application review')),
    #     ('pre', _('Interaction allowed')),
    #     ('csi', _('Closed wo/i')),
    #     ('cci', _('Closed w/i')),
    # )

    # INTERACTION_MODEL_CHOICESPHASE_CHOICES = PHS_CHOICES + (
    #     ('sus', _('Interaction suspended')),
    #     ('rec', _('Interaction rejected')),
    # )

    

    # STATUS_CHOICES = (
    #     ("A", _("Agent")),
    #     ("K", _("KPMG")),
    #     ("F", _("Completed")),
    # )

    

    # date_created_begin = forms.DateField(
    #     label=_('From'),
    #     required=False,
    #     widget=forms.DateInput(attrs={'class': 'datepicker'})
    # )
    # date_created_end = forms.DateField(
    #     label=_('To'),
    #     required=False,
    #     widget=forms.DateInput(attrs={'class': 'datepicker'})
    # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["division"].widget.attrs["class"] = "form-select"
        # self.fields["division"].widget.attrs["data-control"] = "select2"
        # self.fields["division"].widget.attrs["multiple"] = "multiple"
        # self.fields["interaction_type"].widget.attrs["class"] = "form-select"
        # self.fields["interaction_type"].widget.attrs["data-control"] = "select2"
        self.fields["evaluation"].widget.attrs["class"] = "form-select"
        self.fields["evaluation"].widget.attrs["data-control"] = "select2"
        self.fields["company"].widget.attrs["class"] = "form-select"
        self.fields["company"].widget.attrs["data-control"] = "select2"
        self.fields["certification_year"].widget.attrs["class"] = "form-select"
        self.fields["certification_year"].widget.attrs["data-control"] = "select2"
        self.fields["certification_period"].widget.attrs["class"] = "form-select"
        self.fields["certification_period"].widget.attrs["data-control"] = "select2"
        self.fields["process_status"].widget.attrs["class"] = "form-select"
        self.fields["process_status"].widget.attrs["data-control"] = "select2"
        self.fields["control_status"].widget.attrs["class"] = "form-select"
        self.fields["control_status"].widget.attrs["data-control"] = "select2"