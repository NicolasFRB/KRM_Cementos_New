# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from krm.utils.models import AuditModel

from krm.users.models import User


class Question(AuditModel):
    """Question model.
    Modelo que usaremos para representar una pregunta
    """

    ref = models.CharField(
        verbose_name=_("Ref"),
        max_length=2000,
    )

    scopes = models.ManyToManyField(
        "questionnaires.Scope",
        verbose_name=_("Alcances"),
        blank=True,
        related_name='questions'
    )

    title = models.TextField(
        verbose_name=_("Enunciado"),
        max_length=5000
    )

    def __str__(self):
        return str(self.ref)

    class Meta:
        verbose_name = _("Pregunta")
        verbose_name_plural = _("Preguntas")
        ordering = ['ref']

    @property
    def potential_respondents(self):
        User.objects.filter(pk__in=self.scopes.values_list(
            'user_to_assign', flat=True).distinct())

    @property
    def questionnaires(self):
        return list(set([scope.questionnaire for scope in self.scopes.all()]))

    @property
    def questionnaires_pk(self):
        return list(set([scope.questionnaire.pk for scope in self.scopes.all()]))

    @property
    def title_lang_split(self):
        return self.title.split('ENG:')
