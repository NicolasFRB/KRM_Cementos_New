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

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.companies.forms import CompanyCreateForm
from krm.companies.models import Company

from krm.users.decorators import is_global_admin


@method_decorator([is_global_admin, ], name='dispatch')
class GaCompanyListView(ListView):
    model = Company
    template_name = 'companies/GaCompanyList.html'
    context_object_name = 'companies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ga_company_list')},
        ]
        context['page_title'] = _('Companías')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('companies:ga_company_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([is_global_admin, ], name='dispatch')
class GaCompanyDetailView(DetailView):
    model = Company
    template_name = 'companies/GaCompanyDetail.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ga_company_list')},
            {'title': self.object.vat}
        ]
        context['page_title'] = f"{_('Compañía')} : {self.object.name}"
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('companies:ga_company_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]

        return context


@method_decorator([is_global_admin, ], name='dispatch')
class GaCompanyCreateView(CreateView):
    form_class = CompanyCreateForm
    model = Company
    template_name = 'companies/GaCompanyCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ga_company_list')},
            {'title': _('Nueva Compañía'), 'url': reverse(
                'companies:ga_company_create')},
        ]
        context['page_title'] = _('Nueva Compañía')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Compañía creada correctamente')
        )
        return reverse_lazy(
            'companies:ga_company_list'
        )


@method_decorator([is_global_admin, ], name='dispatch')
class GaCompanyUpdateView(UpdateView):
    form_class = CompanyCreateForm
    model = Company
    template_name = 'companies/GaCompanyCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ga_company_list')},
            {'title': _('Editar')},
        ]
        context['page_title'] = _('Editar Compañía')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Compañía actualizada correctamente')
        )
        return reverse_lazy(
            'companies:ga_company_list'
        )


@method_decorator([is_global_admin, ], name='dispatch')
class GaCompanyDeleteView(DeleteView):
    model = Company
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ga_company_list')},
            {'title': _('Eliminar')},
        ]
        context['page_title'] = _("Eliminar Compañía")
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Compañía eliminada correctamente")
        )
        return reverse_lazy("companies:ga_company_list")

    def get_confirm_text_message(self):
        return _(
            '<span class="kt-font-bold">¿Seguro que desea eliminar la Companía y todas sus evaluaciónes?: </span> {0}? <span class="kt-font-bold">Se borrarán todos los datos asociados la misma.</span>'
        ).format(str(self.object))
