# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0040_product_allow_qtty'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('override_desc', models.BooleanField(default=False)),
                ('show_price', models.BooleanField(default=False)),
                ('webImage', models.ImageField(upload_to=b'website/category/images/', verbose_name=b'Image to Show for Category')),
                ('category', models.ForeignKey(to='ordertogo.category')),
            ],
            options={
                'verbose_name': 'Web Category',
                'verbose_name_plural': 'Web Categories',
            },
        ),
        migrations.CreateModel(
            name='WebProduct',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('webImage', models.ImageField(upload_to=b'website/product/images/', verbose_name=b'Image to Show for Product')),
                ('product', models.ForeignKey(to='ordertogo.product')),
                ('webCat', models.ForeignKey(to='website.WebCategory')),
            ],
            options={
                'verbose_name': 'Web Product',
                'verbose_name_plural': 'Web Products',
            },
        ),
        migrations.CreateModel(
            name='WebText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('text', models.TextField(max_length=3000)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Text',
                'verbose_name_plural': 'Texts',
            },
        ),
    ]
