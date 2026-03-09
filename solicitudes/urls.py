from django.urls import path
from .views import SolicitudViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'solicitudes',SolicitudViewSet)

urlpatterns = router.urls 