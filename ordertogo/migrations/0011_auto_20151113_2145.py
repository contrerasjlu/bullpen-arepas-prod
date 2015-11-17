# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0010_generic_variable'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='generic_variable',
            new_name='GenericVariable',
        ),
    ]
