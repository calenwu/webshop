# Generated by Django 3.2.3 on 2021-05-16 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20210516_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='name',
            field=models.CharField(default='Temp', max_length=255),
            preserve_default=False,
        ),
    ]
