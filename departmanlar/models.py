from django.db import models


# Create your models here.
class Departmanlar(models.Model):
    code = models.CharField(verbose_name="Departman Kodu", max_length=9999)
    emails = models.TextField(verbose_name="Email Listesi", help_text="Mailleri Her Satıra Bir Tane Gelecek Şekilde Yazın")

    class Meta:
        verbose_name = "Bölge Mail Liste"
        verbose_name_plural = "Bölge Mail Listeleri"

    def __str__(self):
        return self.code