# Generated by Django 3.2.3 on 2022-09-25 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sorgu', '0002_raporreferanslari'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RaporReferanslari',
            new_name='SorguReferanslari',
        ),
    ]