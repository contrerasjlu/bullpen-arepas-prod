# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_auto_20160111_2032'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='webproduct',
            name='foot_image',
        ),
        migrations.RemoveField(
            model_name='webproduct',
            name='foot_image_check',
        ),
        migrations.AddField(
            model_name='webcategory',
            name='foot_image',
            field=models.ImageField(help_text=b'This Image will be on the Footer od the Modal Window Content', upload_to=b'website/product/images/footer/', verbose_name=b'Image for Footer', blank=True),
        ),
        migrations.AddField(
            model_name='webcategory',
            name='foot_image_check',
            field=models.BooleanField(default=False, verbose_name=b'Aditional Image?'),
        ),
    ]
