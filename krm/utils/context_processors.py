from django.urls import reverse_lazy

from django.conf import settings
from krm.configuration.models import Configuration


def get_menu_urls(request, pk=None):
    if 'pk' in request.resolver_match.kwargs:
        pk = request.resolver_match.kwargs['pk']
    domain_risks_urls = [
        reverse_lazy('domain_risks:ga_domain_risk_list'),
        reverse_lazy('domain_risks:ga_domain_risk_create'),
    ]
    risks_masters_urls = [
        reverse_lazy('risks_masters:ga_risk_master_list'),
        reverse_lazy('risks_masters:ga_risk_master_create'),
    ]
    risks_urls = [
        reverse_lazy('risks:ga_risk_list'),
        reverse_lazy('risks:ga_risk_create'),
    ]
    controls_urls = [
        reverse_lazy('controls:ga_control_list'),
        reverse_lazy('controls:ga_control_create'),
    ]
    companies_urls = [
        reverse_lazy('companies:ga_company_list'),
        reverse_lazy('companies:ga_company_create'),
        reverse_lazy('companies:ca_company_list')
    ]
    users_urls = [
        reverse_lazy('users:ga_user_list'),
        reverse_lazy('users:ga_user_create'),
    ]
    process_urls = [
        reverse_lazy('process:ga_process_list'),
        reverse_lazy('process:ga_process_create'),
    ]
    sub_process_urls = [
        reverse_lazy('subprocess:ga_sub_process_list'),
        reverse_lazy('subprocess:ga_sub_process_create'),
    ]
    evaluations_urls = [
        reverse_lazy('evaluations:ga_evaluation_list'),
        reverse_lazy('evaluations:ga_evaluation_create'),
    ]
    evaluations_krm_urls = [
        reverse_lazy('evaluations_krm:ga_evaluation_inherent_list'),
        reverse_lazy('evaluations_krm:ga_evaluation_inherent_create'),
        reverse_lazy('evaluations_krm:ga_evaluation_residual_list'),
        reverse_lazy('evaluations_krm:ga_evaluation_residual_create'),
    ]
    ca_evaluations_urls = [
        reverse_lazy('evaluations:ca_evaluation_list'),
        reverse_lazy('evaluations:ca_evaluation_create'),
    ]
    ca_evaluations_krm_urls = [
        reverse_lazy('evaluations_krm:ca_evaluation_inherent_list'),
        reverse_lazy('evaluations_krm:ca_evaluation_inherent_create'),
        reverse_lazy('evaluations_krm:ca_evaluation_residual_list'),
        reverse_lazy('evaluations_krm:ca_evaluation_residual_create'),
    ]

    questionnaires_urls = [
        reverse_lazy('questionnaires:ga_questionnaire_list'),
        reverse_lazy('questionnaires:ga_questionnaire_create'),
        reverse_lazy('questionnaires:ga_questionnaire_import'),
    ]

    questions_urls = [
        reverse_lazy('questions:ga_question_list'),
    ]

    evaluation_questionnaires_urls = [
        reverse_lazy(
            'evaluation_questionnaires:ga_evaluation_questionnaire_create'),
        reverse_lazy(
            'evaluation_questionnaires:ga_evaluation_questionnaire_list'),
    ]

    if pk is not None:
        domain_risks_urls = domain_risks_urls + [
            reverse_lazy(
                'domain_risks:ga_domain_risk_detail',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'domain_risks:ga_domain_risk_update',
                kwargs={'pk': pk}
            )
        ]
        # urls['domain_risk'].append(
        #     reverse_lazy(
        #         'domain_risks:ga_domain_risk_delete',
        #         kwargs={'pk': pk}
        #     )
        # )
        risks_urls = risks_urls + [
            reverse_lazy(
                'risks:ga_risk_detail',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'risks:ga_risk_update',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'risks:ga_risk_delete',
                kwargs={'pk': pk}
            )
        ]
        risks_masters_urls = risks_masters_urls + [
            reverse_lazy(
                'risks_masters:ga_risk_master_detail',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'risks_masters:ga_risk_master_update',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'risks_masters:ga_risk_master_delete',
                kwargs={'pk': pk}
            )
        ]
        controls_urls = controls_urls + [
            reverse_lazy(
                'controls:ga_control_detail',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'controls:ga_control_update',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'controls:ga_control_delete',
                kwargs={'pk': pk}
            )
        ]
        companies_urls = companies_urls + [
            reverse_lazy(
                'companies:ga_company_detail',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'companies:ga_company_update',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'companies:ga_company_delete',
                kwargs={'pk': pk}
            )
        ]
        users_urls = users_urls + [
            reverse_lazy(
                'users:ga_user_detail',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'users:ga_user_update',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'users:ga_user_delete',
                kwargs={'pk': pk}
            )
        ]
        process_urls = process_urls + [
            reverse_lazy(
                'process:ga_process_detail',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'process:ga_process_update',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'process:ga_process_delete',
                kwargs={'pk': pk}
            )
        ]
        sub_process_urls = sub_process_urls + [
            reverse_lazy(
                'subprocess:ga_sub_process_detail',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'subprocess:ga_sub_process_update',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'subprocess:ga_sub_process_delete',
                kwargs={'pk': pk}
            )
        ]
        evaluations_urls = evaluations_urls + [
            reverse_lazy(
                'evaluations:ga_evaluation_detail',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'evaluations:ga_evaluation_update',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'evaluations:ga_evaluation_delete',
                kwargs={'pk': pk}
            )
        ]
        ca_evaluations_urls = ca_evaluations_urls + [
            reverse_lazy(
                'evaluations:ca_evaluation_detail',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'evaluations:ca_evaluation_update',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'evaluations:ca_evaluation_delete',
                kwargs={'pk': pk}
            )
        ]

        evaluations_krm_urls = evaluations_krm_urls + [
            reverse_lazy(
                'evaluations_krm:ga_evaluation_krm_inherent_detail',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'evaluations_krm:ga_evaluation_krm_residual_detail',
                kwargs={'pk': pk}
            ),
        ]

        evaluation_questionnaires_urls = evaluation_questionnaires_urls + [
            reverse_lazy(
                'evaluation_questionnaires:ga_evaluation_questionnaire_detail',
                kwargs={'pk': pk}
            ),
        ]

        questionnaires_urls = questionnaires_urls + [
            reverse_lazy(
                'questionnaires:ga_questionnaire_detail',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'questionnaires:ga_questionnaire_update',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'questionnaires:ga_questionnaire_delete',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'scopes:ga_scope_detail',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'scopes:ga_scope_update',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'scopes:ga_scope_delete',
                kwargs={'pk': pk}
            )
        ]

        questions_urls = questions_urls + [
            reverse_lazy(
                'questions:ga_question_detail',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'questions:ga_question_update',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'questions:ga_question_delete',
                kwargs={'pk': pk}
            )
        ]

    if settings.KRM_ACTIVATE:
        KRM_ACTIVATE = True
    else:
        KRM_ACTIVATE = False

    return {
        'RISKS_MASTERS_URLS': risks_masters_urls,
        'RISKS_URLS': risks_urls,
        'DOMAIN_RISKS_URLS': domain_risks_urls,
        'CONTROLS_URLS': controls_urls,
        'COMPANIES_URLS': companies_urls,
        'USERS_URLS': users_urls,
        'PROCESS_URLS': process_urls,
        'SUBPROCESS_URLS': sub_process_urls,
        'EVALUATIONS_URLS': evaluations_urls,
        'EVALUATIONS_KRM_URLS': evaluations_krm_urls,
        'CA_EVALUATIONS_KRM_URLS': ca_evaluations_krm_urls,
        'CA_EVALUATIONS_URLS': ca_evaluations_urls,
        'KRM_ACTIVATE': KRM_ACTIVATE,
        'DEV': settings.DEV,
        'DEVJS': settings.DEVJS,
        'BRAND': settings.BRAND,
        'QUESTIONNAIRES_URLS': questionnaires_urls,
        'QUESTIONS_URLS': questions_urls,
        'EVALUATIONS_QUESTIONNAIRES_URLS': evaluation_questionnaires_urls,
        'CONFIGURATION': Configuration.objects.get(pk=1)
    }
