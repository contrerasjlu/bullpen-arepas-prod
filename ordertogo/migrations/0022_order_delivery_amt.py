# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0021_auto_20151118_2320'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_amt',
            field=models.DecimalField(default=0, verbose_name=b'Delivery', max_digits=10, decimal_places=2),
        ),
    ]
