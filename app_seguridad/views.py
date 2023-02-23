from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from app_seguridad.decorators import login_required
from app_seguridad.models import User, token_user, config_sistema, config_correo
from django.contrib.auth.hashers import make_password
from django.contrib import messages
import string, secrets
import smtplib
from email.message import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from sfi.settings import BASE_DIR
import os

#Esta es la vista del logout
@login_required
def logout(request):
    django_logout(request)
    return redirect('login')

#Esta es la vista del login
def login(request):
    #django_logout(request) #primero ejecuto el logout por si se quedó una sesión activa
    if request.user.is_authenticated==True:
        return redirect('dashboard')
    title = 'Iniciar sesión | SFI'
    notif = messages.get_messages(request)
    subtitle = 'Bienvenido 👋'
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        pre_user = User.objects.filter(username__exact=username).first()
        user = authenticate(username=username, password=password)
        if user is not None:
            if pre_user.estado == 1:
                django_login(request, user)
                return redirect('dashboard')
            elif pre_user.estado == 2:
                notif_pend = ('Su usuario aun no se ha activado. Revise su correo')
            elif pre_user.estado == 3:
                notif_desact = ('Su usuario está desactivado. Contacte con el administrador del sistema')
        else:
            error = ('Usuario o contraseña incorrectos')
    return render(request, 'login.html', locals())


def pendiente_nclave(request):
    title = 'Registrarse | SFI'
    subtitle = 'Su clave anterior ya es cosa del pasado 😊'
    subtitle2 = 'Hemos enviado a su correo las instrucciones para establecer una nueva clave para su usuario'
    return render(request, 'pendiente.html', locals())

def crear_token(id_usuario, tipo):
    user = User.objects.get(id=id_usuario)
    if token_user.objects.filter(id_usuario=id_usuario).exists():
        token_user.objects.filter(id_usuario=id_usuario).delete()
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for i in range(128))
    token_user.objects.create(id_usuario=user, token=token, tipo=tipo)

def clave_olvidada(request):
    if request.user.is_authenticated==True:
        return redirect('dashboard')
    notif = messages.get_messages(request)
    title = 'Nueva contraseña | SFI'
    subtitle = '¿Olvidó su contraseña? 🔒'
    if request.POST:
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.filter(email__exact=email).first()
            user.estado = 2
            user.save()
            crear_token(id_usuario=user.id, tipo=2)
            enviar_token_nclave(id_usuario=user.id)
            return redirect('pendiente_nclave')
        else:
            messages.add_message(request, messages.ERROR, 'No se pudo encontrar un usuario con esa dirección de correo. Verifique')
    return render(request, 'clave_olvidada.html', locals())

def enviar_token_nclave(id_usuario):
    tok = token_user.objects.filter(id_usuario=id_usuario).first()
    cs = config_sistema.objects.first()
    us = User.objects.get(id=id_usuario)
    titulo = 'Bienvenido a SFI'
    subtitulo = 'Gracias por usar nuestro sistema. Para completar el registo del usuario <strong>' + us.username.__str__() + '</strong> haga click en el botón a continuación'
    subtitulo2 = 'No es necesario respoder a este correo, si no fue usted el que solicitó esta acción sencillamente elimine este correo y disculpe las molestias ocasionadas.'
    footer = 'Estamos en <strong>www.ca3soft.cu</strong> dispuestos a trabajar por y para usted'
    link = cs.url_sistema.__str__() + '/nueva_clave=' + tok.token.__str__()
    text_boton = 'Nueva Clave'
    d = {'titulo': titulo, 'subtitulo': subtitulo, 'subtitulo2': subtitulo2, 'footer': footer, 'link': link,
         'text_boton': text_boton}
    enco = enviar_correo_html(id_usuario=id_usuario, contenido=d)
    if enco:
        #tok.enviado = True
        tok.save()

def nueva_clave(request, token):
    t = token_user.objects.filter(token__exact=token).first()
    if t and t.tipo==2:
        if request.POST:
            password = request.POST['password']
            u = User.objects.get(id=t.id_usuario.id)
            u.password=make_password(password)
            u.estado = 1
            u.save()
            t.delete()
            messages.add_message(request, messages.SUCCESS, 'Su contraseña ha sido cambiada 😉')
            return redirect('login')
        return render(request, 'nueva_clave.html', locals())
    else:
        return redirect('error_nclave')

def error_nclave(request):
    title = 'Registrarse | SFI'
    subtitle = 'No ha se ha podido crear nueva clave'
    subtitle2 = 'Revise que ha seguido las instrucciones que se han enviado a su correo o verifique que su clave ya haya sido cambiada'
    return render(request, 'pendiente.html', locals())

def enviar_correo_html(id_usuario, contenido):
    try:
        user = User.objects.get(id=id_usuario)
        conf = config_correo.objects.first()
        subject = conf.asunto.__str__()
        from_email = conf.usuario.__str__()
        to = user.email.__str__()
        # plaintext = get_template('plantilla_email.html')
        html_template = get_template('plantilla_email.html')
        # text_content = plaintext.render()
        text_content = ''
        html_content = html_template.render(contenido)
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True
    except Exception as e:
        print("Error: el mensaje no pudo ser enviado: " + e.__str__())
        return False