from django.db import models
from django.conf import settings
from equipos.models import EquipoBiomedico

# Create your models here.


class Solicitud(models.Model):

    TIPO_SERVICIO_CHOICES = [
        ('biomedico','Biomedico'),
        ('sistemas','Sistemas'),
        ('infraestructura','Infraestructura'),
    ]

    PRIORIDAD_CHOICES = [
        ('baja','Baja'),
        ('media','Media'),
        ('alta','Alta'),
        ('critica','Crítica')
    ]

    ESTADO_CHOICES = [
        ('pendiente','Pendiente'),
        ('aprobada','Aprobada'),
        ('rechazada','Rechazada'),
        ('convertida','Convertida en Orden')
    ]

    equipo = models.ForeignKey(
        'equipos.EquipoBiomedico',
        on_delete=models.PROTECT,
        related_name='solicitudes'
    )

    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT  
    )

    tipo_servicio = models.CharField(
        max_length=20,
        choices=TIPO_SERVICIO_CHOICES
    )

    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDAD_CHOICES,
        default='media'
    )

    descripcion = models.TextField()

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='pendiente'
    )
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitud {self.id} - {self.equipo.nombre}"
