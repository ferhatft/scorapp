from django.db import models

# Create your models here.


#Ekipman_Hareketi --> Envanter_Tarihcesi
class Envanter_Tarihcesi(models.Model):
    islem_no = models.CharField(max_length=500,blank=True,null=True)
    islem_tarihi = models.CharField(max_length=500,blank=True,null=True)
    parca_kodu = models.CharField(max_length=500,blank=True,null=True)
    parca_tanimi = models.CharField(max_length=500,blank=True,null=True)
    islem_miktari = models.IntegerField(blank=True,null=True)
    olcum_birimi = models.CharField(max_length=500,blank=True,null=True)
    kaynak_yeri = models.CharField(max_length=500,blank=True,null=True)
    islem_tipi = models.CharField(max_length=500,blank=True,null=True)
    form_no = models.CharField(max_length=500,blank=True,null=True)
    hedef_departman = models.CharField(max_length=500,blank=True,null=True)
    hedef_lokasyon = models.CharField(max_length=500,blank=True,null=True)
    kullanici_adi = models.CharField(max_length=500,blank=True,null=True)
    ekipman_tipi = models.CharField(max_length=500,blank=True,null=True)
    seri_no = models.CharField(max_length=500,blank=True,null=True)
    maliyet = models.CharField(max_length=500,blank=True,null=True)

    def __str__(self):
        return self.islem_no
        
