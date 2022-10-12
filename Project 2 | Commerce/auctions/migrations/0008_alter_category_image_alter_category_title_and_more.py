# Generated by Django 4.1 on 2022-08-12 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_category_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.CharField(blank=True, default='/static/auctions/placeholder.jpg', max_length=2048),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='auctions.category'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='image',
            field=models.CharField(blank=True, default='/static/auctions/placeholder.jpg', max_length=2048),
        ),
    ]