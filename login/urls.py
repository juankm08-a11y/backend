from django.urls import path 
from .views import (
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView
)
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('login/',LoginView.as_view()),
    path('recuperar-acceso',PasswordResetView.as_view()),
    path('recuperar-acceso/confirmar/',PasswordResetConfirmView.as_view()),
    path('token/',CustomTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh')
]