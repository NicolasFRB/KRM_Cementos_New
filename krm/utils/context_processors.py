from django.urls import reverse_lazy


def get_menu_urls(request, pk=None):
    if 'pk' in request.resolver_match.kwargs:
        pk = request.resolver_match.kwargs['pk']
    domain_risks_urls = [
        reverse_lazy('domain_risks:ga_domain_risk_list'),
        reverse_lazy('domain_risks:ga_domain_risk_create'),
    ]
    risks_urls = [
        reverse_lazy('risks:ga_risk_list'),
        reverse_lazy('risks:ga_risk_create'),
    ]
    risk_masters_urls = [
        reverse_lazy('risk_masters:ga_risk_master_list'),
        reverse_lazy('risk_masters:ga_risk_master_list'),
    ]
    controls_urls = [
        reverse_lazy('controls:ga_control_list'),
        reverse_lazy('controls:ga_control_create'),
    ]
    companies_urls = [
        reverse_lazy('companies:ga_company_list'),
        reverse_lazy('companies:ga_company_create'),
    ]
    users_urls = [
        reverse_lazy('users:ga_user_list'),
        reverse_lazy('users:ga_user_create'),
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
            )
        ]
        # urls['risks'].append(
        #     reverse_lazy(
        #         'risks:ga_risk_delete',
        #         kwargs={'pk': pk}
        #     )
        # )
        risk_masters_urls = risk_masters_urls + [
            reverse_lazy(
                'risk_masters:ga_risk_master_detail',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'risk_masters:ga_risk_master_update',
                kwargs={'pk': pk}
            ),
            reverse_lazy(
                'risk_masters:ga_risk_master_delete',
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
    return {
        'RISKS_URLS': risks_urls,
        'DOMAIN_RISKS_URLS': domain_risks_urls,
        'RISKS_MASTER_URLS': risk_masters_urls,
        'CONTROLS_URLS': controls_urls,
        'COMPANIES_URLS': companies_urls,
        'USERS_URLS': users_urls,
    }
