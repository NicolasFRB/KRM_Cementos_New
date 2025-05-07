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
from django.forms.models import model_to_dict

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from krm.evaluations.forms.evaluation_forms import EvaluationAssignImportForm, EvaluationDownload, EvaluationActionForm, EvaluationTemplateAssignDownload
from krm.evaluations.models import ControlTest

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations_krm.models import EvaluationKrmInherent
from krm.companies.models import Company

from krm.evaluations_krm.forms import (
    EvaluationInherentCreateForm,
)

from krm.risks.models import RiskCompany

from krm.evaluations_krm.models import RiskTestInherent
from krm.companies.models import CompanyDomainRiskExperts

from krm.users.decorators import (
    is_company_admin,
    user_can_view_evaluation_inherent,
    is_auditor
)

from krm.evaluations_krm.forms import (
    EvaluationInherenetCompleteForm,
    EvaluationInherentNotificationForm
)


@method_decorator([login_required, is_auditor, ], name='dispatch')
class AuEvaluationInherentListView(ListView):
    model = EvaluationKrmInherent
    template_name = 'evaluations_krm/AuEvaluationInherentList.html'
    context_object_name = 'evaluations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Inherente KRM'), 'url': reverse(
                'evaluations_krm:au_evaluation_inherent_list')},
        ]
        context['page_title'] = _('Evaluaciones de Riesgo Inherente KRM')
        context['breadcrums'] = breadcrums

        domain_risk_audit = self.request.user.audit_domain_risk.all()

        ev_pending = EvaluationKrmInherent.objects.filter(status="EP")

        # De estas solo nos quedamos con las que tienen riesgos del dominio de que el auditor puede auditar
        for e in ev_pending:
            if e.get_domain_risk_in_evaluation().filter(pk__in=domain_risk_audit).count() == 0:
                ev_pending = ev_pending.exclude(pk=e.pk)

        ev_finished = EvaluationKrmInherent.objects.filter(status="FI")

        # De estas solo nos quedamos con las que tienen riesgos del dominio de que el auditor puede auditar
        for e in ev_finished:
            if e.get_domain_risk_in_evaluation().filter(pk__in=domain_risk_audit).count() == 0:
                ev_finished = ev_finished.exclude(pk=e.pk)

        for ev in ev_pending:
            ev.nrisk_test_inherents_pending = ev.nrisk_test_inherents_by_state(
                1)
            ev.nrisk_test_inherents_delivered = ev.nrisk_test_inherents_by_state(
                2)
            ev.nrisk_test_inherents_finished = ev.nrisk_test_inherents_by_state(
                3)

            ev.experts_pending = ev.get_experts_by_rit_state(1)
            ev.experts_delivered = ev.get_experts_by_rit_state(2)
            ev.experts_finished = ev.get_experts_by_rit_state(3)

            ev.total_experts = ev.experts_pending.count() + ev.experts_delivered.count() + \
                ev.experts_finished.count()

            ev.domain_risks = ev.get_domain_risk_in_evaluation()

        for ev in ev_finished:
            ev.nrisk_test_inherents_pending = ev.nrisk_test_inherents_by_state(
                1)
            ev.nrisk_test_inherents_delivered = ev.nrisk_test_inherents_by_state(
                2)
            ev.nrisk_test_inherents_finished = ev.nrisk_test_inherents_by_state(
                3)

            ev.experts_pending = ev.get_experts_by_rit_state(1)
            ev.experts_delivered = ev.get_experts_by_rit_state(2)
            ev.experts_finished = ev.get_experts_by_rit_state(3)

            ev.total_experts = ev.experts_pending.count() + ev.experts_delivered.count() + \
                ev.experts_finished.count()

            ev.domain_risks = ev.get_domain_risk_in_evaluation()

        context['evaluations_pending'] = ev_pending
        context['evaluations_finished'] = ev_finished
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([login_required, is_auditor, user_can_view_evaluation_inherent], name='dispatch')
class AuEvaluationInherentDetailView(DetailView):
    template_name = 'evaluations_krm/AuEvaluationInherentDetail.html'
    model = EvaluationKrmInherent

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['evaluation'] = self.object
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Inherente KRM'), 'url': reverse(
                'evaluations_krm:au_evaluation_inherent_list')},
            {'title': self.object.ref}
        ]
        context['page_title'] = f"{_('Evaluación de Riesgo Inherente KRM')} : {self.object.ref}"
        context['breadcrums'] = breadcrums

        context['evaluation'].nrisk_test_inherents_pending = context['evaluation'].nrisk_test_inherents_by_state(1)
        context['evaluation'].nrisk_test_inherents_delivered = context['evaluation'].nrisk_test_inherents_by_state(2)
        context['evaluation'].nrisk_test_inherents_finished = context['evaluation'].nrisk_test_inherents_by_state(3)
        context['evaluation'].experts_pending = context['evaluation'].get_experts_by_rit_state(1)
        context['evaluation'].experts_delivered = context['evaluation'].get_experts_by_rit_state(2)
        context['evaluation'].experts_finished = context['evaluation'].get_experts_by_rit_state(3)
        context['evaluation'].sev_not_stablished = context['evaluation'].nrisk_test_inherents_by_severity('SE')
        context['evaluation'].sev_very_low = context['evaluation'].nrisk_test_inherents_by_severity('MB')
        context['evaluation'].sev_low = context['evaluation'].nrisk_test_inherents_by_severity('B')
        context['evaluation'].sev_medium = context['evaluation'].nrisk_test_inherents_by_severity('M')
        context['evaluation'].sev_high = context['evaluation'].nrisk_test_inherents_by_severity('A')
        context['evaluation'].sev_very_high = context['evaluation'].nrisk_test_inherents_by_severity('MA')
        context['evaluation'].total_experts = context['evaluation'].experts_pending.count(
        ) + context['evaluation'].experts_delivered.count() + context['evaluation'].experts_finished.count()

        context['evaluation'].domain_risks = context['evaluation'].get_domain_risk_in_evaluation()

        context['rit'] = RiskTestInherent.objects.filter(evaluation=self.object)

        context['rit_dict'] = []
        for risk_test in context['rit']:
            information = {}
            information['ref']= risk_test.risk.risk.ref
            information['name']= risk_test.risk.risk.name
            information['evaluator']= risk_test.expert.username_no_domain
            information['impact_evaluator']= risk_test.impact_level_expert
            information['probability_evaluator']= risk_test.probability_level_expert
            information['severity_evaluator']= risk_test.severity_level_expert
            information['administrator']= self.object.admin_supervisor.username_no_domain if self.object.admin_supervisor else ''
            information['impact_administrator']= risk_test.impact_level_administrator
            information['probability_administrator']= risk_test.probability_level_administrator
            information['severity_administrator']= risk_test.severity_level_administrator
            context['rit_dict'].append(information)

        if self.object.admin_supervisor:
            context['rit_dict'] = sorted(context['rit_dict'], key=lambda x: x['severity_administrator'], reverse=False)
        else:
            context['rit_dict'] = sorted(context['rit_dict'], key=lambda x: x['severity_evaluator'], reverse=False)

        # Errores de encoding caracteres portugueses y españoles
        # for i, m in enumerate(context['rit_dict']):
        #     for k in m:
        #         if type(context['rit_dict'][i][k]) == str:
        #             context['rit_dict'][i][k] = context['rit_dict'][i][k].encode(
        #                 'utf-8').decode('utf-8')

        # JSON DUMP
        context['rit_json'] = json.dumps(context['rit_dict'], default=str, ensure_ascii=True)
        context['js_template'] = ['js/custom/datatables.js']

        return context
