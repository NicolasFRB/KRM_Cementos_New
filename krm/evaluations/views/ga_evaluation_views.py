from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
import xlwt
from xlrd import open_workbook
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
from krm.evaluations.forms.evaluation_forms import EvaluationAssignImportForm, EvaluationDownload, EvaluationInitForm, EvaluationTemplateAssignDownload
from krm.evaluations.models import ControlTest

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations.forms import EvaluationCreateForm, EvaluationUpdateForm
# from krm.evaluations.forms import EvaluationTestTemplateAssignDownload

from krm.evaluations.models import Evaluation
from krm.companies.models import Company
from krm.controls.models import Control

from krm.evaluations.forms import (
    EvaluationInitForm,
    EvaluationTemplateAssignDownload,
    EvaluationDownload,
    EvaluationAssignImportForm
)

from krm.users.decorators import is_global_admin


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaEvaluationListView(ListView):
    model = Evaluation
    template_name = 'evaluations/GaEvaluationList.html'
    context_object_name = 'evaluations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones'), 'url': reverse(
                'evaluations:ga_evaluation_list')},
        ]
        context['page_title'] = _('Evaluaciones')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('evaluations:ga_evaluation_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaEvaluationDetailView(DetailView, FormView):
    model = Evaluation
    template_name = 'evaluations/GaEvaluationDetail.html'
    context_object_name = 'evaluation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones'), 'url': reverse(
                'evaluations:ga_evaluation_list')},
            {'title': self.object.ref}
        ]
        context['page_title'] = f"{_('Evaluación')} : {self.object.ref}"
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('evaluations:ga_evaluation_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']

        return context

    def get_form_class(self):
        evaluation = get_object_or_404(Evaluation, pk=self.kwargs.get("pk"))

        # Si la evaluación está sin iniciar le mandamos el formulario de descarga de excel de asignación
        if evaluation.status == 'SI':
            return EvaluationInitForm

        # if evaluation.status == "FI":
        #     return EvaluationTestDownload
        # else:
        #     if evaluation.is_completed_assing:
        #         return EvaluationTestInitForm
        #     else:
        #         return EvaluationTestTemplateAssignDownload
        return EvaluationAssignImportForm

    def form_valid(self, form):
        from krm.evaluations.models import Evaluation
        from krm.evaluations.forms import EvaluationInitForm, EvaluationTemplateAssignDownload

        if type(form) is EvaluationTemplateAssignDownload:
            # Comienzo de la creacion de archivo de descarga con plantilla de asignación de controles y usuarios
            evaluation = get_object_or_404(
                Evaluation, pk=form.cleaned_data["evaluation"])
            filename = "{} template_asign_process.xls".format(pt.pk)
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
                ws.write(row_num, 5, ct.control.description_safe, font_style)

            # Ocultamos la columna de los pk
            ws.col(0).hidden = 1

            wb.save(response)

            return response

        elif type(form) is EvaluationInitForm:
            evaluation = get_object_or_404(
                Evaluation, pk=form.cleaned_data["evaluation_pk"])
            if self.get_object() == evaluation:
                evaluation.status = "EP"
                evaluation.save()
                users_notificated = []
                for ct in evaluation.control_tests.all():
                    ct.status = "WO"
                    ct.save()
                    if ct.control_test_owner not in users_notificated:
                        users_notificated.append(ct.control_test_owner)
                        ct.send_notification()
                messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    _("Evaluación iniciada correctamente"),
                )

        elif type(form) is EvaluationDownload:
            evaluation = get_object_or_404(
                Evaluation, pk=form.cleaned_data["evaluation_pk"])
            if self.get_object() == evaluation:

                # Comienzo de la creacion de archivo de descarga del Test de Proceso
                filename = "{}_download_process_test.xls".format(evaluation.pk)
                response = HttpResponse(content_type="application/ms-excel")
                response["Content-Disposition"] = 'attachment; filename="{}"'.format(
                    filename
                )

                wb = xlwt.Workbook(encoding="utf-8")
                ws = wb.add_sheet("Controls")

                # Sheet header, first row
                row_num = 0

                font_style_title = xlwt.easyxf(
                    "align: vert centre, horiz left")
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
                    "PROCESO",  # 0
                    "SUBPROCESO",  # 1
                    "RIESGO - DESCRIPCIÓN",  # 2
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
                    "MARCO NORMATIVO\nSCIIF - Sistema de Control Interno de la información financiera\nMPD - Modelo de prevención de delitos\nAML - Prevención de Blanqueo de Capitales\nCFT - Prevención de financiación al terrorismo\nKYC - Conoce a tu cliente\nFI - Política Fiscal Corporativa",
                    # 21
                    "TEST DE CONTROL ID",  # 22
                    "TEST DE CONTROL STATUS",  # 23
                    "CONTROL OWNER",  # 24
                    "CONTROL OWNER EMPRESAS",  # 25
                    "CONTROL OWNER RESPUESTA",  # 26
                    "CONTROL OWNER FECHA RESPUESTA",  # 27
                    "CONTROL OWNER ADJUNTO",  # 28
                    "ADJUNTO LINK",  # 29
                    "RESULTADO\nEF (efectivo)\nNE (no efectivo)",  # 30
                    "PLAN DE REMEDIACIÓN TEXTO",  # 31
                    "PLAN DE REMEDIACIÓN FECHA",  # 32
                    "CONTROL SUPERVISOR",  # 33
                    "CONTROL SUPERVISOR EMPRESAS",  # 34
                    "CONTROL SUPERVISOR RESPUESTA",  # 35
                    "CONTROL SUPERVISOR FECHA RESPUESTA",  # 36
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
                        row_num, 0, ct.process_test.process.name, font_style_body
                    )  # 0
                    ws.write(
                        row_num, 1, ct.control.risk.sub_process.name, font_style_body
                    )  # 1
                    ws.write(
                        row_num,
                        2,
                        ct.control.risk.description.replace("<br>", "\n")
                        .replace("<p>", "")
                        .replace("</p>", "\n"),
                        font_style_body_wrap,
                    )  # 2

                    ws.write(row_num, 3, ct.control.ref, font_style_body)  # 3
                    ws.write(
                        row_num,
                        4,
                        ct.control.objective.replace("<br>", "\n")
                        .replace("<p>", "")
                        .replace("</p>", "\n"),
                        font_style_body_wrap,
                    )  # 4
                    ws.write(
                        row_num,
                        5,
                        ct.control.description.replace("<br>", "\n")
                        .replace("<p>", "")
                        .replace("</p>", "\n"),
                        font_style_body_wrap,
                    )  # 5
                    ws.write(
                        row_num,
                        6,
                        ct.control.action_plan.replace("<br>", "\n")
                        .replace("<p>", "")
                        .replace("</p>", "\n"),
                        font_style_body_wrap,
                    )  # 6
                    ws.write(
                        row_num,
                        7,
                        ct.control.testing_procedure.replace("<br>", "\n")
                        .replace("<p>", "")
                        .replace("</p>", "\n"),
                        font_style_body_wrap,
                    )  # 7

                    rf_text = ""
                    for rf in ct.control.regulatory_frameworks.all():
                        rf_text += "{} - {}".format(rf.acronym, rf.name)
                        rf_text += "\n"

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
                    ws.write(row_num, 21, rf_text, font_style_body)  # 21

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
                        if (
                            co_company.business_group
                            == ct.process_test.company.business_group
                        ):
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
                        if answer.attachment.name:
                            resp_attach = "Si"
                        else:
                            resp_attach = "No"
                        ws.write(row_num, 28, resp_attach,
                                 font_style_body)  # 28

                        if answer.attachment.name:
                            resp_attach = (
                                settings.SITE_URL + "/media/" + answer.attachment.name
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

                    ws.write(
                        row_num, 33, ct.control_test_supervisor.email, font_style_body
                    )  # 33

                    # Buscamos las compañías del control supervisor, solo aqueyas que sean del grupo empresarial al que pertenece
                    # la compañía sobre la que se ha lanzado el test de proceso
                    cs_company_str = ""
                    for cs_company in ct.control_test_supervisor.companies.all():
                        if (
                            cs_company.business_group
                            == ct.process_test.company.business_group
                        ):
                            cs_company_str = "{}{}\n".format(
                                cs_company_str, cs_company.name
                            )
                    ws.write(row_num, 34, cs_company_str,
                             font_style_body_wrap)  # 34

                    # Buscamos la última respuesta del control supervisor
                    if ct.answers.filter(user=ct.control_test_supervisor).count() > 0:
                        answer = (
                            ct.answers.filter(user=ct.control_test_supervisor)
                            .order_by("-created")
                            .first()
                        )
                        ws.write(
                            row_num,
                            35,
                            answer.description.replace("<br>", "\n")
                            .replace("<p>", "")
                            .replace("</p>", "\n"),
                            font_style_body_wrap,
                        )  # 35
                        ws.write(
                            row_num,
                            36,
                            answer.created.strftime("%d/%m/%Y, %H:%M:%S"),
                            font_style_body,
                        )  # 36

                wb.save(response)

                return response

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "evaluations:ga_evaluation_detail",
            kwargs={"pk": self.get_object().pk},
        )


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaEvaluationCreateView(FormView):
    form_class = EvaluationCreateForm
    model = Evaluation
    template_name = 'evaluations/GaEvaluationCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones'), 'url': reverse(
                'evaluations:ga_evaluation_list')},
            {'title': _('Nuevo'), 'url': reverse(
                'evaluations:ga_evaluation_create')},
        ]
        context['page_title'] = _('Nueva Evaluación')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        return reverse_lazy(
            'evaluations:ga_evaluation_list'
        )

    def form_valid(self, form):
        controls_created = 0
        evaluations_created = 0

        companies = Company.objects.filter(
            pk__in=(form.cleaned_data["companies"]))
        controls = Control.objects.filter(
            pk__in=(form.cleaned_data["controls"]))

        for company in companies:
            evaluation = Evaluation.objects.create(
                ref=f'{form.cleaned_data["ref"]} - {company.name}',
                company=company,
                date_begin=form.cleaned_data["date_begin"],
                date_intermediate=form.cleaned_data["date_intermediate"],
                date_end=form.cleaned_data["date_end"],
                certification_year=form.cleaned_data["certification_year"],
                certification_period=form.cleaned_data["certification_period"],
                allow_self_autosupervision=form.cleaned_data[
                    "allow_self_autosupervision"
                ],
            )

            # Para cada evaluación hay que crear los test controls de los controles que se han pasado
            for control in controls:
                control_test = ControlTest.objects.create(
                    evaluation=evaluation,
                    control=control,
                    date_begin=form.cleaned_data["date_begin"]
                )

                controls_created += 1

            evaluations_created += 1

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("%s Evaluaciones creadas correctamente") % str(evaluations_created),
        )

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("%s Test de Control creados correctamente") % str(controls_created),
        )
        return super().form_valid(form)


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaEvaluationUpdateView(UpdateView):
    form_class = EvaluationUpdateForm
    model = Evaluation
    template_name = 'evaluations/GaEvaluationUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones'), 'url': reverse(
                'evaluations:ga_evaluation_list')},
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
            'evaluations:ga_evaluation_detail',
            kwargs={"pk": self.object.pk},
        )


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaEvaluationDeleteView(DeleteView):
    model = Evaluation
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones'), 'url': reverse(
                'evaluations:ga_evaluation_list')},
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
        return reverse_lazy("evaluations:ga_evaluation_list")

    def get_confirm_text_message(self):
        return _(
            '<span class="kt-font-bold">¿Seguro que desea eliminar la Evaluación y los datos asociados?: </span> {0}? <span class="kt-font-bold">Se borrarán todos los riesgos y controles asociados al mismo.</span>'
        ).format(str(self.object.ref))
