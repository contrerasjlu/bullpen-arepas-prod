# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0003_auto_20151104_0038'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name=b'Order Date and Time')),
                ('order_number', models.IntegerField(verbose_name=b'Order Number')),
                ('order_type', models.CharField(help_text=b"Please Choose if you're going to pick it up o we're going to deliver the order", max_length=1, verbose_name=b'Order Type', choices=[(b'D', b'Delivery'), (b'P', b'Pick it Up')])),
                ('email', models.EmailField(help_text=b'Please enter your email address', max_length=254, verbose_name=b'Email')),
                ('open_for_deluvery', models.BooleanField(default=True)),
                ('address', models.CharField(help_text=b'Please enter the delivery adress', max_length=100, verbose_name=b'Adress', blank=True)),
                ('time', models.CharField(blank=True, help_text=b"Please select how many minutes you're going to pick the order up", max_length=2, verbose_name=b'Time to Pick the order Up', choices=[(b'15', b'15 Minutes'), (b'20', b'20 Minutes'), (b'25', b'25 Minutes')])),
                ('sub_amt', models.DecimalField(verbose_name=b'Subtotal', max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('tax_amt', models.DecimalField(verbose_name=b'Tax', max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.0)])),
                ('total_amt', models.DecimalField(verbose_name=b'Total', max_digits=10, decimal_places=2, validators=[django.core.validators.MinValueValidator(0.0)])),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.IntegerField(verbose_name=b'Item')),
                ('order_number', models.ForeignKey(to='ordertogo.Order')),
                ('product_selected', models.ForeignKey(to='ordertogo.product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPaymentDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cardholder_name', models.CharField(max_length=50)),
                ('card_type', models.CharField(max_length=20)),
                ('card_number', models.CharField(max_length=4)),
                ('exp_date', models.CharField(max_length=4)),
                ('gateway_message', models.CharField(max_length=15)),
                ('bank_message', models.CharField(max_length=50)),
                ('bank_resp_code', models.CharField(max_length=50)),
                ('gateway_resp_code', models.CharField(max_length=50)),
                ('cvv2', models.CharField(max_length=5)),
                ('amount', models.CharField(max_length=19)),
                ('transaction_tag', models.CharField(max_length=50)),
                ('transaction_type', models.CharField(max_length=50)),
                ('currency', models.CharField(max_length=4)),
                ('correlation_id', models.CharField(max_length=50)),
                ('token_type', models.CharField(max_length=50)),
                ('token_value', models.CharField(max_length=50)),
                ('transaction_status', models.CharField(max_length=50)),
                ('validation_status', models.CharField(max_length=50)),
                ('method', models.CharField(max_length=50)),
                ('transaction_id', models.CharField(max_length=100)),
                ('order_number', models.ForeignKey(to='ordertogo.Order')),
            ],
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='status',
            field=models.CharField(default=b'O', help_text=b'Indica el Estado Actual del Lote, No pueden existir mas de un Lote Abierto', max_length=1, verbose_name=b'Estado', choices=[(b'O', b'Abierto'), (b'C', b'Cerrado')]),
        ),
    ]
