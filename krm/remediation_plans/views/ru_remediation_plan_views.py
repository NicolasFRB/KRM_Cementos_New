import json
import uuid
import xlwt

# import forms
from django import forms
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

from krm.users.decorators import is_global_admin, user_can_view_remediation_plan

from krm.remediation_plans.forms import RemediationPlanCreateForm, RemediationPlanUpdateForm
from krm.remediation_plans.models import RemediationPlanAnswer
from krm.remediation_plans.forms import RemediationPlanAnswerCreateForm, RuSupervisorRemediationPlanAnswerCreateForm, RuResponsibleRemediationPlanAnswerCreateForm

@method_decorator([login_required, ], name='dispatch')
class RuRemediationPlanListView(ListView):
    model = RemediationPlan
    template_name = 'remediation_plans/RuRemediationPlanList.html'
    context_object_name = 'remediation_plans'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Planes de remediación'), 'url': reverse(
                'remediation_plans:ru_remediation_plan_list')},
        ]
        context['page_title'] = _('Planes de remediación')
        context['breadcrums'] = breadcrums

        context['js_template'] = ['js/custom/datatables.js']

        context['rp_responsible'] = RemediationPlan.objects.filter(responsible=self.request.user, status='EP')
        context['rp_supervisor'] = RemediationPlan.objects.filter(supervisor=self.request.user, status='EP')
        context['rp_others'] = RemediationPlan.objects.filter(additional_users=self.request.user, status='EP')
        context['rp_finished'] = self.request.user.get_finished_remediaton_plans()

        return context


@method_decorator([login_required, user_can_view_remediation_plan, ], name='dispatch')
class RuRemediationPlanDetailView(CreateView):
    template_name = 'remediation_plans/RuRemediationPlanDetail.html'
    model = RemediationPlanAnswer

    def dispatch(self, request, *args, **kwargs):
        remediation_plan = get_object_or_404(RemediationPlan, pk=self.kwargs.get("pk"))
        self.remediation_plan = remediation_plan
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Planes de Remediación'), 'url': reverse(
                'remediation_plans:ga_remediation_plan_list')},
            {'title': self.remediation_plan}
        ]
        context['page_title'] = f"{_('Plan de Remediación')} : {self.remediation_plan.pk}"
        context['breadcrums'] = breadcrums
        context['remediation_plan'] = self.remediation_plan

        context['js_template'] = ['js/custom/datatables.js']

        return context


    def form_valid(self, form):
        form.instance.remediation_plan = self.remediation_plan
        form.instance.user = self.request.user
        form.save()

        # Si el plan está pendiente de respuesta del Responsable y el usado es el responsable
        if self.request.user == self.remediation_plan.responsible and self.remediation_plan.next_to_reply == 'WR':
            self.remediation_plan.next_to_reply = 'WS'
        elif self.request.user == self.remediation_plan.supervisor:
            self.remediation_plan.next_to_reply = form.instance.next_to_reply
            self.remediation_plan.status = form.instance.status

        self.remediation_plan.save()
        self.remediation_plan.sent_notification()

        # Añadir mensaje de plan de remediación respondido correctamente
        messages.success(self.request, _('Respuesta añadida al Plan de remediación correctamente'))

        return super().form_valid(form)


    def get_success_url(self):
      return reverse_lazy('remediation_plans:ru_remediation_plan_list')


    def get_form_class(self):
        if self.remediation_plan.next_to_reply == "WR" and self.request.user == self.remediation_plan.responsible:
            return RuResponsibleRemediationPlanAnswerCreateForm
        elif self.remediation_plan.next_to_reply == "WS" and self.request.user == self.remediation_plan.supervisor:
            return RuSupervisorRemediationPlanAnswerCreateForm
        else:
            return RemediationPlanAnswerCreateForm
