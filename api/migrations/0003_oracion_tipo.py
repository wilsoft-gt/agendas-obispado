# Generated by Django 5.0.4 on 2024-04-17 04:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_oracion_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='oracion',
            name='tipo',
            field=models.CharField(choices=[('primera', 'Primera Oracion'), ('final', 'Oracion Final')], default=django.utils.timezone.now, max_length=10),
            preserve_default=False,
        ),
    ]
