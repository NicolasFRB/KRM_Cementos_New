from django.shortcuts import render

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

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from krm.users.decorators import is_global_admin

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.risks.forms import DomainRiskCreateForm

from krm.risks.models import DomainRisk
from django.db.models import Count

@method_decorator([login_required, is_global_admin], name='dispatch')
class GaDomainRiskListView(ListView):
    model = DomainRisk
    template_name = 'domain_risks/GaDomainRiskList.html'
    context_object_name = 'domain_risks'
    queryset = DomainRisk.objects.all().prefetch_related('risks__risks').all().annotate(n_risks_master=Count('risks', distinct=True), n_risks=Count('risks__risks', distinct=True))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Dominios de Riesgo'), 'url': reverse(
                'domain_risks:ga_domain_risk_list')},
        ]
        context['page_title'] = _('Dominios de Riesgo')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('domain_risks:ga_domain_risk_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([login_required, is_global_admin], name='dispatch')
class GaDomainRiskDetailView(DetailView):
    model = DomainRisk
    template_name = 'domain_risks/GaDomainRiskDetail.html'
    context_object_name = 'domain_risk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Dominios de Riesgo'), 'url': reverse(
                'domain_risks:ga_domain_risk_list')},
            {'title': self.object.name}
        ]
        context['page_title'] = f"{_('Dominio de Riesgo')} : {self.object.name}"
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('domain_risks:ga_domain_risk_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]
        
        return context


@method_decorator([login_required, ], name='dispatch')
class GaDomainRiskCreateView(CreateView):
    form_class = DomainRiskCreateForm
    model = DomainRisk
    template_name = 'domain_risks/GaDomainRiskCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Dominios de Riesgo'), 'url': reverse(
                'domain_risks:ga_domain_risk_list')},
            {'title': _('Nuevo'), 'url': reverse(
                'domain_risks:ga_domain_risk_create')},
        ]
        context['page_title'] = _('Nuevo Dominio de Riesgo')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Dominio de Riesgo creado correctamente')
        )
        return reverse_lazy(
            'domain_risks:ga_domain_risk_list'
        )


@method_decorator([login_required, is_global_admin], name='dispatch')
class GaDomainRiskUpdateView(UpdateView):
    form_class = DomainRiskCreateForm
    model = DomainRisk
    template_name = 'domain_risks/GaDomainRiskUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Dominios de Riesgo'), 'url': reverse(
                'domain_risks:ga_domain_risk_list')},
            {'title': _('Editar')},
        ]
        context['page_title'] = _('Editar Dominio de Riesgo')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Dominio de Riesgo actualizado correctamente')
        )
        return reverse_lazy(
            'domain_risks:ga_domain_risk_detail',
            kwargs={"pk": self.object.pk},
        )


@method_decorator([login_required, is_global_admin], name='dispatch')
class GaDomainRiskDeleteView(DeleteView):
    model = DomainRisk
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Dominios de Riesgo'), 'url': reverse(
                'domain_risks:ga_domain_risk_list')},
            {'title': _('Eliminar')},
        ]
        context['page_title'] = _(
            "Eliminar Dominio de Riesgo: #%s") % str(self.object.name)
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Dominio de Riesgo eliminado correctamente")
        )
        return reverse_lazy("domain_risks:ga_domain_risk_list")

    def get_confirm_text_message(self):
        return _(
            '<span class="kt-font-bold">¿Seguro que desea eliminar el Dominio de Riesgo, Riesgos Maestros y los riesgos asociados?: </span> {0} {1}? <span class="kt-font-bold">Se borrarán todos los riesgos y controles asociados al mismo.</span>'
        ).format(str(self.object.ref), self.object.name)
