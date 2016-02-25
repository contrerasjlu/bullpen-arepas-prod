# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordertogo', '0045_productrestriction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Active',
            field=models.BooleanField(default=True, verbose_name=b'Active?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_drinks',
            field=models.BooleanField(default=True, help_text=b'This indicates that the item \t\t\t\t\t\t\t\t\t              will be a Meal with Soft Drinks\t\t\t\t\t\t\t\t\t              (Category "Soft Drinks")'),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_extras',
            field=models.BooleanField(default=True, help_text=b'This indicates that the item \t\t\t\t\t\t\t\t\t              will display the Players \t\t\t\t\t\t\t\t\t              Category', verbose_name=b'Allow Players?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_paid_extras',
            field=models.BooleanField(default=True, help_text=b'This indicates that the \t\t\t\t\t\t\t\t\t\t\titem will display the "On The Bench \t\t\t\t\t\t\t\t\t\t\tCategory', verbose_name=b'Allow "On the Bench"?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_qtty',
            field=models.BooleanField(default=False, help_text=b'This indicates that the item \t\t\t\t\t\t\t\t\t            will have a quantity field', verbose_name=b'Allow Quantty?'),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_sauces',
            field=models.BooleanField(default=True, help_text=b'This indicates \t\t\t\t\t\t\t\t\t   that the item will display the "Sauces" \t\t\t\t\t\t\t\t\t   category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='allow_type',
            field=models.BooleanField(default=True, verbose_name=b'Baked or Fries'),
        ),
        migrations.AlterField(
            model_name='product',
            name='extras',
            field=models.IntegerField(default=1, help_text=b'This item will not count if allow \t\t\t\t\t\t\t\t extras is not checked'),
        ),
        migrations.AlterField(
            model_name='product',
            name='order_in_menu',
            field=models.IntegerField(help_text=b'This is the order to present \t\t\t\t\t\t\t\t\t\tthe item in the menu'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(help_text=b'Accepts only 19 digits including \t\t\t\t\t\t\t\t2 decimals', max_digits=19, decimal_places=2),
        ),
    ]
