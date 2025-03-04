from django.db import models

from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags

from ckeditor.fields import RichTextField

from krm.utils.models import AuditModel


FREQUENCY_CONTROL_CHOICES = (
    ("BD", _("Bajo demanda")),
    ("CO", _("Constante")),
    ("DI", _("Diario")),
    ("1W", _("Semanal")),
    ("2W", _("Quincenal")),
    ("1M", _("Mensual")),
    ("2M", _("Bimensual")),
    ("3T", _("Trimestral")),
    ("4T", _("Cuatrimestral")),
    ("6M", _("Semestral")),
    ("1Y", _("Anual")),
    ("2Y", _("Bienal")),
    ("3Y", _("Trienal")),
    ("4Y", _("Cuatrienal")),
    ("5Y", _("Quinquenal"))
)

class Control(AuditModel):
    """Control model.
    Modelo que usaremos para representar un control para un riesgo asociado
    """

    ref = models.CharField(
        _("REF"),
        max_length=140,
        unique=True
    )

    name = RichTextField(
        _("Objetivo del Control"),
        config_name='awesome_ckeditor',
        max_length=10000,
        null=True,
        blank=True
    )

    description = RichTextField(
        _("Descripción del Control"),
        config_name='awesome_ckeditor',
        max_length=10000,
        null=True,
        blank=True
    )

    testing_procedure = RichTextField(
        _("Procedimiento de testeo"),
        config_name='awesome_ckeditor',
        max_length=10000,
        null=True,
        blank=True
    )

    risks = models.ManyToManyField(
        "risks.risk",
        verbose_name=_("Riesgos asociados"),
        blank=True,
        related_name='controls'
    )

    sub_processes = models.ManyToManyField(
        "process.SubProcess",
        verbose_name=_("SubProcesos asociados"),
        blank=True,
        related_name='controls'
    )

    key_control = models.BooleanField(
        default=False, verbose_name=_("¿Es un key control?")
    )

    TYPE_CONTROL_CHOICES = (
        ("P", _("Preventivo")),
        ("D", _("Detectivo")),
    )

    control_type = models.CharField(
        _("Tipo de control"), max_length=2, choices=TYPE_CONTROL_CHOICES
    )

    AUTOMATION_CONTROL_CHOICES = (
        ("M", _("Manual")),
        ("A", _("Automático")),
        ("S", _("Semiautomático")),
    )

    automation = models.CharField(
        _("Automatización del control"),
        max_length=2,
        choices=AUTOMATION_CONTROL_CHOICES,
    )

    systems = models.CharField(
        _("Sistemas"), max_length=140, blank=True, null=True)
    
    plant = models.CharField(
        _("Planta"), max_length=140, blank=True, null=True)

    control_frequency = models.CharField(
        _("Frecuencia del control"), max_length=2, choices=FREQUENCY_CONTROL_CHOICES
    )

    ASSERTION_CHOICES = (
        ("-", _("No aplica")),
        ("Y", _("Sí")),
        ("N", _("No")),
    )

    is_gap = models.CharField(
        _("GAP"), max_length=1, choices=ASSERTION_CHOICES, default="-"
    )

    assert_existence = models.CharField(
        _("Existency"), max_length=1, choices=ASSERTION_CHOICES, default="-"
    )

    assert_completeness = models.CharField(
        _("Completness"), max_length=1, choices=ASSERTION_CHOICES, default="-"
    )

    assert_valuation = models.CharField(
        _("Valuation"), max_length=1, choices=ASSERTION_CHOICES, default="-"
    )

    assert_rights = models.CharField(
        _("Obligation right"), max_length=1, choices=ASSERTION_CHOICES, default="-"
    )

    assert_disclosure = models.CharField(
        _("Presentation"), max_length=1, choices=ASSERTION_CHOICES, default="-"
    )

    assert_accurancy = models.CharField(
        _("Accurancy"), max_length=1, choices=ASSERTION_CHOICES, default="-"
    )

    assert_froud = models.CharField(
        _("Fraud"), max_length=1, choices=ASSERTION_CHOICES, default="-"
    )

    is_elc = models.BooleanField(
        default=False, verbose_name=_("¿Es un control ELC?")
    )

    evidence = RichTextField(
        _("Evidencia"),
        config_name='awesome_ckeditor',
        max_length=10000,
        null=True,
        blank=True
    )

    SCOPE_CHOICES = (
        ("G", _("Grupo")),
        ("P", _("Planta")),
    )

    scope = models.CharField(
        _("Alcance"),
        max_length=1,
        choices=SCOPE_CHOICES,
        null=True,
        blank=True
    )

    block = models.BooleanField(
        default=False,
        verbose_name=_("¿Bloqueado?")
    )

    def __str__(self):
        clean_name = strip_tags(self.name)
        if len(clean_name) > 100:
            clean_name = clean_name[:100] + "..."
        return f"{self.ref} - {clean_name}"

    class Meta:
        verbose_name = _("Control")
        verbose_name_plural = _("Controles")
        ordering = ["ref", ]

    def save(self, *args, **kwargs):
        self.ref = self.ref.upper()
        super().save(*args, **kwargs)

        from krm.companies.models import Company, CompanyControls
        for company in Company.objects.all():
            if CompanyControls.objects.filter(company=company, control=self).count() == 0:
                CompanyControls.objects.create(
                    company=company,
                    control=self
                )

    def domain_risks(self):
        domain_risks = []
        for risk in self.risks.all():
            if risk.risk_master.domain_risk.pk not in domain_risks:
                domain_risks.append(risk.risk_master.domain_risk.pk)
        return domain_risks

    def processes(self):
        processes = []
        for sub_process in self.sub_processes.all():
            if sub_process.process.pk not in processes:
                processes.append(sub_process.process.pk)
        return processes

    def companies(self):
        from krm.risks.models import RiskCompany
        companies = RiskCompany.objects.filter(
            risk__in=(self.risks.all())).values_list('company_id', flat=True)
        companies = set(companies)
        companies = list(companies)
        return companies

    def is_sciff(self):
        if self.is_gap == '-' and self.assert_existence == '-' and self.assert_completeness == '-' and self.assert_valuation == '-' and self.assert_rights == '-' and self.assert_disclosure == '-' and self.assert_accurancy == '-' and self.assert_froud == '-':
            return False
        else:
            return True

    @property
    def domain_risks_objects(self):
        domain_risks = []
        for risk in self.risks.all():
            if risk.risk_master.domain_risk not in domain_risks:
                domain_risks.append(risk.risk_master.domain_risk)

        return domain_risks

    @property
    def control_is_used_by_evaluation(self):
        from krm.evaluations.models import ControlTest
        return ControlTest.objects.filter(control=self).exists()
