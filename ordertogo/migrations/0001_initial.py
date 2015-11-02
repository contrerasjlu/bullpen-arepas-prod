# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
                ('Active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=50)),
                ('name', models.CharField(max_length=80)),
                ('description', models.TextField(max_length=500)),
                ('extras', models.IntegerField(default=1)),
                ('price', models.DecimalField(max_digits=19, decimal_places=2)),
                ('order_in_menu', models.IntegerField()),
                ('Active', models.BooleanField(default=True)),
                ('category', models.ForeignKey(related_name='product', to='ordertogo.category')),
            ],
        ),
    ]
