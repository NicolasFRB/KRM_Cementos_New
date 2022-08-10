"""User models admin."""

# Django
from django.contrib import admin

# Models
from krm.users.models import User

# Forms
from krm.users.forms.users import UserAdmin


admin.site.register(User, UserAdmin)
