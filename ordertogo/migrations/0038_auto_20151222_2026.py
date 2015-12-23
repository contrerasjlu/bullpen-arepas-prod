# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0037_locationsavailable_merchant_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentbatch',
            name='tax_percent',
            field=models.IntegerField(default=7, help_text=b'You must enter the exac value, ex: 7 mean 7%', max_length=2, verbose_name=b'Tax Percent Value for Batch'),
        ),
        migrations.AlterField(
            model_name='locationsavailable',
            name='zip_code',
            field=models.CharField(help_text=b'Type the 4 digits zip code', max_length=5, verbose_name=b'Zip Code'),
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='zip_code_for_truck',
            field=models.CharField(help_text=b'If the Location selected is NOT mobile, please leave blank this field', max_length=5, verbose_name=b'Zip Code', blank=True),
        ),
    ]
