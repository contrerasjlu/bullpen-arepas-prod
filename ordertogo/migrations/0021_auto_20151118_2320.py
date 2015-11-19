# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0020_auto_20151118_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.CharField(help_text=b'Please enter the delivery adress', max_length=1000, verbose_name=b'Adress', blank=True),
        ),
    ]
