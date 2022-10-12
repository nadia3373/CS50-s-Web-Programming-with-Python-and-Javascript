from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add"),
    path("bid/<str:id>", views.bid, name="bid"),
    path("categories", views.categories, name="categories"),
    path("category/<str:id>", views.category, name="category"),
    path("close/<str:id>", views.close, name="close"),
    path("comment/<str:id>", views.comment, name="comment"),
    path("listings/<str:id>", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watched", views.watched, name="watched"),
    path("watchlist/<str:id>", views.watchlist, name="watchlist"),
]
