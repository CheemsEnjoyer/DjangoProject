# Generated by Django 5.1.1 on 2024-09-22 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capybuyra', '0003_alter_orders_client'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.TextField(verbose_name='ФИО'),
        ),
    ]
