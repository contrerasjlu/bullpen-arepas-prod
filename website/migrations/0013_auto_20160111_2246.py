# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_auto_20160111_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webcategory',
            name='show_price',
            field=models.BooleanField(default=False, help_text=b'Only For Image View and Image View - Centered'),
        ),
        migrations.AlterField(
            model_name='webproduct',
            name='aditional_text',
            field=models.CharField(help_text=b'Only for Image View - Centered', max_length=10, verbose_name=b'Aditional Text to Show', blank=True),
        ),
        migrations.AlterField(
            model_name='webproduct',
            name='batter',
            field=models.BooleanField(default=False, help_text=b'Only for Image View', verbose_name=b'Show Batter?'),
        ),
        migrations.AlterField(
            model_name='webproduct',
            name='batter_num',
            field=models.PositiveIntegerField(default=b'0', help_text=b'Only for Image View', verbose_name=b'How Many Batters?'),
        ),
    ]
