# Generated by Django 3.2 on 2021-05-16 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_code', models.CharField(max_length=15)),
                ('product_code', models.CharField(max_length=7)),
                ('quntity', models.CharField(max_length=3)),
                ('UOM', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=25)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trans_code', models.CharField(max_length=15, unique=True)),
                ('customer_code', models.CharField(max_length=20)),
                ('mode_of_transport', models.CharField(max_length=15)),
                ('invoice_number', models.CharField(max_length=7)),
                ('total_pre_tax', models.FloatField()),
                ('discount', models.FloatField(default=0)),
                ('total_price_taxed', models.FloatField()),
                ('is_dispatched', models.BooleanField(default=False)),
                ('is_closed', models.BooleanField(default=False)),
            ],
        ),
    ]