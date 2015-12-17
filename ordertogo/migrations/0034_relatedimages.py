# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0033_auto_20151216_2051'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedImages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=50, verbose_name=b'Image Description')),
                ('image', models.ImageField(upload_to=b'images')),
                ('product', models.ForeignKey(to='ordertogo.product')),
            ],
            options={
                'verbose_name': 'Related Image (For Products)',
                'verbose_name_plural': 'Related Images (For Products)',
            },
        ),
    ]
