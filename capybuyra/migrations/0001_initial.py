# Generated by Django 5.1 on 2024-10-08 12:32

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='ФИО')),
                ('password', models.TextField(verbose_name='Пароль')),
                ('email', models.TextField(verbose_name='Почта')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(verbose_name='Адрес')),
                ('sum', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('status', models.TextField(verbose_name='Статус')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='capybuyra.client')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('description', models.TextField(verbose_name='Статус')),
                ('amount', models.IntegerField(verbose_name='Количество')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='capybuyra.category')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='capybuyra.orders')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='capybuyra.product')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='capybuyra.client')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='capybuyra.product')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='capybuyra.client')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзины',
            },
        ),
        migrations.CreateModel(
            name='ProductShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='capybuyra.product')),
                ('shoppingCart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='capybuyra.shoppingcart')),
            ],
        ),
    ]
