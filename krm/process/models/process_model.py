from django.db import models

import datetime

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags

from django.conf import settings

# Utilities
from krm.utils.models import AuditModel


# class ProcessLockedManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(locked=False)


class Process(AuditModel):
    """Process model.
    Modelo que usaremos para representar un proceso
    """

    ref = models.CharField(
        verbose_name=_("Identificador"), max_length=140
    )

    name = models.CharField(verbose_name=_("Nombre"), max_length=500)

    description = models.TextField(
        _("Descripción"), max_length=10000, null=True, blank=True
    )

    # locked = models.BooleanField(verbose_name=_("Bloqueado"), default=False)

    def __str__(self):
        return self.name

    # objects = models.Manager()  # The default manager.
    # lockeds = (
    #     ProcessLockedManager()
    # )  # El manager por defecto solo devolverá los procesos que no estén bloqueados

    class Meta:
        verbose_name = _("Proceso")
        verbose_name_plural = _("Procesos")
        ordering = ["name"]

    # @property
    # def description_safe(self):
    #     return str(strip_tags(self.description))

    # @property
    # def risks(self):
    #     from krc.process.models import Risk

    #     return Risk.objects.filter(sub_process__in=self.sub_processes.all())

    # @property
    # def controls(self):
    #     from krc.process.models import Control

    #     return Control.objects.filter(risk__in=self.risks)

    # @property
    # def get_regulatory_frameworks(self):
    #     rfs = []
    #     for control in self.controls.all():
    #         for rf in control.regulatory_frameworks.all():
    #             rfs.append(rf)
    #     rfs = set(rfs)
    #     return rfs

    # def duplicate(self):

    #     from krc.process.models import SubProcess, Risk, Control

    #     # Creamos un nuevo Proceso
    #     today_date = "{}{}{}".format(
    #         str(datetime.datetime.today().year),
    #         str(datetime.datetime.today().month).zfill(2),
    #         str(datetime.datetime.today().day).zfill(2),
    #     )
    #     new_process = Process.objects.create(
    #         name=self.name + " #" + today_date,
    #         acronym=self.acronym,
    #         description=self.description,
    #         locked=True,
    #     )

    #     # Copiamos los grupos empresariales que pueden hacer uso del proceso
    #     for bg in self.business_group.all():
    #         new_process.business_group.add(bg)

    #     # Ahora copiamos los subprocesos
    #     for sb in self.sub_processes.all():
    #         new_subprocess = SubProcess.objects.create(
    #             ref=sb.ref,
    #             name=sb.name,
    #             description=sb.description,
    #             process=new_process,
    #         )

    #         for risk in sb.risks.all():
    #             new_risk = Risk.objects.create(
    #                 ref=risk.ref,
    #                 description=risk.description,
    #                 sub_process=new_subprocess,
    #                 category=risk.category,
    #                 impact=risk.impact,
    #                 probability=risk.probability,
    #                 rating=risk.rating,
    #             )

    #             for control in risk.controls.all():
    #                 new_control = Control.objects.create(
    #                     ref=control.ref,
    #                     objective=control.objective,
    #                     description=control.description,
    #                     action_plan=control.action_plan,
    #                     testing_procedure=control.testing_procedure,
    #                     risk=new_risk,
    #                     key_control=control.key_control,
    #                     control_type=control.control_type,
    #                     automation=control.automation,
    #                     systems=control.automation,
    #                     control_frequency=control.control_frequency,
    #                     is_gap=control.is_gap,
    #                     assert_existence=control.assert_existence,
    #                     assert_completeness=control.assert_completeness,
    #                     assert_valuation=control.assert_valuation,
    #                     assert_rights=control.assert_rights,
    #                     assert_disclosure=control.assert_disclosure,
    #                     assert_accurancy=control.assert_accurancy,
    #                     assert_froud=control.assert_froud,
    #                 )
    #                 for rf in control.regulatory_frameworks.all():
    #                     new_control.regulatory_frameworks.add(rf)
    #                     new_control.save()

    #     return new_process
