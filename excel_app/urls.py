from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path
from django.urls.conf import include
from eht.views import envanter_tarihcesi
from envanter.views import envanter
from parcakodlari.views import parcakodu
from rapor.views import (bakimRaporOlustur, scorraporcreate, globalrapor,
                         raporHatali, raporOnayla, resim_ekle, satirEkle,
                         satirSil, sayimSonucRaporuOlustur, scorsayimupdate,
                         sendMailKontrolRapor, sendMailRapor, updateAciklama)
from sahalistesi.views import sahalistesi
from sayim.views import kontrolRaporOlustur, terminal_acıklama_update

from .views import CustomLoginView, SignUpView, permissionDenied

urlpatterns = [
    path('resimekle/<int:pk>/',resim_ekle,name="resim_ekle"),
    path('', CustomLoginView.as_view()),
    path("updateAciklama/", updateAciklama),
    path('register/', SignUpView.as_view()),
    path('bakimRapor/', bakimRaporOlustur,name='bakimRaporOlustur'),
    path('parcakodu/', parcakodu,name="parcakodu"),
    path('envanter/', envanter, name="envanter"),
    path('sahalistesi/',sahalistesi, name="sahalistesi"),
    path('globalrapor/',globalrapor, name="globalrapor"),


    path('login/', CustomLoginView.as_view(), name='login'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('accounts/', include('django.contrib.auth.urls')),
    path("kontroleGonder/", sendMailRapor),
    path("scorsayimupdate/", scorsayimupdate),
    path("sayimSonucRaporuOlustur/", sayimSonucRaporuOlustur,name='sayimSonucRaporuOlustur'),

    path("raporOnayla/", raporOnayla),
    path("raporHatali/", raporHatali),

    path("kontrolRaporlar/", kontrolRaporOlustur),
    path('envanter-tarihcesi/', envanter_tarihcesi,name="envanter_tarihcesi"),
    path('envanter-tarihcesi/send-scor/', scorraporcreate,name="scorraporcreate"),

    path('raporEmaille/', sendMailKontrolRapor),
    path("satirEkle/", satirEkle),
    path("terminal_acıklama_update/", terminal_acıklama_update),
    path("permissionDenied/", permissionDenied),
    #path("bakimHamVeriOlustur/", bakimHamVeriOlustur),
    #path("import_ekipman_hareketi/", import_ekipman_hareketi),
    path("satirSil/", satirSil)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.sites.AdminSite.site_header = 'Scor'
admin.sites.AdminSite.site_title = 'Scor'
admin.sites.AdminSite.index_title = 'Scor Rapor Paneline Hoş Geldiniz'
