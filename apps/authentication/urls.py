# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import login_view, register_user, verify_registration,forget,verify_forget
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('verify/', verify_registration, name="verify_registration"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('forget/', forget, name="forget"),
    path('verify_forget/', verify_forget, name="verify_forget"),
    path('change-password/', views.change_password, name='change_password'),
]
