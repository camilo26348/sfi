# -*- coding: utf-8 -*-
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('iniciar_sesion', views.login, name='login'),
    path('cerrar_sesion', views.logout, name='logout'),
    #path('registrarse', views.registro, name='registro'),
    path('clave_olvidada', views.clave_olvidada, name='clave_olvidada'),
    #path('pendiente_activar', views.pendiente_activar, name='pendiente_activar'),
    path('pendiente_nueva_clave', views.pendiente_nclave, name='pendiente_nclave'),
    #path('activar_usuario=<str:token>', views.activar_usuario, name='activar_usuario'),
    path('nueva_clave=<str:token>', views.nueva_clave, name='nueva_clave'),
    #path('error_activacion', views.error_activar, name='error_activar'),
    path('error_nueva_clave', views.error_nclave, name='error_nclave'),
]