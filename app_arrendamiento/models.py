from django.db import models

# Create your models here.
class entidades(models.Model):
    nombre = models.CharField(max_length=255, unique=False, blank=False, null=False, help_text='')
    activo = models.BooleanField(default=True)


    def __str__(self):
        return self.nombre