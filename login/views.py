from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from django.contrib.auth import login, get_user_model 
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import LoginSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer, CustomTokenObtainPairSerializer
# Create your views here.



User = get_user_model()

class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self,request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request,user)

            return Response({
                "mensaje":"Inicio de sesión exitoso",
                "rol":user.rol,
                "correo":user.correo_institucional
            }, status=status.HTTP_200_OK)
        
        return Response({
            "mensaje":"Credenciales inválidas"
        },status=status.HTTP_401_UNAUTHORIZED)
    

class PasswordResetView(APIView):

    permission_classes = [AllowAny]

    def post(self,request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        correo = serializer.validate_data['correo_institucional']
        
        try: 
            user = User.objects.get(correo_institucional=correo)
        except User.DoesNotExist:
            return Response(
                {"mensaje":"Si el correo existe, se enviará un enlace"},
                status=status.HTTP_200_OK
            )

        uid = urlsafe_base64_decode((force_bytes(user.pk)))
        token = default_token_generator.make_token(user)

        link = f"http://localhost:5173/reset-password/{uid}/{token}/"

        send_mail(
            subject="Recuperar acceso",
            message=f"Usa este enlace para recuperar tu correo:\n{link}",
            from_email="no-reply@sistema.com",
            recipient_list=[correo]
        )

        return Response({
            "mensaje":"Si el correo existe, se enviará un enlace de recuperación"
        }, status=status.HTTP_200_OK)

class PasswordResetConfirmView(APIView):

    permission_classes = [AllowAny]

    def post(self,request):
        serializer = PasswordResetConfirmSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                "mensaje":"Datos inválidos",
            },status=status.HTTP_400_BAD_REQUEST)
        
        uid = serializer.validated_data['uid']
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({
                "mensaje":"Enlace inválido o expirado"
            },status=status.HTTP_400_BAD_REQUEST)
        
        if not default_token_generator.check_token(user,token):
            return Response({
                "mensaje":"Enlace inválido o expirado"
            },status=status.HTTP_400_BAD_REQUEST)
        

        user.set_password(new_password)
        user.save()

        return Response({
            "mensaje":"Contraseña actualizada correctamente"
        },status=status.HTTP_200_OK)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer