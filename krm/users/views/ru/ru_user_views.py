from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

from django.contrib import messages


from django.views.generic import (
    FormView,
    TemplateView,
    ListView,
    RedirectView
)

from django.contrib.auth.decorators import login_required

from krm.users.decorators import (
    is_company_admin
)

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.users.forms import LoginForm, RememberForm, PasswordForm, LoginCodeForm
from krm.users.models import User

decorators = [
    csrf_protect,
    never_cache,
]


@method_decorator([login_required, ], name='dispatch')
class RuDashboardView(TemplateView):
    template_name = 'dashboards/ru/RuDashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:ru_dashboard')},
        ]
        context['page_title'] = _(
            'Dashboard para el usuario regular')
        context['breadcrums'] = breadcrums
        return context
