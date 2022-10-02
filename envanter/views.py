import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import render
from excel_app.import_export import ExportExcel
from excel_app.models import Detay

from .models import Envanter

"""

# envanter_listesi --> envanter
 
"""
@login_required(login_url="users:login")
def envanter(request):
    if request.method == "GET":
        return render(request,'envanter.html')
    elif request.method == "POST":
        if 'saha_no' in request.POST:
            saha_no = request.POST.get("saha_no").upper().strip()
            saha_envater = Envanter.objects.filter(Q(saha_no=saha_no) | Q(saha_kodu=saha_no))

            log = Detay(user=request.user, aksiyon="İncele", saha_no=saha_no, saha_kod="Saha Envanter")
            log.description = f"{request.user} Adlı Kullanıcı {saha_no} Sahasında Saha Envanter kontrol ediliyor."
            log.save()

            return render(request,"envanter.html",{
                'saha_envater':saha_envater,
                 'saha_no':saha_no,
                })
        elif 'export' in request.POST:
            saha_no = request.POST['saha_num']

            log = Detay(user=request.user, aksiyon="Export", saha_no=saha_no, saha_kod="Saha Envanter")
            log.description = f"{request.user} Adlı Kullanıcı {saha_no} Sahasında Saha Envanteri Export ediliyor."
            log.save()

            return export_excel_file(saha_no)

        return render(request,'envanter.html')
        

def  export_excel_file(saha_no):
    excel = ExportExcel().generate_excel(saha_num=saha_no)
    path = excel
    if os.path.exists(path):
        with open(path, "rb") as excel:
            data = excel.read()
            response = HttpResponse(data,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=Saha_Envanter.xlsx'
    return response
