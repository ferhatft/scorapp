from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Detay, Log, UserProfile


class LogResource(resources.ModelResource):
    class Meta:
        model = Log

class LogAdmin(ImportExportModelAdmin):
    list_display = ["id", "aksiyon", "saha_no", "saha_kod", "user", "description", "created_at"]
    search_fields = ["id","aksiyon", "saha_no", "saha_kod", "user"]
    list_filter = ["created_at", "aksiyon", "user"]
    class Meta:
        resource_class = LogResource



class DetayResource(resources.ModelResource):
    class Meta:
        model = Detay

class DetayAdmin(ImportExportModelAdmin):
    list_display = ["id", "aksiyon", "saha_no", "saha_kod", "user", "description", "created_at"]
    search_fields = ["id","aksiyon", "saha_no", "saha_kod", "user"]
    list_filter = ["created_at", "aksiyon", "user"]
    class Meta:
        resource_class = DetayResource


"""class SayimRaporResource(resources.ModelResource):
    class Meta:
        model = SayimSonrasiRapor"""

"""class SayimRaporAdmin(ImportExportModelAdmin):
    resource_class = SayimRaporResource
    list_display = ["id", "saha_no", "saha_kod", "seri", "sayim", "aciklama"]"""



class UserProfileViweResource(resources.ModelResource):
    class Meta:
        model = UserProfile

class UserProfileViweAdmin(ImportExportModelAdmin):
    list_display = ["user", "department_code", "bakimci", "kontrolcu", "denetci","master"]  # Ekranda görünecek kolonlar
    search_fields = ["user", "department_code", "bakimci", "kontrolcu", "denetci","master"]  # İstenen alanlarda arama yapar
    ordering = ["user", "department_code"]
    list_filter = ["department_code", "bakimci", "kontrolcu", "denetci","master"]

    class Meta:
        resource_class = UserProfileViweResource


admin.site.register(Detay, DetayAdmin)
admin.site.register(Log, LogAdmin)
#admin.site.register(SayimSonrasiRapor, SayimRaporAdmin)
admin.site.register(UserProfile, UserProfileViweAdmin)
