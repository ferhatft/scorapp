from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from envanter.models import Envanter

from .models import SahaListesi

@csrf_exempt
@login_required(login_url="users:login")
def sahalistesi(request):
    if request.method == "GET":

        saha_listesi_all = SahaListesi.objects.all()
        context = {
                'saha_listesi':saha_listesi_all
                }
        return render(request,'saha_listesi.html',context)
    elif request.method == "POST":
        saha_kodu_listesi = Envanter.objects.values_list('saha_tipi', 'saha_no','saha_kodu','department_code','yer_tipi').distinct()
        saha_listeleri = []
        for sahalar in saha_kodu_listesi:
            saha_tipi,saha_no,saha_kodu,department_code,yer_tipi = sahalar#[(st,sn,d,any),()]
            try:
                SahaListesi.objects.get(saha_no=saha_no)
            except SahaListesi.DoesNotExist:
                liste = SahaListesi(
                    saha_no=saha_no,
                    saha_kodu=saha_kodu,
                    saha_tipi=saha_tipi,
                    department_code=department_code,
                    yer_tipi=yer_tipi,
                )
                saha_listeleri.append(liste)
            except SahaListesi.MultipleObjectsReturned:
                return render(request,'saha_listesi.html',{'message':'Saha Listesinde Tekrarlı elemanlar mevcut. Ekipmanlar içideki saha kodları unique değil'})

        SahaListesi.objects.bulk_create(saha_listeleri,batch_size=99999)
        SahaListesi.objects.filter(saha_no__contains='.0').delete()

        saha_listesi_all = SahaListesi.objects.all()

        """for saha_list in saha_listesi_all:
            ekpmn = Envanter.objects.filter(saha_kodu=saha_list.saha_kodu)
            if len(ekpmn) == 0:
                saha_list.status = "P" """

        context = {
                'saha_listesi':saha_listesi_all,
                'message':'Güncelleme Başarılı'
                }
        return render(request,'saha_listesi.html',context)
