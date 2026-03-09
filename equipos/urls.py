from django.urls import path
from .views import EquipoListCreateView, EquipoDetailView

urlpatterns = [
    path('equipos/',EquipoListCreateView.as_view()),
    path('equipos/<int:pk>/',EquipoDetailView.as_view())
]