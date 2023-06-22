from django.urls import path
import os

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path("companies/<str:id>", views.company, name="company"),
    path("companies/<str:id>/about", views.about, name="about"),
    path("companies/<str:id>/appointments", views.appointments, name="appointments"),
    path("companies/<str:id>/company_settings", views.company_settings, name="company_settings"),
    path("companies/<str:id>/delete_image/<str:img>", views.delete_image, name="delete_image"),
    path("companies/<str:id>/gallery", views.gallery, name="gallery"),
    path("companies/<str:id>/gallery_management", views.gallery_management, name="gallery_management"),
    path("login", views.login_view, name="login"),
    # path("companies/<str:id>/location", views.location, name="location"),
    path("companies/<str:id>/logout", views.logout_view, name="logout"),
    path("companies/<str:id>/manage", views.manage, name="manage"),
    path("companies/<str:id>/profile", views.profile, name="profile"),
    path("companies/<str:id>/settings", views.settings, name="settings"),
    path("companies/<str:id>/register", views.register, name="register"),
    path("companies/<str:id>/register_manager", views.register_manager, name="register_manager"),
    path("companies/<str:id>/services", views.services, name="services"),
    path("companies/<str:id>/add_service", views.add_service, name="add_service"),
    path("companies/<str:id>/wh", views.wh, name="wh"),
    path("companies/<str:id>/edit_service/<str:sid>", views.edit_service, name="edit_service"),
    path("companies/<str:id>/service/<str:sid>", views.service, name="service"),
    path("companies/<str:id>/cancel/<str:app>", views.cancel, name="cancel"),
    path("companies/<str:id>/confirm/<str:app>", views.confirm, name="confirm"),
    path("companies/<str:id>/<str:sid>/<str:date>", views.times, name="times"),
    path("register", views.register_company, name="register_company")
]