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
from krm.remediation_plans.forms import RemediationPlanAnswerCreateForm

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
        # context['actions'] = [
        #     {
        #         'title': _('Nuevo'),
        #         'url': reverse('remediation_plans:ga_remediation_plan_create'),
        #         'primary': True,
        #         'icon': '<i class="bi bi-plus-lg"></i>'
        #     },
        # ]

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
    # context_object_name = 'remediation_plan'
    form_class = RemediationPlanAnswerCreateForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)
        import ipdb; ipdb.set_trace()
        if not self.request.user.is_admin:
            form.fields['status'].widget = forms.HiddenInput()

        return form


    def dispatch(self, request, *args, **kwargs):
        import ipdb; ipdb.set_trace()

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
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('remediation_plans:ga_remediation_plan_update', kwargs={'pk': self.remediation_plan.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]

        context['js_template'] = ['js/custom/datatables.js']

        return context


    def form_valid(self, form):
        form.instance.remediation_plan = self.remediation_plan
        form.instance.user = self.request.user
        form.save()

        # Si el usuario es administrador global, o el usuario supervisor del plan de remediación, ponemos el plan como completado si el estado propuesto es Completado
        if self.request.user.is_superuser or self.request.user == self.remediation_plan.supervisor:
            if form.instance.status == 'CO':
                self.remediation_plan.status = 'CO'
                self.remediation_plan.next_to_reply = 'FI'
                self.remediation_plan.save()

                form.instance.next_to_reply = 'FI'
                form.save()

        else:
          # Si no, es que es un usaurio responsable, por lo que únicamente tenemos que cambiar es next_to_reply al responsable
          form.instance.next_to_reply = 'WR'
          form.save()
          self.remediation_plan.next_to_reply = 'WS'
          self.remediation_plan.save()

        return super().form_valid(form)

    def get_success_url(self):
      return reverse_lazy('remediation_plans:ga_remediation_plan_detail', kwargs={'pk': self.remediation_plan.pk})
