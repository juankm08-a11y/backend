from django.shortcuts import render
from django.utils import timezone
from rest_framework.views import APIView
from .permissions import PuedeVerDashboard, PuedeFinalizarOrden, PuedeAprobarOrden
from rest_framework.response import Response
from .models import OrdenMantenimiento, ActividadMantenimiento,ObservacionTecnica, Notificacion
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .serializers import OrdenMantenimientoSerializer, ActividadMantenimientoSerializer,ObservacionTecnicaSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Create your views here.

class DashboardResumenView(APIView):

    permission_classes = [IsAuthenticated, PuedeVerDashboard]

    def get(self,request):
        total = OrdenMantenimiento.objects.count()
        pendientes = OrdenMantenimiento.objects.filter(estado='pendiente').count()
        ejecutadas = OrdenMantenimiento.objects.filter(estado='ejecutada').count()

        criticas = OrdenMantenimiento.objects.filter(
            tipo="correctivo",
            estado="pendiente"
        ).count()

        return Response({
            "total_ordenes":total,
            "pendientes":pendientes,
            "ejecutadas":ejecutadas,
            "criticas":criticas
        })
    
    
class OrdenListCreateView(ListCreateAPIView):
    queryset = OrdenMantenimiento.objects.all()
    serializer_class = OrdenMantenimientoSerializer
    permission_classes = [IsAuthenticated, PuedeFinalizarOrden]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = ['estado','tipo','equipo']
    search_fields = ['codigo','descripcion']
    ordering_fields = ['fecha_creacion','fecha_ejecucion']
    ordering = ['-fecha_creacion']

    def perform_create(self,serializer):
        serializer.save(creado_por=self.request.user)

    def get_queryset(self):
        queryset = OrdenMantenimiento.objects.all()
        estado = self.request.query_params.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

class OrdenDetailView(RetrieveUpdateDestroyAPIView):
    queryset = OrdenMantenimiento.objects.all()
    serializer_class = OrdenMantenimientoSerializer
    permission_classes = [IsAuthenticated]

class RegistrarActividadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,orden_id):
        orden = get_object_or_404(OrdenMantenimiento,id=orden_id)

        if orden.estado in ['ejecutada','aprobada']:
            return Response(
                {"error":"No se pueden agregar actividades a una orden ejecutada"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ActividadMantenimientoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                orden=orden,
                creado_por=request.user if request.user.is_authenticated else None
            )

            if orden.estado == 'pendiente':
                orden.estado = 'en_proceso'
                orden.save()

            return Response(
                {"mensaje":"Actividad registrada exitosamente"},
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegistrarObservacionView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request,orden_id):
        orden = get_object_or_404(OrdenMantenimiento,id=orden_id)

        serializer = ObservacionTecnicaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                orden=orden,
                creado_por=request.user if request.user.is_authenticated else None
            )

            return Response(
                {"mensaje":"Observacion registrada exitosamente"},
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class FinalizarOrdenView(APIView):

    permission_classes = [IsAuthenticated, PuedeFinalizarOrden]
    
    def put(self,request,orden_id):
        orden = get_object_or_404(OrdenMantenimiento,id=orden_id)

        try:
            orden.finalizar(request.user)
        except ValidationError as e:
            return Response(
                {"error":str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        Notificacion.objects.create(
            orden=orden,
            mensaje=f"La orden {orden.codigo} fue ejecutada y está pendiente de aprobación."
        )

        return Response(
            {"mensaje":"Orden finalizada exitosamente."},
            status=status.HTTP_200_OK
        )
        
    

class AprobarOrdenView(APIView):
    permission_classes = [IsAuthenticated,PuedeAprobarOrden]

    def put(self,request,orden_id):
        orden = get_object_or_404(OrdenMantenimiento, id=orden_id)
        
        try:
            orden.aprobar(request.user)
        except Exception as e:
            return Response(
                {"error":str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        Notificacion.objects.create(
            orden=orden,
            mensaje=f"La orden {orden.codigo} fue aprobada y cerrada."
        )

class HistorialOrdenView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,orden_id):
        orden = get_object_or_404(OrdenMantenimiento, id=orden_id)

        actividades = ActividadMantenimiento.objects.filter(orden=orden)
        observaciones =  ObservacionTecnica.objects.filter(orden=orden)

        return Response({
            "orden":OrdenMantenimientoSerializer(orden).data,
            "actividades":ActividadMantenimientoSerializer(actividades,many=True).data,
            "observaciones":ObservacionTecnicaSerializer(observaciones,many=True).data
        })
    

class OrdenPendientesAprobacionView(generics.ListAPIView):
    serializer_class = OrdenMantenimientoSerializer

    def get_queryset(self):
        return OrdenMantenimiento.objects.filter(estado='ejecutada')
    

