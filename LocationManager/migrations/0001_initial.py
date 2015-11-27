# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='location_admin_menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=50)),
                ('url', models.CharField(max_length=50, null=True)),
                ('imgClass', models.CharField(max_length=50, null=True)),
                ('activeOn', models.CharField(max_length=20, null=True)),
                ('order', models.IntegerField()),
            ],
        ),
    ]
