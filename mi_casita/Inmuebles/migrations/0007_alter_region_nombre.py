# Generated by Django 5.1.3 on 2024-11-20 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inmuebles', '0006_alter_comuna_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='nombre',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]