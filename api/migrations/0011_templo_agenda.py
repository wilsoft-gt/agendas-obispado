# Generated by Django 5.0.4 on 2024-04-19 18:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_actividad_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='templo',
            name='agenda',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.agenda'),
        ),
    ]