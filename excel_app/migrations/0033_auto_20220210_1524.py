# Generated by Django 3.2.3 on 2022-02-10 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel_app', '0032_ekipman_hareketi'),
    ]

    operations = [
        migrations.AddField(
            model_name='ekipman_hareketi',
            name='maliyet',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='ekipman_hareketi',
            name='seri_no',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
