# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0008_orderdetail_arepa_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='allow_paid_extras',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='allow_sauces',
            field=models.BooleanField(default=True),
        ),
    ]
