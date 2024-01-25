# -*- encoding: utf-8 -*-

from datetime import date

from django import forms
from django.forms import ModelForm,  HiddenInput
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.shortcuts import get_object_or_404
from django.contrib.auth.password_validation import validate_password
from django.forms.widgets import CheckboxSelectMultiple

# from easy_select2 import select2_modelform

from krm.users.models import User


class UserCreateForm(forms.ModelForm):
    """Formulario de creación de usuarios """
    password1 = forms.CharField(label=_('Contraseña'), widget=forms.PasswordInput, required=False,
                                help_text=_('Si no se establece se generará una automáticamente'))
    password2 = forms.CharField(label=_('Repita su contraseña'), widget=forms.PasswordInput,
                                required=False, help_text=_('Debe indicar la misma contraseña que en el campo anterior para prevenir errores'))
    send_email_init_password = forms.BooleanField(
        label=_('Enviar correo para establecer contraseña de acceso'),
        required=False,
        help_text=_(
            'Se le enviará un email al usuario para que pueda establecer su contraseña')
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'position',
            'email',
            'send_email_init_password',
            'is_superuser',
            'companies',
            'companies_admin',
            'notification_language',
            'is_auditor'
        )

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True
        self.fields["companies"].widget.attrs["class"] = "form-select"
        self.fields["companies"].widget.attrs["data-control"] = "select2"
        self.fields["companies_admin"].widget.attrs["class"] = "form-select"
        self.fields["companies_admin"].widget.attrs["data-control"] = "select2"

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError(_('Las contraseñas no coinciden'))

        if password2 != '':
            validate_password(password2)

        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if username == '':
            username = self.cleaned_data['email']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('El nombre de usuario ya existe'))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                _('Ya existe un usuario con dicho email'))
        return email

    def save(self):
        user = super().save(commit=True)
        from krm.users.tasks import send_welcome_email

        if self.cleaned_data.get("send_email_init_password"):
            send_welcome_email.delay(user.pk)

        if self.cleaned_data["password1"] != '':
            user.set_password(self.cleaned_data["password1"])
            user.save()

        return user


class UserUpdateForm(forms.ModelForm):
    """Formulario de creación de usuarios """
    password1 = forms.CharField(label=_('Contraseña'), widget=forms.PasswordInput, required=False,
                                help_text=_('Si no se establece se generará una automáticamente'))
    password2 = forms.CharField(label=_('Repita su contraseña'), widget=forms.PasswordInput,
                                required=False, help_text=_('Debe indicar la misma contraseña que en el campo anterior para prevenir errores'))

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'position',
            'companies',
            'companies_admin',
            'is_superuser',
            'notification_language',
            'is_active',
            'is_auditor'
        )

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields["companies"].widget.attrs["class"] = "form-select"
        self.fields["companies"].widget.attrs["data-control"] = "select2"
        self.fields["companies_admin"].widget.attrs["class"] = "form-select"
        self.fields["companies_admin"].widget.attrs["data-control"] = "select2"

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError(_('Las contraseñas no coinciden'))

        if password2 != '':
            validate_password(password2)

        return password2

    def save(self):
        user = super().save(commit=True)

        if self.cleaned_data["password1"] != '':
            user.set_password(self.cleaned_data["password1"])
            user.save()
        return user

class CaUserUpdateForm(forms.ModelForm):
    """Formulario de creación de usuarios """
    password1 = forms.CharField(label=_('Contraseña'), widget=forms.PasswordInput, required=False,
                                help_text=_('Si no se establece se generará una automáticamente'))
    password2 = forms.CharField(label=_('Repita su contraseña'), widget=forms.PasswordInput,
                                required=False, help_text=_('Debe indicar la misma contraseña que en el campo anterior para prevenir errores'))

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'position',
            'companies',
            'companies_admin',
            'is_superuser',
            'notification_language',
            'is_active'
        )

    def __init__(self, *args, **kwargs):
        super(CaUserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields["companies"].widget.attrs["class"] = "form-select"
        self.fields["companies"].widget.attrs["data-control"] = "select2"
        self.fields["companies"].disabled = True
        self.fields["companies_admin"].widget.attrs["class"] = "form-select"
        self.fields["companies_admin"].widget.attrs["data-control"] = "select2"
        self.fields["companies_admin"].disabled = True

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError(_('Las contraseñas no coinciden'))

        if password2 != '':
            validate_password(password2)

        return password2

    def save(self):
        user = super().save(commit=True)

        if self.cleaned_data["password1"] != '':
            user.set_password(self.cleaned_data["password1"])
            user.save()
        return user

class UserAdminCreateForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'notification_language',
            'is_superuser',
            'is_auditor'
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 != password2:
            raise forms.ValidationError(_('Las contraseñas no coinciden'))

        if password2 != '':
            validate_password(password2)

        return password2

    def clean_username(self):
        username = self.cleaned_data['username']
        if username == '':
            username = self.cleaned_data['email']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('El nombre de usuario ya existe'))
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                _('Ya existe un usuario con dicho email'))
        return email

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if not user.username:
            user.username = user.email
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    # add_form = UserAdminCreateForm
    # form = UserAdminForm
    readonly_fields = ('last_login', )
    list_display = (
        'username',
        'first_name',
        'last_name',
        'is_superuser',
        'last_login'
        # 'created',
        # 'modified'
    )
    list_filter = ('is_superuser', 'is_staff')
    fieldsets = (
        (u'Datos de acceso', {
            'fields': (
                'username',
                'password',
                'last_login'
            )
        }),
        (u'Información personal', {
            'fields': (
                (
                    'email',
                    'first_name',
                    'last_name',
                ),
                (
                    'notification_language',
                )
            )
        }),
        (u'Empresas', {
            'fields': (
                (
                    'companies',
                    'companies_admin'
                ),
            )
        }),
        ('Claves de recuperación y login', {
            'fields': (
                'remember_key',
            ),
        }),
        ('Grupos y Permisos', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'is_auditor',
                'groups',
                # 'user_permissions'
            ),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('email',)
    filter_horizontal = (
        # 'user_permissions',
        'groups',
        'companies',
        'companies_admin'
    )

class UsersActionForm(forms.Form):

    action = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['action'].widget = HiddenInput()
