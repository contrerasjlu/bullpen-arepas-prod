# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0002_auto_20151104_0032'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymentbatch',
            old_name='x_Coord',
            new_name='x_coord',
        ),
        migrations.RenameField(
            model_name='paymentbatch',
            old_name='y_Coord',
            new_name='y_coord',
        ),
        migrations.AddField(
            model_name='paymentbatch',
            name='zip_code',
            field=models.CharField(default=1, help_text=b'Ingrese el c\xc3\xb3digo postal de la ubicacion del truck', max_length=4, verbose_name=b'C\xc3\xb3digo Zip'),
            preserve_default=False,
        ),
    ]
