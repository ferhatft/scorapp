# Generated by Django 3.2.3 on 2022-03-05 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel_app', '0035_auto_20220305_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='sayimoncesienvanter',
            name='ustekipman',
            field=models.CharField(default='', max_length=5000, verbose_name='Üst Ekipman'),
        ),
    ]