# Generated by Django 4.1 on 2022-08-14 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_bid_bidder_alter_bid_listing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]