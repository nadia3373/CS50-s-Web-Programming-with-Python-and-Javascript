from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
COUNTRIES = (
    ("Russia", "Russia"),
    ("United States", "United States"),
    ("United Kingdom", "United Kingdom"),
)


STATUSES = (
    ("Archived", "Archived"),
    ("Cancelled", "Cancelled"),
    ("Created", "Created"),
    ("Finished", "Finished"),
    ("Verified", "Verified"),
)

# TIMES = tuple([(x,x) for x in range(24)])


def logo_images_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/core/logo_images/<company_domain>/<filename>
    return f"core/logo_images/{instance.domain}/{filename}"


def gallery_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/core/gallery/<company_domain>/<filename>
    return f"core/gallery/{instance.company.domain}/{filename}"


def service_images_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/core/service_images/<company_domain>/<filename>
    return f"core/service_images/{instance.company.domain}/{filename}"


def profile_images_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/core/profile_images/<company_domain>/<filename>
    return f"core/profile_images/{instance.company.domain}/{filename}"


class Company(models.Model):
    building = models.CharField(max_length=10)
    city = models.CharField(default="Krasnoyarsk", max_length=100)
    country = models.CharField(max_length = 20, choices = COUNTRIES, default="Russia")
    description = models.CharField(blank=True, max_length=1000)
    domain = models.CharField(max_length=100)
    latitude = models.CharField(blank=True, max_length=15)
    logo = models.ImageField(blank=True, upload_to=logo_images_path)
    longitude = models.CharField(blank=True, max_length=15)
    name = models.CharField(max_length=100)
    office = models.CharField(max_length=10)
    status = models.BooleanField(default=True)
    street = models.CharField(max_length=100)


class Image(models.Model):
    company = models.ForeignKey(Company, blank=True, on_delete=models.CASCADE, related_name="gallery")
    description = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(blank=True, upload_to=gallery_path)


class Service(models.Model):
    company = models.ForeignKey(Company, blank=True, on_delete=models.CASCADE, related_name="services")
    description = models.CharField(max_length=300)
    image = models.ImageField(blank=True, upload_to=service_images_path)
    length = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(24)])
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    status = models.BooleanField(default=True)


class User(AbstractUser):
    company = models.ForeignKey(Company, blank=True, null=True, on_delete=models.CASCADE, related_name="clients")
    dob = models.DateField(blank=True)
    ip_address = models.CharField(blank=True, max_length=15)
    manager = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=10, unique=True)
    photo = models.ImageField(blank=True, upload_to=profile_images_path)
    telegram_id = models.CharField(max_length=100, blank=True)
    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']


class Working_hours(models.Model):
    company = models.ForeignKey(Company, blank=True, on_delete=models.CASCADE, related_name="working_hours")
    workday_start = models.TimeField()
    workday_finish = models.TimeField()


class Appointment(models.Model):
    appointment_date = models.DateField()
    appointment_start_time = models.TimeField(choices = [])
    appointment_status = models.CharField(choices = STATUSES, default="Created", max_length=20)
    client = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="service_clients")
    company = models.ForeignKey(Company, blank=True, on_delete=models.CASCADE, related_name="company_appointments")
    service = models.ForeignKey(Service, blank=True, on_delete=models.CASCADE, related_name="services_appointments")


class Message(models.Model):
    message_date = models.DateTimeField(auto_now_add=True)
    receiver = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="inbox")
    sender = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="sent")
    text = models.CharField(max_length=4096)