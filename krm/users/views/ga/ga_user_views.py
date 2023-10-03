from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from django.contrib import messages
# import pandas as pd

from django.views.generic import (
    FormView,
    TemplateView,
    ListView,
    RedirectView
)

from django.contrib.auth.decorators import login_required

from krm.users.decorators import (
    is_company_admin,
    is_global_admin
)

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.users.forms import LoginForm, RememberForm, PasswordForm, LoginCodeForm
from krm.users.models import User

decorators = [
    csrf_protect,
    never_cache,
]


@method_decorator([login_required, is_global_admin], name='dispatch')
class GaDashboardView(TemplateView):
    template_name = 'dashboards/ga/GaDashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:ga_dashboard')},
        ]
        context['page_title'] = _(
            'Dashboard para el Administrador Global')
        context['breadcrums'] = breadcrums
        # df = pd.DataFrame(
        #     [{'tipo': 'Autopista', 'info': 'Third-party screening and due diligence', 'ref': 'USA-R07', 'x': 4.0, 'y': 3.0}, {'tipo': 'Autopista', 'info': 'Liability arising from employees ', 'ref': 'USA-R05', 'x': 3.0, 'y': 3.0}, {'tipo': 'Autopista', 'info': 'Financiación ilegal de partidos políticos', 'ref': 'GRU-R11', 'x': 3.2, 'y': 2.0}, {'tipo': 'Autopista', 'info': 'Malversación', 'ref': 'GRU-R28', 'x': 2.7, 'y': 2.3}, {'tipo': 'Autopista', 'info': 'Corrupción en los negocios', 'ref': 'GRU-R02', 'x': 3.1, 'y': 1.9}, {'tipo': 'Corporación', 'info': 'Cohecho', 'ref': 'GRU-R01', 'x': 4.0, 'y': 3.0}, {'tipo': 'Corporación', 'info': 'Tráfico de Influencias', 'ref': 'GRU-R03', 'x': 4.0, 'y': 3.0}, {'tipo': 'Corporación', 'info': 'Estafa', 'ref': 'GRU-R05', 'x': 4.0, 'y': 3.0}, {'tipo': 'Corporación', 'info': 'Malversación', 'ref': 'GRU-R28', 'x': 4.0, 'y': 3.0}, {'tipo': 'Corporación', 'info': 'Mercado y Consumidores', 'ref': 'GRU-R07', 'x': 4.0, 'y': 2.0}, {'tipo': 'Corporación', 'info': 'Financiación ilegal de partidos políticos', 'ref': 'GRU-R11', 'x': 4.0, 'y': 2.0}, {'tipo': 'Corporación', 'info': 'Corrupción en los negocios', 'ref': 'GRU-R02', 'x': 2.5, 'y': 2.5}, {'tipo': 'Corporación', 'info': 'Descubrimiento y revelación de secretos', 'ref': 'GRU-R04', 'x': 2.0, 'y': 3.0}, {'tipo': 'Ferrocarril', 'info': 'Falsificación de tarjetas de crédito, débito y cheques de viaje', 'ref': 'GRU-R14', 'x': 4.0, 'y': 4.0}, {'tipo': 'Ferrocarril', 'info': 'Cohecho', 'ref': 'GRU-R01', 'x': 4.0, 'y': 3.0}, {'tipo': 'Ferrocarril', 'info': 'Tráfico de Influencias', 'ref': 'GRU-R03', 'x': 4.0, 'y': 3.0}, {'tipo': 'Ferrocarril', 'info': 'Financiación ilegal de partidos políticos', 'ref': 'GRU-R11', 'x': 4.0, 'y': 3.0}, {'tipo': 'Ferrocarril', 'info': 'Malversación', 'ref': 'GRU-R28', 'x': 4.0, 'y': 3.0}, {'tipo': 'Innovación', 'info': 'Propiedad Industrial e Intelectual', 'ref': 'GRU-R18', 'x': 3.7, 'y': 3.0}, {'tipo': 'Innovación', 'info': 'Corrupción en los negocios', 'ref': 'GRU-R02', 'x': 3.8, 'y': 2.5}, {'tipo': 'Innovación', 'info': 'Liability arising from employees ', 'ref': 'USA-R05', 'x': 3.0, 'y': 3.0}, {'tipo': 'Innovación', 'info': 'Descubrimiento y revelación de secretos', 'ref': 'GRU-R04', 'x': 3.4, 'y': 2.6}, {'tipo': 'Innovación', 'info': 'Blanqueo de capitales', 'ref': 'GRU-R10', 'x': 3.8, 'y': 2.2}]
        # )
        # df['severidad'] = df['x']*df['y']
        # df = df.sort_values('severidad', ascending=False)
        # context['df'] = df
        context['js_template'] = ['js/custom/datatables.js']

        return context
