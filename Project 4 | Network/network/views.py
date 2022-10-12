import json
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from . import util
from .models import *


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
          "text": forms.Textarea(attrs={'rows': 2, 'cols': 40}),
        }


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]


@login_required
def add(request):
    """
    Add new post
    """
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            return redirect(f"/posts/{util.add(form, request.user)}")
    return render(request, "network/add.html", {"form": PostForm()})


@login_required
def comment(request, id):
    """
    Leave a comment
    """
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            return redirect(f"/posts/{util.comment(form, Post.objects.filter(id=id).first(), request.user)}")
    return redirect(f"/posts/{id}")


@login_required
def edit(request, id):
    """
    Edit a post
    """
    if request.method == "PUT":
        return HttpResponse(status=204) if util.edit(json.loads(request.body), request.user, id) else redirect(f"/posts/{id}")
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)


@login_required
def follow(request, id):
    """
    Follow and unfollow users
    """
    following, status = FollowingList.objects.get_or_create(user=request.user)
    return JsonResponse(util.manage_following_list(following, User.objects.filter(id=id).first()))


@login_required
def following(request):
    """
    Get posts from followed users
    """
    following, status = FollowingList.objects.get_or_create(user=request.user)
    posts = Post.objects.filter(author__in=[user for user in following.followees.all()]).order_by('-timestamp')
    return render(request, "network/index.html", {"following": "true", "posts": posts, "page_obj": util.get_paginator(request, posts)})


def index(request):
    """
    Get all posts
    """
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, "network/index.html", {"posts": posts, "page_obj": util.get_paginator(request, posts)})


@login_required
def like(request, id):
    """
    Like and unlike posts
    """
    return JsonResponse(util.manage_likes(request.user, Post.objects.filter(id=id).first()))


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def post(request, id):
    """
    Get a post by id
    """
    post = Post.objects.filter(id=id).first()
    return render(request, "network/post.html", {"comment": CommentForm(), "post": post}) if post else redirect("/")


def profile(request, id):
    """
    Get a profile by id
    """
    user = request.user if id == request.user.id else User.objects.filter(id=id).first()
    following, status = FollowingList.objects.get_or_create(user=user)
    return render(request, "network/user.html", {"followers": [user.user for user in FollowingList.objects.filter(followees__in=[user])], "following": following.followees.all(), "page_obj": util.get_paginator(request, Post.objects.filter(author=user).order_by('-timestamp')), "user_to_show": user})


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
