# Generated by Django 5.0.4 on 2024-05-09 16:33

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0002_alter_vendor_vendor_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('on_time_delivery_rate', models.FloatField(default=0.0)),
                ('quality_rating_avg', models.FloatField(default=0.0)),
                ('average_response_time', models.FloatField(default=0.0)),
                ('fulfillment_rate', models.FloatField(default=0.0)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendors.vendor')),
            ],
            options={
                'verbose_name': 'Vendor Performance',
                'verbose_name_plural': 'Vendor Performances',
            },
        ),
    ]
