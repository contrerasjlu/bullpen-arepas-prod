# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0056_product_type_of_vegetables'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='max_qtty',
            field=models.PositiveIntegerField(default=5, help_text=b'Maximum number of items in a request', verbose_name=b'Max Quantity'),
        ),
    ]
