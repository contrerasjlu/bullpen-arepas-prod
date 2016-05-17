# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0015_webgallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='webgallery',
            name='Order',
            field=models.PositiveIntegerField(default=1, verbose_name=b'Order'),
        ),
        migrations.AlterField(
            model_name='webgallery',
            name='Alternative',
            field=models.CharField(default=b'Alternative', max_length=50, verbose_name=b'Alternative Text'),
        ),
        migrations.AlterField(
            model_name='webgallery',
            name='Caption',
            field=models.CharField(default=b'Caption', max_length=50, verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='webgallery',
            name='Event',
            field=models.CharField(default=b'Evento', max_length=50, verbose_name=b'Event'),
        ),
        migrations.AlterField(
            model_name='webgallery',
            name='Image',
            field=models.ImageField(default=None, upload_to=b'website/gallery/'),
        ),
    ]
