# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0030_auto_20151203_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='category',
            name='show_in_menu',
            field=models.BooleanField(default=True),
        ),
    ]
