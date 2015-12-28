# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_auto_20151227_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webcategory',
            name='description',
            field=models.TextField(max_length=3000, blank=True),
        ),
    ]
