# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0032_auto_20151216_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='allow_drinks',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='allow_extras',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='product',
            name='allow_type',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='extras',
            field=models.IntegerField(default=1, help_text=b'This item will not count if allow extras is not checked'),
        ),
    ]
