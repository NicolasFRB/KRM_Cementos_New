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
            # reverse_lazy(
            #     'risk_masters:ga_risk_master_delete',
            #     kwargs={'pk': pk}
            # )
        ]
    return {
        'RISKS_URLS': risks_urls,
        'DOMAIN_RISKS_URLS': domain_risks_urls,
        'RISKS_MASTER_URLS': risk_masters_urls,
    }
