import requests
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

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme


class HomeView(TemplateView):
    # template_name = "pages/dashboards/dashboard-1.html"
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        """
        # Example to get page name. Refer to dashboards/urls.py file.
        url_name = resolve(self.request.path_info).url_name

        if url_name == 'dashboard-2':
            # Example to override settings at the runtime
            settings.KT_THEME_DIRECTION = 'rtl'
        else:
            settings.KT_THEME_DIRECTION = 'ltr'
        """

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # Include vendors and javascript files for dashboard widgets
        KTTheme.addVendors([])

        return context
