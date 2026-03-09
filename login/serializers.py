from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    correo_institucional = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self,data):
        correo = data.get('correo_institucional')
        password = data.get('password')

        if not correo or not password:
            raise serializers.ValidationError(
                "Usuario o contraseña no válidos"
            )
        
        user = authenticate(
            username=correo,
            password=password
        )

        if not user:
            raise serializers.ValidationError(
                "Usuario o contraseña no válidos"
            )
        
        data['user'] = user
        return data
    
class PasswordResetSerializer(serializers.Serializer):
    correo_institucional = serializers.EmailField()

    def validate_correo_institucional(self,value):
        if not User.objects.filter(correo_institucional=value).exists():
            raise serializers.ValidationError(
                "Si el correo existe, se enviará un enlace de recuperación"
            )
        
        if not self.correo_institucional.endswith("@hospital.com"):
            raise serializers.ValidationError("Debe usar correo institucional")
        

class PasswordResetConfirmSerializer(serializers.Serializer):
    def validate_new_password(self,value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    username_field = 'correo_institucional'

    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)

        token['rol'] = user.rol  
        token['correo'] = user.correo_institucional

        return token
