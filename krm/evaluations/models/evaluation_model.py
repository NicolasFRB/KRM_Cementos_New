import datetime
from django.db import models

from django.utils.translation import gettext_lazy as _
from django.utils.html import strip_tags

from ckeditor.fields import RichTextField

from krm.utils.models import AuditModel
from krm.risks.models import DomainRisk
from krm.users.models import User


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

    admin_supervisor = models.ForeignKey(
        'users.User',
        verbose_name=_('Administrador que ha supervisado la evaluación'),
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    notification_text = models.TextField(
        _("Texto personalizado de notificación"),
        help_text=_("Este texto aparecerá en el correo de notificación de nueva evaluación"),
        max_length=5000,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.ref)

    class Meta:
        verbose_name = _("Evaluación KRC")
        verbose_name_plural = _("Evaluaciones KRC")

    @property
    def certification_period_with_year(self):
        if self.certification_period and self.certification_year:
            return f"{self.certification_period} - {self.certification_year}"
        elif self.certification_period:
            return self.certification_period
        elif self.certification_year:
            return self.certification_year
        return ""

    @property
    def is_completed_assing(self):
        for ct in self.control_tests.all():
            if ct.control_test_supervisor is None or ct.control_test_owner is None:
                return False
        return True

    def delete_notification_text(self):
        if self.notification_text:
            self.notification_text = None
            self.save()

    def get_all_control_test_in_evaluation(self):
        return self.control_tests.all()

    # RETURN number of ctrls by state in evaluation
    # OPTIONAL ARG: Filter by user
    def ncontrols_test_by_state(self, status, user=None, rol=None):

        if user and rol:
            if rol == 'control_test_owner':
                return self.control_tests.filter(
                    status=status,
                    control_test_owner=user,
                ).distinct().count()

            elif rol == 'control_test_supervisor':
                return self.control_tests.filter(
                    status=status,
                    control_test_supervisor=user,
                ).distinct().count()

        else:
            return self.control_tests.filter(
                status=status,
            ).distinct().count()

    # RETURN number of ctrl by result in evaluation
    # OPTIONAL ARG: Filter by user
    def ncontrols_test_by_result(self, result, user=None, rol=None):

        if user and rol:
            if rol == 'control_test_owner':
                return self.control_tests.filter(
                    result=result,
                    control_test_owner=user,
                ).distinct().count()

            elif rol == 'control_test_supervisor':
                return self.control_tests.filter(
                    result=result,
                    control_test_supervisor=user,
                ).distinct().count()

        else:
            return self.control_tests.filter(
                result=result,
            ).distinct().count()

    def get_domain_risk_in_evaluation(self):

        domain_risks_pks, already_checked = [], []
        for ct in self.control_tests.all():
            for r in ct.control.risks.all():

                if r.pk not in already_checked:
                    domain_pk = r.risk_master.domain_risk.pk
                    if domain_pk not in domain_risks_pks:
                        domain_risks_pks.append(domain_pk)
                    already_checked.append(r.pk)

        return DomainRisk.objects.filter(id__in=domain_risks_pks)

    # RETURN users by state of ctrl in evaluation
    def get_users_by_ct_state(self, status = None):

        if status == "WO":
            experts_id = set([rt.control_test_owner.pk for rt in self.control_tests.filter(
            status=status)])

        elif status == "WS":
            experts_id = set([rt.control_test_supervisor.pk for rt in self.control_tests.filter(
            status=status)])

        return User.objects.filter(id__in=experts_id)

    # GET EVALUATORS FOR NOTIFICATIONS TABLE BY STATE
    def get_evaluators_for_notifications_by_role(self, status):

        evaluators_all = self.get_users_by_ct_state(status)
        evaluators = []
        ev_pk_found = {}

        notif_subtype_map = {
            'WO': 'COwner',
            'WS': 'CSupervisor',
        }

        role_map = {
            'WO': 'control_test_owner',
            'WS': 'control_test_supervisor',
        }

        for evaluator in evaluators_all:

            notifications = [[n.action_description, n.created] for n in evaluator.actions_log.all() if self.ref in n.action_description and notif_subtype_map[status] in n.action_description]

            if evaluator.pk not in ev_pk_found:
                ev_pk_found[evaluator.pk] = len(evaluators)
                evaluators.append({
                    'qt_pk': -1,
                    'evaluator_pk': evaluator.pk,
                    'evaluator_email': evaluator.email,
                    'objects_pending': 0,
                    'objects_delivered': 0,
                    'notifications': notifications,
                    })

            evaluators[ev_pk_found[evaluator.pk]]['objects_pending'] += self.ncontrols_test_by_state(status, evaluator, role_map[status])

            if status == "WO":
                evaluators[ev_pk_found[evaluator.pk]]['objects_delivered'] += self.ncontrols_test_by_state('WS', evaluator, role_map[status])

            evaluators[ev_pk_found[evaluator.pk]]['objects_delivered'] += self.ncontrols_test_by_state('WA', evaluator, role_map[status])
            evaluators[ev_pk_found[evaluator.pk]]['objects_delivered'] += self.ncontrols_test_by_state('FI', evaluator, role_map[status])

            if evaluators[ev_pk_found[evaluator.pk]]['objects_pending'] > 0 and status == "WO":
                evaluators[ev_pk_found[evaluator.pk]]['qt_pk'] = self.control_tests.filter(
                    evaluation__ref = self.ref,
                    status=status,
                    control_test_owner=evaluator,
                    ).first().pk

            if evaluators[ev_pk_found[evaluator.pk]]['objects_pending'] > 0 and status == "WS":
                evaluators[ev_pk_found[evaluator.pk]]['qt_pk'] = self.control_tests.filter(
                    evaluation__ref = self.ref,
                    status=status,
                    control_test_supervisor=evaluator,
                    ).first().pk

        return evaluators

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
