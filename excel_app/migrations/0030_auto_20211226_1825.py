# Generated by Django 3.2.3 on 2021-12-26 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('excel_app', '0029_reportimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='reportimage',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='excel_app.sayimsonrasienvanter'),
        ),
    ]
