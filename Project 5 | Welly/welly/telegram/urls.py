from django.urls import path
import os

from . import views


urlpatterns = [
    path("messages", views.messages, name="messages"),
]