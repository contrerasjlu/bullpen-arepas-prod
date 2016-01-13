# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_webcategory_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='webproduct',
            name='foot_image',
            field=models.ImageField(help_text=b'This Image will be on the Footer od the Modal Window Content', upload_to=b'website/product/images/footer/', verbose_name=b'Image for Footer', blank=True),
        ),
        migrations.AddField(
            model_name='webproduct',
            name='foot_image_check',
            field=models.BooleanField(default=False, verbose_name=b'Aditional Image?'),
        ),
        migrations.AlterField(
            model_name='webcategory',
            name='type_cat',
            field=models.CharField(default=b'I', max_length=1, verbose_name=b'Category Style', choices=[(b'L', b'List Product'), (b'I', b'Image View'), (b'C', b'Image View - Centered')]),
        ),
    ]
