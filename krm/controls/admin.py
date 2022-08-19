from django.contrib import admin

from ckeditor.widgets import CKEditorWidget

# Register your models here.
from .models import Control


@admin.register(Control)
class ControlAdmin(admin.ModelAdmin):
    model = Control
    # list_display = ('ref', 'name', )
