# Generated by Django 5.0.4 on 2024-04-18 04:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_himno_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='oracion',
            name='fecha',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
