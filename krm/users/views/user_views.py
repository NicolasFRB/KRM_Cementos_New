import requests
from openpyxl import load_workbook
from io import BytesIO
import re
import xlwt

from krm.configuration.forms import ImportForm

# Django
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    FormView,
)

from django.utils import translation
from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.users.models import User
from krm.companies.models import Company

from krm.users.forms.user_form import(
    UserCreateForm,
    UserUpdateForm,
    CaUserUpdateForm,
    UsersActionForm
)

from krm.users.decorators import (
    is_global_admin,
    is_company_admin,
)

from django.http import HttpResponse


@method_decorator([is_global_admin], name='dispatch')
class GaUserListView(ListView):
    template_name = 'users/GaUserList.html'
    model = User
    context_object_name = 'users'
    form_class = UsersActionForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Usuarios'), 'url': reverse(
                'users:ga_user_list')},
        ]
        context['page_title'] = _('Usuarios')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('users:ga_user_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        users = User.objects.all()

        if action == 'd':

            # Comienzo de la creacion de archivo de descarga del Test de Proceso
            filename = "download_users.xls"
            response = HttpResponse(content_type="application/ms-excel")
            response["Content-Disposition"] = 'attachment; filename="{}"'.format(
                filename
            )

            wb = xlwt.Workbook(encoding="utf-8")
            ws = wb.add_sheet("Controls")

            # Sheet header, first row
            row_num = 0

            font_style_title = xlwt.easyxf("align: vert centre, horiz left")
            font_style_title.font.bold = True

            font_style_title_wrap = xlwt.easyxf(
                "align: vert centre, horiz left, wrap yes"
            )
            font_style_title_wrap.font.bold = True

            font_style_body = xlwt.easyxf("align: vert top, horiz left")
            font_style_body_wrap = xlwt.easyxf(
                "align: vert top, horiz left, wrap yes"
            )

            date_format = xlwt.Style.XFStyle()
            date_format.num_format_str = 'DD/MM/YY'

            ws.col(0).width = 256 * 25
            ws.col(1).width = 256 * 25
            ws.col(2).width = 256 * 25
            ws.col(3).width = 256 * 25
            ws.col(4).width = 256 * 25
            ws.col(5).width = 256 * 25
            ws.col(6).width = 256 * 25
            ws.col(7).width = 256 * 25
            ws.col(8).width = 256 * 25
            ws.col(9).width = 256 * 25

            columns = [
                "NOMBRE",  # 0
                "CARGO",  # 2
                "CORREO ELECTRÓNICO",  # 3
                "ACTIVO",  # 3
                "SUPERUSUARIO",  # 3
                "ÚLTIMO INICIO DE SESIÓN",  # 4
                "ÚLTIMA ACCIÓN",  # 5
                "IDIOMA DE NOTIFICACIONES",  # 6
                "COMPAÑÍAS A LAS QUE PERTENECE",  # 7
                "COMPAÑÍAS QUE ADMINISTRA",  # 8
            ]

            for col_num in range(len(columns)):
                if col_num in (21, 28):
                    ws.write(
                        row_num, col_num, columns[col_num], font_style_title_wrap
                    )
                else:
                    ws.write(row_num, col_num,
                             columns[col_num], font_style_title)

            for u in users:
                row_num += 1
                ws.write(
                    row_num, 0, u.full_name, font_style_body
                )  # 0
                ws.write(
                    row_num, 1, u.position, font_style_body
                )  # 1
                ws.write(row_num, 2, u.email, font_style_body)  
                ws.write(row_num, 3, u.is_active, font_style_body)  
                ws.write(row_num, 4, u.is_admin, font_style_body)  
                
                last_login = u.last_login

                if last_login != None:
                    ws.write(row_num, 5, last_login.strftime("%d/%m/%Y %H:%M:%S"))
                else:
                    ws.write(row_num, 5, '', font_style_body)    
                # ws.write(row_num, 5, u.last_login, font_style_body)  
                
                last_action_log = str(u.actions_log.last())

                if last_action_log != 'None':
                    ws.write(row_num, 6, last_action_log, font_style_body)
                else:
                    ws.write(row_num, 6, '', font_style_body)                
                
                ws.write(row_num, 7, u.notification_language, font_style_body)  
                companies = ''
                for company in u.companies.all():
                    companies += f'{company.name}\n'
                ws.write(
                    row_num,
                    8,
                    companies,
                    font_style_body_wrap,
                ) 
                companies_admin = ''
                for company in u.companies_admin.all():
                    companies_admin += f'{company.name}\n'
                ws.write(
                    row_num,
                    9,
                    companies_admin,
                    font_style_body_wrap,
                ) 

            wb.save(response)
            return response
        return redirect('users:ga_user_list')
    
@method_decorator([is_company_admin], name='dispatch')
class CaUserListView(ListView):
    template_name = 'users/CaUserList.html'
    model = User
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Usuarios'), 'url': reverse(
                'users:ca_user_list')},
        ]
        context['page_title'] = _('Usuarios')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('users:ca_user_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context

@method_decorator([is_global_admin], name='dispatch')
class GaUserDetailView(DetailView):
    template_name = 'users/GaUserDetail.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Usuarios'), 'url': reverse(
                'users:ga_user_list')},
            {'title': self.object.full_name}
        ]
        context['page_title'] = f"{_('Usuario')} : {self.object.full_name}"
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('users:ga_user_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]

        return context
    
@method_decorator([is_company_admin], name='dispatch')
class CaUserDetailView(DetailView):
    template_name = 'users/CaUserDetail.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Usuarios'), 'url': reverse('users:ca_user_list')},
            {'title': self.object.full_name}
        ]
        context['page_title'] = f"{_('Usuario')} : {self.object.full_name}"
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('users:ca_user_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]

        return context


@method_decorator([is_global_admin], name='dispatch')
class GaUserCreateView(CreateView):
    template_name = 'users/GaUserCreate.html'
    model = User
    form_class = UserCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Usuarios'), 'url': reverse(
                'users:ga_user_list')},
            {'title': _('Nuevo usuario'), 'url': reverse(
                'users:ga_user_create')},
        ]
        context['page_title'] = _('Nuevo Usuario')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Usuario creado correctamente')
        )
        return reverse_lazy(
            'users:ga_user_list'
        )


@method_decorator((is_global_admin), name='dispatch')
class GaUserUpdateView(UpdateView):
    template_name = 'users/GaUserUpdate.html'
    model = User
    form_class = UserUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Usuarios'), 'url': reverse(
                'users:ga_user_list')},
            {'title': _('Editar usuario')},
        ]
        context['page_title'] = _('Editar Usuario')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Usuario modificado correctamente')
        )

        return reverse_lazy(
            'users:ga_user_detail',
            kwargs={'pk': self.object.pk}
        )

@method_decorator((is_company_admin), name='dispatch')
class CaUserUpdateView(UpdateView):
    template_name = 'users/CaUserUpdate.html'
    model = User
    form_class = CaUserUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Usuarios'), 'url': reverse(
                'users:ca_user_list')},
            {'title': _('Editar usuario')},
        ]
        context['page_title'] = _('Editar Usuario')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Usuario modificado correctamente')
        )

        return reverse_lazy(
            'users:ca_user_detail',
            kwargs={'pk': self.object.pk}
        )

@method_decorator((is_global_admin), name='dispatch')
class GaUserDeleteView(DeleteView):
    model = User
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Usuarios'), 'url': reverse(
                'users:ga_user_list')},
            {'title': _('Eliminar')},
        ]
        context['page_title'] = _("Eliminar Usuario")
        context['breadcrums'] = breadcrums

        return context

    def get_confirm_text_message(self):
        return _('¿Seguro que desea <span class="kt-font-bold">eliminar el Usuario %s</span>? Se borrarán todos los datos asociados al mismo.') % self.object.email

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Usuario eliminado correctamente')
        )

        return reverse_lazy(
            'users:ga_user_list'
        )


@method_decorator([login_required, ], name='dispatch')
class GaUserImportView(FormView):
    template_name = 'users/GaUserImport.html'
    form_class = ImportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Importador de Usuarios')},
        ]
        context['page_title'] = _('Importador de Usuarios')
        context['breadcrums'] = breadcrums
        return context

    def form_valid(self, form):
        input_excel = self.request.FILES['data_file'].read()
        wb = load_workbook(filename=BytesIO(input_excel), data_only=True)

        # Evaluaciones inherentes
        users_to_create = []

        nrow = 0
        rows = wb['USER IMPORT'].rows
        for i, row in enumerate(rows):
            if nrow < 1:
                nrow += 1
                continue

            user = {}

            if (row[0].value != '' and
                    row[1].value != '' and
                    row[2].value != '' and
                    row[3].value != ''):
                user['email'] = str(row[0].value).lower().replace(' ', '')
                user['first_name'] = str(row[1].value).title()
                user['last_name'] = str(row[2].value).title()
                user['password'] = str(row[3].value)
                user['welcome_email'] = str(row[4].value)
                user['companies'] = [x.strip()
                                     for x in str(row[5].value).split(',')]
                user['notification_language'] = str(row[6].value).strip()
                user['username'] = str(row[7].value).strip()

                # Tenemos que comprobar que el email esté bien formado
                if not re.match(
                    '^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$',
                    user['email'].lower()
                ):
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(u'En la fila %s el email introducido no es correcto. Se ha abortado la importación') % str(
                                i+1)
                        )
                    )
                    return super(
                        GaUserImportView,
                        self
                    ).form_invalid(form)
                    break

                # Tenemos que comprobar que no esté dado de alta
                if User.objects.filter(email=user['email']).count() > 0:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(u'El email introducido en la fila %s ya está registrado por otro usuario') % str(
                                i+1)
                        )
                    )
                    return super(
                        GaUserImportView,
                        self
                    ).form_invalid(form)
                    break

                # Tenemos que comprobar que las compañías especificadas existen
                for c in user['companies']:
                    if Company.objects.filter(ref=c).count() == 0:
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _(u'La compañía %s de la fila %s no existe!') % (
                                    str(c), str(i+1))
                            )
                        )
                        return super(
                            GaUserImportView,
                            self
                        ).form_invalid(form)
                        break

                if user['notification_language'].lower() not in ['es', 'en']:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(u'El lenguaje de notificación %s de la fila %s no existe! (Use "en" o "es" para inlgés o español, respectivamente)') % (
                                str(user['notification_language']), str(i+1))
                        )
                    )
                    return super(
                        GaUserImportView,
                        self
                    ).form_invalid(form)

            else:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _(u'En la fila %s falta algún campo obligatorio (columnas 1,2,3,4). Se ha abortado la importación') % str(
                            i+1)
                    )
                )
                return super(
                    GaUserImportView,
                    self
                ).form_invalid(form)
                break

            users_to_create.append(user)

        # Vamos a crear cosas =)
        from krm.users.tasks import send_welcome_email
        for c in users_to_create:
            u = self.create_new_user(
                c['username'],
                c['email'],
                c['first_name'],
                c['last_name'],
                c['password'],
                c['notification_language'],
                c['companies'],
            )

            u.add_action('User created')            

            if c['welcome_email'] == 'Y':
                # send_welcome_email.delay(u.pk)
                send_welcome_email(u.pk)

        messages.add_message(
            self.request,
            messages.SUCCESS, 
            (
                _(u'Se han creado %s usuarios para la compañía') % str(
                    len(users_to_create))
            )
        )

        return super(GaUserImportView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("users:ga_import_users")
    
    def create_new_user(  username: str, email, first_name, last_name, password, notification_language, companies):
        user = User.objects.create_user(username, email)
        user.first_name = first_name
        user.last_name = last_name
        user.notification_language = notification_language
        
        if password != '':
            user.set_password(password)

        for comp in companies:
            company_obj = Company.objects.filter(ref=comp).first()
            user.companies.add(company_obj)

        user.save()
        return user
