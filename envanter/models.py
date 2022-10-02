from django.db import models

# Create your models here.
from rapor.models import Rapor

 
#SayimOncesiEnvanter --> Envanter
class Envanter(models.Model):
    saha_no = models.CharField(verbose_name="Saha No", max_length=50, default="")
    saha_kodu = models.CharField(verbose_name="Saha Kod", max_length=50, default="")
    saha_tipi = models.CharField(verbose_name="Saha Tipi", max_length=5000, default="")
    yer_tipi = models.CharField(verbose_name="Yer Tipi", max_length=5000, default="")
    ekipman_seri_no = models.CharField(verbose_name="Ekipman Seri No", max_length=5000, default="")
    ekipman_parca_kodu = models.CharField(verbose_name="Ekipman Parça Kodu", max_length=5000, default="")
    parca_tanimi = models.CharField(verbose_name="Parça Tanımı", max_length=5000, default="")
    kurulumu_tarihi = models.CharField(verbose_name="Tarih", max_length=5000, default="")
    department_code = models.CharField(verbose_name="Department", max_length=5000, default="")
    quantity = models.IntegerField(verbose_name="Quantity", default=0)
    ustekipman = models.CharField(verbose_name="Üst Ekipman", max_length=5000, default="")
    created_at = models.DateTimeField(verbose_name="Oluşturulma Tarihi", auto_now_add=True)

class Meta:
        verbose_name = "Envanter"
        verbose_name_plural = "Envanterler"




class NewEnvanter(models.Model):
    saha_no                         = models.CharField(verbose_name="Saha No", max_length=70, blank=True, null=True, unique=True)
    saha_kodu                       = models.CharField(verbose_name="Saha Kodu", max_length=70, blank=True, null=True, unique=True)
    kts_saha_no                     = models.CharField(verbose_name="KTS Saha No", max_length=70, blank=True, null=True, unique=True)
    saha_tipi                       = models.CharField(verbose_name="Saha Tipi", max_length=70, blank=True, null=True, unique=True)
    ana_yer_tipi                    = models.CharField(verbose_name="Ana Yer Tipi", max_length=70, blank=True, null=True, unique=True)
    ekipman_no                      = models.CharField(verbose_name="Ekipman No", max_length=70, blank=True, null=True, unique=True)
    seri_no                         = models.CharField(verbose_name="Seri No", max_length=70, blank=True, null=True, unique=True)
    parca_kodu                      = models.CharField(verbose_name="Parça Kodu", max_length=70, blank=True, null=True, unique=True)
    parca_tanimi                    = models.CharField(verbose_name="Parça Tanımı", max_length=250, blank=True, null=True, unique=True)
    stok_tipi_1                     = models.CharField(verbose_name="Stok Tipi 1", max_length=70, blank=True, null=True, unique=True)
    stok_tipi_2                     = models.CharField(verbose_name="Stok Tipi 2", max_length=70, blank=True, null=True, unique=True)
    stok_tipi_3                     = models.CharField(verbose_name="Stok Tipi 3", max_length=70, blank=True, null=True, unique=True)
    stok_tipi_4                     = models.CharField(verbose_name="Stok Tipi 4", max_length=70, blank=True, null=True, unique=True)
    stok_tipi_5                     = models.CharField(verbose_name="Stok Tipi 5", max_length=70, blank=True, null=True, unique=True)
    stok_tipi_6                     = models.CharField(verbose_name="Stok Tipi 6", max_length=70, blank=True, null=True, unique=True)
    stok_tipi_7                     = models.CharField(verbose_name="Stok Tipi 7", max_length=70, blank=True, null=True, unique=True)
    stok_tipi_8                     = models.CharField(verbose_name="Stok Tipi 8", max_length=70, blank=True, null=True, unique=True)
    teslim_alma_tarihi              = models.DateTimeField(verbose_name="Teslim Alma Tarihi", blank=True, null=True)
    sahaya_kurulum_tarihi           = models.DateTimeField(verbose_name="Sahaya Kurulum Tarihi", blank=True, null=True)
    sirket                          = models.CharField(verbose_name="Sirket", max_length=70, blank=True, null=True, unique=True)
    organizasyon                    = models.CharField(verbose_name="Organizasyon", max_length=70, blank=True, null=True, unique=True)
    department                      = models.CharField(verbose_name="Department", max_length=70, blank=True, null=True, unique=True)
    quantity                        = models.IntegerField(verbose_name="Quantity", blank=True, null=True,)



    def __str__(self):
        return self.parca_kodu

    def save(self,*args,**kwargs):
        return super(Envanter, self).save(*args, **kwargs)


varyasyon_secimi = (
  ('sarf','sarf'),
  ('seri','seri')
)

class EnvanterTarihcesi(models.Model):
    
    variation_category = models.CharField(max_length=64,choices=varyasyon_secimi,default='sarf')
    parca_kodu                      = models.CharField(verbose_name="Parça Kodu", max_length=70, blank=True, null=True, unique=True)
    saha_kodu                       = models.CharField(verbose_name="Saha Kodu", max_length=70, blank=True, null=True, unique=True)
    sirket                          = models.CharField(verbose_name="Sirket", max_length=70, blank=True, null=True, unique=True)
    kullanici_adi                   = models.CharField(verbose_name="Kullanici Adi", max_length=70, blank=True, null=True, unique=True)
    olcum_birimi                    = models.CharField(verbose_name="Olcum Birimi", max_length=70, blank=True, null=True, unique=True)
    parca_kodu_tipi                 = models.CharField(verbose_name="Parça Kodu Tipi", max_length=70, blank=True, null=True, unique=True)
    birim_maliyet                   = models.DecimalField(verbose_name="Birim Maliyet", max_digits=50 ,decimal_places=2 )
    form_no                         = models.CharField(verbose_name="Form No", max_length=70, blank=True, null=True, unique=True)
    hedef_departman                 = models.CharField(verbose_name="Hedef Departman", max_length=70, blank=True, null=True, unique=True)
    islem_miktari                   = models.IntegerField(verbose_name="Islem Miktari",  )
    islem_no                        = models.CharField(verbose_name="Islem No", max_length=70, blank=True, null=True, unique=True)
    islem_tarihi                    = models.DateTimeField(verbose_name="Islem Tarihi", blank=True, null=True)
    islem_tipi                      = models.CharField(verbose_name="Islem Tipi", max_length=70, blank=True, null=True, unique=True)
    kalem_kategori                  = models.CharField(verbose_name="Kalem Kategori", max_length=70, blank=True, null=True, unique=True)
    kaynak_departman                = models.CharField(verbose_name="Kaynak Departman", max_length=70, blank=True, null=True, unique=True)
    kaynak_organizasyon_kodu        = models.CharField(verbose_name="Kaynak Organizasyon Kodu", max_length=70, blank=True, null=True, unique=True)
    kaynak_stok_adresi              = models.CharField(verbose_name="Kaynak Stok Adresi", max_length=70, blank=True, null=True, unique=True)
    kaynak_stok_yeri                = models.CharField(verbose_name="Kaynak Stok Yeri", max_length=70, blank=True, null=True, unique=True)
    kaynak_surec                    = models.CharField(verbose_name="Kaynak Surec", max_length=70, blank=True, null=True, unique=True)
    referans                        = models.CharField(verbose_name="Referans", max_length=70, blank=True, null=True, unique=True)
    transfer_organizasyon_kodu      = models.CharField(verbose_name="Transfer Organizasyon Kodu", max_length=70, blank=True, null=True, unique=True)
    transfer_stok_adresi            = models.CharField(verbose_name="Transfer Stok Adresi", max_length=70, blank=True, null=True, unique=True)
    transfer_stok_yeri              = models.CharField(verbose_name="Transfer Stok Yeri", max_length=70, blank=True, null=True, unique=True)
    source_code                     = models.CharField(verbose_name="Source Code", max_length=70, blank=True, null=True, unique=True)
    parca_kodu                      = models.CharField(verbose_name="Parça Kodu", max_length=70, blank=True, null=True, unique=True)
    saha_no                         = models.CharField(verbose_name="Saha No", max_length=70, blank=True, null=True, unique=True)
    parca_tanimi                    = models.CharField(verbose_name="Parça Tanımı", max_length=70, blank=True, null=True, unique=True)
    seri_no                         = models.CharField(verbose_name="Seri No", max_length=70, blank=True, null=True, unique=True)
    ıs_emri                         = models.CharField(verbose_name="Is Emri", max_length=70, blank=True, null=True, unique=True)
    onent_kullanici                 = models.CharField(verbose_name="ONENT Kullanici", max_length=70, blank=True, null=True, unique=True)


    def __str__(self):
        return self.parca_kodu

    def save(self,*args,**kwargs):
        return super(EnvanterTarihcesi, self).save(*args, **kwargs)

