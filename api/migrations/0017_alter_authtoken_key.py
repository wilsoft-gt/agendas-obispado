# Generated by Django 5.0.4 on 2024-04-23 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_authtoken_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authtoken',
            name='key',
            field=models.CharField(max_length=32),
        ),
    ]