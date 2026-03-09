from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.
class Usuario(AbstractUser):
    correo_institucional = models.EmailField(unique=True)
    rol = models.CharField(
        max_length=30,
        choices=[
            ('ingeniero','Ingeniero Biomédico'),
            ('coordinador','Coordinador Biomédico'),
            ('admin','Administrador'),
        ],
        default='ingeniero'
    )

    is_activo = models.BooleanField(default=True)

    USERNAME_FIELD = 'correo_institucional'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        self.correo_institucional = self.correo_institucional.lower()
        super().save(*args,**kwargs)
