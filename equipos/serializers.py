from rest_framework import serializers
from .models import EquipoBiomedico

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipoBiomedico
        fields = [
            'id',
            'nombre',
            'codigo',
            'marca',
            'modelo',
            'numero_serie',
            'ubicacion',
            'estado',
            'fecha_registro'
        ]