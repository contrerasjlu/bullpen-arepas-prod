# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0049_remove_paymentbatch_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='allow_additionals',
            field=models.BooleanField(default=True, help_text=b'This Indicates that \t\t\t\t\t\t\t\t\t\t\t\t\t   the item will display \t\t\t\t\t\t\t\t\t\t\t\t\t   the additionals category', verbose_name=b'Additionals?'),
        ),
        migrations.AddField(
            model_name='product',
            name='max_additionals',
            field=models.PositiveIntegerField(default=1, help_text=b'This item will not \t\t\t\t\t\t\t\t\t\t\t\t  \t\t\t count if Additionals \t\t\t\t\t\t\t\t\t\t\t\t  \t\t\t is not checked'),
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='close_date',
            field=models.DateTimeField(auto_now=True, verbose_name=b'Close Date'),
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='date',
            field=models.DateTimeField(help_text=b'Fecha en la que se Apertur\xc3\xb3 el Truck', verbose_name=b'Open Date', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='paymentbatch',
            name='status',
            field=models.CharField(default=b'O', help_text=b'Indica el Estado Actual del Lote, Debe estar Abierto para Aceptar Pedidos', max_length=1, verbose_name=b'State', choices=[(b'O', b'Open'), (b'C', b'Closed')]),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_drinks',
            field=models.BooleanField(default=True, help_text=b'This indicates that the item \t\t\t\t\t\t\t\t\t              will be a Meal with Soft Drinks\t\t\t\t\t\t\t\t\t              (Category "Soft Drinks")', verbose_name=b'Drinks?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_extras',
            field=models.BooleanField(default=True, help_text=b'This indicates that the item \t\t\t\t\t\t\t\t\t              will display the Players \t\t\t\t\t\t\t\t\t              Category', verbose_name=b'Meats?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_paid_extras',
            field=models.BooleanField(default=True, help_text=b'This indicates that the \t\t\t\t\t\t\t\t\t\t\titem will display the "On The Bench \t\t\t\t\t\t\t\t\t\t\tCategory', verbose_name=b'Paid Extras?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_sauces',
            field=models.BooleanField(default=True, help_text=b'This indicates \t\t\t\t\t\t\t\t\t   that the item will display the "Sauces" \t\t\t\t\t\t\t\t\t   category', verbose_name=b'Sauces?'),
        ),
    ]
