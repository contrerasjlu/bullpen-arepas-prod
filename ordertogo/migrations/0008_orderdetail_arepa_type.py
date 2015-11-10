# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0007_auto_20151104_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='arepa_type',
            field=models.CharField(default=b'Baked', max_length=5, verbose_name=b'Baked or Fried', blank=True),
        ),
    ]
