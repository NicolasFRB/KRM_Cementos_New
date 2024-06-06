from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.evaluations.views import (
    ControlTestAssign,
    ControlTestDetail,
    ControlTestUpdate,
    RuControlTestSupervisorList,
    RuControlTestOwnerList,
    RuControlTestDetail,
    RuRemediationPlanCreate,
    RuRemediationPlanUpdate,

    CaControlTestAssign,
    CaControlTestAdministratorList,
    CaControlTestDetail,

    AuControlTestDetail,

    delete_attachment
)

urlpatterns = [
    path(
        "<pk>/assign/",
        ControlTestAssign.as_view(),
        name="control_test_assign",
    ),

    path(
        "<pk>/detail/",
        ControlTestDetail.as_view(),
        name="control_test_detail",
    ),

    path(
        "<pk>/update/",
        ControlTestUpdate.as_view(),
        name="control_test_update",
    ),

    path(
        "ru/control-test-owner/list/",
        RuControlTestOwnerList.as_view(),
        name="ru_control_test_owner_list",
    ),

    path(
        "ru/control-test-supervisor/list/",
        RuControlTestSupervisorList.as_view(),
        name="ru_control_test_supervisor_list",
    ),

    path(
        "ru/control-test-detail/<pk>/",
        RuControlTestDetail.as_view(),
        name="ru_control_test_detail",
    ),

    path(
        "ru/control-test-detail/<pk>/create-remediation-plan/",
        RuRemediationPlanCreate.as_view(),
        name="ru_control_test_detail_create_remediation_plan",
    ),

    path(
        "ru/control-test-detail/update-remediation-plan/<pk>/",
        RuRemediationPlanUpdate.as_view(),
        name="ru_control_test_detail_update_remediation_plan",
    ),

    path(
        "ca/<pk>/assign/",
        CaControlTestAssign.as_view(),
        name="ca_control_test_assign",
    ),

    path(
        "ca/control-test/list/",
        CaControlTestAdministratorList.as_view(),
        name="ca_control_test_administrator_list",
    ),

    path(
        "ca/<pk>/detail/",
        CaControlTestDetail.as_view(),
        name="ca_control_test_detail",
    ),

    path(
        "au/<pk>/detail/",
        AuControlTestDetail.as_view(),
        name="au_control_test_detail",
    ),

    path(
        "control-test-detail/delete-attachment/<pk_answer>/<pk_attachment>/",
        delete_attachment,
        name='delete_attachment'
    )
]
