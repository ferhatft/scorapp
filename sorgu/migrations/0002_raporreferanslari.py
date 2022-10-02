# Generated by Django 3.2.3 on 2022-09-17 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sorgu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RaporReferanslari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sorgu_no', models.CharField(default='', max_length=5000, verbose_name='Sorgu No')),
                ('ref', models.CharField(default='', max_length=5000, verbose_name='Ref')),
                ('ekipman_parca_kodu', models.CharField(default='', max_length=5000, verbose_name='Ekipman Parça Kodu')),
                ('parca_tanimi', models.CharField(default='', max_length=5000, verbose_name='Parça Tanımı')),
                ('grup_tanimi', models.CharField(default='', max_length=5000, verbose_name='Grup Tanımı')),
                ('rapor_tanimi', models.CharField(default='', max_length=5000, verbose_name='Rapor Tanımı')),
                ('ref_grup', models.CharField(default='', max_length=5000, verbose_name='Ref Grup')),
                ('kategori', models.CharField(default='', max_length=5000, verbose_name='Kategori')),
                ('analiz_no', models.CharField(default='', max_length=5000, verbose_name='Analiz No')),
            ],
            options={
                'verbose_name': 'Sorgu Referans',
                'verbose_name_plural': 'Sorgu Referansları',
            },
        ),
    ]