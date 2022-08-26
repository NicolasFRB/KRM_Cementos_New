# -*- encoding: utf-8 -*-
"""Users views."""

from xlrd import open_workbook
import re

# Django
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import PermissionDenied

from django.views.generic import (
    FormView,
    TemplateView,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from krc.business_group.models import (
    BusinessGroup,
    Company
)

from krc.business_group.forms import (
    BusinessGroupCreateForm
)

from krc.business_group.forms import (
    CompanyCreateForm,
    CompanyImportForm
)

from krc.users.decorators import (
    is_business_group_admin,
    is_global_admin
)

decorators = [
    csrf_protect,
]


@method_decorator((login_required, is_global_admin), name='dispatch')
class BusinessGroupList(ListView):
    template_name = 'business_group/ga/BusinessGroupList.html'
    model = BusinessGroup


@method_decorator((login_required, is_global_admin), name='dispatch')
class BusinessGroupDetail(DetailView):
    template_name = 'business_group/ga/BusinessGroupDetail.html'
    model = BusinessGroup

    # @method_decorator(login_required)
    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.business_group_admin:
    #         return HttpResponseRedirect(reverse_lazy(
    #             'business_group:age_business_group_detail'
    #         ))

    #     return super(BusinessGroupDetail, self).dispatch(
    #         request, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(BusinessGroupDetail, self).get_context_data(**kwargs)
        if 'tab' in self.kwargs:
            context['active'] = self.kwargs.get('tab')
        else:
            context['active'] = 'tab-dashboard'

        if context['active'] == 'tab-dashboard':
            context['process_tests_status'] = self.object.get_process_tests_status_aggregate()
            context['control_tests_status'] = self.object.get_control_tests_status_aggregate()
            context['control_tests_result'] = self.object.get_control_tests_result_aggregate()
        return context


@method_decorator((login_required, is_global_admin), name='dispatch')
class BusinessGroupCreate(CreateView):
    form_class = BusinessGroupCreateForm
    model = BusinessGroup
    template_name = 'business_group/ga/BusinessGroupCreate.html'

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Grupo Empresarial añadido correctamente')
        )
        return reverse_lazy('business_group:ga_business_group_list')

    def get_title_template(self):
        return _('Nuevo Grupo Empresarial')


@method_decorator((login_required, is_global_admin), name='dispatch')
class BusinessGroupUpdate(UpdateView):
    form_class = BusinessGroupCreateForm
    model = BusinessGroup
    template_name = 'business_group/ga/BusinessGroupCreate.html'

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Grupo Empresarial modificado correctamente')
        )
        return reverse_lazy(
            'business_group:ga_business_group_detail',
            kwargs={'pk': self.object.pk}
        )

    def get_object(self, queryset=None):
        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        if queryset is None:
            queryset = self.get_queryset()
        if pk is not None:
            if self.request.user.is_global_admin:
                queryset = queryset.filter(pk=pk)
            elif self.request.user.business_group_admin:
                return self.request.user.business_group_admin
            else:
                raise Http404(_("No se ha encontrado") %
                              {'verbose_name': queryset.model._meta.verbose_name})

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404(_("No se ha encontrado") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_title_template(self):
        return _('Editar Grupo Empresarial: %s') % self.object.name


@method_decorator([login_required, is_global_admin], name='dispatch')
class BusinessGroupDelete(DeleteView):
    model = BusinessGroup
    template_name = 'layout/_base_confirm_delete.html'
    confirm_text_message = _(
        '¿Seguro que desea <span class="kt-font-bold">eliminar el Grupo Empresarial</span>? Se borrarán todos los datos asociados al mismo.')

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS,
            _('Grupo Empresarial eliminado correctamente')
        )
        return reverse_lazy(
            'business_group:ga_business_group_list'
        )

    def get_title_template(self):
        return u'Eliminar Grupo Empresarial: %s' % self.object.name

    def get_confirm_text_message(self):
        return _('¿Seguro que desea <span class="kt-font-bold">eliminar el Grupo Empresarial %s</span>? Se borrarán todos los datos asociados al mismo.') % self.object.name


@method_decorator((login_required, is_global_admin), name='dispatch')
class BusinessGroupCompanyCreate(CreateView):
    form_class = CompanyCreateForm
    model = Company
    template_name = 'business_group/ga/BusinessGroupCompanyCreate.html'

    def get_initial(self):
        if self.request.user.is_global_admin:
            business_group = get_object_or_404(BusinessGroup, pk=self.kwargs.get('pk'))
        elif self.request.user.business_group_admin:
            business_group = self.request.user.business_group_admin
        return {
            'business_group': business_group
        }

    def get_context_data(self, **kwargs):
        context = super(BusinessGroupCompanyCreate, self).get_context_data(**kwargs)
        context['business_group'] = get_object_or_404(BusinessGroup, pk=self.kwargs.get('pk'))
        context['title_template'] = _('Nueva Compañía')
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        bg = get_object_or_404(BusinessGroup, pk=self.kwargs.get('pk'))
        if request.user.is_global_admin or request.user.business_group_admin == bg:
            return super(BusinessGroupCompanyCreate, self).dispatch(
                request, request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Compañía creada correctamente')
        )
        return reverse_lazy(
            'business_group:ga_business_group_company_detail',
            kwargs={'pk': self.object.pk}
        )


@method_decorator((login_required, is_global_admin), name='dispatch')
class BusinessGroupCompanyDetail(DetailView):
    model = Company
    template_name = 'business_group/ga/BusinessGroupCompanyDetail.html'

    def get_context_data(self, **kwargs):
        context = super(BusinessGroupCompanyDetail, self).get_context_data(**kwargs)
        if 'tab' in self.kwargs:
            context['active'] = self.kwargs.get('tab')
        else:
            context['active'] = 'tab-dashboard'

        if context['active'] == 'tab-dashboard':
            context['process_tests_status'] = self.object.get_process_tests_status_aggregate()
            context['control_tests_status'] = self.object.get_control_tests_status_aggregate()
            context['control_tests_result'] = self.object.get_control_tests_result_aggregate()
        return context


@method_decorator((login_required, is_global_admin), name='dispatch')
class BusinessGroupCompanyUpdate(UpdateView):
    form_class = CompanyCreateForm
    model = Company
    template_name = 'business_group/ga/BusinessGroupCompanyUpdate.html'

    def get_context_data(self, **kwargs):
        context = super(BusinessGroupCompanyUpdate, self).get_context_data(**kwargs)
        # context['business_group'] = self.object.business_group
        context['title_template'] = _('Editar Compañía')
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Compañía modificacda correctamente')
        )
        return reverse_lazy(
            'business_group:ga_business_group_company_detail',
            kwargs={'pk': self.object.pk}
        )


@method_decorator((login_required, is_global_admin), name='dispatch')
class BusinessGroupCompanyDelete(DeleteView):
    model = Company
    template_name = 'layout/_base_confirm_delete.html'

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS,
            _('Compañía eliminada correctamente')
        )
        return reverse_lazy(
            'business_group:ga_business_group_detail',
            kwargs={'pk': self.object.business_group.pk, 'tab': 'tab-companies'}
        )

    def get_title_template(self):
        return u'Eliminar Región: %s' % self.object.name

    def get_confirm_text_message(self):
        return _('¿Seguro que desea <span class="kt-font-bold">eliminar la Región %s</span>? Se borrarán todos los datos asociados a la misma.') % self.object.name


@method_decorator((login_required, is_global_admin), name='dispatch')
class BusinessGroupCompanyImport(FormView):
    template_name = 'business_group/ga/BusinessGroupCompanyImport.html'
    form_class = CompanyImportForm

    def dispatch(self, request, *args, **kwargs):
        try:
            self.business_group = BusinessGroup.objects.get(pk=kwargs['pk'])
        except BusinessGroup.DoesNotExist:
            raise Http404
        return super(BusinessGroupCompanyImport, self).dispatch(
            request, request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super(BusinessGroupCompanyImport, self).get_context_data(
            **kwargs
        )
        context['business_group'] = self.business_group
        return context

    def form_valid(self, form):
        input_excel = self.request.FILES['companies_file']
        book = open_workbook(file_contents=input_excel.read())
        hoja = book.sheet_by_index(0)
        companies_to_create = []

        n_row = 0
        for row in range(hoja.nrows):
            if hoja.cell(row, 0).value == '':
                n_row = row
                break

        for row in range(n_row):

            if row > 1:
                company = {}
                # NOMBRE - VAT - DIRECCION - POBLACIÓN - CP - CODIGO PAIS - PAIS - EMAIL

                """
                    cell.ctype 's

                    XL_CELL_EMPTY	0	empty string ‘’
                    XL_CELL_TEXT	1	a Unicode string
                    XL_CELL_NUMBER	2	float
                    XL_CELL_DATE	3	float
                    XL_CELL_BOOLEAN	4	int; 1 means True, 0 means False
                    XL_CELL_ERROR	5	int representing internal Excel codes; for a text representation, refer to the supplied dictionary error_text_from_code
                    XL_CELL_BLANK	6	empty string ‘’. Note: this type will appear only when open_workbook(..., formatting_info= True) is used.
                """
                # Comprobamos que hay contenido en todas las celdas obligatorias
                if (hoja.cell(row, 0).value != '' and
                        hoja.cell(row, 1).value != ''):
                    company['name'] = str(hoja.cell(row, 0).value).title()
                    company['vat'] = str(hoja.cell(row, 1).value).title()
                    company['address'] = str(hoja.cell(row, 2).value)
                    company['state'] = str(hoja.cell(row, 3).value).upper()
                    cell = hoja.cell(row, 4)
                    cell_value = cell.value
                    try:
                        cell_value = int(cell_value)
                    except:
                        cell_value = None
                    company['cp'] = cell_value
                    company['country'] = str(hoja.cell(row, 5).value).upper()
                    company['email'] = str(hoja.cell(row, 7).value).lower().replace(' ', '')

                    # Tenemos que comprobar que el email esté bien formado
                    if company['email'] != '':
                        if not re.match(
                            '^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$',
                            company['email'].lower()
                        ):
                            messages.add_message(
                                self.request,
                                messages.ERROR,
                                (
                                    _(u'En la fila %s el email introducido no es correcto. Se ha abortado la importación') % str(row+1)
                                )
                            )
                            return super(
                                BusinessGroupCompanyImport,
                                self
                            ).form_invalid(form)
                            break

                    if Company.objects.filter(vat=company['vat']).count() > 0:
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _(u'El VAT introducido en la fila %s ya está registrado por otra compañía') % str(row+1)
                            )
                        )
                        return super(
                            BusinessGroupCompanyImport,
                            self
                        ).form_invalid(form)
                        break

                else:

                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(u'En la fila %s falta algún campo obligatorio. Se ha abortado la importación') % str(row+1)
                        )
                    )
                    return super(
                        BusinessGroupCompanyImport,
                        self
                    ).form_invalid(form)
                    break

                companies_to_create.append(company)

        for c in companies_to_create:
            Company.objects.create(
                name=c['name'],
                business_group=self.business_group,
                vat=c['vat'],
                address=c['address'],
                cp=c['cp'],
                email=c['email'],
                state=c['state'],
                country=c['country']
            )

        messages.add_message(
            self.request,
            messages.SUCCESS, (
                _(u'Se han importado %s compañías al grupo empresarial') % str(len(companies_to_create)))
        )

        return super(BusinessGroupCompanyImport, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'business_group:ga_business_group_detail',
            kwargs={
                'pk': self.business_group.pk,
                'tab': 'tab-companies'
            }
        )
