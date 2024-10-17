from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page

from krm.questionnaires.views import (
    GaQuestionListView,
    GaQuestionCreateView,
    GaQuestionDetailView,
    GaQuestionDeleteView,
    GaQuestionUpdateView,
    GaQuestionCreateView
)


urlpatterns = [

    path(
        '',
        GaQuestionListView.as_view(),
        name='ga_question_list'
    ),
    path(
        'detail/<pk>/',
        GaQuestionDetailView.as_view(),
        name='ga_question_detail'
    ),
    path(
        'delete/<pk>/',
        GaQuestionDeleteView.as_view(),
        name='ga_question_delete'
    ),
    path(
        'update/<pk>/',
        GaQuestionUpdateView.as_view(),
        name='ga_question_update'
    ),
    path(
        'create/<questionnaire>/',
        GaQuestionCreateView.as_view(),
        name='ga_question_create'
    ),
    path(
        'create/',
        GaQuestionCreateView.as_view(),
        name='ga_question_create'
    ),

]
