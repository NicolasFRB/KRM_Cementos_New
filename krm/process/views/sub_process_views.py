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

from krm.process.forms import SubProcessCreateForm

from krm.process.models import SubProcess, Process


@method_decorator([login_required, ], name='dispatch')
class GaSubProcessListView(ListView):
    model = SubProcess
    template_name = 'subprocess/GaSubProcessList.html'
    context_object_name = 'subprocess'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Sub Procesos'), 'url': reverse(
                'subprocess:ga_sub_process_list')},
        ]
        context['page_title'] = _('Sub Procesos')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('subprocess:ga_sub_process_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([login_required, ], name='dispatch')
class GaSubProcessDetailView(DetailView):
    model = SubProcess
    template_name = 'subprocess/GaSubProcessDetail.html'
    context_object_name = 'subprocess'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Sub Procesos'), 'url': reverse(
                'subprocess:ga_sub_process_list')},
            {'title': self.object.name}
        ]
        context['page_title'] = f"{_('Sub Proceso')} : {self.object.name}"
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('subprocess:ga_sub_process_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]

        return context


@method_decorator([login_required, ], name='dispatch')
class GaSubProcessCreateView(CreateView):
    form_class = SubProcessCreateForm
    model = SubProcess
    template_name = 'subprocess/GaSubProcessCreate.html'

    def get_initial(self):
        if 'process' in self.kwargs:
            process = get_object_or_404(
                Process, pk=self.kwargs.get('process')
            )
            return {
                'process': process
            }
        else:
            return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Sub Procesos'), 'url': reverse(
                'subprocess:ga_sub_process_list')},
            {'title': _('Nuevo'), 'url': reverse(
                'subprocess:ga_sub_process_create')},
        ]
        context['page_title'] = _('Nuevo Sub Proceso')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Sub PRoceso creado correctamente')
        )
        return reverse_lazy(
            'subprocess:ga_sub_process_list'
        )


@method_decorator([login_required, ], name='dispatch')
class GaSubProcessUpdateView(UpdateView):
    form_class = SubProcessCreateForm
    model = SubProcess
    template_name = 'subprocess/GaSubProcessCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Sub Procesos'), 'url': reverse(
                'subprocess:ga_sub_process_list')},
            {'title': _('Editar')},
        ]
        context['page_title'] = _('Editar Sub Proceso')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Sub Proceso actualizado correctamente')
        )
        return reverse_lazy(
            'subprocess:ga_sub_process_list'
        )


@method_decorator([login_required, ], name='dispatch')
class GaSubProcessDeleteView(DeleteView):
    model = SubProcess
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Sub Procesos'), 'url': reverse(
                'subprocess:ga_sub_process_list')},
            {'title': _('Eliminar')},
        ]
        context['page_title'] = _(
            "Eliminar Sub Proceso: %s") % str(self.object.name)
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Sub Proceso eliminado correctamente")
        )
        return reverse_lazy("subprocess:ga_sub_process_list")

    def get_confirm_text_message(self):
        return _(
            '<span class="kt-font-bold">¿Seguro que desea eliminar el Sub Proceso: </span> {0} {1}? <span class="kt-font-bold">Se borrarán todos los datos asociados al mismo.</span>'
        ).format(str(self.object.ref), self.object.name)
