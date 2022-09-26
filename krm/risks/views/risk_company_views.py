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

from krm.risks.forms import RiskCompanyUpdateForm

from krm.risks.models import RiskCompany


# @method_decorator([login_required, ], name='dispatch')
# class GaRiskCompanyDetailView(DetailView):
#     model = RiskCompany
#     template_name = 'risks_masters/GaRiskCompanyDetail.html'
#     context_object_name = 'risk_master'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context = KTLayout.init(context)
#         breadcrums = [
#             {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
#             {'title': _('Riesgos Maestros'), 'url': reverse(
#                 'risks_masters:ga_risk_master_list')},
#             {'title': self.object.name}
#         ]
#         context['page_title'] = f"{_('Riesgo Maestro')} : {self.object.name}"
#         context['breadcrums'] = breadcrums
#         context['actions'] = [
#             {
#                 'title': _('Editar'),
#                 'url': reverse('risks_masters:ga_risk_master_update', kwargs={'pk': self.object.pk}),
#                 'primary': True,
#                 'icon': '<i class="bi bi-pencil"></i>'
#             },
#         ]

#         return context


@method_decorator([login_required, ], name='dispatch')
class RiskCompanyUpdateView(UpdateView):
    form_class = RiskCompanyUpdateForm
    model = RiskCompany
    template_name = 'risks_company/GaRiskCompanyUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {
                'title': _('Dashboard'),
                'url': reverse('users:dashboard')
            },
            {
                'title': self.object.company.name,
                'url': reverse('risks_masters:ga_risk_master_list'),
            },
            {'title': _('Editar')}
        ]
        context['page_title'] = _('Editar Riesgo Compañía')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Riesgo-Compañía actualizado correctamente')
        )
        return reverse_lazy(
            'companies:ga_company_detail',
            kwargs={'pk': self.object.company.pk}
        )


# @method_decorator([login_required, ], name='dispatch')
# class GaRiskCompanyDeleteView(DeleteView):
#     model = RiskCompany
#     template_name = "_includes/_base_confirm_delete.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context = KTLayout.init(context)

#         breadcrums = [
#             {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
#             {'title': _('Riesgos Maestros'), 'url': reverse(
#                 'risks_masters:ga_risk_master_list')},
#             {'title': _('Eliminar')},
#         ]
#         context['page_title'] = _(
#             "Eliminar Riesgo Maestro: %s") % str(self.object.name)
#         context['breadcrums'] = breadcrums

#         return context

#     def get_success_url(self):
#         messages.add_message(
#             self.request, messages.SUCCESS, _(
#                 "Riesgo Maestro eliminado correctamente")
#         )
#         return reverse_lazy("risks_masters:ga_risk_list")

#     def get_confirm_text_message(self):
#         return _(
#             '<span class="kt-font-bold">¿Seguro que desea eliminar el Riesgo Maestro: </span> {0} {1}? <span class="kt-font-bold">Se borrarán todos los datos asociados al mismo.</span>'
#         ).format(str(self.object.ref), self.object.name)
