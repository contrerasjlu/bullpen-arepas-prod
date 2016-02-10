# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0042_auto_20160204_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='adress2',
            field=models.CharField(help_text=b'Ex: Suite 23, Floor 2', max_length=200, verbose_name=b'Adress Line 2', blank=True),
        ),
    ]
