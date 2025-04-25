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
from django.forms.models import model_to_dict

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations_krm.models import EvaluationKrmResidual
from krm.companies.models import Company

from krm.evaluations_krm.forms import (
    EvaluationResidualCreateForm,
)

from krm.evaluations_krm.models import (
    EvaluationKrmResidual,
    RiskTestResidual,
    RiskCompanyResidual
)

from krm.risks.models import RiskCompany

from krm.evaluations_krm.models import RiskTestInherent
from krm.companies.models import (
    CompanyDomainRiskEvaluator
)

from krm.users.decorators import (
    is_company_admin,
    user_can_view_evaluation_residual,
    is_auditor
)

from krm.evaluations_krm.forms import (
    EvaluationResidualCompleteForm,
    EvaluationResidualCreateForm,
    EvaluationResidualNotificationForm
)


@method_decorator([login_required, is_auditor, ], name='dispatch')
class AuEvaluationResidualListView(ListView):
    model = EvaluationKrmResidual
    template_name = 'evaluations_krm/AuEvaluationResidualList.html'
    context_object_name = 'evaluations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Residual KRM'), 'url': reverse(
                'evaluations_krm:au_evaluation_residual_list')},
        ]
        context['page_title'] = _('Evaluaciones de Riesgo Residual KRM')
        context['breadcrums'] = breadcrums

        domain_risk_audit = self.request.user.audit_domain_risk.all()

        ev_pending = EvaluationKrmResidual.objects.filter(status="EP")

        # De estas solo nos quedamos con las que tienen riesgos del dominio de que el auditor puede auditar
        for e in ev_pending:
            if e.get_domain_risk_in_evaluation().filter(pk__in=domain_risk_audit).count() == 0:
                ev_pending = ev_pending.exclude(pk=e.pk)

        ev_finished = EvaluationKrmResidual.objects.filter(status="FI")
        # De estas solo nos quedamos con las que tienen riesgos del dominio de que el auditor puede auditar
        for e in ev_finished:
            if e.get_domain_risk_in_evaluation().filter(pk__in=domain_risk_audit).count() == 0:
                ev_finished = ev_finished.exclude(pk=e.pk)

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



@method_decorator([login_required, is_auditor, user_can_view_evaluation_residual], name='dispatch')
class AuEvaluationResidualDetailView(DetailView):
    template_name = 'evaluations_krm/AuEvaluationResidualDetail.html'
    model = EvaluationKrmResidual

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['evaluation'] = self.object
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Residual KRM'), 'url': reverse(
                'evaluations_krm:au_evaluation_residual_list')},
            {'title': self.object.ref}
        ]
        context['page_title'] = f"{_('Evaluación de Riesgo Residual KRM')} : {self.object.ref}"
        context['breadcrums'] = breadcrums

        context['evaluation'].nrisk_test_residuals_pending = context['evaluation'].nrisk_test_residuals_by_state(1)
        context['evaluation'].nrisk_test_residuals_delivered = context['evaluation'].nrisk_test_residuals_by_state(2)
        context['evaluation'].nrisk_test_residuals_finished = context['evaluation'].nrisk_test_residuals_by_state(3)
        context['evaluation'].evaluators_pending = context['evaluation'].get_evaluators_by_rrt_state(1)
        context['evaluation'].evaluators_delivered = context['evaluation'].get_evaluators_by_rrt_state(2)
        context['evaluation'].evaluators_finished = context['evaluation'].get_evaluators_by_rrt_state(3)
        context['evaluation'].sev_not_stablished = context['evaluation'].nrisk_test_residuals_by_severity('SE')
        context['evaluation'].sev_very_low = context['evaluation'].nrisk_test_residuals_by_severity('MB')
        context['evaluation'].sev_low = context['evaluation'].nrisk_test_residuals_by_severity('B')
        context['evaluation'].sev_medium = context['evaluation'].nrisk_test_residuals_by_severity('M')
        context['evaluation'].sev_high = context['evaluation'].nrisk_test_residuals_by_severity('A')
        context['evaluation'].sev_very_high = context['evaluation'].nrisk_test_residuals_by_severity('MA')
        context['evaluation'].total_evaluators = context['evaluation'].evaluators_pending.count(
        ) + context['evaluation'].evaluators_delivered.count() + context['evaluation'].evaluators_finished.count()
        context['evaluation'].domain_risks = context['evaluation'].get_domain_risk_in_evaluation()

        # Serializar Evaluation no incluye sus hijos :(
        # Busco los hijos
        context['rrt'] = RiskTestResidual.objects.filter(
            evaluation=self.object)

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
