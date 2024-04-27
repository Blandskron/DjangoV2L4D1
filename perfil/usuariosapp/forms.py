from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser


class SignUpForm(UserCreationForm):
    nombre = forms.CharField(max_length=100, required=True)
    apellido = forms.CharField(max_length=100, required=True)
    correo = forms.EmailField(required=True)
    edad = forms.IntegerField(required=False)
    foto_perfil = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'nombre', 'apellido', 'correo', 'edad', 'foto_perfil']
        labels = {
            'username': 'Nombre de usuario',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'correo': 'Correo electrónico',
            'edad': 'Edad',
            'foto_perfil': 'Foto de perfil'
        }

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'nombre', 'apellido', 'correo', 'edad', 'foto_perfil')
