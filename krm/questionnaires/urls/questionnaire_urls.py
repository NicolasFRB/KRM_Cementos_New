from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page

from krm.questionnaires.views import (
    GaQuestionnaireListView,
    GaQuestionnaireDetailView,
    GaQuestionnaireDeleteView,
    GaQuestionnaireUpdateView,
    GaQuestionnaireCreateView,
)


urlpatterns = [
    path(
        '',
        GaQuestionnaireListView.as_view(),
        name='ga_questionnaire_list'
    ),
    path(
        'detail/<pk>/',
        GaQuestionnaireDetailView.as_view(),
        name='ga_questionnaire_detail'
    ),
    path(
        'delete/<pk>/',
        GaQuestionnaireDeleteView.as_view(),
        name='ga_questionnaire_delete'
    ),
    path(
        'update/<pk>/',
        GaQuestionnaireUpdateView.as_view(),
        name='ga_questionnaire_update'
    ),
    path(
        'create/',
        GaQuestionnaireCreateView.as_view(),
        name='ga_questionnaire_create'
    ),

]
