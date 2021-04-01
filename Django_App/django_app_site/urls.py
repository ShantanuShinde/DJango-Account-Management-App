from django.urls import path

from . import views

urlpatterns = [
    path('', views.register),
    path('verification/', views.verify),
    path('login/', views.user_login),
    path('ver_ack/', views.verify_ack),
    path('main_page/', views.main_page),
    path('logout/', views.user_logout),
    path('change_cred/', views.change_credenials),
]