from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework import authentication, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from api.serializers import GlobalRaporSerializer

import pandas
from django.contrib.auth.decorators import login_required
from .models import Parcakodu
from eht.models import Envanter_Tarihcesi

"""
# parcakoduviwe --> parcakoduview  --> parcakodu

"""
@login_required(login_url="/login")
def parcakodu(request):

    if request.method == "POST":

        #Parcakodu.objects.all().delete()
        #eht_parca_kodlari = SayimOncesiEnvanter.objects.values_list('ekipman_parca_kodu', 'parca_tanimi').distinct()
        #parca_kodlari_all = pandas.DataFrame(eht_parca_kodlari)


        eht_parca_kodlari = Envanter_Tarihcesi.objects.values_list('parca_kodu', 'parca_tanimi','olcum_birimi','ekipman_tipi').distinct()
        parca_kodlari_all = pandas.DataFrame(eht_parca_kodlari)
        #dict_data = parca_kodlari_all.to_dict(orient="records")

        #parca_kodlari_list = Parcakodu.objects.values_list('parca_kodu', 'parca_tanimi').distinct()
        parca_kodlari_list = Parcakodu.objects.values_list('parca_kodu', 'parca_tanimi','olcum_birimi','ekipman_tipi').distinct()
        parca_kodlari_list = pandas.DataFrame(parca_kodlari_list)

        merged = parca_kodlari_list.merge(parca_kodlari_all, how='right', indicator=True).query('_merge == "right_only"').drop('_merge', 1)
        dict_data = merged.to_dict(orient="records")

        parcalar_list = []

        for row in dict_data:
            parca_kodu = row[0]
            parca_tanimi = row[1]
            olcum_birimi = row[2]
            ekipman_tipi = row[3]

            parcalar = Parcakodu(parca_kodu=parca_kodu, parca_tanimi=parca_tanimi,olcum_birimi=olcum_birimi,ekipman_tipi=ekipman_tipi)
            parcalar_list.append(parcalar)

        Parcakodu.objects.bulk_create(parcalar_list, batch_size=999999999999)

    #Parcakodu.objects.all().delete()
    parcakodulistesi = Parcakodu.objects.all()

    context = {
        'parcakodulistesi': parcakodulistesi
    }

    return render(request, "parcakodu.html", context)
