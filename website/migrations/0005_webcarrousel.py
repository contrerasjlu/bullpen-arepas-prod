# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20151227_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebCarrousel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'website/carrousel/')),
                ('alt', models.CharField(help_text=b'This text is show if the Image is not Loaded', max_length=50, verbose_name=b'Alternative Text')),
                ('order', models.PositiveIntegerField(verbose_name=b'Order')),
            ],
            options={
                'verbose_name': 'Web Carrousel Image',
                'verbose_name_plural': 'Web Carrousel Images',
            },
        ),
    ]
