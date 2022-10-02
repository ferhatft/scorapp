# Generated by Django 3.2.3 on 2022-09-14 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParcaKodlari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parca_kodu', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Parça Kodu')),
                ('parca_tanimi', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Parça Tanımı')),
                ('aciklama', models.CharField(blank=True, max_length=250, null=True, unique=True, verbose_name='Açıklama')),
                ('olcum_birimi', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Olcum Birimi')),
                ('parca_kodu_tipi', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Parça Kodu Tipi')),
                ('referans_grup', models.CharField(blank=True, max_length=250, null=True, unique=True, verbose_name='Referans Grup')),
                ('referans_kategorisi', models.CharField(blank=True, max_length=250, null=True, unique=True, verbose_name='Referans Kategorisi')),
                ('muadil_parca_kodu', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Muadil Parça Kodu')),
                ('referans_grup_1', models.CharField(blank=True, max_length=250, null=True, unique=True, verbose_name='Referans Grup-1')),
                ('referans_grup_2', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Referans Grup-2')),
                ('referans_grup_3', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Referans Grup-3')),
                ('referans_grup_4', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Referans Grup-4')),
                ('referans_grup_5', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Referans Grup-5')),
            ],
        ),
    ]
