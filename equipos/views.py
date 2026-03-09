from django.shortcuts import render
from rest_framework import generics
from .models import EquipoBiomedico
from .serializers import EquipoSerializer
from rest_framework.permissions import AllowAny

# Create your views here.
class EquipoListCreateView(generics.ListCreateAPIView):
    queryset = EquipoBiomedico.objects.all()
    serializer_class = EquipoSerializer
    permission_classes = [AllowAny]

class EquipoDetailView(generics.RetrieveAPIView):
    queryset = EquipoBiomedico.objects.all()
    serializer_class = EquipoSerializer
    permission_classes = [AllowAny]