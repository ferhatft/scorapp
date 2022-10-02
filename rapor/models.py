from departmanlar.models import Departmanlar
from django.db import models


# Create your models here.
class Rapor(models.Model):
    user = models.ForeignKey("auth.User", related_name="raporlar", on_delete=models.SET_NULL, null=True, blank=True)
    saha_no = models.CharField(verbose_name="Saha No", max_length=9999, default="")
    saha_kod = models.CharField(verbose_name="Saha Kodu", max_length=9999, default="")
    created_at = models.DateTimeField(verbose_name="Oluşturulma Tarihi", auto_now_add=True)
    department_code = models.ForeignKey(Departmanlar, on_delete=models.SET_DEFAULT, default="", null=True, blank=True,related_name="Department_code")
    onay = models.BooleanField(verbose_name="Rapor Onaylı'mı?", default=False)
    child = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    hatali = models.BooleanField(verbose_name="Hatalı mı?", default=False)

    class Meta:
        verbose_name = "Kontrol-Bakım Raporu"
        verbose_name_plural = "Kontrol-Bakım Raporları"

    def __str__(self):
        return f"{self.saha_no} Saha No'suna Ait {self.id} ID'li Rapor"


#SayimSonrasiEnvanter --> ScorSayım
class ScorSayım(models.Model):
    saha_no = models.CharField(verbose_name="Saha No", max_length=50, default="")
    saha_kodu = models.CharField(verbose_name="Saha Kod", max_length=50, default="")
    ekipman_seri_no = models.CharField(verbose_name="Ekipman Seri No", max_length=5000, default="")
    ekipman_parca_kodu = models.CharField(verbose_name="Ekipman Parça Kodu", max_length=5000, default="")
    parca_tanimi = models.CharField(verbose_name="Parça Tanımı", max_length=5000, default="")
    department_code = models.CharField(verbose_name="Department", max_length=5000, default="")
    quantity = models.IntegerField(verbose_name="Quantity", default="")
    aciklama = models.CharField(verbose_name="Açıklama", max_length=5000, default="")
    sayim = models.IntegerField(verbose_name="Sayim", default=0)
    rapor = models.ForeignKey(Rapor, on_delete=models.CASCADE, related_name="sayim_sonrasi_envanter")
    image = models.ImageField(upload_to="images/",blank=True,null=True)

    class Meta:
        verbose_name = "Bakım Sonrası Envanter"
        verbose_name_plural = "Bakım Sonrası Envanterları"

# SayimRapor --> ScorRapor
class ScorRapor(models.Model):
    saha_no = models.CharField(verbose_name="Saha No", max_length=50, default="")
    saha_kod = models.CharField(verbose_name="Saha Kod", max_length=50, default="")
    ref_1 = models.IntegerField(verbose_name="Referans-1")
    ref_2 = models.IntegerField(verbose_name="Referans-2")
    ref_3 = models.IntegerField(verbose_name="Referans-3")
    ref_4 = models.IntegerField(verbose_name="Referans-4")
    ref_5 = models.IntegerField(verbose_name="Referans-5")
    ref_6 = models.IntegerField(verbose_name="Referans-6")
    ref_grup = models.CharField(verbose_name="Ref Grup", max_length=5000, default="")
    sonuc = models.CharField(verbose_name="Sonuç", max_length=50, default="")
    kontrol = models.CharField(verbose_name="Kontrol", max_length=5000, default="")
    kategori = models.CharField(verbose_name="Kategori", max_length=50, default="")
    sorgu_no = models.CharField(verbose_name="Sorgu No", max_length=50, default="")
    aciklama = models.CharField(verbose_name="Açıklama", max_length=5000,blank=True,null=False, default="")
    rapor = models.ForeignKey(Rapor, related_name="girdiler", on_delete=models.CASCADE)

    is_sayim_sonrasi = models.BooleanField(verbose_name="Sayım Sonrası Girdisi Mi?", default=False)
    created_at = models.DateTimeField(verbose_name="Oluşturulma Tarihi", auto_now_add=True)

    class Meta:
        verbose_name = "Kontro Uyumsuzluk Rapor"
        verbose_name_plural = "Kontrol Uyumsuzluk Raporları"

    def serializer(self):
        return {
            "saha_no":self.saha_no,
            "saha_kod":self.saha_kod,
            "ref_1":self.ref_1,
            "ref_2":self.ref_2,
            "ref_3":self.ref_3,
            "ref_4":self.ref_4,
            "ref_5":self.ref_5,
            "ref_6":self.ref_6,
            "ref_grup":self.ref_grup,
            "sonuc":self.sonuc,
            "kontrol":self.kontrol,
            "sorgu_no":self.sorgu_no,

        }

    def __str__(self):
        return self.kontrol


# GlobalSayimRapor --> GlobalRapor  yapılacak
class GlobalSayimRapor(models.Model):
    saha_no = models.CharField(verbose_name="Saha No", max_length=50, default="")
    saha_kod = models.CharField(verbose_name="Saha Kod", max_length=50, default="")
    ref_1 = models.IntegerField(verbose_name="Referans-1")
    ref_2 = models.IntegerField(verbose_name="Referans-2")
    ref_3 = models.IntegerField(verbose_name="Referans-3")
    ref_4 = models.IntegerField(verbose_name="Referans-4")
    ref_5 = models.IntegerField(verbose_name="Referans-5")
    ref_6 = models.IntegerField(verbose_name="Referans-6")
    ref_grup = models.CharField(verbose_name="Ref Grup", max_length=250, default="")
    sonuc = models.CharField(verbose_name="Sonuç", max_length=50, default="")
    kontrol = models.CharField(verbose_name="Kontrol", max_length=250, default="")
    kategori = models.CharField(verbose_name="Kategori", max_length=50, default="")
    sorgu_no = models.CharField(verbose_name="Sorgu No", max_length=50, default="")
    department_code = models.CharField(verbose_name="Department", max_length=5000, default="")
    aciklama = models.CharField(verbose_name="Açıklama", max_length=250,blank=True,null=False, default="")
    created_at = models.DateTimeField(verbose_name="Oluşturulma Tarihi", auto_now_add=True)
    update_at = models.DateTimeField(verbose_name="Güncelleme Tarihi", blank=True, null=True)

    class Meta:
        verbose_name = "Global Uyumsuzluk Rapor"
        verbose_name_plural = "Global Uyumsuzluk Raporları"

    def __str__(self):
        return self.kontrol
