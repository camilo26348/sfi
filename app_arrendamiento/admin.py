from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(entidades)
admin.site.register(tipo_cliente)
admin.site.register(clientes)
admin.site.register(tipo_facturas)
admin.site.register(factura_cabecera)
admin.site.register(factura_detalle)