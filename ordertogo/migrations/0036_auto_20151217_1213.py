# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0035_product_allow_vegetables'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=50, verbose_name=b'First Name')),
                ('lastname', models.CharField(max_length=50, verbose_name=b'Last Name')),
                ('email', models.EmailField(max_length=254, verbose_name=b'E-mail')),
                ('phone', models.CharField(max_length=50, verbose_name=b'Telephone Number', blank=True)),
                ('order', models.ForeignKey(to='ordertogo.Order')),
            ],
            options={
                'verbose_name': 'Guest Detail',
                'verbose_name_plural': 'Guest Details',
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='locationsavailable',
            options={'verbose_name': 'Location Available', 'verbose_name_plural': 'Locations Available'},
        ),
    ]
