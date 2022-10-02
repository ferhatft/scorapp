from django.contrib import admin
from .models import Departmanlar


class DepartmanlarAdmin(admin.ModelAdmin):
    model = Departmanlar
    list_display = ["code", "emails"]


    
admin.site.register(Departmanlar, DepartmanlarAdmin)