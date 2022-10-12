from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import *
from . import util


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "image", "starting_price", "category"]
        widgets = {
          "description": forms.Textarea(attrs={'rows': 2, 'cols': 15}),
          "starting_price": forms.TextInput(attrs={'min': 0, 'type': 'number', 'step': '0.1'}),
        }


def categories(request):
    """
    Display all categories.
    """
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all(),
    })


def category(request, id):
    """
    Display all items in a category.
    """
    return render(request, "auctions/category.html", {
        "items": Listing.objects.filter(category=Category.objects.filter(id=id).first(), status=True),
    })


def index(request):
    """
    Display all active items.
    """
    return render(request, "auctions/index.html", {
        "items": Listing.objects.filter(status=True),
    })


def listing(request, id):
    """
    Render a listing page.
    """
    user = request.user if request.user else None
    context = util.get_listing_context(user, Listing.objects.filter(id=id).first())
    if context:
        return render(request, "auctions/listing.html", context)
    return redirect("/")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def add(request):
    """
    Add a listing.
    """
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            return redirect(f"/listings/{util.add(form, request.user)}")
        else:
            return render(request, "auctions/add.html", {
                "form": form,
                "error": "Price must be at least 0 Galleons."
            }) 
    return render(request, "auctions/add.html", {
        "form": ListingForm()
    })


@login_required
def bid(request, id):
    """
    Place a bid.
    """
    if request.method == "POST":
        bid = util.BidForm(request.POST)
        util.validator_listing = id
        if bid.is_valid():
            util.bid(bid, request.user, Listing.objects.filter(id=id).first())
        else:
            context = util.get_listing_context(request.user, Listing.objects.filter(id=id).first())
            context["error_bid"] = "Bid is incorrect. Please enter the amount at least as large as the starting price and greater than the other bids."
            context["bid"] = bid
            return render(request, "auctions/listing.html", context)
    return redirect(f"/listings/{id}")


@login_required
def close(request, id):
    """
    Close a listing.
    """
    util.close(request.user, Listing.objects.filter(id=id).first())
    return redirect(f"/listings/{id}")


@login_required
def comment(request, id):
    """
    Post a comment.
    """
    if request.method == "POST":
        form = util.CommentForm(request.POST)
        if form.is_valid():
            util.comment(form, request.user, Listing.objects.filter(id=id).first())
        else:
            context = util.get_listing_context(request.user,
                      Listing.objects.filter(id=id).first())
            context["comment"] = form
            return render(request, "auctions/listing.html", context)
    return redirect(f"/listings/{id}")


@login_required
def watched(request):
    """
    Render a watchlist for current user.
    """
    return render(request, "auctions/watchlist.html", {
        "watchlist": util.get_watchlist(request.user),
    })

@login_required
def watchlist(request, id):
    """
    Add/remove item from watchlist.
    """
    util.manage_watchlist(Listing.objects.get(id=id), request.user)
    return redirect(f"/listings/{id}")
