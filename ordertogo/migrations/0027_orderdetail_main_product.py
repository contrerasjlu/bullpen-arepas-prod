# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0026_auto_20151122_1811'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='main_product',
            field=models.BooleanField(default=False, verbose_name=b'Indica si es el producto principal del item'),
        ),
    ]
