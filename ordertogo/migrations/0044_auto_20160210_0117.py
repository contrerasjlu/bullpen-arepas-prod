# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0043_order_adress2'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='car_brand',
            field=models.CharField(max_length=50, verbose_name=b'Car Brand', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='car_color',
            field=models.CharField(max_length=50, verbose_name=b'Car Color', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='car_license',
            field=models.CharField(max_length=50, verbose_name=b'Car License', blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='car_model',
            field=models.CharField(max_length=50, verbose_name=b'Car Model', blank=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.CharField(help_text=b"Please Choose if you're going to pick it up o we're going to deliver the order", max_length=2, verbose_name=b'Order Type', choices=[(b'D', b'Delivery'), (b'P', b'Pick it Up'), (b'PL', b'Parking Lot')]),
        ),
    ]
