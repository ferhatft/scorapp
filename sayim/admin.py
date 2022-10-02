from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import AndroidSayim, TerminalSayim 
# Register your models here.
admin.site.register(AndroidSayim)

class RaporEnvanterResource(resources.ModelResource):
    class Meta:
        model = TerminalSayim



class RaporEnvanterAdmin(ImportExportModelAdmin):
    resource_class = RaporEnvanterResource
    list_display = ["rapor_id", "saha_no", "user", "parca_kodu", "miktar", "bolge"]
    search_fields = ["rapor_id"]

        
admin.site.register(TerminalSayim, RaporEnvanterAdmin)

