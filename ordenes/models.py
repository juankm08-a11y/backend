from django.db import models
from django.conf import settings 
from django.utils import timezone
from django.core.exceptions import ValidationError
from equipos.models import EquipoBiomedico
from solicitudes.models import Solicitud

# Create your models here.
class OrdenMantenimiento(models.Model):
    TIPO_CHOICES = [
        ('preventivo','Preventivo'),
        ('correctivo','Correctivo')
    ]

    ESTADO_CHOICES = [
        ('pendiente','Pendiente'),
        ('proceso','En proceso'),
        ('ejecutada','Ejecutada'),
        ('aprobada','Aprobada')
    ]

    codigo = models.CharField(max_length=50,unique=True)
    
    equipo = models.ForeignKey(
        EquipoBiomedico,
        on_delete=models.CASCADE,
        related_name='ordenes_mantenimiento'
    )

    tipo = models.CharField(max_length=20,choices=TIPO_CHOICES)
    
    descripcion = models.TextField()

    estado = models.CharField(max_length=20,choices=ESTADO_CHOICES,default='pendiente')
    
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    fecha_ejecucion = models.DateTimeField(null=True,blank=True)

    aprobado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ordenes_aprobadas'
    )

    fecha_aprobacion = models.DateTimeField(null=True,blank=True)

    solicitud = models.OneToOneField(
        Solicitud,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orden_generada'
    )

    def finalizar(self,usuario):
        if self.estado not in ['pendiente','en_proceso']:
            raise ValidationError("Solo se pueden finalizar órdenes pendientes o en proceso.")
        
        if not self.actividades.exists():
            raise ValidationError("No se puede finalizar sin actividades registradas.")
        
        self.estado = 'ejecutada'
        self.fecha_ejecucion = timezone.now()
        self.save()
        
    def aprobar(self,usuario):
        if self.estado != 'ejecutada':
            raise ValidationError("Solo se pueden aprobar órdenes ejecutadas.")
        
        self.estado = 'aprobada'
        self.fecha_aprobacion = timezone.now()
        self.aprobado_por = usuario
        self.save()

    def __str__(self):
        return f"{self.codigo} - {self.equipo.nombre}"

    class Meta:
        permissions = [
            ("puede_finalizar_orden","Puede finalizar_orden"),
            ("puede_aprobar_orden","Puede aprobar orden"),
            ("puede_ver_dashboard","Puede ver dashboard")
        ]
    

class ActividadMantenimiento(models.Model):

    orden = models.ForeignKey(
        'OrdenMantenimiento',
        on_delete=models.CASCADE,
        related_name='actividades'
    )

    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Actividad Orden {self.orden.codigo}"
    
class ObservacionTecnica(models.Model):
    orden = models.ForeignKey(
        'OrdenMantenimiento',
        on_delete=models.CASCADE,
        related_name='observaciones'
    )

    observacion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Observación Orden {self.orden.codigo}"
    

class Notificacion(models.Model):
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    orden= models.ForeignKey(
        OrdenMantenimiento,
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )
    
    def __str__(self):
        return self.mensaje
    
    