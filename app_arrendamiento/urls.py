# -*- coding: utf-8 -*-
from django.urls import path, re_path
from app_arrendamiento import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
]