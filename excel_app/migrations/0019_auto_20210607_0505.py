# Generated by Django 3.2.3 on 2021-06-07 02:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('excel_app', '0018_auto_20210605_0558'),
    ]

    operations = [
        migrations.AddField(
            model_name='rapor',
            name='hatali',
            field=models.BooleanField(default=False, verbose_name='Hatalı mı?'),
        ),
        migrations.AlterField(
            model_name='rapor',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='raporlar', to=settings.AUTH_USER_MODEL),
        ),
    ]