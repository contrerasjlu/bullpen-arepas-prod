# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_webcategory_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name=b'Name')),
                ('email', models.EmailField(max_length=254, verbose_name=b'Email')),
                ('info', models.TextField(verbose_name=b'Tell us, What do you need?')),
            ],
            options={
                'verbose_name': 'Web Info',
                'verbose_name_plural': 'Email',
            },
        ),
        migrations.AlterField(
            model_name='webcategory',
            name='override_desc',
            field=models.BooleanField(default=False, verbose_name=b'Override Name?'),
        ),
    ]
