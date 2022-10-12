from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=80)
    image = models.CharField(max_length=2048, blank=True, default="/static/auctions/placeholder.jpg")

    def __str__(self):
        return f"{self.title}"


class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=80)
    description = models.TextField(max_length=800)
    image = models.CharField(max_length=2048, blank=True)
    starting_price = models.FloatField(validators=[MinValueValidator(0)])
    current_price = models.FloatField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items", blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", blank=True)
    price = models.FloatField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", blank=True)

    def __str__(self):
        return f"Listing: {self.listing} - Price: {self.price} - Bidder: {self.bidder}"


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", blank=True)
    text = models.TextField(max_length=500)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    def __str__(self):
        return f"Author: {self.author} – Listing: {self.listing}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watching")
    listing = models.ManyToManyField(Listing)

    def __str__(self):
       return f" Watchlist of {self.user}"