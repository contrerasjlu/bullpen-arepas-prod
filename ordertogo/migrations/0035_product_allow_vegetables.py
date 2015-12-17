# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0034_relatedimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='allow_vegetables',
            field=models.BooleanField(default=True),
        ),
    ]
