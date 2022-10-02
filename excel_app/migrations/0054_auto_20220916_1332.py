# Generated by Django 3.2.3 on 2022-09-16 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('departmanlar', '0001_initial'),
        ('excel_app', '0053_delete_parcakodu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rapor',
            name='department_code',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='Department_code', to='departmanlar.departmanlar'),
        ),
        migrations.DeleteModel(
            name='Departmanlar',
        ),
    ]
