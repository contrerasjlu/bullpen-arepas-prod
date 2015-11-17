# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0014_auto_20151115_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentbatch',
            name='description',
            field=models.CharField(default=1, max_length=100, verbose_name=b'Descripcion Humanizada'),
            preserve_default=False,
        ),
    ]
