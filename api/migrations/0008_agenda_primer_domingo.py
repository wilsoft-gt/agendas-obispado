# Generated by Django 5.0.4 on 2024-04-18 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_remove_oracion_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenda',
            name='primer_domingo',
            field=models.BooleanField(default=False),
        ),
    ]
