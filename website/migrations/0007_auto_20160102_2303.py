# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_webcarrousel_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='webcategory',
            name='type_cat',
            field=models.CharField(default=b'I', max_length=1, verbose_name=b'Category Style', choices=[(b'L', b'List Product'), (b'I', b'Image View')]),
        ),
        migrations.AddField(
            model_name='webproduct',
            name='batter',
            field=models.BooleanField(default=False, verbose_name=b'Show Batter?'),
        ),
        migrations.AddField(
            model_name='webproduct',
            name='batter_num',
            field=models.PositiveIntegerField(default=b'0', verbose_name=b'How Many Batters?'),
        ),
    ]
