# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0027_orderdetail_main_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationsavailable',
            name='x_coord',
            field=models.CharField(max_length=50, verbose_name=b'Latitud', blank=True),
        ),
        migrations.AlterField(
            model_name='locationsavailable',
            name='y_coord',
            field=models.CharField(max_length=50, verbose_name=b'Longitud', blank=True),
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='address_for_truck',
            field=models.CharField(help_text=b'If the Location selected is NOT mobile, please leave blank this field', max_length=1000, verbose_name=b'Address for Truck', blank=True),
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='batch_code',
            field=models.CharField(help_text=b'This code will be used as a identifier for the batch', unique=True, max_length=10, verbose_name=b'Batch Code'),
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='max_miles',
            field=models.IntegerField(help_text=b'Please insert a value for the coverage round area', verbose_name=b'Max miles for Delivery'),
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='open_for_delivery',
            field=models.BooleanField(default=True, verbose_name=b'Open for Delivery?'),
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='status',
            field=models.CharField(default=b'O', help_text=b'Indica el Estado Actual del Lote, Debe estar Abierto para Aceptar Pedidos', max_length=1, verbose_name=b'Estado', choices=[(b'O', b'Open'), (b'C', b'Closed')]),
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='time_to_close',
            field=models.TimeField(help_text=b'Ingrese la Hora de cierre del lote en hora militar, Ej: 23000', verbose_name=b'Hora de Cierre', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='zip_code_for_truck',
            field=models.CharField(help_text=b'If the Location selected is NOT mobile, please leave blank this field', max_length=4, verbose_name=b'Zip Code', blank=True),
        ),
    ]
