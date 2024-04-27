from django.contrib.auth.backends import ModelBackend
from .models import CustomUser

class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Intenta autenticar con el modelo de usuario predeterminado
            user = super().authenticate(request, username=username, password=password, **kwargs)
            if user:
                return user
            
            # Si la autenticación con el usuario predeterminado falla, intenta con el modelo personalizado
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            pass
        
        # Si no se encuentra ningún usuario válido, devuelve None
        return None
