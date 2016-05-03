# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0054_auto_20160501_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='arepa_type',
            field=models.CharField(default=b'Baked', max_length=100, verbose_name=b'Baked or Fried', blank=True),
        ),
    ]
