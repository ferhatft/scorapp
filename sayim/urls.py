from django.urls import path 
from .views import * 

urlpatterns = [
  path('', ListAndroidSayım.as_view() , name="api_home")
]