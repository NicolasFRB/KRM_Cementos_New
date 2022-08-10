"""Main URLs module."""

from django.conf import settings
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

# from krm.layout.views import get_sage_code

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',
         include(('krm.layout.urls', 'layout'),
                 namespace='layout')
         ),
    path('',
         include(('krm.users.urls', 'users'),
                 namespace='users')
         ),
    # path('companies/',
    #      include(('krm.companies.urls', 'companies'),
    #              namespace='companies')
    #      ),
    # path('customers/',
    #      include(('krm.customers.urls.customer_urls', 'customers'),
    #              namespace='customers')
    #      ),
    # path('rates/',
    #      include(('krm.customers.urls.rate_urls', 'rates'),
    #              namespace='rates')
    #      ),
    # path('sage/',
    #      include(('krm.sage.urls', 'sage'),
    #              namespace='sage')
    #      ),
]


if 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]


admin.site.index_title = _('KRM TOOL')
admin.site.site_header = _('KRM TOOL')
admin.site.site_title = _('KRM TOOL')
