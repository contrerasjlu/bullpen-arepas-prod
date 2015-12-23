# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0036_auto_20151217_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationsavailable',
            name='merchant_ref',
            field=models.CharField(default=b'MyPOS', help_text=b'This number is provided by Payeezy', max_length=50, verbose_name=b'Merchant Reference'),
        ),
    ]
