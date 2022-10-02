from django.urls import path 
from sayim.views import * 
from envanter.views import ListApiEnvanterSayım
urlpatterns = [
  path('android_sayim/', ListAndroidSayım.as_view() , name="android_sayim"),
  path('android_sayimv2/', ListApiAndroidSayım.as_view() , name="android_sayim"),
  path('envanter/', ListApiEnvanterSayım.as_view(),name="envanter")
]