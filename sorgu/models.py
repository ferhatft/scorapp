from django.db import models

# Create your models here.

# SorguList --> Sorgular
class Sorgular(models.Model):
    sorgu_no = models.CharField(verbose_name="Sorgu No", max_length=5000, default="")
    kontrol = models.CharField(verbose_name="Kontrol", max_length=5000, default="")
    ref_grup = models.CharField(verbose_name="Ref Grup", max_length=5000, default="")
    kategori = models.CharField(verbose_name="Kategori", max_length=5000, default="")
    check = models.CharField(verbose_name="Check", max_length=5000, default="")

    class Meta:
        verbose_name = "Sorgu"
        verbose_name_plural = "Sorgular"


# RaporReferanslari --> SorguReferanslari
class SorguReferanslari(models.Model):

    sorgu_no = models.CharField(verbose_name="Sorgu No", max_length=5000, default="")
    ref = models.CharField(verbose_name="Ref", max_length=5000, default="")
    ekipman_parca_kodu = models.CharField(verbose_name="Ekipman Parça Kodu", max_length=5000, default="")
    parca_tanimi = models.CharField(verbose_name="Parça Tanımı", max_length=5000, default="")
    grup_tanimi = models.CharField(verbose_name="Grup Tanımı", max_length=5000, default="")
    rapor_tanimi = models.CharField(verbose_name="Rapor Tanımı", max_length=5000, default="")
    ref_grup = models.CharField(verbose_name="Ref Grup", max_length=5000, default="")
    kategori = models.CharField(verbose_name="Kategori", max_length=5000, default="")
    analiz_no = models.CharField(verbose_name="Analiz No", max_length=5000, default="")

    class Meta:
        verbose_name = "Sorgu Referans"
        verbose_name_plural = "Sorgu Referansları"
