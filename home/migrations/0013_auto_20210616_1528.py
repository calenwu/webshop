# Generated by Django 3.2.3 on 2021-06-16 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20210616_1527'),
    ]

    operations = [
        migrations.AddField(
            model_name='footer',
            name='title_de',
            field=models.CharField(max_length=63, null=True),
        ),
        migrations.AddField(
            model_name='footer',
            name='title_en',
            field=models.CharField(max_length=63, null=True),
        ),
        migrations.AddField(
            model_name='footeritem',
            name='title',
            field=models.CharField(default='Hello', max_length=63),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='footeritem',
            name='title_de',
            field=models.CharField(max_length=63, null=True),
        ),
        migrations.AddField(
            model_name='footeritem',
            name='title_en',
            field=models.CharField(max_length=63, null=True),
        ),
    ]
