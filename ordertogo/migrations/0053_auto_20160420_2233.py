# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0052_auto_20160420_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentrequest',
            name='OrderNumber',
            field=models.CharField(max_length=20),
        ),
    ]
