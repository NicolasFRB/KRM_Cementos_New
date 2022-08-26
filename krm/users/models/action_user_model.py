from django.db import models

from django.utils.translation import gettext_lazy as _

from krm.utils.models import AuditModel


class ActionLogUser(AuditModel):
    """ActionLogUser model.
    Modelo que usaremos para representar las acciones realizadas por un usuario
    """

    user = models.ForeignKey(
        'users.User',
        related_name="actions_log",
        on_delete=models.CASCADE
    )
    action_description = models.CharField(
        _("Descripción de la acción realizada"),
        max_length=300
    )

    class Meta:
        verbose_name = _("Acción de usuario")
        verbose_name_plural = _("Acciones de usuario")
        ordering = [
            "created",
        ]

    def __str__(self):
        return "{} - {}".format(
            self.created.strftime("%d %b %Y %H:%M:%S"), self.action_description
        )
        # return '%s - %s'.format(self.created, self.action_description)
