# Generated by Django 3.2.3 on 2022-09-14 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalRapor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saha_kodu', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Saha Kodu')),
                ('saha_no', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Saha No')),
                ('department', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Department')),
                ('aciklama', models.CharField(blank=True, max_length=250, null=True, unique=True, verbose_name='Açıklama')),
                ('durum', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Durum')),
                ('sorgu_no', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Sorgu No')),
                ('created_at', models.DateTimeField(blank=True, null=True, verbose_name='created_at')),
                ('referans_gruplari', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Referans Grupları')),
                ('sorgu_basliği', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Sorgu Başlığı')),
                ('sorgu_kategorisi', models.CharField(blank=True, max_length=70, null=True, unique=True, verbose_name='Sorgu Kategorisi')),
                ('ref_1', models.IntegerField(verbose_name='Ref_1')),
                ('ref_2', models.IntegerField(verbose_name='Ref_2')),
                ('ref_3', models.IntegerField(verbose_name='Ref_3')),
                ('ref_4', models.IntegerField(verbose_name='Ref_4')),
                ('ref_5', models.IntegerField(verbose_name='Ref_5')),
                ('ref_6', models.IntegerField(verbose_name='Ref_6')),
                ('update_at', models.DateTimeField(blank=True, null=True, verbose_name='update_at')),
            ],
        ),
    ]
