# Generated by Django 5.0.4 on 2024-04-17 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oracion',
            name='fecha',
            field=models.DateField(),
        ),
    ]
