# Generated by Django 3.2.3 on 2022-03-20 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel_app', '0041_globalsayimrapor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcakodu',
            name='ekip_aciklama',
            field=models.CharField(default='', max_length=250, verbose_name='Ekip Açıklama'),
        ),
        migrations.AlterField(
            model_name='parcakodu',
            name='ekip_tanimi',
            field=models.CharField(default='', max_length=250, verbose_name='Ekip Tanımı'),
        ),
        migrations.AlterField(
            model_name='parcakodu',
            name='grup_tanimi',
            field=models.CharField(default='', max_length=250, verbose_name='Grup Tanımı'),
        ),
        migrations.AlterField(
            model_name='parcakodu',
            name='parca_kodu',
            field=models.CharField(default='', max_length=50, verbose_name='Ekipman Parça Kodu'),
        ),
        migrations.AlterField(
            model_name='parcakodu',
            name='parca_tanimi',
            field=models.CharField(default='', max_length=250, verbose_name='Parça Tanımı'),
        ),
    ]
