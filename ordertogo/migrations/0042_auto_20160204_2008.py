# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0041_album'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='email',
            field=models.EmailField(unique=True, max_length=254),
        ),
    ]
