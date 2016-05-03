# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0055_auto_20160501_1235'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='type_of_vegetables',
            field=models.CharField(default=b'T', max_length=1, choices=[(b'T', b'Traditionals (System - Vegetables)'), (b'P', b'Pico de Gallo')]),
        ),
    ]
