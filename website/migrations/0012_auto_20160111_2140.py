# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_auto_20160111_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='webproduct',
            name='aditional_text',
            field=models.CharField(max_length=10, verbose_name=b'Aditional Text to Show', blank=True),
        ),
        migrations.AddField(
            model_name='webproduct',
            name='description',
            field=models.TextField(verbose_name=b'Description', blank=True),
        ),
        migrations.AddField(
            model_name='webproduct',
            name='override_desc',
            field=models.BooleanField(default=False, verbose_name=b'Override Description?'),
        ),
    ]
