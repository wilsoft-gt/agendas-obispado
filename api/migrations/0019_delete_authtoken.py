# Generated by Django 5.0.4 on 2024-04-23 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_authtoken_value_alter_authtoken_key'),
    ]

    operations = [
        migrations.DeleteModel(
            name='AuthToken',
        ),
    ]
