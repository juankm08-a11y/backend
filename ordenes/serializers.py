from rest_framework import serializers
from .models import OrdenMantenimiento, ActividadMantenimiento,ObservacionTecnica

class OrdenMantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenMantenimiento
        fields = [
            'id',
            'codigo',
            'equipo',
            'tipo',
            'descripcion',
            'estado',
            'creado_por',
            'fecha_ejecucion',
            'fecha_creacion'
        ]

        read_only_fields = [
            'id',
            'estado',
            'creado_por',
            'fecha_creacion',
            'fecha_ejecucion'
        ]

    def validate_estado(self,value):
        if value in ['ejecutada','aprobada']:
            raise serializers.ValidationError("No puede crear una orden ya cerrada.")
        return value


class ActividadMantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadMantenimiento
        fields = ['id','descripcion','fecha']
        read_only_fields = ['id','fecha']

class ObservacionTecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObservacionTecnica
        fields = ['id','observacion','fecha']
        read_only_fields = ['id','fecha']

