from django.db import models


class AuditModel(models.Model):
    """Modelo para heredar con campos de fecha de creación y edición de modo automático.

    AuditModel es una clase abstracta que se usará para heredar funcionalidad por parte de todos los modelos de la aplicación. Esta clase proveerá de los siguientes atributos::
        + created (DateTime): Store the datetime the object was created.
        + modified (DateTime): Store the last datetime the object was modified.
    """

    created = models.DateTimeField(
        'Fecha de creación',
        auto_now_add=True,
        help_text='Fecha y hora de la creación del objeto.'
    )
    modified = models.DateTimeField(
        'Fecha de modificación',
        auto_now=True,
        help_text='Fecha y hora de la última modificación del objeto.'
    )

    class Meta:
        """Meta option."""

        abstract = True

        get_latest_by = 'created'
        ordering = ['-modified', '-created']


class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
