# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0044_auto_20160210_0117'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductRestriction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.ForeignKey(to='ordertogo.LocationsAvailable')),
                ('product', models.ForeignKey(to='ordertogo.product')),
            ],
            options={
                'verbose_name': 'Product Restriction',
                'verbose_name_plural': 'Products Restrictions',
            },
        ),
    ]
