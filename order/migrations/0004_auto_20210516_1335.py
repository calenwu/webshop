# Generated by Django 3.2.3 on 2021-05-16 13:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_country_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Coupon name'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_method_name',
            field=models.CharField(default='Free Shipping', max_length=255, verbose_name='Shipping method name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_method_price',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Shipping method price'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='discount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Discount on order'),
        ),
    ]
