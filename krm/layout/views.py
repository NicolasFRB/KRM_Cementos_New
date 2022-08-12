from django.shortcuts import render

from django.views.generic import (
    FormView,
    TemplateView,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.configuration.forms import ConfigurationUpdateForm
from krm.configuration.models import Configuration

# class HomeView(TemplateView):
#     # template_name = "pages/dashboards/dashboard-1.html"
#     template_name = "home.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context = KTLayout.init(context)
#         KTTheme.addVendors([])
#         return context


@method_decorator([login_required, ], name='dispatch')
class DomainUpdate(UpdateView):
    form_class = ConfigurationUpdateForm
    model = Configuration
    template_name = 'configuration/ConfigurationUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addVendors([])
        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Dominio de riesgo actualizado correctamente')
        )
        return reverse_lazy(
            'users:dashboard'
        )
