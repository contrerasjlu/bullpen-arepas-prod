# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_auto_20160102_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='webcategory',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name=b'Order To Show in Page'),
        ),
    ]
