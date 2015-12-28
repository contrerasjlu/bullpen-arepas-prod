# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_webcarrousel'),
    ]

    operations = [
        migrations.AddField(
            model_name='webcarrousel',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
