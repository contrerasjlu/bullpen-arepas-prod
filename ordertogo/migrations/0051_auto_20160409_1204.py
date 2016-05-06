# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0050_auto_20160408_2359'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='max_paid_extras',
            field=models.PositiveIntegerField(default=1, help_text=b'Maximum number of paid extras for teh item'),
        ),
        migrations.AddField(
            model_name='product',
            name='max_qtty',
            field=models.PositiveIntegerField(default=1, help_text=b'Maximum number of items in a request', verbose_name=b'Max Quantity'),
        ),
        migrations.AddField(
            model_name='product',
            name='max_sauces',
            field=models.PositiveIntegerField(default=1, help_text=b'Maximum number of sauces for teh item'),
        ),
        migrations.AddField(
            model_name='product',
            name='max_vegetables',
            field=models.PositiveIntegerField(default=1, help_text=b'Maximum numer of \t\t\t\t\t\t\t\t\t\t\t\t            vegeatbles for the item'),
        ),
    ]
