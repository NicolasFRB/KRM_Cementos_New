from django.contrib import admin

from ckeditor.widgets import CKEditorWidget

# Register your models here.
from krm.process.models import Process, SubProcess


@admin.register(Process)
class ProcessAdmin(admin.ModelAdmin):
    model = Process
    list_display = ('ref', 'name', )


@admin.register(SubProcess)
class SubProcessAdmin(admin.ModelAdmin):
    model = SubProcess
    list_display = ('process', 'ref', 'name', )
