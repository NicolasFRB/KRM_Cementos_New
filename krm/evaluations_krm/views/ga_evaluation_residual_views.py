from django.shortcuts import render
from django.conf import settings
import json
import uuid

import re

# Create your views here.
from django.shortcuts import render

from django.views.generic import (
    FormView,
    ListView
)
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _

from django.shortcuts import get_object_or_404

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations_krm.models import (
    EvaluationKrmResidual,
    RiskTestResidual
)
from krm.companies.models import (
    CompanyDomainRiskEvaluator,
    Company
)

from krm.risks.models import RiskCompany

from krm.evaluations_krm.forms import (
    EvaluationResidualCreateForm,
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
            ev.nrisk_test_residuals_pending = ev.nrisk_test_residuals_by_state(1)
            ev.nrisk_test_residuals_delivered = ev.nrisk_test_residuals_by_state(2)
            ev.nrisk_test_residuals_finished = ev.nrisk_test_residuals_by_state(3)

            ev.evaluators_pending = ev.get_evaluators_by_rrt_state(1)
            ev.evaluators_delivered = ev.get_evaluators_by_rrt_state(2)
            ev.evaluators_finished = ev.get_evaluators_by_rrt_state(3)

            ev.total_evaluators = ev.evaluators_pending.count() + ev.evaluators_delivered.count() + ev.evaluators_finished.count()

            ev.domain_risks = ev.get_domain_risk_in_evaluation()

        for ev in ev_finished:
            ev.nrisk_test_residuals_pending = ev.nrisk_test_residuals_by_state(1)
            ev.nrisk_test_residuals_delivered = ev.nrisk_test_residuals_by_state(2)
            ev.nrisk_test_residuals_finished = ev.nrisk_test_residuals_by_state(3)

            ev.evaluators_pending = ev.get_evaluators_by_rrt_state(1)
            ev.evaluators_delivered = ev.get_evaluators_by_rrt_state(2)
            ev.evaluators_finished = ev.get_evaluators_by_rrt_state(3)

            ev.total_evaluators = ev.evaluators_pending.count() + ev.evaluators_delivered.count() + ev.evaluators_finished.count()

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
