
"""Main URLs module."""

from django.conf import settings
from django.urls import path, include, re_path
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from rest_framework import routers

from krm.base.healthchecks import simpleHealthCheck

from krm.users.views import (
    DashboardView,
)

from krm.controls.api import ControlViewSet
from krm.risks.api import (
    RiskViewSet,
    DomainRiskViewSet
)
from krm.process.api import (
    ProcessViewSet,
    SubProcessViewSet,
)

from krm.risks.api.views import (
    RiskCompanyApiView,
    RiskCompanyResidualApiView,
    DomainRiskCompanyApiView,
    RiskDomainRiskApiView,
    RiskCompanyExpertApiView
)

from krm.controls.api.views import ControlCompanyApiView, ControlPeriodicityApiView, ControlScopesApiView

from krm.companies.api import (
    CompanyViewSet,
)

from krm.evaluations_krm.api import (
    RiskTestInherentExpertApiView,
    RiskTestResidualEvaluatorApiView,
    RiskCompanyResidualAdminApiView
)

from krm.questionnaires.api import (
    QuestionnaireViewSet,
    QuestionViewSet,
    QuestionTestApiView,
    ScopeViewSet,
)

from krm.users.api import (
    UserViewSet,
)

from krm.configuration.models import Configuration


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'controls', ControlViewSet)
router.register(r'risks', RiskViewSet)
router.register(r'process', ProcessViewSet)
router.register(r'subprocesses', SubProcessViewSet)
router.register(r'domain-risks', DomainRiskViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'questionnaires', QuestionnaireViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'scopes', ScopeViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
     # path(r'ht/', include('health_check.urls')),
     path('liveness-probe/', simpleHealthCheck),
     path('startup-probe/', simpleHealthCheck),

     path('i18n/', include('django.conf.urls.i18n')),
     path('api/', include(router.urls)),
     path('api-auth/', include('rest_framework.urls')),
     path('api/riskscompany/',
          RiskCompanyApiView.as_view()),
     path('api/risksdomainrisks/',
          RiskDomainRiskApiView.as_view()),
     path('api/domainriskscompany/',
          DomainRiskCompanyApiView.as_view()),
     path('api/riskscompanyresidual/',
          RiskCompanyResidualApiView.as_view()),
     path('api/risktestinherentexpert/',
          RiskTestInherentExpertApiView.as_view()
          ),
     path('api/risktestresidualevaluator/',
          RiskTestResidualEvaluatorApiView.as_view()
          ),
     path('api/riskcompanyresidualadmin/',
          RiskCompanyResidualAdminApiView.as_view()
          ),
     path('api/controlscompany/',
          ControlCompanyApiView.as_view()),
     path('api/questiontest/',
          QuestionTestApiView.as_view()),
     path('api/riskcompanyexperts/',
          RiskCompanyExpertApiView.as_view()),
]

urlpatterns += i18n_patterns(
     path('api/controlScopes/',
          ControlScopesApiView.as_view()),
    path('api/controlperiodicity/',
         ControlPeriodicityApiView.as_view()),
    path(
        '',
        DashboardView.as_view(),
        name='dashboard'
    ),

    path('admin/', admin.site.urls),

    path('auth/',
         include(('krm.users.urls.user_auth_urls', 'users'),
                 namespace='auth')
         ),
    path('users/',
         include(('krm.users.urls.user_urls', 'users'),
                 namespace='users')
         ),
    path('config/',
         include(('krm.configuration.urls', 'configuration'),
                 namespace='configuration')
         ),
    path('domain-risks/',
         include(('krm.risks.urls.domain_risk_urls', 'domain_risks'),
                 namespace='domain_risks')
         ),
    path('risks/',
         include(('krm.risks.urls.risk_urls', 'risks'),
                 namespace='risks')
         ),
    path('risks-masters/',
         include(('krm.risks.urls.risk_master_urls', 'risks_masters'),
                 namespace='risks_masters')
         ),
    path('risks-company/',
         include(('krm.risks.urls.risk_company_urls', 'risks_company'),
                 namespace='risks_company')
         ),
    path('controls/',
         include(('krm.controls.urls.control_urls', 'controls'),
                 namespace='controls')
         ),
    path('companies/',
         include(('krm.companies.urls.company_urls', 'companies'),
                 namespace='companies')
         ),
    path('process/',
         include(('krm.process.urls.process_urls', 'process'),
                 namespace='process')
         ),
    path('subprocess/',
         include(('krm.process.urls.sub_process_urls', 'subprocess'),
                 namespace='subprocess')
         ),
    path('evaluations/',
         include(('krm.evaluations.urls.evaluations_urls', 'evaluations'),
                 namespace='evaluations')
         ),
    path('evaluations/control-test/',
         include(('krm.evaluations.urls.control_test_urls', 'control_tests'),
                 namespace='control_tests')
         ),
    path('evaluations/krm/',
         include(('krm.evaluations_krm.urls.evaluation_krm_urls', 'evaluations_krm'),
                 namespace='evaluations_krm')
         ),
    path('remediation-plans/',
         include(('krm.remediation_plans.remediation_plan_urls', 'remediation_plans'),
                 namespace='remediation_plans')
         ),
    path('questionnaires/',
         include(('krm.questionnaires.urls.questionnaire_urls', 'questionnaires'),
                 namespace='questionnaires')
         ),
    path('questionnaires/scopes/',
         include(('krm.questionnaires.urls.scope_urls', 'scopes'),
                 namespace='scopes')
         ),
    path('questionnaires/questions/',
         include(('krm.questionnaires.urls.question_urls', 'questions'),
                 namespace='questions')
         ),
    path('questionnaires/evaluations/',
         include(('krm.questionnaires.urls.evaluation_questionnaire_urls', 'evaluation_questionnaires'),
                 namespace='evaluation_questionnaires')
         ),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if 'debug_toolbar' in settings.INSTALLED_APPS and settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('rosetta/', include('rosetta.urls'))
    ]

admin.site.index_title = "Compliance Tool"
admin.site.site_header = "Compliance Tool"
admin.site.site_title = "Compliance Tool"
