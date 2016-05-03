# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0051_auto_20160409_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('RequestDate', models.DateTimeField(auto_now=True)),
                ('CreditCardType', models.CharField(max_length=20)),
                ('CreditCardNumber', models.CharField(max_length=12)),
                ('CardHolderName', models.CharField(max_length=50)),
                ('Amount', models.CharField(max_length=17)),
                ('OrderNumber', models.ForeignKey(to='ordertogo.Order')),
            ],
            options={
                'verbose_name': 'Payment Request',
                'verbose_name_plural': 'Payment Requests',
            },
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_additionals',
            field=models.BooleanField(default=False, help_text=b'This Indicates that \t\t\t\t\t\t\t\t\t\t\t\t\t   the item will display \t\t\t\t\t\t\t\t\t\t\t\t\t   the additionals category', verbose_name=b'Additionals?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_drinks',
            field=models.BooleanField(default=False, help_text=b'This indicates that the item \t\t\t\t\t\t\t\t\t              will be a Meal with Soft Drinks\t\t\t\t\t\t\t\t\t              (Category "Soft Drinks")', verbose_name=b'Drinks?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_extras',
            field=models.BooleanField(default=False, help_text=b'This indicates that the item \t\t\t\t\t\t\t\t\t              will display the Players \t\t\t\t\t\t\t\t\t              Category', verbose_name=b'Meats?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_paid_extras',
            field=models.BooleanField(default=False, help_text=b'This indicates that the \t\t\t\t\t\t\t\t\t\t\titem will display the "On The Bench \t\t\t\t\t\t\t\t\t\t\tCategory', verbose_name=b'Paid Extras?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_qtty',
            field=models.BooleanField(default=True, help_text=b'This indicates that the item \t\t\t\t\t\t\t\t\t            will have a quantity field', verbose_name=b'Allow Quantty?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_sauces',
            field=models.BooleanField(default=False, help_text=b'This indicates \t\t\t\t\t\t\t\t\t   that the item will display the "Sauces" \t\t\t\t\t\t\t\t\t   category', verbose_name=b'Sauces?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_type',
            field=models.BooleanField(default=False, verbose_name=b'Baked or Fried'),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_vegetables',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='extras',
            field=models.IntegerField(default=1, help_text=b'This item will not count if allow \t\t\t\t\t\t\t\t extras is not checked', verbose_name=b'Max Meats'),
        ),
        migrations.AlterField(
            model_name='product',
            name='max_qtty',
            field=models.PositiveIntegerField(default=99, help_text=b'Maximum number of items in a request', verbose_name=b'Max Quantity'),
        ),
    ]
