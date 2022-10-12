from django.core.paginator import Paginator

from .models import *


def add(post, user):
    """
    Add a post
    """
    post = post.save(commit=False)
    post.author = user
    post.save()
    return post.pk


def comment(comment, post, user):
    """
    Add a comment
    """
    comment = comment.save(commit=False)
    comment.post = post
    comment.user = user
    comment.save()
    return post.id


def edit(data, user, id):
    """
    Edit a post
    """
    if data.get("content") is not None:
        post = Post.objects.filter(id=id).first()
        if (post.author == user):
            post.content = data["content"]
            post.save()


def get_paginator(request, posts):
    """
    Break post lists by pages
    """
    paginator = Paginator(posts, 10)
    return paginator.get_page(request.GET.get('page'))


def manage_following_list(list, user):
    """
    Follow and unfollow
    """
    list.followees.remove(user) if user in list.followees.all() else list.followees.add(user)
    return {"status": user in list.followees.all(), "followers": len([usr.user for usr in FollowingList.objects.filter(followees__in=[user])]), "user": user.username}


def manage_likes(user, post):
    """
    Like and unlike
    """
    post.likes.remove(user) if user in post.likes.all() else post.likes.add(user)
    return {"status": user in post.likes.all(), "likes": len(post.likes.all())}