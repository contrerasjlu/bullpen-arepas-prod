# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LocationManager', '0002_location_admin_menu_child_of'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location_admin_menu',
            options={'verbose_name': 'Menu Option', 'verbose_name_plural': 'Menu Options'},
        ),
    ]
