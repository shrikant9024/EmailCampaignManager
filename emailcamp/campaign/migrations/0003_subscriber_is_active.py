# Generated by Django 4.1.5 on 2023-09-08 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0002_rename_subscribe_subscriber'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]