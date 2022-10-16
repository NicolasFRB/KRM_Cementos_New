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

from krm.risks.forms import RiskCreateForm

from krm.risks.models import Risk, RiskMaster


@method_decorator([login_required, ], name='dispatch')
class GaRiskListView(ListView):
    model = Risk
    template_name = 'risks/GaRiskList.html'
    context_object_name = 'risks'
    queryset = Risk.objects.all().prefetch_related('controls')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Riesgos'), 'url': reverse(
                'risks:ga_risk_list')},
        ]
        context['page_title'] = _('Riesgos (N2)')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('risks:ga_risk_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([login_required, ], name='dispatch')
class GaRiskDetailView(DetailView):
    model = Risk
    template_name = 'risks/GaRiskDetail.html'
    context_object_name = 'risk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Riesgos (N2)'), 'url': reverse(
                'risks:ga_risk_list')},
            {'title': self.object.name}
        ]
        context['page_title'] = f"{_('Riesgo (N2)')} : {self.object.name}"
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('risks:ga_risk_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]

        return context


@method_decorator([login_required, ], name='dispatch')
class GaRiskCreateView(CreateView):
    form_class = RiskCreateForm
    model = Risk
    template_name = 'risks/GaRiskCreate.html'

    def get_initial(self):
        if 'domain_risk' in self.kwargs:
            risk_master = get_object_or_404(
                RiskMaster, pk=self.kwargs.get('risk_master')
            )
            return {
                'risk_master': risk_master
            }
        else:
            return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Riesgos'), 'url': reverse(
                'risks:ga_risk_list')},
            {'title': _('Nuevo (N2)'), 'url': reverse(
                'risks:ga_risk_create')},
        ]
        context['page_title'] = _('Nuevo Riesgo')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Riesgo creado correctamente')
        )
        return reverse_lazy(
            'risks:ga_risk_list'
        )


@method_decorator([login_required, ], name='dispatch')
class GaRiskUpdateView(UpdateView):
    form_class = RiskCreateForm
    model = Risk
    template_name = 'risks/GaRiskCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Riesgos'), 'url': reverse(
                'risks:ga_risk_list')},
            {'title': _('Editar')},
        ]
        context['page_title'] = _('Editar Riesgo (N2)')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Riesgo actualizado correctamente')
        )
        return reverse_lazy(
            'risks:ga_risk_detail',
            kwargs={"pk": self.object.pk},
        )


@method_decorator([login_required, ], name='dispatch')
class GaRiskDeleteView(DeleteView):
    model = Risk
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Riesgos (N2)'), 'url': reverse(
                'risks:ga_risk_list')},
            {'title': _('Eliminar')},
        ]
        context['page_title'] = _(
            "Eliminar Riesgo: %s") % str(self.object.name)
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Riesgo (N2) eliminado correctamente")
        )
        return reverse_lazy("risks:ga_risk_list")

    def get_confirm_text_message(self):
        return _(
            '<span class="kt-font-bold">¿Seguro que desea eliminar el Riesgo (N2): </span> {0} {1}? <span class="kt-font-bold">Se borrarán todos los datos asociados al mismo.</span>'
        ).format(str(self.object.ref), self.object.name)
