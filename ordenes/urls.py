from django.urls import path
from .views import DashboardResumenView,OrdenListCreateView, OrdenDetailView, RegistrarActividadView,RegistrarObservacionView,FinalizarOrdenView, AprobarOrdenView, HistorialOrdenView, OrdenPendientesAprobacionView

urlpatterns = [
    path('dashboard/resumen/',DashboardResumenView.as_view()),
    path('ordenes/',OrdenListCreateView.as_view()),
    path('ordenes/<int:pk>/',OrdenDetailView.as_view()),
    path('ordenes/<int:orden_id>/actividades/', RegistrarActividadView.as_view()),
    path('ordenes/<int:orden_id>/observaciones/',RegistrarObservacionView.as_view()),
    path('ordenes/<int:orden_id>/finalizar/',FinalizarOrdenView.as_view()),
    path('ordenes/<int:orden_id>/aprobar/',AprobarOrdenView.as_view()),
    path('ordenes/<int:orden_id>/historial/',HistorialOrdenView.as_view()),
    path('ordenes/pendientes-aprobacion/',OrdenPendientesAprobacionView.as_view()),
]