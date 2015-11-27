# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0025_auto_20151121_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_status',
            field=models.CharField(default=b'P', max_length=1, verbose_name=b'Status', choices=[(b'P', b'Paid'), (b'K', b'Kitchen'), (b'O', b'Out for Delivery'), (b'D', b'Delivered')]),
        ),
        migrations.AlterField(
            model_name='locationsavailable',
            name='description',
            field=models.CharField(max_length=100, verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='locationsavailable',
            name='location',
            field=models.CharField(help_text=b'Type the address without the zip code', max_length=1000, verbose_name=b'Address'),
        ),
        migrations.AlterField(
            model_name='locationsavailable',
            name='zip_code',
            field=models.CharField(help_text=b'Type the 4 digits zip code', max_length=4, verbose_name=b'Zip Code'),
        ),
    ]
