# Generated by Django 4.1 on 2022-08-12 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_listing_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(default='Miscellaneous', max_length=80),
        ),
    ]
