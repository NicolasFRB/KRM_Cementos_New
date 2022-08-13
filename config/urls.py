"""Main URLs module."""

from django.conf import settings
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path('admin/', admin.site.urls),

    # path('',
    #      include(('krm.layout.urls', 'layout'),
    #              namespace='layout')
    #      ),
    path('',
         include(('krm.users.urls', 'users'),
                 namespace='users')
         ),
    path('',
         include(('krm.configuration.urls', 'configuration'),
                 namespace='configuration')
         ),
    path('domain-risks/',
         include(('krm.risks.urls.domain_risk_urls', 'domain_risks'),
                 namespace='domain_risks')
         ),
    path('risk-masters/',
         include(('krm.risks.urls.risk_master_urls', 'risk_masters'),
                 namespace='risk_masters')
         ),
]


if 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]


admin.site.index_title = _('KRM TOOL')
admin.site.site_header = _('KRM TOOL')
admin.site.site_title = _('KRM TOOL')
