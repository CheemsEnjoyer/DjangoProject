# Generated by Django 5.1 on 2024-11-30 10:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capybuyra', '0010_remove_shoppingcart_sum_productshoppingcart_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productshoppingcart',
            name='shopping_cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='capybuyra.shoppingcart'),
        ),
    ]