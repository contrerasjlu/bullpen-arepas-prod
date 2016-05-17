# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_auto_20160312_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebGallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Event', models.CharField(max_length=50, verbose_name=b'Event')),
                ('Image', models.ImageField(upload_to=b'website/gallery/')),
                ('Alternative', models.CharField(max_length=50, verbose_name=b'Alternative Text')),
                ('State', models.BooleanField(default=True, verbose_name=b'State')),
                ('Caption', models.CharField(max_length=50, verbose_name=b'Description')),
            ],
            options={
                'verbose_name': 'Web Gallery',
                'verbose_name_plural': 'Web Galleries',
            },
        ),
    ]
