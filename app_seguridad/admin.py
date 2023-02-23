from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(token_user)
admin.site.register(config_correo)
admin.site.register(config_sistema)
admin.site.register(usuarios_entidades)