import datetime
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags

from ckeditor.fields import RichTextField

from krm.utils.models import AuditModel
from krm.users.models import User


def year_choices():
    return [(r, r) for r in range(2000, datetime.date.today().year + 1)]


def current_year():
    return datetime.date.today().year


class EvaluationQuestionnaire(AuditModel):
    """Evaluation de Cuestionario
    """

    ref = models.CharField(
        _("REF"),
        max_length=140,
        unique=True
    )

    questionnaire = models.ForeignKey(
        "questionnaires.Questionnaire",
        verbose_name=_("Cuestionario"),
        on_delete=models.CASCADE,
        related_name='evaluations'
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
        verbose_name = _("Evaluación de Cuestionario")
        verbose_name_plural = _("Evaluaciones de Cuestionario")

    # RETURN number of risks by state in evaluation
    # OPTIONAL ARG: Filter by user
    def nquestion_test_by_state(self, status, user=None):

        if user:
            return self.question_tests.filter(
                status=status,
                evaluator=user,
            ).distinct().count()
        else:
            return self.question_tests.filter(
                status=status,
            ).distinct().count()

    # RETURN experts by state of risks in evaluation
    def get_evaluators_by_qt_state(self, status):

        evaluators_id = set([qt.evaluator.pk for qt in self.question_tests.filter(
            status=status)])

        return User.objects.filter(id__in=evaluators_id)

    # GET EVALUATED SCOPES
    def evaluated_scopes(self):

        from krm.questionnaires.models import Scope
        
        scopes_id = set([qt.scope.pk for qt in self.question_tests.all()])

        return Scope.objects.filter(id__in = scopes_id)
