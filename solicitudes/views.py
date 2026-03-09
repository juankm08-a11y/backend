from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Solicitud
from .serializers import SolicitudSerializer
from ordenes.models import OrdenMantenimiento

# Create your views here.

class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(solicitante=self.request.user)

    
    @action(detail=True,methods=['patch'])
    def aprobar(self,request,pk=None):
        solicitud = self.get_object()

        if request.user.rol != "administrador":
            return Response(
                {"error":"No tienes permisos"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        solicitud.estado = "aprobada"
        solicitud.aprobado_por = request.user 
        solicitud.save()
        
        return Response({"mensaje":"Solicitud aprobada"})
    
    @action(detail=True,methods=['post'])
    def convertir_a_orden(self,request,pk=None):
        solicitud = self.get_object()

        if solicitud.estado != 'aprobada':
            return Response(
                {"error":"Solo solicitudes aprobadas pueden convertirse en orden"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        orden = OrdenMantenimiento.objects.create(
            codigo=codigo_generado,
            equipo=solicitud.equipo,
            tipo="correctivo",
            descripcion=solicitud.descripcion,
            creado_por=request.user,
            solicitud=solicitud
        )

        solicitud.estado = "convertida"
        solicitud.save()

        return Response({
            "mensaje":"Orden creada exitosamente",
            "orden_id":orden.id
        })