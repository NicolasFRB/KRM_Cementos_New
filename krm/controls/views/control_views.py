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

from krm.controls.forms import ControlCreateForm
from krm.controls.models import Control
from krm.risks.models import Risk

from krm.users.decorators import is_global_admin


@method_decorator([is_global_admin, ], name='dispatch')
class GaControlListView(ListView):
    model = Control
    template_name = 'controls/GaControlList.html'
    context_object_name = 'controls'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Controles'), 'url': reverse(
                'controls:ga_control_list')},
        ]
        context['page_title'] = _('Controles')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('controls:ga_control_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([is_global_admin, ], name='dispatch')
class GaControlDetailView(DetailView):
    model = Control
    template_name = 'controls/GaControlDetail.html'
    context_object_name = 'control'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Controles'), 'url': reverse(
                'controls:ga_control_list')},
            {'title': self.object.ref}
        ]
        context['page_title'] = f"{_('Control')} : {self.object.ref}"
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('controls:ga_control_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]

        return context


@method_decorator([is_global_admin, ], name='dispatch')
class GaControlCreateView(CreateView):
    form_class = ControlCreateForm
    model = Control
    template_name = 'controls/GaControlCreate.html'

    def get_initial(self):
        if 'domain_Control' in self.kwargs:
            risk = get_object_or_404(
                Risk, pk=self.kwargs.get('risk')
            )
            return {
                'risk': risk
            }
        else:
            return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Controles'), 'url': reverse(
                'controls:ga_control_list')},
            {'title': _('Nuevo control'), 'url': reverse(
                'controls:ga_control_create')},
        ]
        context['page_title'] = _('Nuevo Control')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Control creado correctamente')
        )
        return reverse_lazy(
            'controls:ga_control_list'
        )


@method_decorator([is_global_admin, ], name='dispatch')
class GaControlUpdateView(UpdateView):
    form_class = ControlCreateForm
    model = Control
    template_name = 'controls/GaControlCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Controles'), 'url': reverse(
                'controls:ga_control_list')},
            {'title': _('Editar')},
        ]
        context['page_title'] = _('Editar Control')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Control actualizado correctamente')
        )
        return reverse_lazy(
            'controls:ga_control_list'
        )


@method_decorator([is_global_admin, ], name='dispatch')
class GaControlDeleteView(DeleteView):
    model = Control
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Controles'), 'url': reverse(
                'controls:ga_control_list')},
            {'title': _('Eliminar')},
        ]
        context['page_title'] = _("Eliminar Riesgo")
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Control eliminado correctamente")
        )
        return reverse_lazy("controls:ga_control_list")

    def get_confirm_text_message(self):
        return _(
            '<span class="kt-font-bold">¿Seguro que desea eliminar el Control: </span> {0}? <span class="kt-font-bold">Se borrarán todos los datos asociados al mismo.</span>'
        ).format(str(self.object))
