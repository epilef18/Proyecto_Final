from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inmuebles', '0010_alter_inmueble_imagen_inmueble_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='imagen_region',
            field=models.ImageField(blank=True, null=True, upload_to='regiones'),
        ),
    ]
