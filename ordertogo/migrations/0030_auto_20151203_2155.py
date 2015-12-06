# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0029_auto_20151127_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentbatch',
            name='address_for_truck',
            field=models.CharField(help_text=b'Must be a Valid Address', max_length=1000, verbose_name=b'Address for Truck', blank=True),
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='batch_code',
            field=models.CharField(help_text=b'This code will be used to identify the batch', unique=True, max_length=10, verbose_name=b'Batch Code'),
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='open_for_delivery',
            field=models.BooleanField(default=True, help_text=b'Indicates if the Location accept Delivery Orders', verbose_name=b'Open for Delivery?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to=b'images', blank=True),
        ),
    ]
