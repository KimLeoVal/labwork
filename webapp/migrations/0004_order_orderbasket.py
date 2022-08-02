# Generated by Django 4.0.5 on 2022-08-01 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_proinbasket'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.CharField(max_length=20, verbose_name='Имя')),
                ('name', models.CharField(max_length=20, verbose_name='Имя')),
                ('phone', models.CharField(max_length=20, verbose_name='Телефон')),
                ('adres', models.CharField(max_length=60, verbose_name='Адрес')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
            ],
        ),
        migrations.CreateModel(
            name='OrderBasket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='webapp.order', verbose_name='Заказ')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderb', to='webapp.product', verbose_name='Продукт')),
            ],
        ),
    ]