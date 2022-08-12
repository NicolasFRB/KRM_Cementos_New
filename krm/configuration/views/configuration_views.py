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

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.configuration.forms import ConfigurationUpdateForm
from krm.configuration.models import Configuration


@method_decorator([login_required, ], name='dispatch')
class ConfigurationDetailView(DetailView):
    model = Configuration
    template_name = 'configuration/ConfigurationDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Configuración'), 'url': reverse(
                'configuration:configuration_detail')},
        ]
        context['page_title'] = _('Configuración Global')
        context['breadcrums'] = breadcrums
        return context

    def get_object(self):
        return Configuration.objects.first()


@method_decorator([login_required, ], name='dispatch')
class ConfigurationUpdateView(UpdateView):
    form_class = ConfigurationUpdateForm
    model = Configuration
    template_name = 'configuration/ConfigurationUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Configuración'), 'url': reverse(
                'configuration:configuration_detail')},
            {'title': _('Editar'), 'url': reverse(
                'configuration:configuration_update')},
        ]
        context['page_title'] = _('Editar Configuración Global')
        context['breadcrums'] = breadcrums
        return context

    def get_object(self):
        return Configuration.objects.first()

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Configuración actualizada correctamente')
        )
        return reverse_lazy(
            'configuration:configuration_detail'
        )
