# Generated by Django 3.2.3 on 2021-05-15 14:59

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloglistingpage',
            name='content_de',
            field=wagtail.core.fields.StreamField([('banner', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image', required=True)), ('text', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text_color', wagtail.core.blocks.CharBlock(help_text='#ffffff', required=True))]))], blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bloglistingpage',
            name='content_en',
            field=wagtail.core.fields.StreamField([('banner', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image', required=True)), ('text', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text_color', wagtail.core.blocks.CharBlock(help_text='#ffffff', required=True))]))], blank=True, null=True),
        ),
    ]
