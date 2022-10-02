from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Envanter

exclude_data = ("stok_tipi_1",
                    "stok_tipi_2",
                    "stok_tipi_3",
                    "stok_tipi_4",
                    "stok_tipi_5",
                    "stok_tipi_6",
                    "stok_tipi_7",
                    "stok_tipi_8",
                    "ekipman_no",
                    "teslim_alma_tarihi",
                    "sirket",
                    "organization_code",
                    "kts_saha_no"
                    )

class HamVeriResource(resources.ModelResource):
    class Meta:
        model = Envanter
        exclude = exclude_data
        batch_size = 100000000000

class HamVeriAdmin(ImportExportModelAdmin):
    list_display = ["saha_no", "saha_kodu", "ekipman_parca_kodu", "department_code"]
    resource_class = HamVeriResource
    exclude = exclude_data
    search_fields = ["saha_no", "saha_kodu", "ekipman_parca_kodu", "department_code"]
    list_filter = ["department_code"]
    list_per_page = 10

    
admin.site.register(Envanter, HamVeriAdmin)

