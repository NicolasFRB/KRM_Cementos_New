import json
import uuid
import xlwt, os

from django.shortcuts import render
from django.conf import settings

# Create your views here.
from django.shortcuts import render
from django.views.generic import (
    FormView,
    TemplateView,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    View
)
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from krm.evaluations.forms.evaluation_forms import EvaluationAssignImportForm, EvaluationDownload, EvaluationActionForm, EvaluationTemplateAssignDownload
from krm.evaluations.models import ControlTest

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations.forms import EvaluationCreateForm, EvaluationUpdateForm
# from krm.evaluations.forms import EvaluationTestTemplateAssignDownload

from krm.evaluations.models import Evaluation
from krm.companies.models import Company
from krm.controls.models import Control

from krm.evaluations.forms import (
    EvaluationActionForm,
    EvaluationTemplateAssignDownload,
    EvaluationDownload,
    EvaluationAssignImportForm,
    EvaluationNotificationForm
)

from krm.users.models import User

from krm.users.decorators import (
    is_company_admin,
    user_can_view_evaluation
)

from krm.utils.utils import clean_html, pluralize

from krm.evaluations.forms import EvaluationFilterForm


@method_decorator([login_required, is_company_admin], name='dispatch')
class CaEvaluationListView(ListView):
    model = Evaluation
    template_name = 'evaluations/CaEvaluationList.html'
    context_object_name = 'evaluations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones'), 'url': reverse(
                'evaluations:ca_evaluation_list')},
        ]
        context['page_title'] = _('Evaluaciones')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('evaluations:ca_evaluation_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]

        json_path_es = os.path.join('krm', 'static', 'lang', 'es.json')
        json_path_en = os.path.join('krm', 'static', 'lang', 'en.json')

        try:
            with open(json_path_es, 'r', encoding= 'utf-8') as file:
                translations_data= json.load(file)
                translations_es= json.dumps(translations_data)
        except FileNotFoundError:
            print("No se ha encontrado ese archivo")
            translations_es= {}

        try:
            with open(json_path_en, 'r', encoding= 'utf-8') as file:
                translations_data= json.load(file)
                translations_en= json.dumps(translations_data)
        except FileNotFoundError:
            translations_en= {}

        context['translations_es']= translations_es
        context['translations_en']= translations_en

        ev_pending = Evaluation.objects.filter(status__in=["SI", "EP"], company__in=self.request.user.companies_admin.all())
        ev_finished = Evaluation.objects.filter(status="FI", company__in=self.request.user.companies_admin.all())

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

        context['evaluation_filter_form'] = EvaluationFilterForm()

        posible_values_certification_period = [
            (evaluation.certification_period_with_year,
             evaluation.certification_period_with_year)
            for evaluation in Evaluation.objects.filter(company__in=self.request.user.companies_admin.all()).order_by("certification_year")
        ]

        # Quitar duplicados
        posible_values_certification_period = list(set(posible_values_certification_period))

        context['evaluation_filter_form'].fields['certification_period'].choices = posible_values_certification_period

        domain_risks = []
        for evaluation in Evaluation.objects.filter(company__in=self.request.user.companies_admin.all()):
            for dr in evaluation.get_domain_risk_in_evaluation():
                if dr not in domain_risks:
                    domain_risks.append(dr)
        domain_risk = [[dr.ref, dr.ref] for dr in domain_risks]
        context['evaluation_filter_form'].fields['domain_risk'].choices = domain_risk

        context['js_template'] = ['js/custom/datatables.js']
        return context

    def get_queryset(self):
        return Evaluation.objects.filter(company__in=self.request.user.companies_admin.all())

@method_decorator([login_required, is_company_admin, ], name='dispatch')
class CaEvaluationDetailView(FormView):
    template_name = 'evaluations/CaEvaluationDetail.html'
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
                'evaluations:ca_evaluation_list')},
            {'title': self.evaluation.ref}
        ]
        context['page_title'] = f"{_('Evaluación')} : {self.evaluation.ref}"
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('evaluations:ca_evaluation_update', kwargs={'pk': self.evaluation.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]

        json_path_es = os.path.join('krm', 'static', 'lang', 'es.json')
        json_path_en = os.path.join('krm', 'static', 'lang', 'en.json')

        try:
            with open(json_path_es, 'r', encoding= 'utf-8') as file:
                translations_data= json.load(file)
                translations_es= json.dumps(translations_data)
        except FileNotFoundError:
            print("No se ha encontrado ese archivo")
            translations_es= {}

        try:
            with open(json_path_en, 'r', encoding= 'utf-8') as file:
                translations_data= json.load(file)
                translations_en= json.dumps(translations_data)
        except FileNotFoundError:
            translations_en= {}

        context['translations_es']= translations_es
        context['translations_en']= translations_en

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
        context['evaluation'].ncontrols_test_by_result_efr= context['evaluation'].ncontrols_test_by_result(
            "EFR")
        context['evaluation'].ncontrols_test_by_result_ne = context['evaluation'].ncontrols_test_by_result(
            "NE")
        context['evaluation'].ncontrols_test_by_result_na = context['evaluation'].ncontrols_test_by_result(
            "NA")

        context['evaluation'].domain_risks = context['evaluation'].get_domain_risk_in_evaluation()

        context['js_template'] = ['js/custom/datatables.js']

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
                "RESULTADO\nEF (efectivo)\nNE (no efectivo)\nNA (no aplica)",  # 30
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

                if ct.rp_control_test.count() > 0:
                    remediation_plan = ct.rp_control_test.order_by(
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

                    # if remediation_plan.attachment:
                    #     resp_attach = settings.SITE_URL + "/media/" + remediation_plan.attachment.name
                    #     ws.write(
                    #         row_num,
                    #         33,
                    #         xlwt.Formula(
                    #             'HYPERLINK("%s";"Enlace al documento")'
                    #             % resp_attach
                    #         ),
                    #         font_style_body,
                    #     )  # 33

                # if ct.remediation_plans.count() > 0:
                #     remediation_plan = ct.remediation_plans.order_by(
                #         "created"
                #     ).first()
                #     ws.write(
                #         row_num, 31, remediation_plan.description, font_style_body
                #     )  # 31
                #     ws.write(
                #         row_num,
                #         32,
                #         remediation_plan.date_end.strftime(
                #             "%d/%m/%Y, %H:%M:%S"),
                #         font_style_body,
                #     )  # 32

                #     if remediation_plan.attachment:
                #         resp_attach = settings.SITE_URL + "/media/" + remediation_plan.attachment.name
                #         ws.write(
                #             row_num,
                #             33,
                #             xlwt.Formula(
                #                 'HYPERLINK("%s";"Enlace al documento")'
                #                 % resp_attach
                #             ),
                #             font_style_body,
                #         )  # 33

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
            "evaluations:ca_evaluation_detail",
            kwargs={"pk": self.evaluation.pk},
        )


@method_decorator([login_required, is_company_admin, ], name='dispatch')
class CaEvaluationCreateView(FormView):
    form_class = EvaluationCreateForm
    model = Evaluation
    template_name = 'evaluations/CaEvaluationCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones'), 'url': reverse(
                'evaluations:ca_evaluation_list')},
            {'title': _('Nuevo'), 'url': reverse(
                'evaluations:ca_evaluation_create')},
        ]
        context['page_title'] = _('Nueva Evaluación')
        context['breadcrums'] = breadcrums
        context['js_template'] = ['js/custom/datatables.js']
        return context

    def get_success_url(self):

        return reverse_lazy(
            'evaluations:ca_evaluation_list'
        )

    def form_valid(self, form):
        controls_created = 0
        evaluations_created = 0

        controls_companies = json.loads(
            form.cleaned_data["controls_companies_to_evaluate"])

        for cc in controls_companies:
            if len(cc['cs']) > 0:

                company = Company.objects.get(pk=cc['c'])
                if Evaluation.objects.filter(
                    ref=f'{form.cleaned_data["ref"]} - {company.name}'
                ).count() > 0:
                    ref = f'{form.cleaned_data["ref"]} - {company.name} - {uuid.uuid4().hex}'
                else:
                    ref = f'{form.cleaned_data["ref"]} - {company.name}'

                evaluation = Evaluation.objects.create(
                    ref=ref,
                    company=company,
                    description=form.cleaned_data["description"],
                    date_begin=form.cleaned_data["date_begin"],
                    date_intermediate=form.cleaned_data["date_intermediate"],
                    date_end=form.cleaned_data["date_end"],
                    certification_year=form.cleaned_data["certification_year"],
                    certification_period=form.cleaned_data["certification_period"],
                    allow_self_autosupervision=form.cleaned_data[
                        "allow_self_autosupervision"
                    ],
                    notification_text=form.cleaned_data["notification_text"]
                )

                # Ahora en este array nos llegará también el control owner y el control supervisor

                # [
                #     {
                #         "pk": 976,
                #         "ownersSelected": [
                #             {
                #                 "pk": 98,
                #                 "email": "39@39.com",
                #                 "full_name": "Mario Ar"
                #             },
                #             {
                #                 "pk": 106,
                #                 "email": "bienvenidosaez@baetica.com",
                #                 "full_name": "Bienvenido Sáez Muelas"
                #             },
                #             {
                #                 "pk": 107,
                #                 "email": "ru@baetica.com",
                #                 "full_name": "ru@baetica.com "
                #             }
                #         ],
                #         "supervisorsSelected": [
                #             {
                #                 "pk": 105,
                #                 "email": "mrevuelta.deca@gmail.com",
                #                 "full_name": "asd asd"
                #             }
                #         ]
                #     }
                # ]

                for control in cc['csData']:
                    control_owner = None
                    control_supervisor = None

                    control_object = Control.objects.get(pk=control['pk'])

                    # Si el número de supervisores es menor que el número de owners, me quedo con el primer supervisor e itero por los owners
                    # if len(control['supervisorsSelected']) < len(control['ownersSelected']) or len(control['supervisorsSelected']) > len(control['ownersSelected']):
                    if len(control['supervisorsSelected']) < len(control['ownersSelected']) or (len(control['supervisorsSelected']) > len(control['ownersSelected']) and len(control['ownersSelected']) > 0):
                        control_supervisor = None
                        if len(control['supervisorsSelected']) > 0:
                            control_supervisor = control['supervisorsSelected'][0]['pk']
                        for owner in control['ownersSelected']:
                            control_owner = owner['pk']
                            control_test = ControlTest.objects.create(
                                evaluation=evaluation,
                                control=control_object,
                                date_begin=form.cleaned_data["date_begin"],
                                control_test_owner=User.objects.get(
                                    pk=control_owner) if control_owner != None else None,
                                control_test_supervisor=User.objects.get(
                                    pk=control_supervisor) if control_supervisor != None else None
                            )
                            controls_created += 1

                    # Si el número de supervisores es igual que el número de owners, itero por los owners y supervisores
                    elif len(control['supervisorsSelected']) > 0 and len(control['supervisorsSelected']) == len(control['ownersSelected']):
                        for i, owner in enumerate(control['ownersSelected']):
                            control_owner = owner['pk']
                            control_supervisor = control['supervisorsSelected'][i]['pk']
                            control_test = ControlTest.objects.create(
                                evaluation=evaluation,
                                control=control_object,
                                date_begin=form.cleaned_data["date_begin"],
                                control_test_owner=User.objects.get(
                                    pk=control_owner),
                                control_test_supervisor=User.objects.get(
                                    pk=control_supervisor)
                            )
                            controls_created += 1

                    # Si el número de supervisores es 0 y el número de owners es 0
                    elif len(control['supervisorsSelected']) == 0 and len(control['ownersSelected']) == 0:
                        control_test = ControlTest.objects.create(
                            evaluation=evaluation,
                            control=control_object,
                            date_begin=form.cleaned_data["date_begin"],
                            control_test_owner=None,
                            control_test_supervisor=None
                        )
                        controls_created += 1

                    # Si el número de supervisores es 0 y el número de owners es mayor que 0
                    elif len(control['supervisorsSelected']) == 0 and len(control['ownersSelected']) > 0:
                        for i, owner in enumerate(control['ownersSelected']):
                            control_owner = owner['pk']
                            control_test = ControlTest.objects.create(
                                evaluation=evaluation,
                                control=control_object,
                                date_begin=form.cleaned_data["date_begin"],
                                control_test_owner=User.objects.get(
                                    pk=control_owner),
                                control_test_supervisor=None
                            )
                            controls_created += 1

                    # Si el número de owners es 1 y supervisors es mayor que owners
                    elif len(control['supervisorsSelected']) > len(control['ownersSelected']) and len(control['ownersSelected']) == 1:
                        # Itero por los supervisores y creo un test de control para cada uno con el mismo owner
                        for i, supervisor in enumerate(control['supervisorsSelected']):
                            control_supervisor = supervisor['pk']
                            control_test = ControlTest.objects.create(
                                evaluation=evaluation,
                                control=control_object,
                                date_begin=form.cleaned_data["date_begin"],
                                control_test_owner=User.objects.get(
                                    pk=control['ownersSelected'][0]['pk']),
                                control_test_supervisor=User.objects.get(
                                    pk=control_supervisor)
                            )
                            controls_created += 1

                    # Si el número de supervisores es mayor que 0 y el número de owners es 0
                    elif len(control['supervisorsSelected']) > 0 and len(control['ownersSelected']) == 0:
                        for i, supervisor in enumerate(control['supervisorsSelected']):
                            control_supervisor = supervisor['pk']
                            control_test = ControlTest.objects.create(
                                evaluation=evaluation,
                                control=control_object,
                                date_begin=form.cleaned_data["date_begin"],
                                control_test_owner=None,
                                control_test_supervisor=User.objects.get(
                                    pk=control_supervisor),
                            )
                            controls_created += 1

                    else:
                        pass

                evaluations_created += 1

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _(
                'Se han creado %s y %s de control correctamente'
                ) % (
                    pluralize(evaluations_created, _('evaluación'), _('evaluaciones')), pluralize(controls_created, 'test')
                )
        )

        return super().form_valid(form)


@method_decorator([login_required, is_company_admin, ], name='dispatch')
class CaEvaluationUpdateView(UpdateView):
    form_class = EvaluationUpdateForm
    model = Evaluation
    template_name = 'evaluations/CaEvaluationUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones'), 'url': reverse(
                'evaluations:ca_evaluation_list')},
            {'title': _('Editar')},
        ]
        context['page_title'] = _('Editar Evaluación')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Evaluación actualizada correctamente')
        )
        return reverse_lazy(
            'evaluations:ca_evaluation_detail',
            kwargs={"pk": self.object.pk},
        )


@method_decorator([login_required, is_company_admin, ], name='dispatch')
class CaEvaluationDeleteView(DeleteView):
    model = Evaluation
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones'), 'url': reverse(
                'evaluations:ca_evaluation_list')},
            {'title': _('Eliminar')},
        ]
        context['page_title'] = _(
            "Eliminar Evaluación: #%s") % str(self.object.ref)
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Evaluación eliminada correctamente")
        )
        return reverse_lazy("evaluations:ca_evaluation_list")

    def get_confirm_text_message(self):
        return _(
            '<span class="kt-font-bold">¿Seguro que desea eliminar la Evaluación y los datos asociados?: </span> {0}? <span class="kt-font-bold">Se borrarán todos los riesgos y controles asociados al mismo.</span>'
        ).format(str(self.object.ref))


@method_decorator((login_required, user_can_view_evaluation), name="dispatch")
class CaEvaluationAssignImport(FormView):
    template_name = "evaluations/GaEvaluationImportAssign.html"
    form_class = EvaluationAssignImportForm

    def dispatch(self, request, *args, **kwargs):
        self.evaluation = get_object_or_404(
            Evaluation, pk=self.kwargs.get("pk"))
        return super(CaEvaluationAssignImport, self).dispatch(
            request, request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['evaluation'] = self.evaluation
        context['page_title'] = f"{_('Asignar controles para la evaluación')} : {self.evaluation.ref}"
        return context

    def form_valid(self, form):
        input_excel = self.request.FILES["evaluation_assign_file"]
        book = open_workbook(file_contents=input_excel.read())

        control_test_sheet = book.sheet_by_index(0)
        control_tests = []
        # Primero tenemos que controlar que todos los controles existen y pertenecen al Test de Proceso
        for row in range(control_test_sheet.nrows):
            if row > 0:
                control_test_pk = int(control_test_sheet.cell(row, 0).value)
                control_test_supervisor_email = str(
                    control_test_sheet.cell(row, 2).value
                )
                control_test_owner_email = str(
                    control_test_sheet.cell(row, 3).value)
                # Comprobamos que el test de control existe y que pertenece al test de proceso
                control_test = get_object_or_404(
                    ControlTest, pk=control_test_pk)
                if control_test.evaluation != self.evaluation:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                "En la fila %s hay un control que no pertenece a dicho Test de Control. Se ha abortado la importación"
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(CaEvaluationAssignImport, self).form_invalid(form)
                    break
                # Cromprobamos que el control owner existe y que pertenecen a la compañía del Test de Proceso
                if control_test_owner_email != "":
                    try:
                        control_test_owner = User.objects.get(
                            email=control_test_owner_email
                        )
                    except Exception as e:
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _("En la fila %s el control owner no existe")
                                % str(row + 1)
                            ),
                        )
                        return super(CaEvaluationAssignImport, self).form_invalid(form)
                    control_tests.append(control_test)
                    if not control_test_owner.companies.filter(
                        pk=self.evaluation.company.pk
                    ):
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _(
                                    "En la fila %s el control owner no pertenece a la compañía sobre la que está realizado la evaluación"
                                )
                                % str(row + 1)
                            ),
                        )
                        return super(CaEvaluationAssignImport, self).form_invalid(form)
                    control_test.control_test_owner = control_test_owner
                else:
                    control_test.control_test_owner = None

                if control_test_supervisor_email != "":
                    #  Comprobamos que el control supervisor existe y que pertenecen a la compañía del Test de Proceso
                    try:
                        control_test_supervisor = User.objects.get(
                            email=control_test_supervisor_email
                        )
                    except Exception as e:
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _("En la fila %s el control owner no existe")
                                % str(row + 1)
                            ),
                        )
                        return super(CaEvaluationAssignImport, self).form_invalid(form)
                    control_tests.append(control_test)
                    if not control_test_supervisor.companies.filter(
                        pk=self.evaluation.company.pk
                    ):
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _(
                                    "En la fila %s el control owner no pertenece a la compañía sobre la que está realizado la evaluación"
                                )
                                % str(row + 1)
                            ),
                        )
                        return super(CaEvaluationAssignImport, self).form_invalid(form)
                    control_test.control_test_supervisor = control_test_supervisor
                else:
                    control_test.control_test_supervisor = None

                if (
                    control_test.control_test_owner is not None
                    and control_test.control_test_owner
                    == control_test.control_test_supervisor
                    and control_test.evaluation.allow_self_autosupervision is False
                ):
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                "En la fila %s el control owner y el control supervisor son el mismo usuario. La evaluación no permite la autosupervisión"
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(CaEvaluationAssignImport, self).form_invalid(form)

                control_tests.append(control_test)

        for control_test in control_tests:
            control_test.save()

        messages.add_message(
            self.request, messages.SUCCESS, (_(
                "Controles asignados correctamente"))
        )

        return super(CaEvaluationAssignImport, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "evaluations:ca_evaluation_detail", kwargs={"pk": self.evaluation.pk}
        )

@method_decorator([is_company_admin, ], name='dispatch')
class CaEvaluationNotificationView(DetailView, FormView):
    template_name = 'evaluations/CaEvaluationNotifications.html'
    model = Evaluation
    context_object_name = 'evaluation'
    form_class = EvaluationNotificationForm

    def dispatch(self, request, *args, **kwargs):
        self.evaluation = get_object_or_404(
            Evaluation, pk=self.kwargs.get("pk"))
        return super(CaEvaluationNotificationView, self).dispatch(
            request, request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones KRC'), 'url': reverse(
                'evaluations:ca_evaluation_list')},
            {'title': self.object.ref, 'url': reverse(
                "evaluations:ca_evaluation_detail", kwargs={'pk': self.object.pk})}
        ]
        context['page_title'] = f"{_('Notificaciones de Controles')} : {self.object.ref}"
        context['breadcrums'] = breadcrums

        context['evaluation'].evaluators_notifications_co = context['evaluation'].get_evaluators_for_notifications_by_role(
            "WO")
        context['evaluation'].evaluators_notifications_cs = context['evaluation'].get_evaluators_for_notifications_by_role(
            "WS")

        context['js_template'] = ['js/custom/datatables.js']

        return context

    def post(self, request, *args, **kwargs):
        ct_selected_co = request.POST.getlist('notify_pk_co')
        ct_selected_cs = request.POST.getlist('notify_pk_cs')
        notification_text = request.POST.get('notification_text')

        self.evaluation.notification_text = notification_text
        self.evaluation.save()

        from krm.evaluations.models import ControlTest

        if ct_selected_co:
            for pk in ct_selected_co:
                ct = ControlTest.objects.filter(pk=int(pk)).first()
                ct.send_notification('Reminder')

            messages.add_message(
                self.request, messages.SUCCESS, _(
                    "Enviadas notificaciones a %d usuarios!" % len(ct_selected_co))
            )

        if ct_selected_cs:
            for pk in ct_selected_cs:
                ct = ControlTest.objects.filter(pk=int(pk)).first()
                ct.send_notification('Reminder')

            messages.add_message(
                self.request, messages.SUCCESS, _(
                    "Enviadas notificaciones a %d usuarios!" % len(ct_selected_cs))
            )

        return HttpResponseRedirect(
            reverse_lazy(
                "evaluations:ca_evaluation_detail",
                kwargs={'pk': self.evaluation.pk}
            )
        )
