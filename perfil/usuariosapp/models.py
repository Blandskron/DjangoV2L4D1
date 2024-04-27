from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    edad = models.IntegerField(blank=True, null=True)
    foto_perfil = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name='custom_users')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_users')


    def __str__(self):
        return self.username
