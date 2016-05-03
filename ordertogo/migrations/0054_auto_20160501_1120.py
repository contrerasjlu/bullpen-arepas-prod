# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0053_auto_20160420_2233'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='allow_sour_cream',
            field=models.BooleanField(default=False, help_text=b'This Indicates if the Product can be served with Sour Cream'),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='Amount',
            field=models.CharField(max_length=17, verbose_name=b'Amount'),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='CardHolderName',
            field=models.CharField(max_length=50, verbose_name=b'Cardholder Name'),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='CreditCardNumber',
            field=models.CharField(max_length=12, verbose_name=b'Credit Card Number'),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='CreditCardType',
            field=models.CharField(max_length=20, verbose_name=b'Credit Card Type'),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='OrderNumber',
            field=models.CharField(max_length=20, verbose_name=b'Order Number'),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='RequestDate',
            field=models.DateTimeField(auto_now=True, verbose_name=b'Request Date'),
        ),
    ]
