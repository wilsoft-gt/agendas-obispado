# Generated by Django 5.0.4 on 2024-04-18 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_oracion_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='himno',
            name='tipo',
            field=models.CharField(choices=[('1er', 'Himno inicial'), ('2do', 'Himno Sacramental'), ('3er', 'Himno intermedio'), ('4to', 'Himno final'), ('pre', 'Preludio'), ('pos', 'Posludio'), ('esp', 'Himno Especial')], max_length=3),
        ),
    ]
