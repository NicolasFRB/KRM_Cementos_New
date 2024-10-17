import xlwt

from django.shortcuts import render
from django.conf import settings

# Create your views here.
from django.shortcuts import render
from django.views.generic import (
    FormView,
    TemplateView,
    ListView,
    DetailView,
)
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from krm.evaluations.models import ControlTest

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations.models import Evaluation
from krm.companies.models import Company
from krm.controls.models import Control

from krm.evaluations.forms import (
    EvaluationActionForm,
)

from krm.utils.utils import clean_html

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from krm.users.decorators import (
    user_can_view_evaluation,
    is_auditor
)


@method_decorator([login_required, is_auditor], name='dispatch')
class AuEvaluationListView(ListView):
    model = Evaluation
    template_name = 'evaluations/AuEvaluationList.html'
    context_object_name = 'evaluations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones'), 'url': reverse(
                'evaluations:au_evaluation_list')},
        ]
        context['page_title'] = _('Evaluaciones')
        context['breadcrums'] = breadcrums
        context['actions'] = []

        ev_pending = Evaluation.objects.filter(status__in=["SI", "EP"])
        ev_finished = Evaluation.objects.filter(status="FI")

        for ev in ev_pending:
            ev.ncontrols_test_by_state_si = ev.ncontrols_test_by_state(
                "SI")
            ev.ncontrols_test_by_state_wo = ev.ncontrols_test_by_state(
                "WO")
            ev.ncontrols_test_by_state_ws = ev.ncontrols_test_by_state(
                "WS")
            ev.ncontrols_test_by_state_wa = ev.ncontrols_test_by_state(
                "WA")
            ev.ncontrols_test_by_state_fi = ev.ncontrols_test_by_state(
                "FI")

            ev.domain_risks = ev.get_domain_risk_in_evaluation()

        for ev in ev_finished:
            ev.ncontrols_test_by_state_si = ev.ncontrols_test_by_state(
                "SI")
            ev.ncontrols_test_by_state_wo = ev.ncontrols_test_by_state(
                "WO")
            ev.ncontrols_test_by_state_ws = ev.ncontrols_test_by_state(
                "WS")
            ev.ncontrols_test_by_state_wa = ev.ncontrols_test_by_state(
                "WA")
            ev.ncontrols_test_by_state_fi = ev.ncontrols_test_by_state(
                "FI")

            ev.domain_risks = ev.get_domain_risk_in_evaluation()

        context['evaluations_pending'] = ev_pending
        context['evaluations_finished'] = ev_finished

        context['js_template'] = ['js/custom/datatables.js']

        return context


@method_decorator([login_required, is_auditor, user_can_view_evaluation], name='dispatch')
class AuEvaluationDetailView(FormView):
    template_name = 'evaluations/AuEvaluationDetail.html'
    model = Evaluation
    form_class = EvaluationActionForm

    def dispatch(self, request, *args, **kwargs):
        evaluation = get_object_or_404(Evaluation, pk=self.kwargs.get("pk"))
        self.evaluation = evaluation
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['evaluation'] = self.evaluation

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones'), 'url': reverse(
                'evaluations:au_evaluation_list')},
            {'title': self.evaluation.ref}
        ]
        context['page_title'] = f"{_('Evaluación')} : {self.evaluation.ref}"
        context['breadcrums'] = breadcrums
        context['actions'] = []
        context['js_template'] = ['js/custom/datatables.js']

        context['evaluation'].ncontrols_test_by_state_si = context['evaluation'].ncontrols_test_by_state(
            "SI")
        context['evaluation'].ncontrols_test_by_state_wo = context['evaluation'].ncontrols_test_by_state(
            "WO")
        context['evaluation'].ncontrols_test_by_state_ws = context['evaluation'].ncontrols_test_by_state(
            "WS")
        context['evaluation'].ncontrols_test_by_state_wa = context['evaluation'].ncontrols_test_by_state(
            "WA")
        context['evaluation'].ncontrols_test_by_state_fi = context['evaluation'].ncontrols_test_by_state(
            "FI")

        context['evaluation'].ncontrols_test_by_result_se = context['evaluation'].ncontrols_test_by_result(
            "SE")
        context['evaluation'].ncontrols_test_by_result_ef = context['evaluation'].ncontrols_test_by_result(
            "EF")
        context['evaluation'].ncontrols_test_by_result_ne = context['evaluation'].ncontrols_test_by_result(
            "NE")
        context['evaluation'].ncontrols_test_by_result_na = context['evaluation'].ncontrols_test_by_result(
            "NA")

        context['evaluation'].domain_risks = context['evaluation'].get_domain_risk_in_evaluation()

        return context

    def form_valid(self, form):
        action = form.cleaned_data["action"]
        evaluation = self.evaluation

        if action == "i":
            evaluation.status = "EP"
            evaluation.save()
            users_notificated = []
            for ct in evaluation.control_tests.all():
                ct.status = "WO"
                ct.save()
                if ct.control_test_owner not in users_notificated:
                    users_notificated.append(ct.control_test_owner)
                    ct.send_notification('Initial notification')

            messages.add_message(
                self.request,
                messages.SUCCESS,
                _("Evaluación iniciada correctamente"),
            )
        elif action == 'f':
            evaluation.status = "FI"
            evaluation.admin_supervisor = self.request.user
            evaluation.save()
            evaluation.control_tests.update(
                status='FI'
            )

            messages.add_message(
                self.request,
                messages.SUCCESS,
                _("Evaluación finalizada correctamente"),
            )
        elif action == 'd':

            evaluation = self.evaluation

            # Comienzo de la creacion de archivo de descarga del Test de Proceso
            filename = "{}_download_evaluation.xls".format(evaluation.pk)
            response = HttpResponse(content_type="application/ms-excel")
            response["Content-Disposition"] = 'attachment; filename="{}"'.format(
                filename
            )

            wb = xlwt.Workbook(encoding="utf-8")
            ws = wb.add_sheet("Controls")

            # Sheet header, first row
            row_num = 0

            font_style_title = xlwt.easyxf("align: vert centre, horiz left")
            font_style_title.font.bold = True

            font_style_title_wrap = xlwt.easyxf(
                "align: vert centre, horiz left, wrap yes"
            )
            font_style_title_wrap.font.bold = True

            font_style_body = xlwt.easyxf("align: vert top, horiz left")
            font_style_body_wrap = xlwt.easyxf(
                "align: vert top, horiz left, wrap yes"
            )

            ws.col(0).width = 256 * 25
            ws.col(1).width = 256 * 60
            ws.col(2).width = 256 * 80
            ws.col(3).width = 256 * 20
            ws.col(4).width = 256 * 80
            ws.col(5).width = 256 * 80
            ws.col(6).width = 256 * 80
            ws.col(7).width = 256 * 80
            ws.col(8).width = 256 * 20
            ws.col(9).width = 256 * 20
            ws.col(10).width = 256 * 20
            ws.col(11).width = 256 * 20
            ws.col(12).width = 256 * 20
            ws.col(13).width = 256 * 20
            ws.col(14).width = 256 * 20
            ws.col(15).width = 256 * 20
            ws.col(16).width = 256 * 20
            ws.col(17).width = 256 * 20
            ws.col(18).width = 256 * 20
            ws.col(19).width = 256 * 20
            ws.col(20).width = 256 * 20
            ws.col(21).width = 256 * 65
            ws.col(22).width = 256 * 65
            ws.col(23).width = 256 * 30
            ws.col(24).width = 256 * 45
            ws.col(25).width = 256 * 45
            ws.col(26).width = 256 * 45
            ws.col(27).width = 256 * 30
            ws.col(28).width = 256 * 45
            ws.col(29).width = 256 * 45
            ws.col(30).width = 256 * 45
            ws.col(31).width = 256 * 45
            ws.col(32).width = 256 * 45
            ws.col(33).width = 256 * 45
            ws.col(34).width = 256 * 45

            columns = [
                "EVALUACIÓN",  # 0
                "SUBPROCESOS",  # 1
                "RIESGOS",  # 2
                "CONTROL - ID",  # 3
                "CONTROL - OBJETIVO",  # 4
                "CONTROL - DESCRIPCIÓN",  # 5
                "CONTROL - PLAN DE ACCIÓN",  # 6
                "CONTROL - PROCEDIMIENTO DE TESTEO",  # 7
                "CONTROL - KEY",  # 8
                "CONTROL - TIPO",  # 9
                "CONTROL - AUTOMATIZACIÓN",  # 10
                "CONTROL - SISTEMAS",  # 11
                "CONTROL - PERIODICIDAD",  # 12
                "CONTROL - GAP",  # 13
                "EXISTENCY",  # 14
                "COMPLETNESS",  # 15
                "VALUATION",  # 16
                "OBLIGATION RIGHT",  # 17
                "PRESENTATION",  # 18
                "ACCURACY",  # 19
                "FRAUD",  # 20
                "DOMINIOS DE RIESGO",  # 21
                "TEST DE CONTROL ID",  # 22
                "TEST DE CONTROL STATUS",  # 23
                "CONTROL OWNER",  # 24
                "CONTROL OWNER EMPRESAS",  # 25
                "CONTROL OWNER RESPUESTA",  # 26
                "CONTROL OWNER FECHA RESPUESTA",  # 27
                "CONTROL OWNER ADJUNTO",  # 28
                "ADJUNTO LINK",  # 29
                "RESULTADO\nEF (efectivo)\nNE (no efectivo)\nNA (No aplica en el periodo certificado)",  # 30
                "PLAN DE REMEDIACIÓN TEXTO",  # 31
                "PLAN DE REMEDIACIÓN FECHA",  # 32
                "PLAN DE REMEDIACIÓN LINK",  # 33
                "CONTROL SUPERVISOR",  # 34
                "CONTROL SUPERVISOR EMPRESAS",  # 35
                "CONTROL SUPERVISOR RESPUESTA",  # 36
                "CONTROL SUPERVISOR FECHA RESPUESTA",  # 37
                "CONTROL ADMIN",  # 38
                "CONTROL ADMIN RESPUESTA",  # 39
                "CONTROL ADMIN FECHA RESPUESTA",  # 40
            ]

            for col_num in range(len(columns)):
                if col_num in (21, 28):
                    ws.write(
                        row_num, col_num, columns[col_num], font_style_title_wrap
                    )
                else:
                    ws.write(row_num, col_num,
                             columns[col_num], font_style_title)

            for ct in evaluation.control_tests.all().order_by("control__ref"):
                row_num += 1
                ws.write(
                    row_num, 0, evaluation.ref, font_style_body
                )  # 0
                sb_text = ''
                for sb in ct.control.sub_processes.all():
                    sb_text += f'{sb.ref} - {sb.name}\n'
                ws.write(
                    row_num, 1, sb_text, font_style_body_wrap
                )  # 1
                risk_text = ''
                for risk in ct.control.risks.all():
                    risk_text += f'{risk.ref} - {risk.name}\n'
                ws.write(
                    row_num,
                    2,
                    risk_text,
                    font_style_body_wrap,
                )  # 2

                ws.write(row_num, 3, ct.control.ref, font_style_body)  # 3
                ws.write(
                    row_num,
                    4,
                    clean_html(ct.control.name),
                    font_style_body_wrap,
                )  # 4
                ws.write(
                    row_num,
                    5,
                    clean_html(ct.control.description),
                    font_style_body_wrap,
                )  # 5
                ws.write(
                    row_num,
                    6,
                    '',
                    font_style_body_wrap,
                )  # 6
                ws.write(
                    row_num,
                    7,
                    clean_html(ct.control.testing_procedure),
                    font_style_body_wrap,
                )  # 7

                rf_text = ""

                ws.write(row_num, 8, ct.control.key_control,
                         font_style_body)  # 8
                ws.write(
                    row_num,
                    9,
                    ct.control.get_control_type_display(),
                    font_style_body,
                )  # 9
                ws.write(
                    row_num,
                    10,
                    ct.control.get_automation_display(),
                    font_style_body,
                )  # 10
                ws.write(row_num, 11, ct.control.systems,
                         font_style_body)  # 11
                ws.write(
                    row_num,
                    12,
                    ct.control.get_control_frequency_display(),
                    font_style_body,
                )  # 12
                ws.write(
                    row_num, 13, ct.control.get_is_gap_display(), font_style_body
                )  # 13
                ws.write(
                    row_num,
                    14,
                    ct.control.get_assert_existence_display(),
                    font_style_body,
                )  # 14
                ws.write(
                    row_num,
                    15,
                    ct.control.get_assert_completeness_display(),
                    font_style_body,
                )  # 15
                ws.write(
                    row_num,
                    16,
                    ct.control.get_assert_valuation_display(),
                    font_style_body,
                )  # 16
                ws.write(
                    row_num,
                    17,
                    ct.control.get_assert_rights_display(),
                    font_style_body,
                )  # 17
                ws.write(
                    row_num,
                    18,
                    ct.control.get_assert_disclosure_display(),
                    font_style_body,
                )  # 18
                ws.write(
                    row_num,
                    19,
                    ct.control.get_assert_accurancy_display(),
                    font_style_body,
                )  # 19
                ws.write(
                    row_num,
                    20,
                    ct.control.get_assert_froud_display(),
                    font_style_body,
                )  # 20

                domain_risks_text = ''
                for risk in ct.control.risks.all():
                    domain_risks_text += f'{risk.risk_master.domain_risk.ref} - {risk.risk_master.domain_risk.name}\n'
                ws.write(
                    row_num,
                    21,
                    domain_risks_text,
                    font_style_body_wrap,
                )  # 21

                ws.write(row_num, 22, ct.identifier, font_style_body)  # 22
                ws.write(
                    row_num, 23, ct.get_status_display(), font_style_body
                )  # 23
                ws.write(
                    row_num, 24, ct.control_test_owner.email, font_style_body
                )  # 24

                # Buscamos las compañías del control owner, solo aqueyas que sean del grupo empresarial al que pertenece
                # la compañía sobre la que se ha lanzado el test de proceso
                co_company_str = ""
                for co_company in ct.control_test_owner.companies.all():
                    co_company_str = "{}{}\n".format(
                        co_company_str, co_company.name
                    )
                ws.write(row_num, 25, co_company_str,
                         font_style_body_wrap)  # 25

                # Buscamos la última respuesta del control owner
                if ct.answers.filter(user=ct.control_test_owner).count() > 0:
                    # Si el control owner es el mismo que el control supervisor habrá que coger la penúltima respuesta ya que se supone que el control supervisor es el último en responder
                    if ct.control_test_owner == ct.control_test_supervisor:
                        if (
                            ct.answers.filter(
                                user=ct.control_test_owner).count()
                            > 1
                        ):
                            answer = ct.answers.filter(
                                user=ct.control_test_owner
                            ).order_by("-created")[1]
                        else:
                            answer = ct.answers.filter(
                                user=ct.control_test_owner
                            ).order_by("-created")[0]
                    else:
                        answer = (
                            ct.answers.filter(user=ct.control_test_owner)
                            .order_by("-created")
                            .first()
                        )
                    ws.write(
                        row_num,
                        26,
                        answer.description.replace("<br>", "\n")
                        .replace("<p>", "")
                        .replace("</p>", "\n"),
                        font_style_body_wrap,
                    )  # 26
                    ws.write(
                        row_num,
                        27,
                        answer.created.strftime("%d/%m/%Y, %H:%M:%S"),
                        font_style_body,
                    )  # 27
                    if answer.attachment_1.name:
                        resp_attach = "Si"
                    else:
                        resp_attach = "No"
                    ws.write(row_num, 28, resp_attach, font_style_body)  # 28

                    if answer.attachment_1.name:
                        resp_attach = (
                            settings.SITE_URL + "/media/" + answer.attachment_1.name
                        )
                        ws.write(
                            row_num,
                            29,
                            xlwt.Formula(
                                'HYPERLINK("%s";"Enlace al documento")'
                                % resp_attach
                            ),
                            font_style_body,
                        )  # 29
                    else:
                        resp_attach = " "
                        ws.write(row_num, 29, resp_attach,
                                 font_style_body)  # 29

                ws.write(
                    row_num, 30, ct.get_result_display(), font_style_body
                )  # 30

                if ct.remediation_plans.count() > 0:
                    remediation_plan = ct.remediation_plans.order_by(
                        "created"
                    ).first()
                    ws.write(
                        row_num, 31, remediation_plan.description, font_style_body
                    )  # 31
                    ws.write(
                        row_num,
                        32,
                        remediation_plan.date_end.strftime(
                            "%d/%m/%Y, %H:%M:%S"),
                        font_style_body,
                    )  # 32

                    if remediation_plan.attachment:
                        resp_attach = settings.SITE_URL + "/media/" + remediation_plan.attachment.name
                        ws.write(
                            row_num,
                            33,
                            xlwt.Formula(
                                'HYPERLINK("%s";"Enlace al documento")'
                                % resp_attach
                            ),
                            font_style_body,
                        )  # 33

                ws.write(
                    row_num, 34, ct.control_test_supervisor.email, font_style_body
                )  # 34

                # Buscamos las compañías del control supervisor, solo aqueyas que sean del grupo empresarial al que pertenece
                # la compañía sobre la que se ha lanzado el test de proceso
                cs_company_str = ""
                for cs_company in ct.control_test_supervisor.companies.all():
                    cs_company_str = "{}{}\n".format(
                        cs_company_str, cs_company.name
                    )
                ws.write(row_num, 35, cs_company_str,
                         font_style_body_wrap)  # 35

                # Buscamos la última respuesta del control supervisor
                if ct.answers.filter(user=ct.control_test_supervisor).count() > 0:
                    answer = (
                        ct.answers.filter(user=ct.control_test_supervisor)
                        .order_by("-created")
                        .first()
                    )
                    ws.write(
                        row_num,
                        36,
                        answer.description.replace("<br>", "\n")
                        .replace("<p>", "")
                        .replace("</p>", "\n"),
                        font_style_body_wrap,
                    )  # 36
                    ws.write(
                        row_num,
                        37,
                        answer.created.strftime("%d/%m/%Y, %H:%M:%S"),
                        font_style_body
                    )  # 37

                if ct.answers.last() is not None:
                    if ct.answers.last().user.is_superuser:
                        last_admin_answer = ct.answers.last()

                        ws.write(
                            row_num,
                            38,
                            last_admin_answer.user.email,
                            font_style_body_wrap
                        )  # 38
                        ws.write(
                            row_num,
                            39,
                            last_admin_answer.description.replace(
                                "<br>", "\n"),
                            font_style_body_wrap
                        )  # 39
                        ws.write(
                            row_num,
                            40,
                            last_admin_answer.created.strftime(
                                "%d/%m/%Y, %H:%M:%S"),
                            font_style_body_wrap
                        )  # 40

            wb.save(response)

            return response

        elif action == 'a':
            filename = "{} template_asign_evaluation.xls".format(evaluation.pk)
            response = HttpResponse(content_type="application/ms-excel")
            response["Content-Disposition"] = 'attachment; filename="{}"'.format(
                filename
            )

            wb = xlwt.Workbook(encoding="utf-8")
            ws = wb.add_sheet("Controls")

            ws.col(0).width = 256 * 25
            ws.col(1).width = 256 * 25
            ws.col(2).width = 256 * 40
            ws.col(3).width = 256 * 40
            ws.col(4).width = 256 * 40
            ws.col(4).width = 256 * 40

            # Sheet header, first row
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = [
                "PK",
                "REF",
                "CONTROL SUPERVISOR",
                "CONTROL OWNER",
                "CONTROL - REF",
                "CONTROL",
            ]

            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()

            for ct in evaluation.control_tests.all().order_by("control__ref"):
                row_num += 1
                ws.write(row_num, 0, ct.pk, font_style)
                ws.write(row_num, 1, ct.identifier, font_style)
                if ct.control_test_supervisor is not None:
                    ws.write(
                        row_num, 2, ct.control_test_supervisor.email, font_style)
                if ct.control_test_owner is not None:
                    ws.write(row_num, 3, ct.control_test_owner.email, font_style)
                ws.write(row_num, 4, ct.control.ref, font_style)
                ws.write(row_num, 5, clean_html(ct.control.name), font_style)

            # Ocultamos la columna de los pk
            ws.col(0).hidden = 1

            wb.save(response)

            return response

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "evaluations:au_evaluation_detail",
            kwargs={"pk": self.evaluation.pk},
        )
