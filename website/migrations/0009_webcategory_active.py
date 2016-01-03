# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_webcategory_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='webcategory',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
