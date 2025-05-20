from django.shortcuts import render
from django.conf import settings
import json
import uuid
import xlsxwriter
import re, os

# Create your views here.
from django.shortcuts import render

from django.views.generic import (
    FormView,
    DetailView,
    ListView
)
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _

from django.shortcuts import get_object_or_404

from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations_krm.models import (
    EvaluationKrmResidual,
    RiskTestResidual,
    RiskCompanyResidual
)

from krm.companies.models import (
    CompanyDomainRiskEvaluator,
    Company
)

from krm.risks.models import RiskCompany
from krm.users.models import User

from krm.evaluations_krm.forms import (
    EvaluationResidualCreateForm,
    EvaluationResidualCompleteForm,
    EvaluationResidualNotificationForm,
)

from krm.evaluations.forms import (
    EvaluationActionForm
)


from krm.users.decorators import is_global_admin, user_can_view_evaluation

from krm.utils.utils import clean_html, pluralize


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaEvaluationResidualListView(ListView):
    model = EvaluationKrmResidual
    template_name = 'evaluations_krm/GaEvaluationResidualList.html'
    context_object_name = 'evaluations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Residual'), 'url': reverse(
                'evaluations_krm:ga_evaluation_inherent_list')},
        ]
        context['page_title'] = _('Evaluaciones de Riesgo Residual')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('evaluations_krm:ga_evaluation_residual_create'),
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

        ev_pending = EvaluationKrmResidual.objects.filter(status="EP")
        ev_finished = EvaluationKrmResidual.objects.filter(status="FI")

        for ev in ev_pending:
            ev.nrisk_test_residuals_pending = ev.nrisk_test_residuals_by_state(
                1)
            ev.nrisk_test_residuals_delivered = ev.nrisk_test_residuals_by_state(
                2)
            ev.nrisk_test_residuals_finished = ev.nrisk_test_residuals_by_state(
                3)

            ev.evaluators_pending = ev.get_evaluators_by_rrt_state(1)
            ev.evaluators_delivered = ev.get_evaluators_by_rrt_state(2)
            ev.evaluators_finished = ev.get_evaluators_by_rrt_state(3)

            ev.total_evaluators = ev.evaluators_pending.count(
            ) + ev.evaluators_delivered.count() + ev.evaluators_finished.count()

            ev.domain_risks = ev.get_domain_risk_in_evaluation()

        for ev in ev_finished:
            ev.nrisk_test_residuals_pending = ev.nrisk_test_residuals_by_state(
                1)
            ev.nrisk_test_residuals_delivered = ev.nrisk_test_residuals_by_state(
                2)
            ev.nrisk_test_residuals_finished = ev.nrisk_test_residuals_by_state(
                3)

            ev.evaluators_pending = ev.get_evaluators_by_rrt_state(1)
            ev.evaluators_delivered = ev.get_evaluators_by_rrt_state(2)
            ev.evaluators_finished = ev.get_evaluators_by_rrt_state(3)

            ev.total_evaluators = ev.evaluators_pending.count(
            ) + ev.evaluators_delivered.count() + ev.evaluators_finished.count()

            ev.domain_risks = ev.get_domain_risk_in_evaluation()

        context['evaluations_pending'] = ev_pending
        context['evaluations_finished'] = ev_finished

        context['js_template'] = ['js/custom/datatables.js']

        return context


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaEvaluationResidualCreateView(FormView):
    form_class = EvaluationResidualCreateForm
    model = EvaluationKrmResidual
    template_name = 'evaluations_krm/GaEvaluationResidualCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Residual'), 'url': reverse(
                'evaluations:ga_evaluation_list')},
            {'title': _('Nuevo'), 'url': reverse(
                'evaluations_krm:ga_evaluation_residual_create')},
        ]
        context['page_title'] = _('Nueva Evaluación de Riesgo Residual')
        context['breadcrums'] = breadcrums
        context['js_template'] = ['js/custom/datatables.js']

        return context

    def get_success_url(self):

        return reverse_lazy(
            'evaluations_krm:ga_evaluation_residual_list'
        )

    def form_valid(self, form):
        risk_tests__created = 0
        evaluations_created = 0
        evaluations = []

        risk_companies = json.loads(form.cleaned_data["risk_companies"])
        for rc in risk_companies:
            company = Company.objects.get(pk=rc['company_pk'])

            riskcompany_pks = []

            for rc in rc['risks']:
                riskcompany_pks.append(rc[0])
                risk_company = RiskCompany.objects.get(pk=(rc[0]))
                risk_company.evaluator = User.objects.get(
                    pk=rc[1]
                )
                risk_company.save()

            risks = RiskCompany.objects.filter(pk__in=(riskcompany_pks))

            if EvaluationKrmResidual.objects.filter(
                ref=f'{form.cleaned_data["ref"]} - {company.name}',
            ).count() > 0:
                ref = f'{form.cleaned_data["ref"]} - {company.name} - {uuid.uuid4().hex}'
            else:
                ref = f'{form.cleaned_data["ref"]} - {company.name}'

            evaluation = EvaluationKrmResidual.objects.create(
                ref=ref,
                company=company,
                description=form.cleaned_data["description"],
                date_begin=form.cleaned_data["date_begin"],
                date_end=form.cleaned_data["date_end"],
                certification_year=form.cleaned_data["certification_year"],
                certification_period=form.cleaned_data["certification_period"]
            )

            evaluations.append(evaluation)

            # Para cada evaluación hay que crear los test controls de los controles que se han pasado
            for risk in risks:

                RiskTestResidual.objects.create(
                    evaluation=evaluation,
                    risk=risk,
                    evaluator=risk.evaluator
                )

                risk_tests__created += 1

            evaluations_created += 1

            # En este caso se puede iniciar ya la evaluación
            users_notificated = []
            for e in evaluations:
                for rt in e.risk_test_residuals.all():
                    rt.status = 1
                    rt.save()
                    if rt.evaluator not in users_notificated:
                        rt.send_notification_evaluator('Initial Notification')
                        users_notificated.append(rt.evaluator)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _(
                'Se han creado %s y %s de riesgo residual correctamente'
                ) % (
                    pluralize(evaluations_created, _('evaluación'), _('evaluaciones')), pluralize(risk_tests__created, 'test')
                )
        )

        return super().form_valid(form)


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaEvaluationResidualDetailView(FormView):
    template_name = 'evaluations_krm/GaEvaluationResidualDetail.html'
    form_class = EvaluationActionForm

    def dispatch(self, request, *args, **kwargs):
        evaluation_krm = get_object_or_404(
            EvaluationKrmResidual, pk=self.kwargs.get("pk"))
        self.evaluation = evaluation_krm
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Función empleada para mandar datos del Backend a la template de HTML y poder visualizar así
        los datos por pantalla, a través de los gráficos del detalle de una Evaluación de Riesgo. Puesto que
        queremos enviar los datos particulares de cada test de riesgo para realizar el gráfico de barras, crearemos
        un orden en el listado de tests de riesgo para representar aquellos con menor severidad los primeros, y
        que la severidad, equivalente a la altura vaya aumentando conforme avanzamos hacia la derecha del gráfico.

        """
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['evaluation'] = self.evaluation
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Residual'), 'url': reverse(
                'evaluations_krm:ga_evaluation_residual_list')},
            {'title': self.evaluation.ref}
        ]
        title= _('Evaluación de Riesgo Residual')
        context['page_title'] = f"{title} : {self.evaluation.ref}"
        context['breadcrums'] = breadcrums

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

        context['evaluation'].nrisk_test_residuals_pending = context['evaluation'].nrisk_test_residuals_by_state(1)
        context['evaluation'].nrisk_test_residuals_delivered = context['evaluation'].nrisk_test_residuals_by_state(2)
        context['evaluation'].nrisk_test_residuals_finished = context['evaluation'].nrisk_test_residuals_by_state(3)
        context['evaluation'].evaluators_pending = context['evaluation'].get_evaluators_by_rrt_state(1)
        context['evaluation'].evaluators_delivered = context['evaluation'].get_evaluators_by_rrt_state(2)
        context['evaluation'].evaluators_finished = context['evaluation'].get_evaluators_by_rrt_state(3)
        context['evaluation'].sev_not_established = context['evaluation'].nrisk_test_residuals_by_severity('SE')
        context['evaluation'].sev_very_low = context['evaluation'].nrisk_test_residuals_by_severity('MB')
        context['evaluation'].sev_low = context['evaluation'].nrisk_test_residuals_by_severity('B')
        context['evaluation'].sev_medium = context['evaluation'].nrisk_test_residuals_by_severity('M')
        context['evaluation'].sev_high = context['evaluation'].nrisk_test_residuals_by_severity('A')
        context['evaluation'].sev_very_high = context['evaluation'].nrisk_test_residuals_by_severity('MA')

        context['evaluation'].total_evaluators = context['evaluation'].evaluators_pending.count(
        ) + context['evaluation'].evaluators_delivered.count() + context['evaluation'].evaluators_finished.count()

        context['evaluation'].domain_risks = context['evaluation'].get_domain_risk_in_evaluation()

        context['rrt'] = RiskTestResidual.objects.filter(
            evaluation=self.evaluation)

        context['rrt_dict'] = []

        for risk_test in context['rrt']:
            information= {}
            information['ref']= risk_test.risk.risk.ref
            information['name']= risk_test.risk.risk.name
            information['evaluator']= risk_test.evaluator.username_no_domain
            information['impact_evaluator']= risk_test.impact_level_evaluator
            information['probability_evaluator']= risk_test.probability_level_evaluator
            information['severity_evaluator']= risk_test.severity_level_evaluator
            information['administrator']= self.evaluation.admin_supervisor.username_no_domain if self.evaluation.admin_supervisor else ''
            information['impact_administrator']= risk_test.impact_level_administrator
            information['probability_administrator']= risk_test.probability_level_administrator
            information['severity_administrator']= risk_test.severity_level_administrator
            context['rrt_dict'].append(information)

        if self.evaluation.admin_supervisor:
            context['rrt_dict'] = sorted(context['rrt_dict'], key=lambda x: x['severity_administrator'], reverse=False)
        else:
            context['rrt_dict'] = sorted(context['rrt_dict'], key=lambda x: x['severity_evaluator'], reverse=False)

        # Errores de encoding caracteres portugueses y españoles
        # for i, m in enumerate(context['rrt_dict']):
        #     for k in m:
        #         if type(context['rrt_dict'][i][k]) == str:
        #             context['rrt_dict'][i][k] = context['rrt_dict'][i][k].encode(
        #                 'utf-8').decode('utf-8')

        context['rrt_json'] = json.dumps(context['rrt_dict'], default=str, ensure_ascii=True)

        # Código antiguo correspondiente a los riesgos de compañía residuales
        # context['rcr'] = RiskCompanyResidual.objects.filter(
        #     evaluation=self.evaluation)
        # context['rcr_dict'] = [model_to_dict(m) for m in context['rcr']]
        # for i, r1 in enumerate(context['rcr']):
        #     context['rcr_dict'][i]['risk_ref'] = r1.risk_company.risk.ref
        #     context['rcr_dict'][i]['risk_name'] = r1.risk_company.risk.name

        #     context['rcr_dict'][i]['impact_inherent'] = r1.get_latest_impact_inherent
        #     context['rcr_dict'][i]['probability_inherent'] = r1.get_latest_probability_inherent
        #     context['rcr_dict'][i]['severity_inherent'] = r1.get_latest_severity_inherent
        #     context['rcr_dict'][i]['probability_residual_eval'] = r1.probability_level_result_evaluator
        #     context['rcr_dict'][i]['probability_residual_admin'] = r1.probability_level_result_admin
        #     context['rcr_dict'][i]['nivel_de_control'] = r1.probability_level_residual_evaluator_aggregate_rounded

        # context['rcr_dict'] = context['rcr_dict']
        # sorted(
        #     context['rcr_dict'], key=lambda x: (x['severity_inherent'] + x['probability_residual_eval']), reverse=True)

        # for i, m in enumerate(context['rcr_dict']):
        #     for k in m:
        #         if type(context['rcr_dict'][i][k]) == str:
        #             context['rcr_dict'][i][k] = context['rcr_dict'][i][k].encode(
        #                 'utf-8').decode('utf-8')

        # context['rcr_json'] = json.dumps(
        #     context['rcr_dict'],
        #     default=str,
        #     ensure_ascii=True,
        # )

        context['js_template'] = ['js/custom/datatables.js']

        return context

    def form_valid(self, form):
        action = form.cleaned_data["action"]
        evaluation = self.evaluation

        if action == 'download':
            import io
            from django.utils.html import strip_tags

            filename = f'residual_evaluation_{evaluation.ref}.xlsx'

            # Create an in-memory output file for the new workbook.
            output = io.BytesIO()

            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet('Evaluation')
            worksheet_2= workbook.add_worksheet('Residual risk tests')

            #Añadimos formatos de escritura
            bold = workbook.add_format({'bold': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
            italic= workbook.add_format({'italic': True})
            text_wrap = workbook.add_format({'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
            colors_format= [workbook.add_format({'color': '#d9d3d2'}), workbook.add_format({'color': '#09ef0d'}), workbook.add_format({'color': '#e8ee0b'}), workbook.add_format({'color': '#fea227'}), workbook.add_format({'color': '#ff6e56'}), workbook.add_format({'color': '#f10606'})]

            evaluation_columns = [
                'Evaluation ID',
                'Company (ID)',
                'Company type',
                'Evaluation description',
                'Start date',
                'End date',
                'Certification year',
                'Certification period',
                'Evaluation status',
                'Company administrator'
            ]

            tests_columns=[
                "Associated risk",
                "Associated master risk",
                "Associated risk domain",
                "Risk's description",
                "Risk's main elements",
                "Risk's main events",
                "Risk's affected activity",
                "Risk's exposed staff",
                "Latest inherent impact assessment",
                "Latest inherent probability assessment",
                "Latest inherent severity assessment",
                "Latest inherent speed of ocurrence assessment",
                "Latest inherent assessment justification",
                "Company risk evaluator",
                "Evaluator's impact assessment",
                "Evaluator's impact qualitative assessment",
                "Evaluator's probability assessment",
                "Evaluator's probability qualitative assessment",
                "Evaluator's severity assesment",
                "Evaluator's severity qualitative assesment",
                "Evaluator's speed of ocurrence assessment",
                "Evaluator's speed of ocurrence qualitative assessment",
                "Evaluator's  justification",
                "Administrator's impact assessment",
                "Administrator's impact qualitative assessment",
                "Administrator's probability assessment",
                "Administrator's probability qualitative assessment",
                "Administrator's severity assesment",
                "Administrator's severity qualitative assesment",
                "Administrator's speed of ocurrence assessment",
                "Administrator's speed of ocurrence qualitative assessment",
                "Administrator's  justification"
            ]

            for index, col_name in enumerate(evaluation_columns):
                worksheet.write(0, index, col_name, bold)

            for index, col_name in enumerate(tests_columns):
                worksheet_2.write(0, index, col_name, bold)

            #Evaluation's sheet column formats (NMB)
            worksheet.set_column('A:B', 25, text_wrap)  #Evaluation ID, Company (ID) column's format
            worksheet.set_column('C:C', 40, text_wrap) #Company type column format
            worksheet.set_column('D:D', 80, text_wrap)
            worksheet.set_column('E:J', 40, text_wrap)

            #Test's sheet column formats (NMB)
            worksheet_2.set_column('A:C', 25, text_wrap)
            worksheet_2.set_column('D:H', 60, text_wrap)
            worksheet_2.set_column('I:L', 20, text_wrap)
            worksheet_2.set_column('M:M', 50, text_wrap)
            worksheet_2.set_column('N:N', 30, text_wrap)
            worksheet_2.set_column('O:V', 20, text_wrap)
            worksheet_2.set_column('W:W', 50, text_wrap)
            worksheet_2.set_column('X:AE', 20, text_wrap)
            worksheet_2.set_column('AF:AF', 50, text_wrap)


            #Writing on the fisrt sheet:
            worksheet.write(1, 0, evaluation.ref, text_wrap)
            worksheet.write(1, 1, evaluation.company.name +' (' + evaluation.company.ref+')' , text_wrap)
            worksheet.write(1, 2, evaluation.company.type_company if evaluation.company.type_company else "Not specified", text_wrap)
            worksheet.write(1, 3, strip_tags(evaluation.description) if evaluation.description else "Not specified", text_wrap)
            worksheet.write(1, 4, evaluation.date_begin.strftime("%d/%m/%Y"), text_wrap)
            worksheet.write(1, 5, evaluation.date_end.strftime("%d/%m/%Y"), text_wrap)
            worksheet.write(1, 6, evaluation.certification_year, text_wrap)
            worksheet.write(1, 7, evaluation.certification_period if evaluation.certification_period else "Not specified", text_wrap)
            if evaluation.status== 'EP':
                worksheet.write(1, 8, "In progress", text_wrap)
            else:
                worksheet.write(1, 8, "Completed", text_wrap)
            worksheet.write(1, 9, evaluation.admin_supervisor.full_name if evaluation.admin_supervisor else "Awaiting evaluation", text_wrap)

            row = 1

            for rr in evaluation.risk_test_residuals.all():
                ri= rr.get_latest_inherent_test
                worksheet_2.write(row, 0, rr.risk.risk.name + ' ('+ rr.risk.risk.ref + ')', text_wrap)
                worksheet_2.write(row, 1, rr.risk.risk.risk_master.name + ' ('+ rr.risk.risk.risk_master.ref + ')', text_wrap)
                worksheet_2.write(row, 2, rr.risk.risk.risk_master.domain_risk.name + ' ('+ rr.risk.risk.risk_master.domain_risk.ref + ')', text_wrap)
                worksheet_2.write(row, 3, strip_tags(rr.risk.risk.description) if rr.risk.risk.description else "Not specified", text_wrap)
                worksheet_2.write(row, 4, strip_tags(rr.risk.risk.krm_main_elements) if rr.risk.risk.krm_main_elements!= '' else "N/A", text_wrap)
                worksheet_2.write(row, 5, strip_tags(rr.risk.risk.krm_main_events) if  rr.risk.risk.krm_main_events!='' else "N/A", text_wrap)
                worksheet_2.write(row, 6, strip_tags(rr.risk.risk.krm_activity_affected) if rr.risk.risk.krm_activity_affected!='' else "N/A", text_wrap)
                worksheet_2.write(row, 7, strip_tags(rr.risk.risk.krm_exposed_staff) if rr.risk.risk.krm_exposed_staff!='' else "N/A", text_wrap)
                worksheet_2.write(row, 8, ri.impact_level_administrator if ri else "No prior inherent risk assessment available", text_wrap)
                worksheet_2.write(row, 9, ri.probability_level_administrator if ri else "No prior inherent risk assessment available", text_wrap)
                worksheet_2.write(row, 10, ri.severity_level_administrator if ri else "No prior inherent risk assessment available", text_wrap)
                worksheet_2.write(row, 11, ri.event_speed_level_administrator if ri else "No prior inherent risk assessment available", text_wrap)
                worksheet_2.write(row, 12, ri.description_administrator if ri else "No prior inherent risk assessment available", text_wrap)
                worksheet_2.write(row, 13, rr.risk.evaluator.full_name if rr.risk.evaluator else "Evaluator not assigned ", text_wrap)
                worksheet_2.write(row, 14, rr.impact_level_evaluator if rr.impact_level_evaluator!=0 else "Awaiting evaluation", text_wrap)
                worksheet_2.write(row, 15, rr.translation_values(rr.impact_level_evaluator), text_wrap)
                worksheet_2.write(row, 16, rr.probability_level_evaluator if rr.probability_level_evaluator!=0 else "Awaiting evaluation", text_wrap)
                worksheet_2.write(row, 17, rr.translation_values(rr.probability_level_evaluator), text_wrap)
                worksheet_2.write(row, 18, rr.severity_level_evaluator if rr.severity_level_evaluator!=0 else "Awaiting evaluation", text_wrap)
                worksheet_2.write(row, 19, rr.qualitative_severity("en", "evaluator"), text_wrap)
                worksheet_2.write(row, 20, rr.event_speed_level_evaluator if rr.event_speed_level_evaluator!=0 else "Awaiting evaluation", text_wrap)
                worksheet_2.write(row, 21, rr.translation_values(rr.event_speed_level_evaluator), text_wrap)
                worksheet_2.write(row, 22, rr.description_evaluator if rr.description_evaluator!='' else "Awaiting evaluation", text_wrap)
                worksheet_2.write(row, 23, rr.impact_level_administrator if rr.impact_level_administrator!=0 else "Awaiting supervision", text_wrap)
                worksheet_2.write(row, 24, rr.translation_values(rr.impact_level_administrator), text_wrap)
                worksheet_2.write(row, 25, rr.probability_level_administrator if rr.probability_level_administrator!=0 else "Awaiting supervision", text_wrap)
                worksheet_2.write(row, 26, rr.translation_values(rr.probability_level_administrator), text_wrap)
                worksheet_2.write(row, 27, rr.severity_level_administrator if rr.severity_level_administrator!=0 else "Awaiting supervision", text_wrap)
                worksheet_2.write(row, 28, rr.qualitative_severity("en", "administrator"), text_wrap)
                worksheet_2.write(row, 29, rr.event_speed_level_administrator if rr.event_speed_level_administrator!=0 else "Awaiting supervision", text_wrap)
                worksheet_2.write(row, 30, rr.translation_values(rr.event_speed_level_administrator), text_wrap)
                worksheet_2.write(row, 31, rr.description_administrator if rr.description_administrator else "Awaiting supervision", text_wrap)
                row += 1

            # Close the workbook before sending the data.
            workbook.close()

            # Rewind the buffer.
            output.seek(0)

            # Set up the Http response.
            response = HttpResponse(
                output,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=%s' % filename

            return response

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "evaluations_krm:ga_evaluation_krm_residual_detail",
            kwargs={"pk": self.evaluation.pk},
        )


@method_decorator([login_required, is_global_admin], name='dispatch')
class GaEvaluationResidualAdminComplete(DetailView, FormView):
    template_name = 'evaluations_krm/GaEvaluationResidualAdminComplete.html'
    model = EvaluationKrmResidual
    context_object_name = 'evaluation'
    form_class = EvaluationResidualCompleteForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Residual')}
        ]
        context['page_title'] = f"{_('Evaluación de Riesgos Residual')} : {self.object.ref}"
        context['breadcrums'] = breadcrums

        risk_tests = self.object.risk_test_residuals.all()

        context['tests'] = risk_tests
        context['evaluation'].domain_risks = context['evaluation'].get_domain_risk_in_evaluation()
        context['js_template'] = ['js/custom/datatables.js']

        return context

    def form_valid(self, form):
        """
        Método para la validación de la valoración del administrador. Este método
        completa los valores del administrador con los dados por el evaluador en el caso
        de que el Administrador haya presionado el botón de "Usar la valoración dada por los evaluadores
        para los riesgos no completados".
        """
        evaluation = self.get_object()
        risk_tests= RiskTestResidual.objects.filter(
            evaluation=evaluation
        )
        for rr in risk_tests:
            rr.status = 3
            if rr.probability_level_administrator == 0:
                rr.probability_level_administrator = rr.probability_level_evaluator
            if rr.impact_level_administrator == 0:
                rr.impact_level_administrator = rr.impact_level_evaluator
            if rr.event_speed_level_administrator==0:
                rr.event_speed_level_administrator = rr.event_speed_level_evaluator
            if rr.description_administrator == '' or rr.description_administrator==None:
                rr.description_administrator = rr.description_evaluator
            rr.save()

        evaluation.status = 'FI'
        evaluation.admin_supervisor = self.request.user
        evaluation.save()
        return super().form_valid(form)

    def get_success_url(self):

        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Evaluación supervisada correctamente como administrador de compañía")
        )

        return reverse_lazy(
            "evaluations_krm:ga_evaluation_residual_list"
        )

@method_decorator([is_global_admin, ], name='dispatch')
class GaEvaluationResidualNotificationsView(DetailView, FormView):
    template_name = 'evaluations_krm/GaEvaluationResidualNotifications.html'
    model = EvaluationKrmResidual
    context_object_name = 'evaluation'
    form_class = EvaluationResidualNotificationForm

    def dispatch(self, request, *args, **kwargs):
        self.evaluation = get_object_or_404(
            EvaluationKrmResidual, pk=self.kwargs.get("pk"))
        return super(GaEvaluationResidualNotificationsView, self).dispatch(
            request, request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Residual'), 'url': reverse(
                'evaluations_krm:ga_evaluation_residual_list')},
            {'title': self.object.ref, 'url': reverse(
                "evaluations_krm:ga_evaluation_krm_residual_detail", kwargs={'pk': self.object.pk})}
        ]
        context['page_title'] = f"{_('Notificaciones de Riesgo Residual')} : {self.object.ref}"
        context['breadcrums'] = breadcrums

        context['evaluation'].evaluators_notifications = context['evaluation'].get_evaluators_for_notifications()

        context['js_template'] = ['js/custom/datatables.js']

        return context

    def post(self, request, *args, **kwargs):
        risk_test_selected = request.POST.getlist('notify_pk')

        from krm.evaluations_krm.models import (
            RiskTestResidual,
        )

        for pk in risk_test_selected:
            rt = RiskTestResidual.objects.filter(pk = int(pk)).first()
            rt.send_notification_evaluator('Reminder')

        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Enviadas notificaciones a %d usuarios!" % len(risk_test_selected))
        )

        return HttpResponseRedirect(
            reverse_lazy(
                "evaluations_krm:ga_evaluation_krm_residual_detail",
                kwargs={'pk': self.evaluation.pk}
            )
        )
