# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from krm.utils.models import AuditModel


class Scope(AuditModel):
    """Scope model.
    Modelo que usaremos para representar el alcance (hijos) de un cuestionario
    """

    ref = models.CharField(
        verbose_name=_("Ref"),
        max_length=200
    )

    name = models.CharField(verbose_name=_("Nombre"), max_length=500)

    questionnaire = models.ForeignKey(
        "questionnaires.Questionnaire",
        verbose_name=_("Cuestionario"),
        on_delete=models.CASCADE,
        related_name='scopes'
    )

    user_to_assign = models.ManyToManyField(
        'users.User',
        verbose_name=_('Posibles respondedores'),
        blank=True,
    )

    def __str__(self):
        return self.ref

    class Meta:
        verbose_name = _("Alcance")
        verbose_name_plural = _("Alcances")
        ordering = ["name"]
