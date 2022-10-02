import pandas
# Create your views here.
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Value
from django.db.models.functions import Replace
from django.shortcuts import render
from excel_app.models import Detay, Log

from .models import Envanter_Tarihcesi
"""
# ehtviwe ---> ehtview --> envanter_tarihcesi
"""
def envanter_tarihcesi(request):
    #Envanter_Tarihcesi.objects.filter(ekipman_tipi="SERI").delete()
    #Envanter_Tarihcesi.objects.filter(islem_tarihi__startswith="6/29/2022").delete()
    #Envanter_Tarihcesi.objects.filter(islem_tarihi__startswith="2022-06-29").delete()
    #Envanter_Tarihcesi.objects.filter(islem_tarihi__startswith="6/30/2022").delete()
    #Envanter_Tarihcesi.objects.filter(islem_tarihi__startswith="2022-06-30").delete()

    # Envanter_Tarihcesi.objects.update(ekipman_tipi=Replace('ekipman_tipi', Value('SERİ'), Value('SERI')))
    #Envanter_Tarihcesi.objects.all().delete()
    try:
        if request.method == "GET":

            return render(request,'eht.html')

        elif request.method == "POST":
            if "saha_no" in request.POST:
                saha_no = request.POST.get("saha_no").upper().strip()
                #eht_list = Envanter_Tarihcesi.objects.filter(hedef_lokasyon=saha_no).distinct()
                eht_list = Envanter_Tarihcesi.objects.filter(hedef_lokasyon=saha_no).values("islem_no","hedef_lokasyon","seri_no","parca_kodu","parca_tanimi","islem_miktari","olcum_birimi","kaynak_yeri","kullanici_adi","form_no","islem_tarihi").distinct().order_by("-islem_tarihi")

                last_update = Envanter_Tarihcesi.objects.latest('islem_tarihi').islem_tarihi
                #today_date = Envanter_Tarihcesi.objects.latest('islem_tarihi').islem_tarihi

                #last_update = today_date.strftime("%d.%m.%Y %H:%M")

                context = {
                'saha_eht_envanter': eht_list, 'last_update':last_update
                }

                log = Detay(user=request.user, aksiyon="İncele", saha_no=saha_no, saha_kod="EHT")
                log.description = f"{request.user} Adlı Kullanıcı {saha_no} Sahasında EHT kontrol ediliyor."
                log.save()

                return render(request, "eht.html", context)
            else:
                my_file = request.FILES["EHT_EnvanterFile"]
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                filename = fs.save(my_file.name, my_file)

                if filename.endswith(".xlsb"):
                    ham_veri = pandas.read_excel(settings.MEDIA_ROOT +"/" + filename, engine="pyxlsb")
                elif filename.endswith(".xlsx"):
                    ham_veri = pandas.read_excel(settings.MEDIA_ROOT +"/" + filename, engine="openpyxl")
                else:
                    ham_veri = pandas.read_excel(settings.MEDIA_ROOT +"/" +  filename, engine="xlrd")

                hareket_list = []

                if "sarf" in request.POST:
                    for row in ham_veri.to_dict(orient="records"):

                        hareket_line = Envanter_Tarihcesi(
                            islem_no = row['Islem No'],
                            islem_tarihi = row['Islem Tarihi'],
                            parca_kodu = row['Kalem Kodu'],
                            parca_tanimi = row['Kalem Adi'],
                            islem_miktari = row['Islem Miktari'],
                            olcum_birimi = row['Olcum Birimi'],
                            kaynak_yeri = row['Kaynak Stok Yeri'],
                            islem_tipi = row['Islem Tipi'],
                            hedef_departman = row['Hedef Departman'],
                            hedef_lokasyon = row['Hedef Lokasyon'],
                            kullanici_adi = row['Kullanici Adi'],
                            ekipman_tipi = row['Kalem Tipi'],
                            maliyet = row['Birim Maliyet'],
                            form_no = row['Form No']
                            )
                        hareket_list.append(hareket_line)

                    Envanter_Tarihcesi.objects.bulk_create(hareket_list,batch_size=9999999)

                    log = Detay(user=request.user, aksiyon="Import", saha_no="IMPORT_SARF", saha_kod="EHT")
                    log.description = f"{request.user} Adlı Kullanıcı Günlük EHT Sarf Dosyasını Yükledi."
                    log.save()
                    message = "Sarf Listeleri Başarlılı ile yüklendi"


                elif "seri" in request.POST:
                    for row in ham_veri.to_dict(orient="records"):

                        hareket_line = Envanter_Tarihcesi(
                            islem_no = row['Islem No'],
                            islem_tarihi = row['Islem Tarihi'],
                            parca_kodu = row['Kalem Kodu'],
                            parca_tanimi = row['Kalem Adi'],
                            islem_miktari = row['Islem Miktari'],
                            olcum_birimi = row['Olcum Birimi'],
                            kaynak_yeri = row['Kaynak Stok Yeri'],
                            islem_tipi = row['Islem Tipi'],
                            hedef_departman = row['Hedef Departman'],
                            hedef_lokasyon = row['Hedef Lokasyon'],
                            kullanici_adi = row['Kullanici Adi'],
                            ekipman_tipi = "SERI",
                            seri_no = row['Seri Numarasi'],
                            maliyet = row['Birim Maliyet'],
                            form_no = row['Form No']
                            )
                        hareket_list.append(hareket_line)

                    Envanter_Tarihcesi.objects.bulk_create(hareket_list,batch_size=9999999)

                    log = Detay(user=request.user, aksiyon="Import", saha_no="IMPORT_SERI", saha_kod="EHT")
                    log.description = f"{request.user} Adlı Kullanıcı Günlük EHT Seri Dosyasını Yükledi."
                    log.save()
                    message = "Seri Listeleri Başarlılı ile yüklendi"

                # Kalem kodu yükleme dosyasında Ekipman bilgisi de geliyor, Seri yüklemede mükerrer olmaması için bu kayıtları silinecek
                Envanter_Tarihcesi.objects.filter(ekipman_tipi='EKIPMAN').delete()

                # ".0" olan Hatalı kayıtları düzeltir.
                Envanter_Tarihcesi.objects.update(form_no=Replace('form_no', Value('.0'), Value('')))
                Envanter_Tarihcesi.objects.update(islem_no=Replace('islem_no', Value('.0'), Value('')))
                """
                # Mükerrer kayıtları sileri çok yavaş siliyor.
                for duplicates in Envanter_Tarihcesi.objects.values("islem_no","seri_no").annotate(records=Count("islem_no")).filter(records__gt=1):
                    for tag in Envanter_Tarihcesi.objects.filter(islem_no=duplicates["islem_no"])[1:]:
                        tag.delete()
                """
            return render(request,'eht.html',{"message":message})

    except:
        message = "Hatalı İşlem"

        return render(request,'eht.html',{"message":message})

