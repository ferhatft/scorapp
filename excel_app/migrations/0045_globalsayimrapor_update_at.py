# Generated by Django 3.2.3 on 2022-03-20 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel_app', '0044_sayimoncesienvanter_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalsayimrapor',
            name='update_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Güncelleme Tarihi'),
        ),
    ]
