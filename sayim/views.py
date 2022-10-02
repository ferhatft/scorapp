import pandas
from api.serializers import UserPublicSerializer
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.db.models import Value
from django.db.models.functions import Replace
from django.http.response import JsonResponse
from django.shortcuts import render
from envanter.models import Envanter
from excel_app.decorators import authUser
from excel_app.models import Detay, Log
from rapor.models import Rapor
from rapor.views import getHamVeriAndCreate
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AndroidSayim, TerminalSayim

#  ikiye bölünecek elif kısmı import exportta olacak 
#  elif --> envanter import 
#  if -->  androidraporcreate
@login_required(login_url="/login")
@authUser(permission_user="kontrolcu")
def kontrolRaporOlustur(request):
    if request.method == "GET":
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
                # Envanter.objects.filter(department_code=request.user.profile.department_code).delete()
                # for row in ham_veri.to_dict(orient="records"):

                departman = ham_veri.drop_duplicates(subset ="Department Code")
                departman = departman.to_dict(orient="records")

                for row in departman:
                    department_code=row["Department Code"]


                    Envanter.objects.filter(department_code=department_code).delete()

                    departman_veri = pandas.DataFrame(ham_veri[ham_veri['Department Code'] == department_code])
                    dict_data = departman_veri.to_dict(orient="records")
                    print("dict_data")
                    print(dict_data)
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
                        print("hamveri_girdi")
                        print(hamveri_girdi)

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



@login_required(login_url="/login")
def terminal_acıklama_update(request):
    girdi_id = request.GET.get("girdi_id")
    girdi = TerminalSayim.objects.get(id=girdi_id)
    girdi.aciklama = request.GET.get("aciklama")
    girdi.save()

    log = Log(user=request.user)
    log.description = f"{request.user} Adlı Kullanıcı Rapor Envanterindeki {girdi.saha_no} Saha No ve {girdi.user} Saha Kodlu {girdi_id} Id'sine Sahip Girdinin Açıklamasını {girdi.aciklama} Şeklinde Değiştirdi."
    log.saha_no = girdi.saha_no
    log.saha_kod = girdi.user
    log.save()

    return JsonResponse({"Msg":"Success"})

















"""
for use of api endpoint
"""
class ListApiAndroidSayım(ListAPIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    queryset = AndroidSayim.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAdminUser]
    
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAdminUser]




"""
Return as a queryset to the html .
"""

class ListAndroidSayım(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'mypage.html'
    # authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        queryset =  AndroidSayim.objects.all()
        context = {
            'queryset':queryset,

        }    
        return Response(context)





# class ListAndroidSayım(APIView):
#     """
#     View to list all users in the system.

#     * Requires token authentication.
#     * Only admin users are able to access this view.
#     """
    
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAdminUser]

#     def get(self, request, format=None):
#         """
#         Return a list of all users.
#         """
#         android_sayim = [obj.username for obj in AndroidSayim.objects.all()]
#         return Response(android_sayim)
