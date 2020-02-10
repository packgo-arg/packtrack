# Generated by Django 3.0.2 on 2020-02-10 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_auto_20200208_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='task_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='destinations', to='tasks.Task'),
        ),
        migrations.AlterField(
            model_name='origin',
            name='task_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='origins', to='tasks.Task'),
        ),
    ]
