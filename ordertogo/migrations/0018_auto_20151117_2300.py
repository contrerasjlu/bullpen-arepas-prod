# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0017_paymentbatch_zip_code_for_truck'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymentbatch',
            old_name='adress_for_truck',
            new_name='address_for_truck',
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='status',
            field=models.CharField(default=b'O', help_text=b'Indica el Estado Actual del Lote, Debe estar Abierto para Aceptar Pedidos', max_length=1, verbose_name=b'Estado', choices=[(b'O', b'Abierto'), (b'C', b'Cerrado')]),
        ),
    ]
