from django.db import models
UNIDADES_MEDIDA = [(1, 'Pesos'), (2, 'Hab'), (3, 'm2'), (4, '%'), (5, 'Días')]
TIPO_FACTURA = [(1, 'Arrendamiento'), (2, 'Penalidades')]
ESTADO_FACTURA = [(1, 'Temporal'), (2, 'Pendiente'), (3, 'Confirmada'), (4, 'Contabilizada'), (5, 'Cancelada')]

CONCEPTO_FACTURACION = \
    [(1, 'Valor Inicial AFT'), (2, 'Total Habitaciones en la Instalación Hotelera'), (3, 'Area Total Arrendada'),
    (4, 'Tasa de Arrendamiento'), (5, 'Tasa de Depreciación'), (6, 'Poliza de Seguro de la Instalación'),
    (7, 'por Habitaciones Fuera de Orden'), (8, 'por Áreas Fuera de Orden'), (9, 'por Sistemas Fuera de Orden'),
    (10, 'por Dismin. en Póliza de Seguro'), (11, 'por Activos Fuera de Orden, reubicados o de baja'),
    (12, 'por Increm. en Póliza de Seguro'), (13, 'por Activos de nueva incorporación'),
    (14, 'Por Mora en el Pago de la factura mes anterior')]

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
    tasa_arrenda = models.DecimalField(unique=False, blank=False, null=True, max_digits=28, decimal_places=5)
    activo = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

class clientes (entidades):
    #esta clase hereda todo_de entidades
    id_arrendador = models.ForeignKey('entidades', related_name='arrendador', on_delete=models.CASCADE, blank=False, null=False)
    no_contrato = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    no_suplemento = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    cod_contab = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    id_tipo = models.ForeignKey('tipo_cliente', on_delete=models.CASCADE, blank=False, null=False)
    total_habi = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    total_area = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    tasa_depre = models.DecimalField(unique=False, blank=True, null=True, max_digits=28, decimal_places=2)
    poli_seguro = models.DecimalField(unique=False, blank=True, null=True, max_digits=28, decimal_places=2)
    id_aft = models.IntegerField(unique=False, blank=False, null=True, help_text='ID del cliente en ZUNaft')
    def __str__(self):
        return self.nombre

class tipo_facturas(models.Model):
    tipo = models.IntegerField(unique=False, blank=False, null=False, help_text='', choices=TIPO_FACTURA)
    cta_ingreso = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='')
    cta_xcobrar = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='')
    actividad = models.CharField(max_length=255, unique=False, blank=True, null=True, help_text='')
    activo = models.BooleanField(default=True)
    def __str__(self):
        return self.get_tipo_display()

class factura_cabecera(models.Model):
    id_entidad = models.ForeignKey('entidades', related_name='entidad', on_delete=models.CASCADE, blank=False, null=False)
    id_cliente = models.ForeignKey('clientes', related_name='cliente', on_delete=models.CASCADE, blank=False, null=False)
    id_tipo_factura = models.ForeignKey('tipo_facturas', related_name='tipo_factura', on_delete=models.CASCADE, blank=False, null=False)
    folio = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='')
    numero = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='')
    fecha_factura = models.DateField(blank=False, null=False)
    fecha_confirmada = models.DateField(blank=True, null=True)
    fecha_facturada = models.DateField(blank=True, null=True)
    estado = models.IntegerField(unique=False, blank=False, null=False, help_text='', choices=ESTADO_FACTURA)
    confirmada_x = models.ForeignKey('app_seguridad.User', related_name='id_user_confirmada', on_delete=models.CASCADE, blank=True, null=True)
    contabilizada_x = models.ForeignKey('app_seguridad.User', related_name='id_user_contabiliza', on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return self.numero.__str__()

class factura_detalle(models.Model):
    id_cabecera = models.ForeignKey('factura_cabecera', on_delete=models.CASCADE, blank=False, null=False)
    concepto = models.IntegerField(unique=False, blank=False, null=False, help_text='', choices=CONCEPTO_FACTURACION)
    um = models.IntegerField(unique=False, blank=False, null=False, help_text='', choices=UNIDADES_MEDIDA)
    valor = models.DecimalField(unique=False, blank=False, null=False, max_digits=28, decimal_places=2)
    importe = models.DecimalField(unique=False, blank=False, null=False, max_digits=28, decimal_places=2)
    def __str__(self):
        return self.id_cabecera.__str__()

class valores_aft(models.Model):
    id_cliente = models.ForeignKey('clientes', on_delete=models.CASCADE, blank=False, null=False)
    id_periodo = models.ForeignKey('periodo_contab', on_delete=models.CASCADE, blank=False, null=True)
    valor = models.DecimalField(unique=False, blank=False, null=False, max_digits=28, decimal_places=2)
    def __str__(self):
        return self.id_cliente.__str__()

class ejerc_contab (models.Model):
    id_entidad = models.ForeignKey('entidades', on_delete=models.CASCADE, blank=False, null=False)
    cod_ejerc_contab = models.IntegerField(unique=False, blank=False, null=True, help_text='')
    nombre = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='')
    class Meta:
        ordering = ['id_entidad','cod_ejerc_contab']
    def __str__(self):
        return self.nombre.__str__()

class periodo_contab (models.Model):
    id_ejercicio = models.ForeignKey('ejerc_contab', on_delete=models.CASCADE, blank=False, null=True)
    cod_periodo_contab = models.IntegerField(unique=False, blank=False, null=True, help_text='')
    nombre = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='')
    desde = models.DateTimeField(blank=True, null=True)
    hasta = models.DateTimeField(blank=True, null=True)
    class Meta:
        ordering = ['desde', 'hasta']
    def __str__(self):
        return self.desde.__str__() + ' ' + self.hasta.__str__() + ' ' + self.nombre.__str__()