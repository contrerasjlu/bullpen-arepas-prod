# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0038_auto_20151222_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentbatch',
            name='tax_percent',
            field=models.IntegerField(default=7, help_text=b'You must enter the exac value, ex: 7 mean 7%', verbose_name=b'Tax Percent Value for Batch'),
        ),
    ]
