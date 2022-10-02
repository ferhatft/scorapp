from django.db import models

# Create your models here.


class Parcakodu(models.Model):
    ekipman_tipi                = models.CharField(verbose_name="Tip", max_length=10, default="")
    olcum_birimi                = models.CharField(verbose_name="Birim", max_length=10, default="")
    parca_kodu                  = models.CharField(verbose_name="Ekipman Parça Kodu", max_length=50, default="")
    parca_tanimi                = models.CharField(verbose_name="Parça Tanımı", max_length=250, default="")
    grup_tanimi                 = models.CharField(verbose_name="Grup Tanımı", max_length=250, default="")
    ekip_tanimi                 = models.CharField(verbose_name="Ekip Tanımı", max_length=250, default="")
    ekip_aciklama               = models.CharField(verbose_name="Ekip Açıklama", max_length=250, default="")
    muadil                      = models.CharField(verbose_name="Muadil", max_length=500, default="")

    class Meta:
        verbose_name = "Parça Kodu"
        verbose_name_plural = "Parça Kodu Listesi"

    def __str__(self):
        return self.parca_kodu
