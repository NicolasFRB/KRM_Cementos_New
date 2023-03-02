# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from krm.utils.models import AuditModel


class Questionnaire(AuditModel):
    """Questionnaire model.
    Modelo que usaremos para representar un cuestionario
    """

    ref = models.CharField(
        verbose_name=_("Ref"),
        max_length=200,
        unique=True
    )

    name = models.CharField(verbose_name=_("Nombre"), max_length=500)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Cuestionario")
        verbose_name_plural = _("Cuestionarios")
        ordering = ["name"]

    @property
    def questions(self):
        from .question_model import Question
        return Question.objects.filter(scopes__in=self.scopes.all()).distinct()
