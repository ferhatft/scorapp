# Generated by Django 3.2.3 on 2022-03-28 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel_app', '0049_alter_ekipman_hareketi_islem_tarihi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ekipman_hareketi',
            name='islem_tarihi',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
