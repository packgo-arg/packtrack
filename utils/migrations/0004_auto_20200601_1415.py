# Generated by Django 3.0.5 on 2020-06-01 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0003_auto_20200601_1343'),
    ]

    operations = [
        migrations.RenameField(
            model_name='state',
            old_name='local',
            new_name='city',
        ),
    ]