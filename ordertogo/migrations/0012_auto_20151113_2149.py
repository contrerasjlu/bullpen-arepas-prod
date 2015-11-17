# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0011_auto_20151113_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericvariable',
            name='code',
            field=models.CharField(unique=True, max_length=45, verbose_name=b'Code'),
        ),
    ]
