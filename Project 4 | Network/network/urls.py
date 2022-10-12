
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("comment/<str:id>", views.comment, name="comment"),
    path("edit/<str:id>", views.edit, name="edit"),
    path("follow/<str:id>", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("like/<str:id>", views.like, name="like"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("posts/<str:id>", views.post, name="post"),
    path("register", views.register, name="register"),
    path("users/<str:id>", views.profile, name="user")
]
