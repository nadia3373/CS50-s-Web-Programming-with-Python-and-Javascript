# Generated by Django 4.1 on 2022-08-11 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listing_comment_bid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='title',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='listing',
            old_name='title',
            new_name='name',
        ),
    ]