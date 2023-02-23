# -*- coding: utf-8 -*-
from django.shortcuts import redirect

def login_required(function):
    def wrapper(*args):
        request = args[0]
        if not request.user.is_authenticated:
            return redirect('login')
        else:
            return function(*args)
    return wrapper
