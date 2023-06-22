# Generated by Django 4.0.6 on 2022-12-28 15:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='working_hours',
            name='break_finish',
        ),
        migrations.RemoveField(
            model_name='working_hours',
            name='break_start',
        ),
        migrations.AlterField(
            model_name='company',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='service',
            name='length',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(24)]),
        ),
        migrations.AlterField(
            model_name='service',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='ip_address',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
