from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Envanter_Tarihcesi 

# Register your models here.


class Envanter_TarihcesiResource(resources.ModelResource):
    class Meta:
        model = Envanter_Tarihcesi
        exclude = ["hedef_lokasyon", "hedef_departman", "islem_tarihi"]

class Envanter_TarihcesiAdmin(ImportExportModelAdmin):
    list_display = ["hedef_lokasyon", "hedef_departman", "islem_tarihi","ekipman_tipi"]
    search_fields = ["hedef_lokasyon"]
    list_filter = ["hedef_departman","ekipman_tipi"]
    list_per_page = 50

    class Meta:
        resource_class = Envanter_TarihcesiResource

admin.site.register(Envanter_Tarihcesi, Envanter_TarihcesiAdmin)
