# Generated by Django 3.2.3 on 2022-09-16 11:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rapor', '0002_rapor'),
        ('excel_app', '0056_auto_20220916_1425'),
        ('envanter', '0005_alter_raporenvanter_rapor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sayimrapor',
            name='rapor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='girdiler', to='rapor.rapor'),
        ),
        migrations.AlterField(
            model_name='sayimsonrasienvanter',
            name='rapor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sayim_sonrasi_envanter', to='rapor.rapor'),
        ),
        migrations.DeleteModel(
            name='Rapor',
        ),
    ]
