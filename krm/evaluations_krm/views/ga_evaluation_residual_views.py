from django.shortcuts import render
from django.conf import settings
import json
import uuid
import xlsxwriter
import re

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

from krm.users.models import User

from krm.companies.models import (
    CompanyDomainRiskEvaluator,
    Company
)

from krm.risks.models import RiskCompany

from krm.evaluations_krm.forms import (
    EvaluationResidualCreateForm,
    EvaluationResidualCompleteForm,
    EvaluationResidualNotificationForm,
)

from krm.evaluations.forms import (
    EvaluationActionForm
)


from krm.users.decorators import is_global_admin, user_can_view_evaluation

from krm.utils.utils import clean_html


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
            {'title': _('Evaluaciones de Riesgo Residual KRM'), 'url': reverse(
                'evaluations_krm:ga_evaluation_inherent_list')},
        ]
        context['page_title'] = _('Evaluaciones de Riesgo Residual KRM')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('evaluations_krm:ga_evaluation_residual_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]

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
            {'title': _('Evaluaciones KRM'), 'url': reverse(
                'evaluations:ga_evaluation_list')},
            {'title': _('Nuevo'), 'url': reverse(
                'evaluations_krm:ga_evaluation_residual_create')},
        ]
        context['page_title'] = _('Nueva Evaluación de Riesgo Residual [KRM]')
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

                # Ahora para cada Evaluación vamos a crear los RiskCompanyResidual
                e.create_risk_company_residual()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("%s Evaluaciones creadas correctamente") % str(evaluations_created),
        )

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("%s Test de Riesgos Residual creados correctamente") % str(
                risk_tests__created),
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
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['evaluation'] = self.evaluation
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones KRM'), 'url': reverse(
                'evaluations_krm:ga_evaluation_residual_list')},
            {'title': self.evaluation.ref}
        ]
        context['page_title'] = f"{_('Evaluación KRM Residual')} : {self.evaluation.ref}"
        context['breadcrums'] = breadcrums

        context['evaluation'].nrisk_test_residuals_pending = context['evaluation'].nrisk_test_residuals_by_state(
            1)
        context['evaluation'].nrisk_test_residuals_delivered = context['evaluation'].nrisk_test_residuals_by_state(
            2)
        context['evaluation'].nrisk_test_residuals_finished = context['evaluation'].nrisk_test_residuals_by_state(
            3)

        context['evaluation'].evaluators_pending = context['evaluation'].get_evaluators_by_rrt_state(
            1)
        context['evaluation'].evaluators_delivered = context['evaluation'].get_evaluators_by_rrt_state(
            2)
        context['evaluation'].evaluators_finished = context['evaluation'].get_evaluators_by_rrt_state(
            3)

        context['evaluation'].total_evaluators = context['evaluation'].evaluators_pending.count(
        ) + context['evaluation'].evaluators_delivered.count() + context['evaluation'].evaluators_finished.count()

        context['evaluation'].domain_risks = context['evaluation'].get_domain_risk_in_evaluation()

        # Serializar Evaluation no incluye sus hijos :(
        # Busco los hijos
        context['rrt'] = RiskTestResidual.objects.filter(
            evaluation=self.evaluation)

        # Paso a dict para json
        context['rrt_dict'] = [model_to_dict(m) for m in context['rrt']]

        # MODEL_TO_DICT not getting properties :(
        # Get .severity_level_expert
        # TBI for cuadratico :/
        # Los risk_inherent_test no tienen ref ni name, es heredado del risk_company
        for i, r1 in enumerate(context['rrt']):
            context['rrt_dict'][i]['risk_ref'] = r1.risk.risk.ref
            context['rrt_dict'][i]['risk_name'] = r1.risk.risk.name
            context['rrt_dict'][i]['evaluator'] = r1.evaluator.username_no_domain

        # Sort by severity for a nice plot
        context['rrt_dict'] = sorted(
            context['rrt_dict'], key=lambda x: (x['risk_ref']), reverse=False)

        # Errores de encoding caracteres portugueses y españoles
        for i, m in enumerate(context['rrt_dict']):
            for k in m:
                if type(context['rrt_dict'][i][k]) == str:
                    context['rrt_dict'][i][k] = context['rrt_dict'][i][k].encode(
                        'utf-8').decode('utf-8')

        # JSON DUMP
        context['rrt_json'] = json.dumps(
            context['rrt_dict'],
            default=str,
            ensure_ascii=True,
        )

        # REPEAT FOR RISK COMPANY RESIDUAL (AGGREGATES)
        context['rcr'] = RiskCompanyResidual.objects.filter(
            evaluation=self.evaluation)
        context['rcr_dict'] = [model_to_dict(m) for m in context['rcr']]
        for i, r1 in enumerate(context['rcr']):
            context['rcr_dict'][i]['risk_ref'] = r1.risk_company.risk.ref
            context['rcr_dict'][i]['risk_name'] = r1.risk_company.risk.name
            
            context['rcr_dict'][i]['impact_inherent'] = r1.get_latest_impact_inherent
            context['rcr_dict'][i]['probability_inherent'] = r1.get_latest_probability_inherent
            context['rcr_dict'][i]['severity_inherent'] = r1.get_latest_severity_inherent
            context['rcr_dict'][i]['probability_residual_eval'] = r1.probability_level_result_evaluator
            context['rcr_dict'][i]['probability_residual_admin'] = r1.probability_level_result_admin
            context['rcr_dict'][i]['nivel_de_control'] = r1.probability_level_residual_evaluator_aggregate_rounded

        context['rcr_dict'] = context['rcr_dict'] 
        # sorted(
        #     context['rcr_dict'], key=lambda x: (x['severity_inherent'] + x['probability_residual_eval']), reverse=True)

        for i, m in enumerate(context['rcr_dict']):
            for k in m:
                if type(context['rcr_dict'][i][k]) == str:
                    context['rcr_dict'][i][k] = context['rcr_dict'][i][k].encode(
                        'utf-8').decode('utf-8')
            
        context['rcr_json'] = json.dumps(
            context['rcr_dict'],
            default=str,
            ensure_ascii=True,
        )
        

        context['js_template'] = ['js/custom/datatables.js']

        return context

    def form_valid(self, form):
        action = form.cleaned_data["action"]
        evaluation = self.evaluation

        if action == 'download':
            import io

            filename = f'residual_evaluation_{evaluation.ref}.xlsx'

            # Create an in-memory output file for the new workbook.
            output = io.BytesIO()

            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet()

            # Add a bold format to use to highlight cells.
            bold = workbook.add_format({'bold': True})
            text_wrap = workbook.add_format({'text_wrap': True})

            columns = [
                'Ev_REF',
                'COMPANY',
                'COMPANY_TYPE',
                'DESCRIPTION',
                'DATE_BEGIN',
                'DATE_END',
                'CERTIFICATION_YEAR',
                'CERTIFICATION_PERIOD',
                'Ev_STATUS',
                'MAIN_ELEMENTS',
                'MAIN_EVENTS',
                'ACTIVITY_AFFECTED',
                'EXPOSED_STAFF',
                'DOMAIN_RISK',
                'RR_REF_N1',
                'RR_REF_N2',
                'RR_NAME',
                'RISK_DESCRIPTION',
                'EXPERT_NAME',
                'JUSTIFICATION_EXPERT',
                'SEVERITY_LEVEL_EXPERT',
                'SEVERITY_LEVEL_EXPERT_QUALITATIVE',
                'IMPACT_LEVEL_EXPERT',
                'IMPACT_LEVEL_EXPERT_QUALITATIVE',
                'PROBABILITY_LEVEL_EXPERT',
                'PROBABILITY_LEVEL_EXPERT_QUALITATIVE',
                'ADMIN_SUPERVISOR',
                'JUSTIFICATION_ADMIN',
                'SEVERITY_LEVEL_ADMIN',
                'SEVERITY_LEVEL_ADMIN_QUALITATIVE',
                'IMPACT_LEVEL_ADMIN',
                'IMPACT_LEVEL_ADMIN_QUALITATIVE',
                'PROBABILITY_LEVEL_ADMIN',
                'PROBABILITY_LEVEL_ADMIN_QUALITATIVE',
                'EVALUATOR_NAMES',
                'JUSTIFICATION_EVALUATORS',
                'SEVERITY_LEVEL_EVALUATORS',
                'SEVERITY_LEVEL_EVALUATORS_QUALITATIVE',
                'SEVERITY_LEVEL_EVALUATORS_AGGREGATE',
                'SEVERITY_LEVEL_EVALUATORS_AGGREGATE_QUALITATIVE',
                'IMPACT_LEVEL_EVALUATORS',
                'IMPACT_LEVEL_EVALUATORS_QUALITATIVE',
                'Nivel de control por evaluador',
                'Nivel de control por evaluador cualitativo',
                'Nivel de control agregado',
                'Nivel de control agregado redondeado',
                'Nivel de control agregado redondeado cualitativo',
                'ADMIN_SUPERVISOR',
                'JUSTIFICATION_ADMIN',
                'SEVERITY_LEVEL_ADMIN',
                'SEVERITY_LEVEL_ADMIN_QUALITATIVE',
                'IMPACT_LEVEL_ADMIN',
                'IMPACT_LEVEL_ADMIN_QUALITATIVE',
                'PROBABILITY_LEVEL_ADMIN',
                'PROBABILITY_LEVEL_ADMIN_QUALITATIVE'
            ]

            for index, col_name in enumerate(columns):
                worksheet.write(0, index, col_name, bold)

            #Ev
            worksheet.set_column(0, 1, 25)    # Ev_REF
            worksheet.set_column(1, 2, 25)    # COMPANY
            worksheet.set_column(2, 3, 70)    # COMPANY_TYPE
            worksheet.set_column(3, 4, 25)    # DESCRIPTION
            worksheet.set_column(4, 5, 25)    # DATE_BEGIN
            worksheet.set_column(5, 6, 25)    # DATE_END
            worksheet.set_column(6, 7, 25)    # CERTIFICATION_YEAR
            worksheet.set_column(7, 8, 25)    # CERTIFICATION_PERIOD
            worksheet.set_column(8, 9, 70)    # Ev_STATUS
            
            worksheet.set_column(9, 10, 70)   # MAIN_ELEMENTS
            worksheet.set_column(10, 11, 70)  # MAIN_EVENTS
            worksheet.set_column(11, 12, 70)  # ACTIVITY_AFFECTED
            worksheet.set_column(12, 13, 25)  # EXPOSED_STAFF

            #RR/RI
            worksheet.set_column(13, 14, 25)  # DOMAIN_RISK
            worksheet.set_column(14, 15, 25)  # RR_REF_N1
            worksheet.set_column(15, 16, 25)  # RR_REF_N2
            worksheet.set_column(16, 17, 70)  # RR_NAME
            worksheet.set_column(17, 18, 25)  # RISK_DESCRIPTION

            #RI
            worksheet.set_column(18, 19, 70)  # EXPERT_NAME
            worksheet.set_column(19, 20, 25)  # JUSTIFICATION_EXPERT
            worksheet.set_column(20, 21, 25)  # SEVERITY_LEVEL_EXPERT
            worksheet.set_column(21, 22, 25)  # SEVERITY_LEVEL_EXPERT_QUALITATIVE
            worksheet.set_column(22, 23, 25)  # IMPACT_LEVEL_EXPERT
            worksheet.set_column(23, 24, 25)  # IMPACT_LEVEL_EXPERT_QUALITATIVE
            worksheet.set_column(24, 25, 25)  # PROBABILITY_LEVEL_EXPERT
            worksheet.set_column(25, 26, 25)  # PROBABILITY_LEVEL_EXPERT_QUALITATIVE

            worksheet.set_column(26, 27, 70)  # ADMIN_SUPERVISOR
            worksheet.set_column(27, 28, 25)  # JUSTIFICATION_ADMIN
            worksheet.set_column(28, 29, 25)  # SEVERITY_LEVEL_ADMIN
            worksheet.set_column(29, 30, 25)  # SEVERITY_LEVEL_ADMIN_QUALITATIVE
            worksheet.set_column(30, 31, 25)  # IMPACT_LEVEL_ADMIN
            worksheet.set_column(31, 32, 25)  # IMPACT_LEVEL_ADMIN_QUALITATIVE
            worksheet.set_column(32, 33, 25)  # PROBABILITY_LEVEL_ADMIN
            worksheet.set_column(33, 34, 25)  # PROBABILITY_LEVEL_ADMIN_QUALITATIVE

            #RR
            worksheet.set_column(34, 35, 70)  # EVALUATOR_NAMES
            worksheet.set_column(35, 36, 25)  # JUSTIFICATION_EVALUATORS
            worksheet.set_column(36, 37, 25)  # SEVERITY_LEVEL_EVALUATORS
            worksheet.set_column(37, 38, 25)  # SEVERITY_LEVEL_EVALUATORS_QUALITATIVE
            worksheet.set_column(38, 39, 25)  # SEVERITY_LEVEL_EVALUATORS_AGGREGATE
            worksheet.set_column(39, 40, 25)  # SEVERITY_LEVEL_EVALUATORS_AGGREGATE_QUALITATIVE
            worksheet.set_column(40, 41, 25)  # IMPACT_LEVEL_EVALUATORS
            worksheet.set_column(41, 42, 25)  # IMPACT_LEVEL_EVALUATORS_QUALITATIVE 
            worksheet.set_column(42, 43, 25)  # Nivel de control por evaluador - PROBABILITY_LEVEL_EVALUATORS
            worksheet.set_column(43, 44, 25)  # Nivel de control por evaluador cualit. - PROBABILITY_LEVEL_EVALUATORS_QUALITATIVE   
            worksheet.set_column(44, 45, 25)  # Nivel de control agregado - PROBABILITY_LEVEL_EVALUATORS_AGGREGATE
            worksheet.set_column(45, 46, 25)  # Nivel de control agregado redondeado - PROBABILITY_LEVEL_EVALUATORS_AGGREGATE_ROUNDED
            worksheet.set_column(46, 47, 25)  # Nivel de control agregado redondeado cualitativo - PROBABILITY_LEVEL_EVALUATORS_QUALITATIVE

            worksheet.set_column(47, 48, 70)  # ADMIN_SUPERVISOR
            worksheet.set_column(48, 49, 25)  # JUSTIFICATION_ADMIN
            worksheet.set_column(49, 50, 25)  # SEVERITY_LEVEL_ADMIN
            worksheet.set_column(50, 51, 25)  # SEVERITY_LEVEL_ADMIN_QUALITATIVE
            worksheet.set_column(51, 52, 25)  # IMPACT_LEVEL_ADMIN
            worksheet.set_column(52, 53, 25)  # IMPACT_LEVEL_ADMIN_QUALITATIVE    
            worksheet.set_column(53, 54, 25)  # PROBABILITY_LEVEL_ADMIN
            worksheet.set_column(54, 55, 25)  # PROBABILITY_LEVEL_ADMIN_QUALITATIVE

            row = 1
            domains = ""

            for rr in evaluation.risk_company_residuals.all():
                #Evaluation 
                worksheet.write(row, 0, evaluation.ref, text_wrap)
                worksheet.write(row, 1, evaluation.company.name, text_wrap)
                worksheet.write(row, 2, evaluation.company.type_company, text_wrap)
                worksheet.write(row, 3, evaluation.description, text_wrap)
                worksheet.write(row, 4, evaluation.date_begin.strftime("%d/%m/%Y"))
                worksheet.write(row, 5, evaluation.date_end.strftime("%d/%m/%Y"))
                worksheet.write(row, 6, evaluation.certification_year)
                worksheet.write(row, 7, evaluation.certification_period)
                worksheet.write(row, 8, evaluation.status)

                worksheet.write(row, 9, rr.get_latest_inherent.risk.krm_main_elements, text_wrap)
                worksheet.write(row, 10, rr.get_latest_inherent.risk.krm_main_events, text_wrap)
                worksheet.write(row, 11, rr.get_latest_inherent.risk.krm_activity_affected, text_wrap)
                worksheet.write(row, 12, rr.get_latest_inherent.risk.krm_exposed_staff, text_wrap)

                for dom in evaluation.get_domain_risk_in_evaluation():
                    if dom.ref not in domains:
                        domains += dom.ref
                        # domains += ","
                worksheet.write(row, 13, domains)
                worksheet.write(row, 14, rr.get_latest_inherent.risk.risk.risk_master.ref, text_wrap)
                worksheet.write(row, 15, rr.get_latest_inherent.risk.risk.ref, text_wrap)
                worksheet.write(row, 16, rr.get_latest_inherent.risk.name, text_wrap)
                worksheet.write(row, 17, rr.get_latest_inherent.risk.description, text_wrap)
                
                #Latest RI
                worksheet.write(row, 18, rr.get_latest_inherent.expert.full_name, text_wrap)
                worksheet.write(row, 19, rr.get_latest_inherent.description, text_wrap)
                worksheet.write(row, 20, rr.get_latest_inherent.severity_level_expert, text_wrap)
                worksheet.write(row, 21, rr.get_latest_inherent.severity_level_expert_qualitative, text_wrap)
                worksheet.write(row, 22, rr.get_latest_inherent.impact_level_expert, text_wrap)
                worksheet.write(row, 23, rr.get_latest_inherent.get_impact_level_expert_display(), text_wrap)
                worksheet.write(row, 24, rr.get_latest_inherent.probability_level_expert, text_wrap)
                worksheet.write(row, 25, rr.get_latest_inherent.get_probability_level_expert_display(), text_wrap)

                if evaluation.admin_supervisor != None:
                    worksheet.write(row, 26, evaluation.admin_supervisor.full_name)
                worksheet.write(row, 27, rr.description_administrator, text_wrap)
                worksheet.write(row, 28, rr.get_latest_inherent.severity_level_admin, text_wrap)
                worksheet.write(row, 29, rr.get_latest_inherent.severity_level_admin_qualitative, text_wrap)
                worksheet.write(row, 30, rr.get_latest_inherent.impact_level_administrator, text_wrap)
                worksheet.write(row, 31, rr.get_latest_inherent.get_impact_level_administrator_display(), text_wrap)
                worksheet.write(row, 32, rr.get_latest_inherent.probability_level_administrator, text_wrap)
                worksheet.write(row, 33, rr.get_latest_inherent.get_probability_level_administrator_display(), text_wrap)
                
                #worksheet.write(row, 18, rr.risk_company.expert_assign, text_wrap)
                rt_list = rr.risk_test_residuals.all()
                evaluators, evaluators_descrp, severity_residual, severity_residual_qualitative, probability, probability_qualitative = [], [], [], [], [], []
                for rt in rt_list:
                    evaluators.append(rt.evaluator.full_name)
                    evaluators_descrp.append(rt.description_evaluator)
                    severity_residual.append(str(rt.severity_residual_evaluator))
                    severity_residual_qualitative.append(rt.severity_residual_evaluator_qualitative)
                    probability.append(str(rt.probability_level_residual_evaluator))
                    probability_qualitative.append(rt.probability_level_residual_evaluator_qualitative)
                
                worksheet.write(row, 34, '\n'.join(evaluators), text_wrap)
                worksheet.write(row, 35, '\n'.join(evaluators_descrp), text_wrap)
                worksheet.write(row, 36, '\n'.join(severity_residual), text_wrap)
                worksheet.write(row, 37, '\n'.join(severity_residual_qualitative), text_wrap)
                worksheet.write(row, 38, rr.severity_residual_evaluator, text_wrap)
                worksheet.write(row, 39, rr.severity_residual_evaluator_qualitative, text_wrap)
                worksheet.write(row, 40, rr.get_latest_inherent.impact_level_expert, text_wrap)
                worksheet.write(row, 41, rr.get_latest_inherent.get_impact_level_expert_display(), text_wrap)
                worksheet.write(row, 42, '\n'.join(probability), text_wrap)
                worksheet.write(row, 43, '\n'.join(probability_qualitative), text_wrap)
                worksheet.write(row, 44, rr.probability_level_residual_evaluator_aggregate, text_wrap)
                worksheet.write(row, 45, rr.probability_level_residual_evaluator_aggregate_rounded, text_wrap)
                worksheet.write(row, 46, rr.probability_residual_evaluator_qualitative, text_wrap)
                
                if evaluation.admin_supervisor != None:
                    worksheet.write(row, 47, evaluation.admin_supervisor.full_name)
                worksheet.write(row, 48, rr.description_administrator, text_wrap)
                worksheet.write(row, 49, rr.severity_residual_admin, text_wrap)
                worksheet.write(row, 50, rr.severity_residual_admin_qualitative, text_wrap)
                worksheet.write(row, 51, rr.get_latest_inherent.impact_level_administrator, text_wrap)
                worksheet.write(row, 52, rr.get_latest_inherent.get_impact_level_administrator_display(), text_wrap)
                worksheet.write(row, 53, rr.probability_level_residual_administrator, text_wrap)
                worksheet.write(row, 54, rr.probability_residual_administrator_qualitative, text_wrap)

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

        # if action == "i":
        #     evaluation.status = "EP"
        #     evaluation.save()
        #     users_notificated = []
        #     for ct in evaluation.control_tests.all():
        #         ct.status = "WO"
        #         ct.save()
        #         if ct.control_test_owner not in users_notificated:
        #             users_notificated.append(ct.control_test_owner)
        #             ct.send_notification()

        #     messages.add_message(
        #         self.request,
        #         messages.SUCCESS,
        #         _("Evaluación iniciada correctamente"),
        #     )
        # elif action == 'f':
        #     evaluation.status = "FI"
        #     evaluation.save()
        #     evaluation.control_tests.update(
        #         status='FI'
        #     )

        #     messages.add_message(
        #         self.request,
        #         messages.SUCCESS,
        #         _("Evaluación finalizada correctamente"),
        #     )

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
        context['page_title'] = f"{_('Evaluación de Riesgos Residuals')} : {self.object.ref}"
        context['breadcrums'] = breadcrums

        # SIMPLIFICACION
        # uso risk_test (nomenclatura), no son risk_test, son risk_company
        risk_tests = self.object.risk_company_residuals.all()

        for r in risk_tests:
            r.controls_attempt_to_mitigate = r.get_controls_attempt_to_mitigate()
            r.test_controls_attempt_to_mitigate = r.get_test_controls_attempt_to_mitigate()

        context['risks_test_residual'] = risk_tests
        # sorted( risk_tests, key=lambda t: t.get_latest_severity_inherent, reverse=True)

        context['evaluation'].domain_risks = context['evaluation'].get_domain_risk_in_evaluation()

        context['js_template'] = ['js/custom/datatables.js']

        return context

    def form_valid(self, form):
        evaluation = self.get_object()
        RiskTestResidual.objects.filter(
            evaluation=evaluation
        ).update(
            status=3
        )

        # Ahora para los que no ha completado el administrador de la compañía, debemos completar con los valores agregados que han dado los evaluadores

        for rr in RiskTestResidual.objects.filter(evaluation=evaluation):
            rr.status = 3
            # Ahora buscamos el Risk Company Residual
            rcr = RiskCompanyResidual.objects.get(
                evaluation=evaluation,
                risk_company=rr.risk
            )

            if rcr.probability_level_residual_administrator == 0:
                if rcr.probability_level_residual_evaluator_aggregate_rounded == 0:
                    rcr.probability_level_residual_administrator = 4
                else:
                    rcr.probability_level_residual_administrator = rcr.probability_level_residual_evaluator_aggregate_rounded
            if rcr.description_administrator == '':
                rcr.description_administrator = _('--Sin completar--')

            rcr.save()
            rr.save()

        evaluation.status = 'FI'
        evaluation.admin_supervisor = self.request.user
        evaluation.save()
        return super().form_valid(form)

    def get_success_url(self):

        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Evaluación supervisada correctamente")
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
            {'title': _('Evaluaciones KRM'), 'url': reverse(
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