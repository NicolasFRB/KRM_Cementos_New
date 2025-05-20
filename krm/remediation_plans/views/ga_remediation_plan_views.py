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


@method_decorator([login_required, is_company_admin, ], name='dispatch')
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
                'url': reverse('remediation_plans:ga_remediation_plan_create_select_company'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]

        # Si no es superusuario, mostramos los planes de la compañía que administra el usuario
        # if not self.request.user.is_superuser:
        #     remediation_plan_in_progress = RemediationPlan.objects.filter(
        #         company__in=self.request.user.companies_admin.all(),
        #         date_end__gte=timezone.now(),
        #         status='EP'
        #     )
        #     remediation_plan_expired = RemediationPlan.objects.filter(
        #         company__in=self.request.user.companies_admin.all(),
        #         date_end__lt=timezone.now(),
        #         status='EP'
        #     )
        #     remediation_plan_completed = RemediationPlan.objects.filter(
        #         company__in=self.request.user.companies_admin.all(),
        #         status='CO'
        #     )

        # Si es superusuario, mostramos todos los planes
        remediation_plan_in_progress = RemediationPlan.objects.filter(
            date_end__gte=timezone.now(),
            status='EP'
        )
        remediation_plan_expired = RemediationPlan.objects.filter(
            date_end__lt=timezone.now(),
            status='EP'
        )
        remediation_plan_completed = RemediationPlan.objects.filter(
            status='CO',
        )

        if not self.request.user.is_superuser and self.request.user.is_company_admin:
            # Si es administrador de compañía, filtraremos únicamente los planes de su compañía
            remediation_plan_in_progress = remediation_plan_in_progress.filter(company__in=self.request.user.companies_admin.all())
            remediation_plan_expired = remediation_plan_expired.filter(company__in=self.request.user.companies_admin.all())
            remediation_plan_completed = remediation_plan_completed.filter(company__in=self.request.user.companies_admin.all())

        context['remediation_plan_in_progress'] = remediation_plan_in_progress
        context['remediation_plan_expired'] = remediation_plan_expired
        context['remediation_plan_completed'] = remediation_plan_completed

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

    # def get_form(self, form_class=None):
    #     form = super().get_form(form_class=None)

    #     # El campo next_to_reply solo se muestra si el usuario es el supervisor del plan o superusuario
    #     if self.request.user == self.remediation_plan.responsible and self.request.user != self.remediation_plan.supervisor:
    #       form.fields['next_to_reply'].widget = forms.HiddenInput()

    #     return form

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

    def post(self, request, *args, **kwargs):
        # Si viene el parámetro action="notificar" enviamos la notificación
        if self.request.POST.get('action') == 'notificar':
            custom_message = None
            if self.request.POST.get('custom_message'):
                custom_message = self.request.POST.get('custom_message')
            self.remediation_plan.sent_notification(custom_message)
            messages.success(self.request, _('Notificación enviada correctamente'))
            # Redirigimos a la misma vista
            return HttpResponseRedirect(reverse('remediation_plans:ga_remediation_plan_detail', kwargs={'pk': self.remediation_plan.pk}))
        else:
            return super().post(request, *args, **kwargs)


    def form_valid(self, form):
        form.instance.remediation_plan = self.remediation_plan
        form.instance.user = self.request.user

        form.save()

        self.remediation_plan.next_to_reply = form.instance.next_to_reply
        self.remediation_plan.status = form.instance.status
        self.remediation_plan.save()

        self.remediation_plan.sent_notification()

        # Añadir mensaje de plan de remediación respondido correctamente
        messages.success(self.request, _('Respuesta añadida al Plan de remediación correctamente'))

        return super().form_valid(form)

    def get_success_url(self):
      return reverse_lazy('remediation_plans:ga_remediation_plan_list')


@method_decorator([login_required, is_company_admin, ], name='dispatch')
class GaRemediationPlanCreateSelectCompanyView(FormView):
    form_class = RemediationPlanCreateSelectCompany
    model = RemediationPlan
    template_name = 'remediation_plans/GaRemediationPlanCreateSelectCompany.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Planes de Remediación'), 'url': reverse(
                'remediation_plans:ga_remediation_plan_list')},
            {'title': _('Nuevo'), 'url': reverse(
                'remediation_plans:ga_remediation_plan_create_select_company')},
        ]
        context['page_title'] = _('Nuevo Plan de Remediación')
        context['breadcrums'] = breadcrums
        context['js_template'] = ['js/custom/datatables.js']
        return context


    def form_valid(self, form):
        # Cogemos el id de la compañaía desde el formulario
        company_id = form.cleaned_data['company']
        self.company = get_object_or_404(Company, pk=company_id)
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('remediation_plans:ga_remediation_plan_create', kwargs={'company_pk': self.company.pk})

    def get_form(self, form_class=None):
        form_class = super().get_form(form_class=None)

        # Si el usuario es superusuario, mostramos todas las compañías
        if self.request.user.is_superuser:
            companies = Company.objects.all()
        else:
            # Si no es superusuario, mostramos las compañías que administra
            companies = self.request.user.companies_admin.all()

        form_class.fields["company"].choices = [(c.pk, c.name) for c in companies]
        form_class.fields["company"].choices = [("", _("-"))] + form_class.fields["company"].choices
        return form_class


@method_decorator([login_required, is_company_admin, ], name='dispatch')
class GaRemediationPlanCreateView(CreateView):
    form_class = RemediationPlanCreateForm
    model = RemediationPlan
    template_name = 'remediation_plans/GaRemediationPlanCreate.html'

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs.get("company_pk"):
            company = get_object_or_404(Company, pk=self.kwargs.get("company_pk"))
            self.company = company
        else:
            # Redireccionamos a la vista anterior
            return HttpResponseRedirect(reverse('remediation_plans:ga_remediation_plan_create_select_company'))
        return super().dispatch(request, *args, **kwargs)


    def get_form(self, form_class=None):

        # Quiero filtrar los usuarios por la compañía seleccionada
        form_class = super().get_form(form_class=None)

        users = User.objects.filter(
            companies__in=(self.company,),
            is_active=True
        )

        form_class.fields["responsible"].queryset = users

        form_class.fields["supervisor"].queryset = users

        form_class.fields["additional_users"].queryset = users

        # form_class.fields["company"].initial = self.company.pk

        # Filtramos los controles únicamente por los que estén activos para la empresa
        company_controls = self.company.company_controls.filter(active=True).values_list('control', flat=True)
        form_class.fields["control"].queryset = Control.objects.filter(id__in=company_controls)

        return form_class

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Planes de Remediación'), 'url': reverse(
                'remediation_plans:ga_remediation_plan_list')},
            {'title': _('Nuevo'), 'url': reverse(
                'remediation_plans:ga_remediation_plan_create_select_company')},
        ]
        context['page_title'] = _('Nuevo Plan de Remediación')
        context['breadcrums'] = breadcrums
        context['js_template'] = ['js/custom/datatables.js']
        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Plan de Remediación creado correctamente')
        )

        # Enviar notificación
        self.object.sent_notification()

        return reverse_lazy(
            'remediation_plans:ga_remediation_plan_list'
        )


    def form_valid(self, form):
        form.instance.company = self.company
        return super().form_valid(form)



@method_decorator([login_required, is_company_admin, ], name='dispatch')
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



    def get_form(self, form_class=None):

        # Quiero filtrar los usuarios por la compañía seleccionada
        form_class = super().get_form(form_class=None)

        users = User.objects.filter(
            companies__in=(self.object.company,),
            is_active=True
        )

        form_class.fields["responsible"].queryset = users

        form_class.fields["supervisor"].queryset = users

        form_class.fields["additional_users"].queryset = users

        # form_class.fields["company"].initial = self.company.pk

        # Filtramos los controles únicamente por los que estén activos para la empresa
        company_controls = self.object.company.company_controls.filter(active=True).values_list('control', flat=True)
        form_class.fields["control"].queryset = Control.objects.filter(id__in=company_controls)

        return form_class



@method_decorator([login_required, is_company_admin, ], name='dispatch')
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
