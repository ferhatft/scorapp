from django.contrib import admin
# Register your models here.
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import SahaListesi


class SahaListesiResource(resources.ModelResource):
    class Meta:
        model = SahaListesi
        exclude = ["hedef_lokasyon", "hedef_departman", "islem_tarihi"]

class SahaListesiAdmin(ImportExportModelAdmin):
    list_display = ["saha_no", "saha_kodu", "department_code","updated"]
    search_fields = ["saha_no","saha_kodu"]
    list_filter = ["department_code"]
    list_per_page = 50

    class Meta:
        resource_class = SahaListesiResource


        
admin.site.register(SahaListesi, SahaListesiAdmin)