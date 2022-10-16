from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import get_object_or_404

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

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.risks.forms import RiskMasterCreateForm

from krm.risks.models import RiskMaster, DomainRisk
from django.db.models import Count

@method_decorator([login_required, ], name='dispatch')
class GaRiskMasterListView(ListView):
    model = RiskMaster
    template_name = 'risks_masters/GaRiskMasterList.html'
    context_object_name = 'risks_masters'
    queryset = RiskMaster.objects.all().prefetch_related('risks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Riesgos Maestros (N1)'), 'url': reverse(
                'risks_masters:ga_risk_master_list')},
        ]
        context['page_title'] = _('Riesgos Maestros (N1)')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('risks_masters:ga_risk_master_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([login_required, ], name='dispatch')
class GaRiskMasterDetailView(DetailView):
    model = RiskMaster
    template_name = 'risks_masters/GaRiskMasterDetail.html'
    context_object_name = 'risk_master'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Riesgos Maestro (N1)'), 'url': reverse(
                'risks_masters:ga_risk_master_list')},
            {'title': self.object.name}
        ]
        context['page_title'] = f"{_('Riesgo Maestro (N1)')}: {self.object.name}"
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('risks_masters:ga_risk_master_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]

        return context


@method_decorator([login_required, ], name='dispatch')
class GaRiskMasterCreateView(CreateView):
    form_class = RiskMasterCreateForm
    model = RiskMaster
    template_name = 'risks_masters/GaRiskMasterCreate.html'

    def get_initial(self):
        if 'domain_risk' in self.kwargs:
            domain_risk = get_object_or_404(
                DomainRisk, pk=self.kwargs.get('domain_risk')
            )
            return {
                'domain_risk': domain_risk
            }
        else:
            return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Riesgos Maestros (N1)'), 'url': reverse(
                'risks_masters:ga_risk_master_list')},
            {'title': _('Nuevo'), 'url': reverse(
                'risks_masters:ga_risk_master_create')},
        ]
        context['page_title'] = _('Nuevo Riesgo Maestro')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Riesgo maestro creado correctamente')
        )
        return reverse_lazy(
            'risks_masters:ga_risk_master_list'
        )


@method_decorator([login_required, ], name='dispatch')
class GaRiskMasterUpdateView(UpdateView):
    form_class = RiskMasterCreateForm
    model = RiskMaster
    template_name = 'risks_masters/GaRiskMasterCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Riesgos Maestros (N1)'), 'url': reverse(
                'risks_masters:ga_risk_master_list')},
            {'title': _('Editar')},
        ]
        context['page_title'] = _('Editar Riesgo Maestro (N1)')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Riesgo Maestro (N1) actualizado correctamente')
        )
        return reverse_lazy(
            'risks_masters:ga_risk_master_detail',
            kwargs={"pk": self.object.pk},
        )


@method_decorator([login_required, ], name='dispatch')
class GaRiskMasterDeleteView(DeleteView):
    model = RiskMaster
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Riesgos Maestros (N1)'), 'url': reverse(
                'risks_masters:ga_risk_master_list')},
            {'title': _('Eliminar')},
        ]
        context['page_title'] = _(
            "Eliminar Riesgo Maestro (N1): %s") % str(self.object.name)
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Riesgo Maestro eliminado correctamente")
        )
        return reverse_lazy("risks_masters:ga_risk_list")

    def get_confirm_text_message(self):
        return _(
            '<span class="kt-font-bold">¿Seguro que desea eliminar el Riesgo Maestro: </span> {0} {1}? <span class="kt-font-bold">Se borrarán todos los datos asociados al mismo.</span>'
        ).format(str(self.object.ref), self.object.name)
