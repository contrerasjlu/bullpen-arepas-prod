# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0012_auto_20151113_2149'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationsAvailable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=100, verbose_name=b'Descripcion')),
                ('location', models.CharField(help_text=b'Ingrese la Direcci\xc3\xb3n donde se ubica la locacion', max_length=1000, verbose_name=b'Direcci\xc3\xb3n de la Locaci\xc3\xb3n')),
                ('zip_code', models.CharField(help_text=b'Ingrese el c\xc3\xb3digo postal de la ubicacion del truck', max_length=4, verbose_name=b'C\xc3\xb3digo Zip')),
                ('x_coord', models.CharField(max_length=50, verbose_name=b'Latitud')),
                ('y_coord', models.CharField(max_length=50, verbose_name=b'Longitud')),
            ],
        ),
        migrations.RemoveField(
            model_name='paymentbatch',
            name='location',
        ),
        migrations.RemoveField(
            model_name='paymentbatch',
            name='x_coord',
        ),
        migrations.RemoveField(
            model_name='paymentbatch',
            name='y_coord',
        ),
        migrations.RemoveField(
            model_name='paymentbatch',
            name='zip_code',
        ),
    ]
