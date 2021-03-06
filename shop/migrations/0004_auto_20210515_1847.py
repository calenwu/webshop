# Generated by Django 3.2.3 on 2021-05-15 18:47

from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20210515_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcolor',
            name='color_de',
            field=models.CharField(db_index=True, max_length=63, null=True),
        ),
        migrations.AddField(
            model_name='productcolor',
            name='color_en',
            field=models.CharField(db_index=True, max_length=63, null=True),
        ),
        migrations.AlterField(
            model_name='productpage',
            name='content',
            field=wagtail.core.fields.StreamField([('title_with_text', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True))])), ('image_left_text_right', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image', required=True))])), ('image_right_text_left', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='image', required=True))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productpage',
            name='content_de',
            field=wagtail.core.fields.StreamField([('title_with_text', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True))])), ('image_left_text_right', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image', required=True))])), ('image_right_text_left', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='image', required=True))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='productpage',
            name='content_en',
            field=wagtail.core.fields.StreamField([('title_with_text', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True))])), ('image_left_text_right', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image', required=True))])), ('image_right_text_left', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='image', required=True))]))], blank=True, null=True),
        ),
    ]
