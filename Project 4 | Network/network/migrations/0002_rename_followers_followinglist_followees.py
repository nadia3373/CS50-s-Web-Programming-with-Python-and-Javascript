# Generated by Django 4.1 on 2022-08-31 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='followinglist',
            old_name='followers',
            new_name='followees',
        ),
    ]
