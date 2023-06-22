# Generated by Django 4.0.6 on 2022-12-28 15:10

import core.models
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('dob', models.DateField(blank=True)),
                ('ip_address', models.CharField(max_length=15)),
                ('manager', models.BooleanField(default=False)),
                ('phone_number', models.CharField(max_length=10, unique=True)),
                ('photo', models.ImageField(blank=True, upload_to=core.models.profile_images_path)),
                ('telegram_id', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('building', models.CharField(max_length=10)),
                ('city', models.CharField(default='Krasnoyarsk', max_length=100)),
                ('country', models.CharField(choices=[('Russia', 'Russia'), ('United States', 'United States'), ('United Kingdom', 'United Kingdom')], default='Russia', max_length=20)),
                ('description', models.CharField(blank=True, max_length=1000)),
                ('domain', models.CharField(max_length=100)),
                ('latitude', models.CharField(blank=True, max_length=15)),
                ('logo', models.ImageField(blank=True, upload_to=core.models.logo_images_path)),
                ('longitude', models.CharField(blank=True, max_length=15)),
                ('name', models.CharField(max_length=100)),
                ('office', models.CharField(max_length=10)),
                ('status', models.BooleanField(default=False)),
                ('street', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Working_hours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('break_start', models.TimeField()),
                ('break_finish', models.TimeField()),
                ('workday_start', models.TimeField()),
                ('workday_finish', models.TimeField()),
                ('company', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='working_hours', to='core.company')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=300)),
                ('image', models.ImageField(blank=True, upload_to=core.models.service_images_path)),
                ('length', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=100)),
                ('price', models.PositiveIntegerField()),
                ('status', models.BooleanField(default=False)),
                ('company', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='services', to='core.company')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_date', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=4096)),
                ('receiver', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='inbox', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('image', models.ImageField(blank=True, upload_to=core.models.gallery_path)),
                ('company', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='core.company')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateField()),
                ('appointment_start_time', models.TimeField(choices=[])),
                ('appointment_status', models.CharField(choices=[('Archived', 'Archived'), ('Cancelled', 'Cancelled'), ('Created', 'Created'), ('Finished', 'Finished'), ('Verified', 'Verified')], default='Created', max_length=20)),
                ('client', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_clients', to=settings.AUTH_USER_MODEL)),
                ('company', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_appointments', to='core.company')),
                ('service', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='services_appointments', to='core.service')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='core.company'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]