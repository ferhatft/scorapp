from django.db import models
from rapor.models import Rapor
# Create your models here.


#  RaporEnvanter  ---> TerminalSayim
class TerminalSayim(models.Model):
    saha_no = models.CharField(verbose_name="Saha No", max_length=50, default="")
    user = models.CharField(verbose_name="Kullanıcı Adı", max_length=50, default="")
    seri_no = models.CharField(verbose_name="Seri No", max_length=5000, default="")
    parca_kodu = models.CharField(verbose_name="Parça Kodu", max_length=5000, default="")
    parca_tanimi = models.CharField(verbose_name="Parça Tanımı", max_length=5000, default="")
    bolge = models.CharField(verbose_name="Bölge", max_length=5000, default="")
    miktar = models.IntegerField(verbose_name="Miktar", default=0)
    sayim_fark = models.IntegerField(verbose_name="Sayım Fark", default=0)
    transfer_adet = models.IntegerField(verbose_name="Transfer Adet", default=0)
    sonuc = models.CharField(verbose_name="Sonuç", max_length=9999, default="")
    durum = models.CharField(verbose_name="Durum", max_length=9999, default="")
    lokasyon = models.CharField(verbose_name="Lokasyon", max_length=9999, default="")
    aciklama = models.CharField(verbose_name="Açıklama", max_length=99999, default="")
    rapor = models.ForeignKey(Rapor, on_delete=models.CASCADE, related_name="rapor_envanter")

    class Meta:
        verbose_name = "Terminal Sayım Envanter"
        verbose_name_plural = "Terminal Sayım Envanter"


#  30 undan sonra android sayım entegresi yapılacak
class AndroidSayim(models.Model):
    parca_kodu                  = models.CharField(verbose_name="Parça Kodu", max_length=70, blank=True, null=True, unique=True)
    saha_kodu                   = models.CharField(verbose_name="Saha Kodu", max_length=70, blank=True, null=True, unique=True)
    saha_no                     = models.CharField(verbose_name="Saha No", max_length=70, blank=True, null=True, unique=True)
    department                  = models.CharField(verbose_name="Department", max_length=70, blank=True, null=True, unique=True)
    parca_tanimi                = models.CharField(verbose_name="Parça Tanımı", max_length=70, blank=True, null=True, unique=True)
    sirket                      = models.CharField(verbose_name="Sirket", max_length=70, blank=True, null=True, unique=True)
    saha_tipi                   = models.CharField(verbose_name="Saha Tipi", max_length=70, blank=True, null=True, unique=True)
    parca_kodu_tipi             = models.CharField(verbose_name="Parça Kodu Tipi", max_length=70, blank=True, null=True, unique=True)
    il                          = models.CharField(verbose_name="İl", max_length=70, blank=True, null=True, unique=True)
    organizasyon                = models.CharField(verbose_name="Organizasyon", max_length=70, blank=True, null=True, unique=True)
    eldeki_miktar               = models.IntegerField(verbose_name="Eldeki Miktar",  )
    kalem_dogruluk_orani        = models.IntegerField(verbose_name="Kalem Dogruluk Orani",  )
    nihai_sayim                 = models.IntegerField(verbose_name="Nihai Sayim",  )
    sayim_baslangic_tarihi      = models.DateField(verbose_name="Sayim Baslangiç Tarihi", blank=True, null=True)
    sayim_bitis_tarihi          = models.DateField(verbose_name="Sayim Bitis Tarihi", blank=True, null=True)
    sayim_dogrulugu             = models.IntegerField(verbose_name="Sayim Dogrulugu",  )
    sayim_kullanici_tipi        = models.CharField(verbose_name="Sayim Kullanici Tipi", max_length=70, blank=True, null=True, unique=True)
    sayim_kullanicisi           = models.CharField(verbose_name="Sayim Kullanicisi", max_length=70, blank=True, null=True, unique=True)
    sayim_no                    = models.CharField(verbose_name="Sayim No", max_length=70, blank=True, null=True, unique=True)


    def __str__(self):
        return self.parca_kodu

    def save(self,*args,**kwargs):
        return super(AndroidSayim, self).save(*args, **kwargs)
        


