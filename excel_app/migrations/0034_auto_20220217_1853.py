# Generated by Django 3.2.3 on 2022-02-17 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excel_app', '0033_auto_20220210_1524'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ekipman_hareketi',
            name='kaynak_adresi',
        ),
        migrations.RemoveField(
            model_name='ekipman_hareketi',
            name='kaynak_departman',
        ),
        migrations.RemoveField(
            model_name='ekipman_hareketi',
            name='kaynak_surec',
        ),
        migrations.RemoveField(
            model_name='ekipman_hareketi',
            name='referans',
        ),
        migrations.RemoveField(
            model_name='ekipman_hareketi',
            name='transfer_adresi',
        ),
        migrations.RemoveField(
            model_name='ekipman_hareketi',
            name='transfer_yeri',
        ),
    ]
