# Generated by Django 3.2.3 on 2022-09-17 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SorguList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sorgu_no', models.CharField(default='', max_length=5000, verbose_name='Sorgu No')),
                ('kontrol', models.CharField(default='', max_length=5000, verbose_name='Kontrol')),
                ('ref_grup', models.CharField(default='', max_length=5000, verbose_name='Ref Grup')),
                ('kategori', models.CharField(default='', max_length=5000, verbose_name='Kategori')),
                ('check', models.CharField(default='', max_length=5000, verbose_name='Check')),
            ],
            options={
                'verbose_name': 'Sorgu Listesi',
                'verbose_name_plural': 'Sorgu Listeleri',
            },
        ),
    ]
