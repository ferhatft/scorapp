import json
import os

import pandas
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.mail import EmailMessage
from django.db.models import Value
from django.db.models.functions import Replace
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from envanter.models import Envanter
from excel_app.decorators import authUser
from excel_app.models import Detay, Log, Rapor
from sahalistesi.models import SahaListesi
from scorfonksiyonlari.Scor_V5_ import rapor_calistir
from scorfonksiyonlari.Scor_V5_New import rapor_calistir_new
from scorfonksiyonlari.Scor_V6 import rapor_calistir_V6
from sorgu.models import Sorgular, SorguReferanslari

from rapor.models import ScorRapor

from .models import GlobalSayimRapor, Rapor, ScorRapor, ScorSayım


def satirSil(request):
    satir_id = request.GET.get("satir_id")
    ScorSayım.objects.get(id=satir_id).delete()

    log = Log(user=request.user, aksiyon ="Sil", saha_no="Scor", saha_kod=satir_id)
    log.description = f"{request.user} Adlı Kullanıcı {satir_id} Id'li satırı sildi."
    log.save()
    return JsonResponse({"Msg":"Success"})

"""
# bakimEnvanterGirdiUpdate --> scorsayimupdate  yapılacak

bakım_rapor.html satır 407 js kodu güncelleme yapıldı
globalrapor.html  satır 194 js kodu güncelleme yapıldı

"""

@login_required(login_url="/login")
def scorsayimupdate(request):
    aciklama = request.GET.get("aciklama")
    sayim = request.GET.get("sayim")
    girdi_id = request.GET.get("girdi_id")
    girdi = ScorSayım.objects.get(id=girdi_id)
    girdi.aciklama = aciklama
    girdi.sayim = int(sayim)
    girdi.save()

    log = Detay(user=request.user)
    log.description = f"{request.user} Adlı Kullanıcı Sayım Sonrası Envanter Raporundaki {girdi.saha_no} Saha No'lu Ve {girdi.id} ID'sine Sahip Girdiyi Güncelledi."
    log.saha_no = girdi.saha_no
    log.saha_kod = girdi.saha_kodu

    return JsonResponse({"Msg": "Success"})


"""
şuanda gizli durumda daha sonra aktif edilecek. 

her satır için bir kaç tane resim eklenecek

"""

def resim_ekle(request,pk):
    envanterler = ScorSayım.objects.filter(rapor=pk)
    #rapor_id = request.POST.get("rapor_id")
    if request.method == "POST":
        for envanter in envanterler:
            image = request.FILES.get(f'{envanter.id}',False)
            if image != False:
                envanter.image = image
                envanter.save()

    return render(request,'resim_ekle.html',{'envanterler':envanterler})

"""
# create_scor --> scorraporcreate  yapılacak

scor\src\templates\eht.html  de  276 satır send-scor  scorraporcreate olarak değiştirildi

"""
@csrf_exempt
def scorraporcreate(request):
    data = json.loads(request.body)
    object_list = data.get('object_list',False)#[{},{}]
    try:
        obj = object_list[0]
    except:
        return JsonResponse({'message':"Hiçbir eleman göndermediniz."})
    hedef_lokasyon = obj['hedef_lokasyon']

    if obj:
        try:
            saha = SahaListesi.objects.get(Q(saha_no=hedef_lokasyon) | Q(saha_kodu=hedef_lokasyon))
        except SahaListesi.DoesNotExist:
            return JsonResponse({'message':'Böyle bir saha bulunmamaktadır.'})
        except SahaListesi.MultipleObjectsReturned:
            return JsonResponse({'message':'Saha Listesinde Tekrarlı değer var. Saha Listenizi Silip ve  Güncelleyip Tekrar Deneyin'})
    else:
        return JsonResponse({'message':'Bir hata oluştu. Muhtemelen hedef lokasyon ulaşmadı.'})

    saha_no = saha.saha_no
    saha_kodu = saha.saha_kodu
    department_code = saha.department_code

    rapor = Rapor.objects.create(user=request.user,saha_no=saha_no)
    rapor.save()


    sorgu_list = pandas.DataFrame(Sorgular.objects.all().values("sorgu_no", "kontrol", "ref_grup", "kategori", "check"))
    sorgu_ref = pandas.DataFrame(SorguReferanslari.objects.all().values("sorgu_no", "ref", "ekipman_parca_kodu"))

    obj_list = []
    for i in object_list:
        obj_dict = {}
        obj_dict['saha_no'] = saha_no
        obj_dict['saha_kodu'] = saha_kodu
        obj_dict['ekipman_parca_kodu'] = i['parca_kodu']
        obj_dict['department_code'] = department_code
        obj_dict['quantity'] = int(i['islem_miktari'])
        obj_list.append(obj_dict)

    ham_veri = pandas.DataFrame(obj_list)

    print("-------------------")
    print(ham_veri)
    rapor_calistir_new(ham_veri,sorgu_list,sorgu_ref,rapor)
    sonuclar = ScorRapor.objects.filter(rapor=rapor)

    log = Detay(user=request.user, aksiyon="İncele", saha_no=saha_no, saha_kod="EHT_Scor")
    log.description = f"{request.user} Adlı Kullanıcı {saha_no} Sahasında EHT kontrol ediliyor."
    log.save()

    return JsonResponse([sonuc.serializer() for sonuc in sonuclar],safe=False)


@csrf_exempt
def satirEkle(request):
    rapor_id, saha_no, saha_kodu, department_code, ekipman_parca_kodu, ekipman_seri_no, parca_tanimi, sayim, aciklama = request.POST.values()

    ekipman_parca_kodu = ekipman_parca_kodu.strip()
    parca_tanimi = parca_tanimi.strip()
    ekipman_seri_no = ekipman_seri_no.strip()
    sayim = sayim.strip()
    aciklama = aciklama.strip()

    rapor = Rapor.objects.get(id=rapor_id)
    sayim_girdi = ScorSayım(saha_no=saha_no, saha_kodu=saha_kodu, ekipman_seri_no=ekipman_seri_no, ekipman_parca_kodu=ekipman_parca_kodu, parca_tanimi=parca_tanimi, department_code=department_code, quantity=0, aciklama=aciklama, sayim=int(sayim), rapor=rapor)
    sayim_girdi.save()

    log = Log(user=request.user, aksiyon ="Ekle", saha_no=saha_no, saha_kod=saha_kodu)
    log.description = f"{request.user} Adlı KUllanıcı {rapor_id} RID için {ekipman_seri_no}  seri, {ekipman_parca_kodu} malzemden {sayim} adet ekledi."
    log.save()
    return JsonResponse({"satir_id":sayim_girdi.id})
    #return render(request, "bakim_envanter_satir_ekle.html", {"satir":sayim_girdi})


def getHamVeriAndCreate(request, child_rapor_id=0, saha_no=""):

    filename = ""
    if saha_no != "":
        # ham_veri = pandas.DataFrame(Envanter.objects.filter(saha_no=saha_no).values())
        saha_no = saha_no.upper().strip()
        ham_veri = pandas.DataFrame(Envanter.objects.filter(Q(saha_no=saha_no) | Q(saha_kodu=saha_no)).values())


        ham_veri = ham_veri.rename(columns={"saha_no":"Saha No", "saha_kodu":"Saha Kodu", "ekipman_seri_no":"Ekipman Seri No", "ekipman_parca_kodu":"Ekipman Parca Kodu", "parca_tanimi":"Parca Tanimi", "department_code":"Department Code", "quantity":"Quantity"})
    else:
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)
        my_file = request.FILES["excelFile"]
        filename = fs.save(my_file.name, my_file)

        if filename.endswith(".xlsb"):
            ham_veri = pandas.read_excel(settings.MEDIA_ROOT +"/" + filename, engine="pyxlsb")
        elif filename.endswith(".xlsx"):
            ham_veri = pandas.read_excel(settings.MEDIA_ROOT +"/" + filename, engine="openpyxl")
        else:
            ham_veri = pandas.read_excel(settings.MEDIA_ROOT +"/" +  filename, engine="xlrd")


    sorgu_list = pandas.DataFrame(Sorgular.objects.all().values("sorgu_no", "kontrol", "ref_grup", "kategori", "check"))
    sorgu_ref = pandas.DataFrame(SorguReferanslari.objects.all().values("sorgu_no", "ref", "ekipman_parca_kodu", "parca_tanimi", "grup_tanimi", "ref_grup", "kategori"))

    rapor = Rapor(user=request.user)
    if child_rapor_id != 0:
        rapor.child = Rapor.objects.get(id=child_rapor_id)

    rapor.save()

    girdiler = rapor_calistir(ham_veri, sorgu_list, sorgu_ref, rapor=rapor)

    log = Detay(user=request.user, aksiyon ="Rapor", saha_no="Scor", saha_kod="Scor")
    log.description = f"{request.user} Adlı KUllanıcı Yeni Bir Rapor Oluşturdu."
    log.save()
    if filename != "":
        fs.delete(filename)
    return {"rapor_id": rapor.id, "data": girdiler}



def raporOnayla(request):
    rapor_id = request.GET.get("rapor_id")
    rapor = Rapor.objects.get(id=rapor_id)
    if rapor.child is not None:
        rapor.child.onay = True
        rapor.child.hatali = False
        rapor.child.save()

    rapor.onay = True
    rapor.hatali = False
    rapor.save()

    return JsonResponse({"Msg": "Success"})
    
"""
İlgili Rapora Ait Girdileri Getirme View'ı
Sayım Sonuç Raporu Oluşturma View'ı

"""
@login_required(login_url="/login")
@csrf_exempt
def sayimSonucRaporuOlustur(request):
    rapor_id = request.POST.get("rapor_id")
    rapor = Rapor.objects.get(id=rapor_id)

    rapor.girdiler.all().delete()

    sayim_sonrasi_envanter = rapor.sayim_sonrasi_envanter.all().values("saha_no", "saha_kodu", "ekipman_seri_no", "ekipman_parca_kodu", "parca_tanimi", "department_code", "sayim")

    ham_veri = pandas.DataFrame(sayim_sonrasi_envanter)

    sorgu_list = pandas.DataFrame(Sorgular.objects.all().values("sorgu_no", "kontrol", "ref_grup", "kategori", "check"))
    sorgu_ref = pandas.DataFrame(SorguReferanslari.objects.all().values("sorgu_no", "ref", "ekipman_parca_kodu", "parca_tanimi", "grup_tanimi", "ref_grup", "kategori"))

    sayim_sonrasi_envanter = rapor.sayim_sonrasi_envanter.all()
    girdiler = rapor_calistir(ham_veri, sorgu_list, sorgu_ref, rapor=rapor)
    return render(request, "bakım_rapor.html", {"sayim_sonuc_girdiler":girdiler, "bakim_envanter":sayim_sonrasi_envanter, "rapor_id":rapor_id, "rapor":rapor})
    #return redirect("/rapor_getir/?rapor_id=" + rapor_id)


def raporGetir(request):
    rapor_id = request.GET.get("rapor_id")
    rapor = Rapor.objects.get(rapor_id)
    sayim_sonrasi_envanter = rapor.sayim_sonrasi_envanter.all()
    sayim_sonuc_girdiler = rapor.girdiler.all()

    return render(request, "bakım_rapor.html", {
        "bakim_envanter":sayim_sonrasi_envanter,
        "sayim_sonuc_girdiler":sayim_sonuc_girdiler,
        "rapor_id":rapor.id,
        "rapor":rapor
    })


"""
Ham Veri Dosyasıyla Sayım Sonrası Envanter Ve Sayım Rapor Girdilerini Oluşturma View'ı


bu view parçalanarak bakım kontrol eth için ayrı ayrı eklenecek   

aslında bu sayım raporu

"""
@login_required(login_url="/login")
@authUser(redirect_url="/permissionDenied", permission_user="bakimci")
def bakimRaporOlustur(request):
    try:
        if request.method == "POST":
            file = request.FILES.get("excelFile", False)
            if not file:
                saha_no = request.POST.get("envanter_saha_no").upper().strip()
                context = getHamVeriAndCreate(request, saha_no=saha_no)
            else:
                context = getHamVeriAndCreate(request)
            rapor_id = context["rapor_id"]
            rapor = Rapor.objects.get(id=rapor_id)
            sayim_sonrasi_envanter = rapor.sayim_sonrasi_envanter.all()
            return render(request, "bakım_rapor.html", {"bakim_envanter":sayim_sonrasi_envanter, "sayim_sonuc_girdiler":context["data"], "rapor_id":rapor.id, "rapor":rapor})
        rapor_id = request.GET.get("rapor_id")
        if rapor_id is not None:
            rapor = Rapor.objects.get(id=rapor_id)

            sayim_sonrasi_envanter = rapor.sayim_sonrasi_envanter.all()
            sayim_sonuc_girdiler = rapor.girdiler.all()

            return render(request, "bakım_rapor.html", {
                "bakim_envanter":sayim_sonrasi_envanter,
                "sayim_sonuc_girdiler":sayim_sonuc_girdiler,
                "rapor_id":rapor.id,
                "rapor":rapor
            })


        return render(request, "bakım_rapor.html")

    except:
        return render(request, "bakım_rapor.html", {"message":"Sistemde kayıtlı böyle bir Saha No yok, kontrol edip tekrar deneyiniz. !!!"})



@login_required(login_url="/login")
@authUser(permission_user="kontrolcu")
def kontrolRaporOlustur(request):
    
    print("fonksiyona geldi")
    if request.method == "GET":
        
        print("get")
        return render(request, "kontrol_rapor.html")

    elif request.method == "POST":
        if "sayım_dosyası" in request.POST:
            try:
                context = getHamVeriAndCreate(request, child_rapor_id=request.POST.get("child_rapor_id"))
                rapor = Rapor.objects.get(id=context["rapor_id"])
                child_rapor_girdiler = rapor.child.girdiler.all()
                context["kontrol_edilecek_girdiler"] = child_rapor_girdiler
                context["kontrol_envanter"] = rapor.rapor_envanter.all()
                context["rapor"] = rapor

                return render(request, "kontrol_rapor.html", context)

            except Exception as e:

                return render(request, "kontrol_rapor.html", {"Error":e})

        elif "envanter_dosyası" in request.POST:
            try:
                my_file = request.FILES["bakimEnvanterFile"]
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)  # defaults to   MEDIA_ROOT
                filename = fs.save(my_file.name, my_file)

                if filename.endswith(".xlsb"):
                    ham_veri = pandas.read_excel(settings.MEDIA_ROOT +"/" + filename, engine="pyxlsb")
                elif filename.endswith(".xlsx"):
                    ham_veri = pandas.read_excel(settings.MEDIA_ROOT +"/" + filename, engine="openpyxl")
                else:
                    ham_veri = pandas.read_excel(settings.MEDIA_ROOT +"/" +  filename, engine="xlrd")

                hamveri_list = []

                print(hamveri_list)

                # Envanter.objects.filter(department_code=request.user.profile.department_code).delete()
                # for row in ham_veri.to_dict(orient="records"):

                departman = ham_veri.drop_duplicates(subset ="Department Code")

                print("departman")
                print(departman)
                departman = departman.to_dict(orient="records")

                for row in departman:
                    department_code=row["Department Code"]

                    print("department_code")
                    print(department_code)


                    Envanter.objects.filter(department_code=department_code).delete()

                    departman_veri = pandas.DataFrame(ham_veri[ham_veri['Department Code'] == department_code])
                    dict_data = departman_veri.to_dict(orient="records")

                    for row in dict_data:
                        saha_no = row["Saha No"]
                        saha_kodu = row["Saha Kodu"]
                        saha_tipi = row["Saha Tipi"]
                        yer_tipi = row["Ana Yer Tipi"]
                        ekipman_seri_no = row["Ekipman Seri No"]
                        ekipman_parca_kodu = row["Ekipman Parca Kodu"]
                        parca_tanimi = row["Parca Tanimi"]
                        kurulumu_tarihi = row["Sahaya Kurulum Tarihi"]
                        department_code = row["Department Code"]
                        quantity = row["Quantity"]
                        ustekipman = row["Ustekipman"]


                        hamveri_girdi = Envanter(saha_no=saha_no, saha_kodu=saha_kodu, saha_tipi=saha_tipi,yer_tipi=yer_tipi,
                                                            ekipman_seri_no=ekipman_seri_no, ekipman_parca_kodu=ekipman_parca_kodu,
                                                            parca_tanimi=parca_tanimi, kurulumu_tarihi=kurulumu_tarihi, department_code=department_code, quantity=quantity, ustekipman=ustekipman)
                        hamveri_list.append(hamveri_girdi)

                        #if len(hamveri_list) > 5000:#toplu kayıt yerine her 5binde bir kayıt edeceğiz.
                        #    Envanter.objects.bulk_create(hamveri_list, batch_size=999999999999)
                        #    hamveri_list = []

                    Envanter.objects.bulk_create(hamveri_list, batch_size=999999999999)
                    hamveri_list = []
                    Envanter.objects.filter(yer_tipi='CN SAHA').delete()
                    Envanter.objects.update(saha_no=Replace('saha_no', Value('.0'), Value('')))

                    log = Detay(user=request.user, aksiyon="Import", saha_no=department_code, saha_kod="Envanter")
                    log.description = f"{request.user} Adlı Kullanıcı {department_code} Bölgesi için Envanter Dosyası Yüklüyor."
                    log.save()
                    message = "Envanter Başarlı ile Yüklemiştir."
                return render(request, "kontrol_rapor.html", {'message':message})

            except:
                message = "Envanter Dosyası Yüklenemedi Dosyayı Kontrol ederek Tekrar deneyinizi..."
                return render(request, "kontrol_rapor.html", {'message':message})
    else:
        return render(request, "kontrol_rapor.html")


@csrf_exempt
def sendMailKontrolRapor(request):
    rapor_id = request.POST.get("rapor_id")

    mail_body = request.POST.get("mail_body")
    rapor = Rapor.objects.get(id=rapor_id)
    child_rapor = rapor.child
    user_email = child_rapor.user.email
    rapor_girdiler = rapor.girdiler.all().values()   # ScorRapor model connection

    rapor_sayim_sonuc_rapor = rapor_girdiler
    rapor_sayim_sonrasi_envanter = rapor.rapor_envanter.all().values()    # Terminal Sayım | RaporEnvanter model connection 
    rapor_child_sayim_sonuc_girdiler_df = pandas.DataFrame(rapor.child.girdiler.all().values()).drop(["id", "created_at", "is_sayim_sonrasi"], axis=1)

    email_list = [email.replace("\r", "") for email in rapor.department_code.emails.split("\n")]

    file_name = f"{rapor.child.saha_no}_{rapor.child.saha_kod}_{rapor.child.id}_kontrol.xlsx"
    output_path = os.path.join(settings.BASE_DIR, "media/send_mail/") + file_name

    writer = pandas.ExcelWriter(output_path)
    rapor_sayim_sonuc_rapor_df = pandas.DataFrame(rapor_sayim_sonuc_rapor).drop(["id", "created_at", "is_sayim_sonrasi"], axis=1)
    rapor_sayim_sonrasi_envanter_df = pandas.DataFrame(rapor_sayim_sonrasi_envanter).drop(["id"], axis=1)

    rapor_child_sayim_sonuc_girdiler_df.to_excel(writer, sheet_name="Bakım Raporu")
    rapor_sayim_sonrasi_envanter_df.to_excel(writer, sheet_name="Kontrol Envanter")
    rapor_sayim_sonuc_rapor_df.to_excel(writer, sheet_name="Kontrol Raporu")

    writer.save()

    mail_subject = f"{child_rapor.saha_no} - {child_rapor.saha_kod} {child_rapor.id} nolu Kontrol Raporu {child_rapor.user}"
    if child_rapor.onay == True:
        mail_subject += " Onaylı"
    else:
        mail_subject += " Tekrar Sayılacak"
    email = EmailMessage(subject=mail_subject, body=mail_body, from_email="rapor@scor-app.com",
                         to=email_list)
    email.attach_file(output_path)

    email.send()
    os.remove(output_path)

    return JsonResponse({"Msg":"Success"})

def raporHatali(request):
    rapor_id = request.GET.get("rapor_id")
    rapor = Rapor.objects.get(id=rapor_id)
    rapor.hatali = True
    rapor.onay = False
    rapor.child.hatali = True
    rapor.child.onay = False
    rapor.child.save()
    rapor.save()
    return JsonResponse({"Msg":"Success"})

@csrf_exempt
def sendMailRapor(request):
    rapor_id = request.POST.get("rapor_id")
    mail_subject = request.POST.get("mail_subject")
    mail_body = request.POST.get("mail_body")
    rapor = Rapor.objects.get(id=rapor_id)
    rapor_girdiler = rapor.girdiler.all().values()

    rapor_sayim_sonuc_rapor = rapor_girdiler

    rapor_sayim_sonrasi_envanter = rapor.sayim_sonrasi_envanter.all().values()
    email_list = [email.replace("\r", "") for email in rapor.department_code.emails.split("\n")]

    file_name = f"{rapor.saha_no}_{rapor.saha_kod}_{rapor.id}_bakım.xlsx"

    output_path = os.path.join(settings.BASE_DIR, "media/send_mail/") + file_name
   
    writer = pandas.ExcelWriter(output_path)
    rapor_sayim_sonuc_rapor_df = pandas.DataFrame(rapor_sayim_sonuc_rapor).drop(["id", "created_at", "is_sayim_sonrasi"], axis=1)
    rapor_sayim_sonrasi_envanter_df = pandas.DataFrame(rapor_sayim_sonrasi_envanter).drop(["id"], axis=1)

    rapor_sayim_sonrasi_envanter_df.to_excel(writer, sheet_name="Sayım Envanter")
    rapor_sayim_sonuc_rapor_df.to_excel(writer, sheet_name="Sayım Raporu")

    writer.save()

    mail_subject = f"{rapor.saha_no} - {rapor.saha_kod} {rapor.id} nolu Sayım Raporu, {rapor.user}"

    email = EmailMessage(subject=mail_subject, body=mail_body, from_email="rapor@scor-app.com",
                         to=email_list)
    email.attach_file(output_path)

    email.send()

    os.remove(output_path)

    return JsonResponse({"msg":"Success"})


@login_required(login_url="/login")
def updateAciklama(request):
    girdi_id = str(request.GET["girdi_id"])
    try:
        girdi = GlobalSayimRapor.objects.get(id=girdi_id)
    except:
        print("girdi bulunamadı")
    girdi.aciklama = request.GET["aciklama"]
    girdi.save()

    log = Log(user=request.user)
    log.description = f"{request.user} Adlı Kullanıcı {girdi.saha_no} Saha No ve {girdi.saha_kod} Saha Kodlu {girdi_id} Id'sine Sahip Girdinin Açıklamasını {girdi.aciklama} Şeklinde Değiştirdi."
    log.saha_no = girdi.saha_no
    log.saha_kod = girdi.saha_kod
    log.save()

    return JsonResponse({"Msg":"Success"})




"""
global rapor views

"""


@csrf_exempt
@login_required(login_url="users:login")
def globalrapor(request):
    if request.method == "GET":
        return render(request,'globalrapor.html')

    elif request.method == "POST":
        if 'saha_no' in request.POST:
            saha_no = request.POST.get("saha_no").upper().strip()
            saha_envater = GlobalSayimRapor.objects.filter(Q(saha_no=saha_no) | Q(saha_kod=saha_no))

            return render(request,'globalrapor.html', {'saha_envater':saha_envater})

        elif 'globalrun' in request.POST:
            rapor_calistir_V6()
            message = "Güncelleme Tamamlanmıştır"
            return render(request,'globalrapor.html', {'message':message})
