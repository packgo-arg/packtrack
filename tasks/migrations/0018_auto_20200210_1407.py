# Generated by Django 3.0.2 on 2020-02-10 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0017_auto_20200210_1358'),
    ]

    operations = [
        migrations.RenameField(
            model_name='destination',
            old_name='t_id',
            new_name='task',
        ),
        migrations.RenameField(
            model_name='origin',
            old_name='t_id',
            new_name='task',
        ),
    ]