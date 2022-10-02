from django.db import models

# Create your models here.


class SahaListesi(models.Model):
    saha_kodu = models.CharField(max_length=400,blank=True,null=True)
    saha_no = models.CharField(max_length=400,blank=True,null=True)
    department_code = models.CharField(max_length=400,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated = models.DateTimeField(auto_now=True,blank=True,null=True)
    yer_tipi = models.CharField(max_length=400,blank=True,null=True)
    saha_tipi = models.CharField(max_length=400,blank=True,null=True)
    STATUS_CHOISES = [
        ('A','Aktif'),
        ('P','Pasif'),
    ]
    status = models.CharField(max_length=2,choices=STATUS_CHOISES,default="A")

    def __str__(self):
        return self.saha_kodu