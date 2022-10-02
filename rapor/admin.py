from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Rapor,GlobalSayimRapor,ScorRapor

from .models import ScorSayım

class RaporResource(resources.ModelResource):
    class Meta:
        model = Rapor

class RaporAdmin(ImportExportModelAdmin):
    list_display = ["id", "child_id", "saha_no", "saha_kod", "onay", "hatali", "user", "department_code", "created_at"]
    search_fields = ["id"]
    list_filter = ["department_code", "onay", "hatali", "created_at"]
    list_per_page = 100

    
admin.site.register(Rapor, RaporAdmin)



class GlobalSayimRaporResource(resources.ModelResource):
    class Meta:
        model = GlobalSayimRapor
        exclude = ["saha_no", "saha_kod", "sonuc","department_code"]

class GlobalSayimRaporAdmin(ImportExportModelAdmin):
    list_display = ["id","saha_no", "saha_kod", "sonuc","department_code"]
    search_fields = ["parca_kodu", "parca_tanimi"]
    list_filter = ["sonuc","department_code"]
    list_per_page = 50

    class Meta:
        resource_class = GlobalSayimRaporResource


admin.site.register(GlobalSayimRapor, GlobalSayimRaporAdmin)




class RaporGirdilerResource(resources.ModelResource):
    class Meta:
        model = ScorRapor

class RaporGirdilerAdmin(ImportExportModelAdmin):
    list_display = ["rapor_id", "saha_no", "saha_kod", "sonuc", "sorgu_no", "aciklama"]
    search_fields = ["id"]

    class Meta:
        resource_class = RaporGirdilerResource
        

admin.site.register(ScorRapor, RaporGirdilerAdmin)




class ScorSayımResource(resources.ModelResource):
    class Meta:
        model = ScorSayım

class ScorSayımAdmin(ImportExportModelAdmin):
    resource_class = ScorSayımResource
    list_display = ["rapor_id", "saha_no", "saha_kodu", "ekipman_parca_kodu", "quantity", "sayim", "aciklama"]
    search_fields = ["rapor_id", "saha_no", "saha_kodu"]

admin.site.register(ScorSayım, ScorSayımAdmin)


