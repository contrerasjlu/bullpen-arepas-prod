# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0028_auto_20151125_2327'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentbatch',
            name='close_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 28, 2, 36, 18, 284195, tzinfo=utc), verbose_name=b'Fecha y Hora de Cierre', auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='date',
            field=models.DateTimeField(help_text=b'Fecha en la que se Apertur\xc3\xb3 el Truck', verbose_name=b'Fecha de Lote', auto_now_add=True),
        ),
    ]
