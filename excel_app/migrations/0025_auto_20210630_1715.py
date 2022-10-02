# Generated by Django 3.2.3 on 2021-06-30 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excel_app', '0024_userprofile_denetci'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='departmanlar',
            options={'verbose_name': 'Bölge Mail Liste', 'verbose_name_plural': 'Bölge Mail Listeleri'},
        ),
        migrations.AlterModelOptions(
            name='rapor',
            options={'verbose_name': 'Kontrol-Bakım Raporu', 'verbose_name_plural': 'Kontrol-Bakım Raporları'},
        ),
        migrations.AlterModelOptions(
            name='raporenvanter',
            options={'verbose_name': 'Terminal Sayım Rapor', 'verbose_name_plural': 'Terminal Sayım Raporları'},
        ),
        migrations.AlterModelOptions(
            name='raporreferanslari',
            options={'verbose_name': 'Sorgu Referans', 'verbose_name_plural': 'Sorgu Referansları'},
        ),
        migrations.AlterModelOptions(
            name='sayimoncesienvanter',
            options={'verbose_name': 'Bakım Uyumsuzluk Rapor', 'verbose_name_plural': 'Bakım Uyumsuzluk Raporları'},
        ),
        migrations.AlterModelOptions(
            name='sayimrapor',
            options={'verbose_name': 'Kontro Uyumsuzluk Rapor', 'verbose_name_plural': 'Kontrol Uyumsuzluk Raporları'},
        ),
        migrations.AlterModelOptions(
            name='sayimsonrasienvanter',
            options={'verbose_name': 'Bakım Sonrası Envanter', 'verbose_name_plural': 'Bakım Sonrası Envanterları'},
        ),
        migrations.AlterModelOptions(
            name='sorgulist',
            options={'verbose_name': 'Sorgu Listesi', 'verbose_name_plural': 'Sorgu Listeleri'},
        ),
    ]