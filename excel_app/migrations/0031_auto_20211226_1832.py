# Generated by Django 3.2.3 on 2021-12-26 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel_app', '0030_auto_20211226_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='sayimsonrasienvanter',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.DeleteModel(
            name='ReportImage',
        ),
    ]