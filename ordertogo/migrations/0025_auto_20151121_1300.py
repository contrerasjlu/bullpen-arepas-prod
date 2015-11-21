# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0024_auto_20151120_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='arepa_type',
            field=models.CharField(default=b'Baked', max_length=15, verbose_name=b'Baked or Fried', blank=True),
        ),
    ]
