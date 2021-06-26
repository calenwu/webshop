# Generated by Django 3.2.3 on 2021-05-15 16:42

import django.core.validators
from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20210515_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='productpage',
            name='reference_buttons_de',
            field=wagtail.core.fields.StreamField([('reference_button', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(help_text='Text', required=True)), ('url', wagtail.core.blocks.URLBlock(help_text='Text', required=True)), ('text_color', wagtail.core.blocks.CharBlock(help_text='#ffffff', required=True)), ('button_bg_color', wagtail.core.blocks.CharBlock(help_text='#ffffff', required=True)), ('border_color', wagtail.core.blocks.CharBlock(help_text='#ffffff', required=False)), ('font_awesome_class', wagtail.core.blocks.CharBlock(help_text='fal fa-nice', required=False))]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productpage',
            name='reference_buttons_en',
            field=wagtail.core.fields.StreamField([('reference_button', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(help_text='Text', required=True)), ('url', wagtail.core.blocks.URLBlock(help_text='Text', required=True)), ('text_color', wagtail.core.blocks.CharBlock(help_text='#ffffff', required=True)), ('button_bg_color', wagtail.core.blocks.CharBlock(help_text='#ffffff', required=True)), ('border_color', wagtail.core.blocks.CharBlock(help_text='#ffffff', required=False)), ('font_awesome_class', wagtail.core.blocks.CharBlock(help_text='fal fa-nice', required=False))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productpage',
            name='price',
            field=models.IntegerField(help_text='Use the smallest unit possible (e.g. cents for EUR/USD)', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='productpage',
            name='weight',
            field=models.IntegerField(default=0, help_text='Use the smallest unit possible (e.g. gramm)', validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
