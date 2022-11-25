from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page

from krm.questionnaires.views import (
    GaEvaluationQuestionnaireListView,
    GaEvaluationQuestionnaireCreateView,
    GaEvaluationQuestionnaireDetailView,
    # GaEvaluationQuestionnaireDeleteView,
    # GaEvaluationQuestionnaireUpdateView,
    # GaEvaluationQuestionnaireCreateView
    RuEvaluationQuestionnaireCompleteView,
    RuEvaluationQuestionnaireListView
)


urlpatterns = [

    path(
        '',
        GaEvaluationQuestionnaireListView.as_view(),
        name='ga_evaluation_questionnaire_list'
    ),
    path(
        'detail/<pk>/',
        GaEvaluationQuestionnaireDetailView.as_view(),
        name='ga_evaluation_questionnaire_detail'
    ),
    # path(
    #     'delete/<pk>/',
    #     GaEvaluationQuestionnaireDeleteView.as_view(),
    #     name='ga_evaluation_questionnaire_delete'
    # ),
    # path(
    #     'update/<pk>/',
    #     GaEvaluationQuestionnaireUpdateView.as_view(),
    #     name='ga_evaluation_questionnaire_update'
    # ),
    path(
        'create/',
        GaEvaluationQuestionnaireCreateView.as_view(),
        name='ga_evaluation_questionnaire_create'
    ),

    path(
        'ru/',
        RuEvaluationQuestionnaireListView.as_view(),
        name='ru_evaluation_questionnaire_list'
    ),
    path(
        'ru/complete/<pk>/',
        RuEvaluationQuestionnaireCompleteView.as_view(),
        name='ru_evaluation_questionnaire_complete'
    ),

]
