# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0009_auto_20151109_2207'),
    ]

    operations = [
        migrations.CreateModel(
            name='generic_variable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=45, verbose_name=b'Code')),
                ('value', models.CharField(max_length=45, verbose_name=b'Value')),
                ('description', models.TextField(max_length=45, verbose_name=b'Descripcion')),
            ],
        ),
    ]
