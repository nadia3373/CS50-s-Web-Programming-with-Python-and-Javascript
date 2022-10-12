from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Max
from django.forms import ModelForm

from .models import *


validator_listing = 0


class BidForm(ModelForm): 
    class Meta:
        model = Bid
        fields = "__all__"
        widgets = {
          "price": forms.TextInput(attrs={'min': 0, 'type': 'number', 'step': '0.1'}),
        }


    def __init__(self, *args, **kwargs):
        validator_price = kwargs.pop('validator_price', None)
        super(BidForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs.update({'min': validator_price, 'value': validator_price})


    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data["price"]
        if price <= validate():
            raise ValidationError("The bid is incorrect")


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["author", "listing", "text", "rating"]
        widgets = {
          "text": forms.Textarea(attrs={'rows': 2, 'cols': 15}),
          "rating": forms.TextInput(attrs={'min': 0, 'value': 0, 'max': 5, 'type': 'number'}),
        }


def add(form, user):
    """
    Add a listing.
    """
    form = form.save(commit=False)
    form.seller = user
    form.current_price = form.starting_price
    if not form.image:
        form.image = "/static/auctions/placeholder.jpg"
    if not form.category:
        form.category = misc_category()
    form.save()
    return form.pk


def bid(bid, user, listing):
    """
    Place a bid.
    """
    bid = bid.save(commit=False)
    bid.bidder = user
    bid.listing = listing
    listing.current_price = bid.price
    bid.save()
    listing.save()


def calculate_rating(comments):
    """
    Calculate rating for a listing.
    """
    rating = 0
    count = 0
    if comments:
        for comment in comments:
            count += 1
            rating += comment.rating
        rating /= count
    return rating


def close(user, listing):
    """
    Close a listing.
    """
    if user.id == listing.seller.id:
        listing.status = "False"
        listing.save()


def comment(comment, user, listing):
    """
    Post a comment.
    """
    comment = comment.save(commit=False)
    comment.author = user
    comment.listing = listing
    comment.save()


def detect_winner(id):
    """
    Detect auction winner.
    """
    bids = Bid.objects.filter(listing=id)
    max = bids.aggregate(Max('price'))
    if max["price__max"] is not None:
        max = bids.filter(price=max["price__max"]).first()
        return max
    return None


def get_listing_context(user, listing):
    """
    Get context for a listing.
    """
    if listing:
        try:
            watchlist = Watchlist.objects.filter(user=user, listing=listing.id).first()
        except:
            watchlist = None
        comments = Comment.objects.filter(listing=listing)
        return {
            "bids": Bid.objects.filter(listing=listing.id).order_by('-price'),
            "bid": BidForm(validator_price=round((listing.current_price + 0.1), 1)),
            "comments": comments,
            "comment": CommentForm(),
            "listing": listing,
            "rating": calculate_rating(comments),
            "winner": None if listing.status is True else detect_winner(listing.id),
            "watchlist": watchlist,
        }
    return None


def get_watchlist(user):
    """
    Get user's watchlist.
    """
    try:
        watchlist = Watchlist.objects.filter(user=user).first().listing.all()
    except:
        watchlist = None;
    return watchlist


def manage_watchlist(listing, user):
    """
    Add or delete item from a watchlist.
    """
    watchlist, status = Watchlist.objects.get_or_create(user=user)
    if listing in watchlist.listing.all():
        watchlist.listing.remove(listing)
    else:
        watchlist.listing.add(listing)


def misc_category():
    """
    Get or create Miscellaneous category.
    """
    category = Category.objects.filter(title="Miscellaneous")
    if not category:
        Category.objects.create(title="Miscellaneous", image="/static/auctions/misc.jpg")
        category = Category.objects.filter(title="Miscellaneous")
    return category.first()


def validate():
    """
    Bid validator.
    """
    price = Bid.objects.filter(listing=validator_listing)
    price = price.aggregate(Max('price'))
    listing = Listing.objects.filter(id = validator_listing).first()
    return price["price__max"] if price["price__max"] is not None else listing.starting_price - 1