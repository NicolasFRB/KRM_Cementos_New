from django.shortcuts import render
from django.conf import settings
import json
import uuid

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

from krm.evaluations_krm.forms import (
    EvaluationResidualCreateForm,
    EvaluationResidualCompleteForm,
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
        print(ev_pending)
        print(ev_finished)
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
            risks = RiskCompany.objects.filter(pk__in=(rc['risks']))

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
                domain_risk = risk.risk.risk_master.domain_risk
                company_risk_evaluators = CompanyDomainRiskEvaluator.objects.get(
                    company=company,
                    domain_risk=domain_risk
                )

                # Hay que crear un test de riesgo por cada evaluador
                for evaluator in company_risk_evaluators.evaluator.all():
                    RiskTestResidual.objects.create(
                        evaluation=evaluation,
                        risk=risk,
                        evaluator=evaluator
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
                        rt.send_notification_evaluator()
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

        context['js_template'] = ['js/custom/datatables.js']

        return context

    def form_valid(self, form):
        action = form.cleaned_data["action"]
        evaluation = self.evaluation

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

        context['risks_test_residual'] = sorted(
            risk_tests, key=lambda t: t.get_latest_severity_inherent, reverse=True)

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
