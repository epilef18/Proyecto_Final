# Generated by Django 5.1.3 on 2024-11-21 23:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inmuebles', '0008_inmueble_imagen_inmueble_region_imagen_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='inmueble',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Inmuebles.region'),
        ),
    ]