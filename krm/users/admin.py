"""User models admin."""

# Django
from django.contrib import admin

# Models
from krm.users.models import User, ActionLogUser

# Forms
from krm.users.forms.user_form import UserAdmin


admin.site.register(User, UserAdmin)


@admin.register(ActionLogUser)
class ActionLogUserAdmin(admin.ModelAdmin):
    model = ActionLogUser
    list_display = ("created", "user", "action_description")
    readonly_fields = ("created",)
