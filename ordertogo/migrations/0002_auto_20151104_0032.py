# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentBatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(help_text=b'Fecha en la que se Apertur\xc3\xb3 el Truck', verbose_name=b'Fecha de Lote', auto_now_add=True)),
                ('location', models.CharField(help_text=b'Ingrese la Direcci\xc3\xb3n donde se ubica el Truck', max_length=1000, verbose_name=b'Direcci\xc3\xb3n de la Locaci\xc3\xb3n')),
                ('x_Coord', models.CharField(max_length=50, verbose_name=b'Latitud')),
                ('y_Coord', models.CharField(max_length=50, verbose_name=b'Longitud')),
                ('max_miles', models.IntegerField(help_text=b'Ingrese la Cantidad de millas m\xc3\xa1ximas para el Delivery', verbose_name=b'Millas M\xc3\xa1ximas')),
                ('batch_code', models.CharField(help_text=b'Ingrese el c\xc3\xb3digo que se asignar\xc3\xa1 al Lote', unique=True, max_length=10, verbose_name=b'C\xc3\xb3digo de Lote')),
                ('status', models.CharField(default=b'O', help_text=b'Indica el Estado Actual del Lote, No pueden existir mas de un Lote Abierto', max_length=20, verbose_name=b'Estado', choices=[(b'O', b'Abierto'), (b'C', b'Cerrado')])),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to=b'', blank=True),
        ),
    ]
