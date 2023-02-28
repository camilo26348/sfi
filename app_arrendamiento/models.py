from django.db import models
UNIDADES_MEDIDA = [(1, 'Pesos'), (2, 'Hab'), (3, 'm2'), (4, '%'), (5, 'Días')]
TIPO_SERVICIO = [(1, 'Arrendamiento'), (2, 'Penalidades')]
TIPO_DET_SERVICIO = [(1, 'Servicios'), (2, 'Descuento'), (3, 'Recargo'), (4, 'Penalidades')]
ESTADO_FACTURA = [(1, 'Temporal'), (2, 'Pendiente'), (3, 'Confirmada'), (4, 'Contabilizada'), (5, 'Cancelada')]

# Create your models here.
class entidades(models.Model):
    nombre = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='')
    direccion = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    telef = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    correo = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    cod_one = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    nit = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    nirc = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    cuenta_cup = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    titular_cup = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    suc_banc = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    ccosto_arrenda = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    activo = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

class tipo_cliente(models.Model):
    nombre = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='')
    tasa_arrendamiento = models.DecimalField(unique=False, blank=False, null=False, max_digits=28, decimal_places=2)
    activo = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

class clientes (entidades):
    id_arrendador = models.ForeignKey('entidades', related_name='arrendador', on_delete=models.CASCADE, blank=True, null=True)
    no_contrato = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    cod_contab = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    id_tipo = models.ForeignKey('tipo_cliente', on_delete=models.CASCADE, blank=False, null=False)

    total_habi = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    total_area = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    def __str__(self):
        return self.nombre

class servicios(models.Model):
    tipo = models.IntegerField(unique=False, blank=False, null=False, help_text='', choices=TIPO_SERVICIO)
    cta_ingreso = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='')
    cta_xcobrar = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='')
    actividad = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    activo = models.BooleanField(default=True)
    def __str__(self):
        return self.get_tipo_display()

class detalle_servicios(models.Model):
    id_servicio = models.ForeignKey('servicios', on_delete=models.CASCADE, blank=False, null=False)
    nombre = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='')
    um = models.IntegerField(unique=False, blank=False, null=False, help_text='', choices=UNIDADES_MEDIDA)
    tipo = models.IntegerField(unique=False, blank=False, null=False, help_text='', choices=TIPO_DET_SERVICIO)
    activo = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

class factura_cabecera(models.Model):
    id_entidad = models.ForeignKey('entidades', related_name='entidad', on_delete=models.CASCADE, blank=False, null=False)
    id_cliente = models.ForeignKey('clientes', related_name='cliente', on_delete=models.CASCADE, blank=False, null=False)
    folio = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='')
    numero = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='')
    fecha_factura = models.DateField(blank=False, null=False)
    fecha_confirmada = models.DateField(blank=True, null=True)
    fecha_facturada = models.DateField(blank=True, null=True)
    estado = models.IntegerField(unique=False, blank=False, null=False, help_text='', choices=ESTADO_FACTURA)
    confirmada_x = models.ForeignKey('app_seguridad.User', related_name='id_user_confirmada', on_delete=models.CASCADE, blank=False, null=False)
    contabilizada_x = models.ForeignKey('app_seguridad.User', related_name='id_user_contabiliza', on_delete=models.CASCADE, blank=False, null=False)
    def __str__(self):
        return self.numero.__str__()

class factura_detalle(models.Model):
    id_cabecera = models.ForeignKey('factura_cabecera', on_delete=models.CASCADE, blank=False, null=False)
    id_detalle_servicio = models.ForeignKey('detalle_servicios', on_delete=models.CASCADE, blank=False, null=False)
    valor = models.DecimalField(unique=False, blank=False, null=False, max_digits=28, decimal_places=2)
    importe = models.DecimalField(unique=False, blank=False, null=False, max_digits=28, decimal_places=2)
    def __str__(self):
        return self.id_cabecera.__str__()