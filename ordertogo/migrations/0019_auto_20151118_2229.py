# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0018_auto_20151117_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericvariable',
            name='value',
            field=models.CharField(max_length=500, verbose_name=b'Value'),
        ),
    ]
