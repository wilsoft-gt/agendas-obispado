# Generated by Django 5.0.4 on 2024-04-23 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_alter_authtoken_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='authtoken',
            name='value',
            field=models.CharField(default=2, max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='authtoken',
            name='key',
            field=models.CharField(max_length=20),
        ),
    ]
