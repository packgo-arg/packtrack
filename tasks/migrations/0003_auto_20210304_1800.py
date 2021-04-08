# Generated by Django 3.1.3 on 2021-03-04 21:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20201202_1807'),
    ]

    operations = [
        migrations.AddField(
            model_name='destination',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='destination',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(default='AAAA000000', max_length=10, validators=[django.core.validators.RegexValidator(code='nomatch', message='Length has to be 10', regex='^.{10}$')]),
        ),
    ]