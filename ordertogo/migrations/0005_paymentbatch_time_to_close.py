# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0004_auto_20151104_0220'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentbatch',
            name='time_to_close',
            field=models.IntegerField(default=2200, help_text=b'Ingrese la Hora de cierre del lote en hora militar, Ej: 23000', verbose_name=b'Hora de Cierre', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24000)]),
            preserve_default=False,
        ),
    ]
