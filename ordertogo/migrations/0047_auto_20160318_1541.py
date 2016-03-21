# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0046_auto_20160212_2117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['order'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='paymentbatch',
            options={'verbose_name': 'Batch', 'verbose_name_plural': 'Batches'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['order_in_menu'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AddField(
            model_name='paymentbatch',
            name='notifier',
            field=models.EmailField(default=b'do-not-reply@bullpenarepas.com', max_length=254),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.CharField(help_text=b"Please Choose if you're going to \t\t\t\t\t\t\t\t  pick it up o we're going to deliver the order", max_length=2, verbose_name=b'Order Type', choices=[(b'D', b'Delivery'), (b'P', b'Pick it Up'), (b'PL', b'Parking Lot')]),
        ),
        migrations.AlterField(
            model_name='order',
            name='time',
            field=models.CharField(blank=True, help_text=b"Please select how many minutes you're \t\t\t\t\t\t\t\t\t   going to pick the order up", max_length=2, verbose_name=b'Time to Pick the order Up', choices=[(b'15', b'15 Minutes'), (b'20', b'20 Minutes'), (b'25', b'25 Minutes')]),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='main_product',
            field=models.BooleanField(default=False, help_text=b'Indicates if the product is the \t\t\t\t\t\t\t\t\t              main Product', verbose_name=b'is the Main Product of the \t\t\t\t\t\t\t\t\t                 Order?'),
        ),
    ]
