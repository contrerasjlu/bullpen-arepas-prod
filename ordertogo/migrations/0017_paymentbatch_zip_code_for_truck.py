# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0016_auto_20151115_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentbatch',
            name='zip_code_for_truck',
            field=models.CharField(default=3302, help_text=b'Ingrese el c\xc3\xb3digo postal de la ubicacion del truck', max_length=4, verbose_name=b'C\xc3\xb3digo Zip'),
            preserve_default=False,
        ),
    ]
