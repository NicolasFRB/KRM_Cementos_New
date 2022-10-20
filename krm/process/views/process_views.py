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

from krm.process.forms import ProcessCreateForm
from krm.process.models import Process

from krm.users.decorators import is_global_admin
from django.contrib.auth.decorators import login_required
from django.db.models import Count


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaProcessListView(ListView):
    model = Process
    template_name = 'process/GaProcessList.html'
    context_object_name = 'processes'
    queryset = Process.objects.all().prefetch_related('sub_processes__controls').all().annotate(n_sub_processes=Count('sub_processes', distinct=True), n_controls=Count('sub_processes__controls', distinct=True))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Procesos'), 'url': reverse(
                'process:ga_process_list')},
        ]
        context['page_title'] = _('Procesos')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('process:ga_process_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaProcessDetailView(DetailView):
    model = Process
    template_name = 'process/GaProcessDetail.html'
    context_object_name = 'process'
    # queryset = Process.objects.all().prefetch_related('sub_processes__controls').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Procesos'), 'url': reverse(
                'process:ga_process_list')},
            {'title': self.object.ref}
        ]
        context['page_title'] = f"{_('Proceso')} : {self.object.name}"
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('process:ga_process_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaProcessCreateView(CreateView):
    form_class = ProcessCreateForm
    model = Process
    template_name = 'process/GaProcessCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Procesos'), 'url': reverse(
                'process:ga_process_list')},
            {'title': _('Nuevo Proceso'), 'url': reverse(
                'process:ga_process_create')},
        ]
        context['page_title'] = _('Nuevo Proceso')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Proceso creado correctamente')
        )
        return reverse_lazy(
            'process:ga_process_list'
        )


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaProcessUpdateView(UpdateView):
    form_class = ProcessCreateForm
    model = Process
    template_name = 'process/GaProcessCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Procesos'), 'url': reverse(
                'process:ga_process_list')},
            {'title': _('Editar')},
        ]
        context['page_title'] = _('Editar Proceso')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Proceso actualizado correctamente')
        )
        return reverse_lazy(
            'process:ga_process_list'
        )


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaProcessDeleteView(DeleteView):
    model = Process
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Procesos'), 'url': reverse(
                'process:ga_process_list')},
            {'title': _('Eliminar')},
        ]
        context['page_title'] = _("Eliminar Proceso")
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Proceso eliminado correctamente")
        )
        return reverse_lazy("process:ga_process_list")

    def get_confirm_text_message(self):
        return _(
            '<span class="kt-font-bold">¿Seguro que desea eliminar el Proceso y todas sus evaluaciónes?: </span> {0}? <span class="kt-font-bold">Se borrarán todos los datos asociados al mismo.</span>'
        ).format(str(self.object))
