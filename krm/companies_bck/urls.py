# -*- encoding: utf-8 -*-

"""Users urls."""

from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from krc.business_group.views.ga.business_group import (
    BusinessGroupCreate,
    BusinessGroupUpdate,
    BusinessGroupList,
    BusinessGroupDetail,
    BusinessGroupDelete,
    BusinessGroupCompanyCreate,
    BusinessGroupCompanyDetail,
    BusinessGroupCompanyUpdate,
    BusinessGroupCompanyDelete,
    BusinessGroupCompanyImport
)

from krc.business_group.views.age.business_group import (
    BusinessGroupDetailAge,
    BusinessGroupUpdateAge,
    BusinessGroupCompanyCreateAge,
    BusinessGroupCompanyDetailAge,
    BusinessGroupCompanyImportAge,
    BusinessGroupCompanyUpdateAge,
    BusinessGroupCompanyDeleteAge
)

from krc.users.views import UserCompanyCreate

from krc.users.views import (
    UserCompanyCreate,
    UserCompanyDetail,
    UserCompanyImport
)

urlpatterns = [

    path(
        'ga/business-groups/',
        BusinessGroupList.as_view(),
        name='ga_business_group_list'
    ),

    path(
        'ga/business-groups/create/',
        BusinessGroupCreate.as_view(),
        name='ga_business_group_create'
    ),

    path(
        'ga/business-groups/<pk>/detail/',
        BusinessGroupDetail.as_view(),
        name='ga_business_group_detail'
    ),

    path(
        'ga/business-groups/<pk>/detail/<str:tab>/',
        BusinessGroupDetail.as_view(),
        name='ga_business_group_detail'
    ),

    path(
        'ga/business-groups/<pk>/company/create/',
        BusinessGroupCompanyCreate.as_view(),
        name='ga_business_group_company_create'
    ),

    path(
        'ga/business-groups/<pk>/company/import/',
        BusinessGroupCompanyImport.as_view(),
        name='ga_business_group_company_import'
    ),

    path(
        'ga/companies/<pk>/detail/',
        BusinessGroupCompanyDetail.as_view(),
        name='ga_business_group_company_detail'
    ),

    path(
        'ga/companies/<pk>/update/',
        BusinessGroupCompanyUpdate.as_view(),
        name='ga_business_group_company_update'
    ),

    path(
        'ga/companies/<pk>/delete/',
        BusinessGroupCompanyDelete.as_view(),
        name='ga_business_group_company_delete'
    ),

    path(
        'ga/companies/<pk>/detail/new-user/',
        UserCompanyCreate.as_view(),
        name='ga_company_user_create'
    ),

    path(
        'ga/companies/<pk>/detail/<str:tab>/',
        BusinessGroupCompanyDetail.as_view(),
        name='ga_business_group_company_detail'
    ),

    path(
        'ga/companies/<pk>/import-users/',
        UserCompanyImport.as_view(),
        name='ga_company_user_import'
    ),

    path(
        'ga/business-groups/<pk>/update/',
        BusinessGroupUpdate.as_view(),
        name='ga_business_group_update'
    ),

    path(
        'ga/business-groups/<pk>/delete/',
        BusinessGroupDelete.as_view(),
        name='ga_business_group_delete'
    )

]

urlpatterns += [

    path(
        'age/business-groups/detail/',
        BusinessGroupDetailAge.as_view(),
        name='age_business_group_detail'
    ),

    path(
        'age/business-group/update/',
        BusinessGroupUpdateAge.as_view(),
        name='age_business_group_update'
    ),

    path(
        'age/business-group/detail/<str:tab>/',
        BusinessGroupDetailAge.as_view(),
        name='age_business_group_detail'
    ),

    path(
        'age/business-group/company/create/',
        BusinessGroupCompanyCreateAge.as_view(),
        name='age_business_group_company_create'
    ),

    path(
        'age/business-group/company/import/',
        BusinessGroupCompanyImportAge.as_view(),
        name='age_business_group_company_import'
    ),

    path(
        'age/business-group/company/<pk>/detail/',
        BusinessGroupCompanyDetailAge.as_view(),
        name='age_business_group_company_detail'
    ),

    path(
        'age/business-group/company/<pk>/detail/<str:tab>/',
        BusinessGroupCompanyDetailAge.as_view(),
        name='age_business_group_company_detail'
    ),

    path(
        'age/business-group/company/<pk>/update/',
        BusinessGroupCompanyUpdateAge.as_view(),
        name='age_business_group_company_update'
    ),

    path(
        'age/business-group/company/<pk>/delete/',
        BusinessGroupCompanyDeleteAge.as_view(),
        name='age_business_group_company_delete'
    ),

]
