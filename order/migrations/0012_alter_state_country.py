# Generated by Django 3.2.3 on 2021-06-16 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_auto_20210616_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='states', to='order.country'),
        ),
    ]
