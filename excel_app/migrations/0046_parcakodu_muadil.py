# Generated by Django 3.2.3 on 2022-03-24 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel_app', '0045_globalsayimrapor_update_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcakodu',
            name='muadil',
            field=models.CharField(default='', max_length=500, verbose_name='Muadil'),
        ),
    ]