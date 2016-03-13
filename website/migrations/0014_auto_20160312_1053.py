# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_auto_20160111_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webcategory',
            name='type_cat',
            field=models.CharField(default=b'I', max_length=1, verbose_name=b'Category Style', choices=[(b'L', b'List Product'), (b'I', b'Image View - Stripped R&B '), (b'C', b'Image View - Stripped R&Y ')]),
        ),
    ]
