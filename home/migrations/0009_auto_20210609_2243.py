# Generated by Django 3.2.3 on 2021-06-09 22:43

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20210606_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='content',
            field=wagtail.core.fields.StreamField([('centered_header', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(help_text='Text', required=True))])), ('full_width_carousel', wagtail.core.blocks.StructBlock([('slides', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image when width is big', required=True)), ('image_small', wagtail.images.blocks.ImageChooserBlock(help_text='Image when width is small', required=True)), ('button_text', wagtail.core.blocks.CharBlock(help_text='Button text', required=False)), ('button_color', wagtail.core.blocks.CharBlock(help_text='Button text color', required=False)), ('button_background_color', wagtail.core.blocks.CharBlock(help_text='Button background_color', required=False)), ('button_border_color', wagtail.core.blocks.CharBlock(help_text='Button border color', required=False)), ('page', wagtail.core.blocks.PageChooserBlock(help_text='Page it redirects to on button click', required=False))])))])), ('centered_title_with_text', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True))])), ('image_left_text_right', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image', required=True))])), ('image_right_text_left', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='image', required=True))])), ('hero_block_text_left', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image', required=True)), ('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.RichTextBlock(help_text='Text', required=True)), ('button_text', wagtail.core.blocks.CharBlock(help_text='Button text', required=False)), ('button_url', wagtail.core.blocks.CharBlock(help_text='Button url', required=False))])), ('hero_block_text_right', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image', required=True)), ('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.RichTextBlock(help_text='Text', required=True)), ('button_text', wagtail.core.blocks.CharBlock(help_text='Button text', required=False)), ('button_url', wagtail.core.blocks.CharBlock(help_text='Button url', required=False))])), ('hero_product', wagtail.core.blocks.StructBlock([('product', wagtail.core.blocks.PageChooserBlock(required=True))])), ('products', wagtail.core.blocks.StructBlock([('products', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('product', wagtail.core.blocks.PageChooserBlock(required=True))])))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='content_de',
            field=wagtail.core.fields.StreamField([('centered_header', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(help_text='Text', required=True))])), ('full_width_carousel', wagtail.core.blocks.StructBlock([('slides', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image when width is big', required=True)), ('image_small', wagtail.images.blocks.ImageChooserBlock(help_text='Image when width is small', required=True)), ('button_text', wagtail.core.blocks.CharBlock(help_text='Button text', required=False)), ('button_color', wagtail.core.blocks.CharBlock(help_text='Button text color', required=False)), ('button_background_color', wagtail.core.blocks.CharBlock(help_text='Button background_color', required=False)), ('button_border_color', wagtail.core.blocks.CharBlock(help_text='Button border color', required=False)), ('page', wagtail.core.blocks.PageChooserBlock(help_text='Page it redirects to on button click', required=False))])))])), ('centered_title_with_text', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True))])), ('image_left_text_right', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image', required=True))])), ('image_right_text_left', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='image', required=True))])), ('hero_block_text_left', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image', required=True)), ('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.RichTextBlock(help_text='Text', required=True)), ('button_text', wagtail.core.blocks.CharBlock(help_text='Button text', required=False)), ('button_url', wagtail.core.blocks.CharBlock(help_text='Button url', required=False))])), ('hero_block_text_right', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image', required=True)), ('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.RichTextBlock(help_text='Text', required=True)), ('button_text', wagtail.core.blocks.CharBlock(help_text='Button text', required=False)), ('button_url', wagtail.core.blocks.CharBlock(help_text='Button url', required=False))])), ('hero_product', wagtail.core.blocks.StructBlock([('product', wagtail.core.blocks.PageChooserBlock(required=True))])), ('products', wagtail.core.blocks.StructBlock([('products', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('product', wagtail.core.blocks.PageChooserBlock(required=True))])))]))], blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='content_en',
            field=wagtail.core.fields.StreamField([('centered_header', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(help_text='Text', required=True))])), ('full_width_carousel', wagtail.core.blocks.StructBlock([('slides', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image when width is big', required=True)), ('image_small', wagtail.images.blocks.ImageChooserBlock(help_text='Image when width is small', required=True)), ('button_text', wagtail.core.blocks.CharBlock(help_text='Button text', required=False)), ('button_color', wagtail.core.blocks.CharBlock(help_text='Button text color', required=False)), ('button_background_color', wagtail.core.blocks.CharBlock(help_text='Button background_color', required=False)), ('button_border_color', wagtail.core.blocks.CharBlock(help_text='Button border color', required=False)), ('page', wagtail.core.blocks.PageChooserBlock(help_text='Page it redirects to on button click', required=False))])))])), ('centered_title_with_text', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True))])), ('image_left_text_right', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image', required=True))])), ('image_right_text_left', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.TextBlock(help_text='Text', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='image', required=True))])), ('hero_block_text_left', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image', required=True)), ('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.RichTextBlock(help_text='Text', required=True)), ('button_text', wagtail.core.blocks.CharBlock(help_text='Button text', required=False)), ('button_url', wagtail.core.blocks.CharBlock(help_text='Button url', required=False))])), ('hero_block_text_right', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(help_text='Image', required=True)), ('title', wagtail.core.blocks.CharBlock(help_text='Title', required=True)), ('text', wagtail.core.blocks.RichTextBlock(help_text='Text', required=True)), ('button_text', wagtail.core.blocks.CharBlock(help_text='Button text', required=False)), ('button_url', wagtail.core.blocks.CharBlock(help_text='Button url', required=False))])), ('hero_product', wagtail.core.blocks.StructBlock([('product', wagtail.core.blocks.PageChooserBlock(required=True))])), ('products', wagtail.core.blocks.StructBlock([('products', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('product', wagtail.core.blocks.PageChooserBlock(required=True))])))]))], blank=True, null=True),
        ),
    ]
