# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0015_paymentbatch_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentbatch',
            name='description',
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='adress_for_truck',
            field=models.CharField(help_text=b'Ingrese la Direcci\xc3\xb3n donde se ubica la locacion movil', max_length=1000, verbose_name=b'Direcci\xc3\xb3n de la Locaci\xc3\xb3n movil', blank=True),
        ),
    ]
