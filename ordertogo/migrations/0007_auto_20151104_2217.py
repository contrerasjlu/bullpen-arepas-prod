# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0006_auto_20151104_2221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='open_for_deluvery',
        ),
        migrations.AddField(
            model_name='paymentbatch',
            name='open_for_delivery',
            field=models.BooleanField(default=True, verbose_name=b'Abierto para Delivery?'),
        ),
    ]
