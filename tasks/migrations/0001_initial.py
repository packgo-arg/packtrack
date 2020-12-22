# Generated by Django 3.1.3 on 2020-12-02 13:47

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('request_id', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.DateTimeField(null=True)),
                ('end_time', models.DateTimeField(null=True)),
                ('delay', models.IntegerField(blank=True, null=True)),
                ('duration', models.PositiveIntegerField(blank=True, null=True)),
                ('accidental_delivery_duration', models.PositiveIntegerField(blank=True, null=True)),
                ('ord_price', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utils.client')),
            ],
        ),
        migrations.CreateModel(
            name='Origin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50)),
                ('house_num', models.CharField(max_length=10)),
                ('ap_unit', models.CharField(blank=True, max_length=10, null=True)),
                ('suburb', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(max_length=50)),
                ('province', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('location', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(0.0, 0.0), geography=True, srid=4326)),
                ('pos_code', models.IntegerField(blank=True, null=True)),
                ('geo_data', models.JSONField(blank=True, null=True)),
                ('is_covered', models.BooleanField(default=False)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='origins', to='tasks.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('st_update', models.DateTimeField(auto_now_add=True)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='utils.driver')),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='utils.state')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ord_status', to='tasks.order')),
                ('provider', models.ForeignKey(default='4fd1d932-f86a-456b-9f39-f9919ad22040', on_delete=django.db.models.deletion.CASCADE, to='utils.provider')),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='utils.status')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('width', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('length', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('volume', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('weight', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('quantity', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99)])),
                ('pack_price', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='tasks.order')),
                ('pack_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='utils.package')),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50)),
                ('house_num', models.CharField(max_length=10)),
                ('ap_unit', models.CharField(blank=True, max_length=50, null=True)),
                ('suburb', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(max_length=50, null=True)),
                ('province', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('location', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(0.0, 0.0), geography=True, srid=4326)),
                ('pos_code', models.IntegerField(blank=True, null=True)),
                ('geo_data', models.JSONField(blank=True, null=True)),
                ('is_covered', models.BooleanField(default=False)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='destinations', to='tasks.order')),
            ],
        ),
    ]