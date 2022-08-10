from django.contrib import admin

# Register your models here.
from .models import Configuration


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    model = Configuration
    list_display = ('app_name', )
