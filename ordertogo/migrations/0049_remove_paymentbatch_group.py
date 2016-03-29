# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0048_paymentbatch_group'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentbatch',
            name='Group',
        ),
    ]
