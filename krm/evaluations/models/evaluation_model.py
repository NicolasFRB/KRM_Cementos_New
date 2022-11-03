import datetime
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags

from ckeditor.fields import RichTextField

from krm.utils.models import AuditModel


def year_choices():
    return [(r, r) for r in range(2000, datetime.date.today().year + 1)]


def current_year():
    return datetime.date.today().year


class Evaluation(AuditModel):
    """Evaluation model.
    Modelo que usaremos para representar una evaluación
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
        related_name="evaluations"
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

    date_intermediate = models.DateField(
        verbose_name=_("Fecha límite para Control Owners"),
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
        ("SI", _("Sin iniciar")),
        ("EP", _("En proceso")),
        ("FI", _("Finalizado")),
    )

    status = models.CharField(
        _("Estado"),
        max_length=2,
        choices=PROCESS_STATUS_CHOICES,
        default="SI",
    )

    allow_self_autosupervision = models.BooleanField(
        _("Permitir auto supervisión de controles"),
        help_text=_(
            "Si se habilita, el Control Supervisor del test de control puede ser el mismo Control Owner"
        ),
        default=False,
    )

    def __str__(self):
        return self.ref

    class Meta:
        verbose_name = _("Evaluación KRC")
        verbose_name_plural = _("Evaluaciones KRC")

    @property
    def is_completed_assing(self):
        for ct in self.control_tests.all():
            if ct.control_test_supervisor is None or ct.control_test_owner is None:
                return False
        return True

    # RETURN number of risks by state in evaluation
    # OPTIONAL ARG: Filter by user
    def ncontrols_test_by_state(self, status, user = None, rol = None):

        if user and rol:
            if rol == 'control_test_owner':
                return self.control_tests.filter(
                        status = status,
                        control_test_owner = user,
                    ).distinct().count()
            
            elif rol == 'control_test_supervisor':
                return self.control_tests.filter(
                        status = status,
                        control_test_supervisor = user,
                    ).distinct().count()
                    
        else:
            return self.control_tests.filter(
                    status = status,
                ).distinct().count()
                
    # def generate_control_tests(self, only_key_control=False):
    #     from krc.process.models import Control
    #     from krc.process_test.models import ControlTest

    #     if only_key_control:
    #         controls = Control.objects.filter(
    #             risk__in=self.process.risks.all(), key_control=True
    #         )
    #     else:
    #         controls = Control.objects.filter(
    #             risk__in=self.process.risks.all())

    #     n_created = 0
    #     for control in controls:
    #         ct, created = ControlTest.objects.get_or_create(
    #             process_test=self, control=control, date_begin=self.date_begin
    #         )
    #         if created:
    #             n_created += 1

    #     return n_created

    # @property
    # def is_completed_assing(self):
    #     for ct in self.control_tests.all():
    #         if ct.control_test_supervisor is None or ct.control_test_owner is None:
    #             return False
    #     return True

    # def get_controls_si(self, controls_filter):
    #     return self.control_tests.filter(
    #         status="SI", control__in=controls_filter
    #     ).count()

    # def get_controls_wo(self, controls_filter):
    #     return self.control_tests.filter(
    #         status="WO", control__in=controls_filter
    #     ).count()

    # def get_controls_ws(self, controls_filter):
    #     return self.control_tests.filter(
    #         status="WS", control__in=controls_filter
    #     ).count()

    # def get_controls_ef(self, controls_filter):
    #     return self.control_tests.filter(
    #         result="EF", control__in=controls_filter
    #     ).count()

    # def get_controls_ne(self, controls_filter):
    #     return self.control_tests.filter(
    #         result="NE", control__in=controls_filter
    #     ).count()

    # def get_absolute_url(self):
    #     return reverse_lazy(
    #         "process_test:ga_process_test_detail", kwargs={"pk": self.pk}
    #     )


# def update_filename(instance, filename):
#     path = "process_test/"
#     name = filename.replace(" ", "_").lower()
#     name = slugify(name)
#     format = (
#         path
#         + str(instance.control.pk)
#         + "_"
#         + urllib.parse.quote(name)
#         + Path(filename).suffix
#     )

#     return format
