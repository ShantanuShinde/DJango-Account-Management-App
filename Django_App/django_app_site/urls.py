from django.urls import path

from . import views

urlpatterns = [
    path('', views.register),
    path('verification/', views.verify),
    path('login/', views.login),
    path('ver_ack/', views.verify_ack),
]