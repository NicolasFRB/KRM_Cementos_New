import datetime
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags

from ckeditor.fields import RichTextField

from krm.utils.models import AuditModel
from krm.users.models import User
from krm.risks.models import DomainRisk


def year_choices():
    return [(r, r) for r in range(2000, datetime.date.today().year + 1)]


def current_year():
    return datetime.date.today().year


class EvaluationKrmInherent(AuditModel):
    """Evaluation de Riesgo Inherente model.
    """

    ref = models.CharField(
        _("REF"),
        max_length=140,
        unique=True
    )

    company = models.ForeignKey(
        "companies.Company",
        verbose_name=_("Empresa"),
        on_delete=models.CASCADE,
        related_name="evaluations_inherent_krm"
    )

    description = RichTextField(
        _("Descripción"),
        config_name='awesome_ckeditor',
        max_length=10000,
        null=True,
        blank=True
    )

    date_begin = models.DateField(
        verbose_name=_("Inicio de Evaluación"),
    )

    date_end = models.DateField(
        verbose_name=_("Fin de la Evaluación"),
    )

    certification_year = models.IntegerField(
        _("Año de certificación"),
        choices=year_choices(),
        default=current_year()
    )

    certification_period = models.CharField(
        verbose_name=_("Periodo de certificación"),
        max_length=140,
        null=True,
        blank=True
    )

    PROCESS_STATUS_CHOICES = (
        ("EP", _("En proceso")),
        ("FI", _("Finalizado")),
    )

    status = models.CharField(
        _("Estado"),
        max_length=2,
        choices=PROCESS_STATUS_CHOICES,
        default="EP",
    )

    def __str__(self):
        return self.ref

    class Meta:
        verbose_name = _("Evaluación Inherente KRM")
        verbose_name_plural = _("Evaluaciones Inherentes KRM")

    # RETURN number of risks by state in evaluation
    # OPTIONAL ARG: Filter by user
    def nrisk_test_inherents_by_state(self, status, user = None):

        if user:
            return self.risk_test_inherents.filter(
                    status = status,
                    expert = user,
                ).distinct().count()
        else:
            return self.risk_test_inherents.filter(
                    status = status,
                ).distinct().count()

    # RETURN experts by state of risks in evaluation
    def get_experts_by_rit_state(self, status):
        
        experts_id = set([rt.expert.pk for rt in self.risk_test_inherents.filter(
                    status = status)])
        
        return User.objects.filter(id__in = experts_id)

    # RETURN domain_risks in evaluation
    def get_domain_risk_in_evaluation(self):

        domain_risks_pks = []
        for rt in self.risk_test_inherents.all():
            domain_pk = rt.risk.risk.risk_master.domain_risk.pk
                
            if domain_pk not in domain_risks_pks:
                domain_risks_pks.append(domain_pk)
        
        return DomainRisk.objects.filter(id__in = domain_risks_pks)