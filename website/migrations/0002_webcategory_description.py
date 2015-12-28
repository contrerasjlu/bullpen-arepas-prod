# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='webcategory',
            name='description',
            field=models.TextField(default='t', max_length=3000),
            preserve_default=False,
        ),
    ]
