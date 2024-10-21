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

@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaRemediationPlanListView(ListView):
    model = RemediationPlan
    template_name = 'remediation_plans/GaRemediationPlanList.html'
    context_object_name = 'remediation_plans'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Planes de remediación'), 'url': reverse(
                'remediation_plans:ga_remediation_plan_list')},
        ]
        context['page_title'] = _('Planes de remediación')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('remediation_plans:ga_remediation_plan_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]

        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([login_required, user_can_view_remediation_plan, ], name='dispatch')
class GaRemediationPlanDetailView(CreateView):
    template_name = 'remediation_plans/GaRemediationPlanDetail.html'
    model = RemediationPlanAnswer
    # context_object_name = 'remediation_plan'
    form_class = RemediationPlanAnswerCreateForm

    def dispatch(self, request, *args, **kwargs):
        remediation_plan = get_object_or_404(RemediationPlan, pk=self.kwargs.get("pk"))
        self.remediation_plan = remediation_plan

        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class=None)

        # El campo next_to_reply solo se muestra si el usuario es el supervisor del plan o superusuario
        if self.request.user == self.remediation_plan.responsible and self.request.user != self.remediation_plan.supervisor:
          form.fields['next_to_reply'].widget = forms.HiddenInput()

        return form

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

        # solo mostramos el botón de editar si es el supervisor del plan o superusuario
        if self.request.user == self.remediation_plan.supervisor or self.request.user.is_admin:
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


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaRemediationPlanCreateView(CreateView):
    form_class = RemediationPlanCreateForm
    model = RemediationPlan
    template_name = 'remediation_plans/GaRemediationPlanCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Planes de Remediación'), 'url': reverse(
                'remediation_plans:ga_remediation_plan_list')},
            {'title': _('Nuevo'), 'url': reverse(
                'remediation_plans:ga_remediation_plan_create')},
        ]
        context['page_title'] = _('Nueva Plan de Remediación')
        context['breadcrums'] = breadcrums
        context['js_template'] = ['js/custom/datatables.js']
        return context

    def get_success_url(self):

        return reverse_lazy(
            'remediation_plans:ga_remediation_plan_list'
        )

@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaRemediationPlanUpdateView(UpdateView):
    form_class = RemediationPlanUpdateForm
    model = RemediationPlan
    template_name = 'remediation_plans/GaRemediationPlanUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Planes de Remediación'), 'url': reverse(
                'remediation_plans:ga_remediation_plan_list')},
            {'title': _('Editar')},
        ]
        context['page_title'] = _('Editar Plan de Remediación')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Plan de Remediación actualizado correctamente')
        )
        return reverse_lazy(
            'remediation_plans:ga_remediation_plan_detail',
            kwargs={"pk": self.object.pk},
        )


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaRemediationPlanDeleteView(DeleteView):
    model = RemediationPlan
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Planes de Remediación'), 'url': reverse(
                'remediation_plans:ga_remediation_plan_list')},
            {'title': _('Eliminar')},
        ]
        context['page_title'] = _(
            "Eliminar Plan de Remediación: #%s") % str(self.object.pk)
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Plan de Remediación eliminada correctamente")
        )
        return reverse_lazy("remediation_plans:ga_remediation_plan_list")

    def get_confirm_text_message(self):
        return _(
            '<span class="kt-font-bold">¿Seguro que desea eliminar la Plan de Remediación y los datos asociados?: </span> {0}? <span class="kt-font-bold">Se borrarán todos los datos asociados al mismo.</span>'
        ).format(str(self.object.pk))



def delete_attachment(request, pk_remediation_plan, pk_attachment):
    # Comprobamos si el usuario está autenticado
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("users:login"))

    # Ahora comprobamos que el usuario es el remediation_plan responsible,remediation_plan supervisor
    remediation_plan_answer = get_object_or_404(RemediationPlanAnswer, pk=pk_remediation_plan)
    if request.user == remediation_plan_answer.remediation_plan.responsible or request.user == remediation_plan_answer.remediation_plan.supervisor or request.user.is_superuser:
        if pk_attachment == '1':
            remediation_plan_answer.attachment_1.delete()
            remediation_plan_answer.attachment_1 = None

        remediation_plan_answer.save()

        # Devolvemos un status 200
        # return HttpResponse(status=200)
        return HttpResponseRedirect(reverse('remediation_plans:ga_remediation_plan_detail', kwargs={'pk': remediation_plan_answer.remediation_plan.pk}))
    else:
        # Devolvemos un status 403
        return HttpResponse(status=403)
