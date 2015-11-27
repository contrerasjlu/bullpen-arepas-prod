# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LocationManager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location_admin_menu',
            name='child_of',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
