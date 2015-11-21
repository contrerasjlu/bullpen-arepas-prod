# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0022_order_delivery_amt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpaymentdetail',
            name='gateway_message',
            field=models.CharField(max_length=50),
        ),
    ]
