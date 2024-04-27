from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.contrib.auth.models import Group, Permission

# Registra el modelo CustomUser en el panel de administración
admin.site.register(CustomUser, UserAdmin)
# Obtiene el grupo de administradores o lo crea si no existe
admin_group, created = Group.objects.get_or_create(name='Administradores')

# Obtiene los permisos necesarios para administrar el modelo CustomUser
custom_user_permissions = Permission.objects.filter(content_type__app_label='tu_app', codename__startswith='change_customuser')

# Asigna los permisos al grupo de administradores
admin_group.permissions.add(*custom_user_permissions)