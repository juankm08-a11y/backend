from django.db import models
from django.conf import settings

# Create your models here.
class EquipoBiomedico(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50,unique=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100,blank=True,null=True)
    ubicacion = models.CharField(max_length=100)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('activo','Activo'),
            ('inactivo','Inactivo'),
        ],
        default='activo'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    hoja_vida_vida = models.FileField(
        upload_to='hojas_vida/',
        null=True,
        blank=True
    )

    qr_codigo = models.ImageField(
        upload_to='qr_equipos/',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
    