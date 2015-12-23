# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0039_auto_20151222_2027'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='allow_qtty',
            field=models.BooleanField(default=False),
        ),
    ]
