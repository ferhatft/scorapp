from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Sorgular, SorguReferanslari



class SorguListResource(resources.ModelResource):
    class Meta:
        model = Sorgular

class SorguListAdmin(ImportExportModelAdmin):
    list_display = ["id", "sorgu_no", "kontrol", "ref_grup", "kategori", "check"]
    search_fields = ["sorgu_no", "kontrol", "ref_grup", "kategori", "check"]
    list_per_page = 100
    class Meta:
        resource_class = SorguListResource

        
admin.site.register(Sorgular, SorguListAdmin)




class RaporReferanslariResource(resources.ModelResource):
    class Meta:
        model = SorguReferanslari
        exclude = ["grup_tanimi", "rapor_tanimi", "ref_grup", "kategori", "analiz_no"]

class RaporReferanslariAdmin(ImportExportModelAdmin):
    list_display = ["id", "sorgu_no", "ref", "ekipman_parca_kodu", "parca_tanimi", "rapor_tanimi"]
    search_fields = ["sorgu_no"]
    list_per_page = 5000

    class Meta:
        resource_class = RaporReferanslariResource

admin.site.register(SorguReferanslari, RaporReferanslariAdmin)