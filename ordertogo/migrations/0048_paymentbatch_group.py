# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('ordertogo', '0047_auto_20160318_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentbatch',
            name='Group',
            field=models.ForeignKey(default=1, to='auth.Group'),
            preserve_default=False,
        ),
    ]
