from rest_framework import serializers
from .models import Solicitud

class SolicitudSerializer(serializers.ModelSerializer):

    class Meta:
        model = Solicitud
        fields = '__all__'
        read_only_fields = ['estado','fecha_creacion','solicitante']

        