import json
import uuid
import xlwt


from django.shortcuts import render
from django.conf import settings
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

# Importar hidden field
from django import forms

# timezone
from django.utils import timezone

from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.remediation_plans.models import RemediationPlan

from krm.users.models import User

from krm.users.decorators import is_global_admin, user_can_view_remediation_plan, is_company_admin

from krm.remediation_plans.forms import RemediationPlanCreateForm, RemediationPlanUpdateForm
from krm.remediation_plans.models import RemediationPlanAnswer
from krm.remediation_plans.forms import RemediationPlanAnswerCreateForm, RemediationPlanCreateSelectCompany

from krm.companies.models import Company
from krm.controls.models import Control
from krm.users.decorators import (
    user_can_view_evaluation,
    is_auditor
)

@method_decorator([login_required, is_auditor, ], name='dispatch')
class AuRemediationPlanListView(ListView):
    model = RemediationPlan
    template_name = 'remediation_plans/AuRemediationPlanList.html'
    context_object_name = 'remediation_plans'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Planes de remediación'), 'url': reverse(
                'remediation_plans:au_remediation_plan_list')},
        ]
        context['page_title'] = _('Planes de remediación')
        context['breadcrums'] = breadcrums

        # Si es superusuario, mostramos todos los planes
        remediation_plan_in_progress = RemediationPlan.objects.filter(
            date_end__gte=timezone.now(),
            status='EP'
        )

        # Vamos a filtrar de los planes de remediación en progreso, aquellos que tengan un dominio de riesgo de los que el usuario auditor audita
        remediation_plan_in_progress_to_show = []
        for rm in remediation_plan_in_progress:
            for domain_risk_audit in self.request.user.audit_domain_risk.all():
                if domain_risk_audit in rm.get_domain_risks():
                    if rm not in remediation_plan_in_progress_to_show:
                        remediation_plan_in_progress_to_show.append(rm)
        remediation_plan_in_progress = remediation_plan_in_progress_to_show

        remediation_plan_expired = RemediationPlan.objects.filter(
            date_end__lt=timezone.now(),
            status='EP'
        )

        # Vamos a filtrar de los planes de remediación en progreso, aquellos que tengan un dominio de riesgo de los que el usuario auditor audita
        remediation_plan_expired_to_show = []
        for rm in remediation_plan_expired:
            for domain_risk_audit in self.request.user.audit_domain_risk.all():
                if domain_risk_audit in rm.get_domain_risks():
                    if rm not in remediation_plan_expired_to_show:
                        remediation_plan_expired_to_show.append(rm)
        remediation_plan_expired = remediation_plan_expired_to_show

        remediation_plan_completed = RemediationPlan.objects.filter(
            status='CO'
        )
        # Vamos a filtrar de los planes de remediación en progreso, aquellos que tengan un dominio de riesgo de los que el usuario auditor audita
        remediation_plan_completed_to_show = []
        for rm in remediation_plan_completed:
            for domain_risk_audit in self.request.user.audit_domain_risk.all():
                if domain_risk_audit in rm.get_domain_risks():
                    if rm not in remediation_plan_completed_to_show:
                        remediation_plan_completed_to_show.append(rm)

        context['remediation_plan_in_progress'] = remediation_plan_in_progress
        context['remediation_plan_expired'] = remediation_plan_expired
        context['remediation_plan_completed'] = remediation_plan_completed

        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([login_required, user_can_view_remediation_plan, ], name='dispatch')
class AuRemediationPlanDetailView(DetailView):
    template_name = 'remediation_plans/AuRemediationPlanDetail.html'
    model = RemediationPlan
    context_object_name = 'remediation_plan'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Planes de Remediación'), 'url': reverse(
                'remediation_plans:au_remediation_plan_list')},
            {'title': self.object}
        ]
        context['page_title'] = f"{_('Plan de Remediación')} : {self.object.pk}"
        context['breadcrums'] = breadcrums

        context['js_template'] = ['js/custom/datatables.js']

        return context
