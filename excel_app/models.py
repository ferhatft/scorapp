from departmanlar.models import Departmanlar
from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.db.models.fields import related
from django.dispatch import receiver
from rapor.models import Rapor

User._meta.get_field('email')._unique = True

"""
log+ auth uygulaması oluşturulacak.

mail + password ile login olacak ileride.
"""


class Log(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Kullanıcı")
    aksiyon = models.CharField(verbose_name="Aksiyon", max_length=50, default="")
    saha_no = models.CharField(verbose_name="Saha No", max_length=50, default="")
    saha_kod = models.CharField(verbose_name="Saha Kod", max_length=50, default="")
    description = models.TextField(verbose_name="Yaptığı İşlem", max_length=9999999, default="")
    created_at = models.DateTimeField(verbose_name="Oluşturulma Tarihi", auto_now_add=True)

    def __str__(self):
        return self.user.username


class Detay(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, verbose_name="Kullanıcı")
    aksiyon = models.CharField(verbose_name="Aksiyon", max_length=50, default="")
    saha_no = models.CharField(verbose_name="Saha No", max_length=50, default="")
    saha_kod = models.CharField(verbose_name="Saha Kod", max_length=50, default="")

    description = models.TextField(verbose_name="Yaptığı İşlem", max_length=9999999, default="")
    created_at = models.DateTimeField(verbose_name="Oluşturulma Tarihi", auto_now_add=True)

    def __str__(self):
        return self.user.username


class UserProfile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, related_name="profile")
    department_code = models.CharField(verbose_name="Departman Kodu", max_length=50)
    kontrolcu = models.BooleanField(verbose_name="Kontrolcü", default=False)
    bakimci = models.BooleanField(verbose_name="Bakımcı", default=False)
    denetci = models.BooleanField(verbose_name="Denetçi", default=False)
    master = models.BooleanField(verbose_name="Master", default=False)

    def __str__(self):
        return self.user.username or self.user.email

@receiver(signals.post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)



"""
import edilen her dosya daha sonra silinmesi gerekiyor 

envanter ve terminal raporları şuanda silinmiyor aynı şekilde android raporları da çalışmıyor onların güncelleme yapıldığında eski xls dosyalarının silinmesi gerekiyor.

"""
class TemporaryExcelFiles(models.Model):
    """ Excel dosyaları üzerinde işlem yapabilmek için kurduğumuz geçici bir
    veri tabanı (her işlemden sonra temizlenir.)
     """
    file = models.FileField(upload_to='sheets/')
