# Generated by Django 3.2.3 on 2022-09-17 22:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('excel_app', '0060_delete_globalsayimrapor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sayimsonrasienvanter',
            name='rapor',
        ),
        migrations.DeleteModel(
            name='SayimRapor',
        ),
        migrations.DeleteModel(
            name='SayimSonrasiEnvanter',
        ),
    ]