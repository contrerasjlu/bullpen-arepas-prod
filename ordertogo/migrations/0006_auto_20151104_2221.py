# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0005_paymentbatch_time_to_close'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentbatch',
            name='time_to_close',
            field=models.TimeField(help_text=b'Ingrese la Hora de cierre del lote en hora militar, Ej: 23000', verbose_name=b'Hora de Cierre'),
        ),
    ]
