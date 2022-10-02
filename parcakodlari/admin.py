from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Parcakodu

# Register your models here.

class ParcakoduResource(resources.ModelResource):
    class Meta:
        model = Parcakodu
        exclude = ["parca_kodu", "parca_tanimi", "ekipman_tipi","olcum_birimi"]

class ParcakoduAdmin(ImportExportModelAdmin):
    list_display = ["id","parca_kodu", "parca_tanimi", "ekipman_tipi","olcum_birimi","grup_tanimi","ekip_tanimi","ekip_aciklama"]
    search_fields = ["parca_kodu", "parca_tanimi","grup_tanimi","ekip_tanimi"]
    list_filter = ["ekipman_tipi","olcum_birimi","grup_tanimi"]
    list_per_page = 100

    class Meta:
        resource_class = ParcakoduResource


admin.site.register(Parcakodu, ParcakoduAdmin)
