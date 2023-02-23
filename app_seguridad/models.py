#-*- coding: utf-8 -*-
from django.db import models
from gettext import gettext as _
from django.contrib.auth.models import AbstractUser

ESTADO = [(1 , 'Activo'), (2 , 'Pendiende'), (3 , 'Desactivado')]
TIPO_TOKEN = [(1 , 'Activar usuario'), (2 , 'Nueva clave')]

# Create your models here.
class User (AbstractUser):
    nombre = models.CharField(max_length=255, blank=True, null=True, unique=False, help_text='Nombre(s) y Apellidos')
    estado = models.IntegerField(unique=False, blank=False, null=False, help_text='', choices=ESTADO, default=1)
    REQUIRED_FIELDS = ['email']
    def __str__(self):
        return self.username

class usuarios_entidades(models.Model):
    id_user = models.ForeignKey('User', on_delete=models.CASCADE, blank=False, null=False)
    id_entidad = models.ForeignKey('app_arrendamiento.entidades', on_delete=models.CASCADE, blank=False, null=False)
    def __str__(self):
        return self.id_user.__str__() + ' - ' + self.id_entidad.__str__()

class token_user (models.Model):
    id_usuario = models.ForeignKey('User', on_delete=models.CASCADE, blank=False, null=False)
    token = models.CharField(max_length=128, unique=False, blank=False, null=False, help_text='')
    fecha_creacion = models.DateTimeField(null=False, blank=False, auto_now=True)
    tipo = models.IntegerField(unique=False, blank=False, null=False, help_text='', choices=TIPO_TOKEN)
    enviado = models.BooleanField(default=False)
    def __str__(self):
        return self.id_usuario.username + ' ' + self.token

class config_correo(models.Model):
    remitente = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='Nombre del remitente')
    asunto = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='Asunto del correo')
    serv_smtp = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='IP o nombre del serividor SMTP')
    serv_puerto = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='Puerto de conexion al SMTP')
    serv_ssl = models.BooleanField(default=False, help_text='Tiene o no SSL el servidor SMTP')
    serv_tls = models.BooleanField(default=True, help_text='Tiene o no TLS el servidor SMTP')
    usuario = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='Usuario para autenticar en el SMTP')
    password = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='Clave para autenticar en el SMTP')
    def __str__(self):
        return self.remitente

class config_sistema(models.Model):
    url_sistema = models.CharField(max_length=255, unique=False, blank=False, null=False, default='http://')
    term_condic = models.TextField(blank=False, null=True)
    def __str__(self):
        return self.url_sistema