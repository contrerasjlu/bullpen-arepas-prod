# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0013_auto_20151115_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentbatch',
            name='adress_for_truck',
            field=models.CharField(default=1, help_text=b'Ingrese la Direcci\xc3\xb3n donde se ubica la locacion movil', max_length=1000, verbose_name=b'Direcci\xc3\xb3n de la Locaci\xc3\xb3n movil'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paymentbatch',
            name='location',
            field=models.ForeignKey(default=1, to='ordertogo.LocationsAvailable'),
            preserve_default=False,
        ),
    ]
