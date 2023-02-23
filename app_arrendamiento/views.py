from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from app_seguridad.decorators import login_required

@login_required
def index(request):
    return redirect('dashboard')

def dashboard(request):
    title = 'Dashboard | SFI'
    link = 'dashboard'
    notif = messages.get_messages(request)
    return render(request, 'dashboard.html', locals())