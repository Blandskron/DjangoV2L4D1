# DjangoV2L4D1

```
python -m venv venv
```

```
venv\Scripts\activate
```

```
pip install django
pip install pillow
pip install psycopg2
```
# O puedes correr esta version
```
pip install django pillow psycopg2
```

```
django-admin startproject perfil
```

```
cd perfil
python manage.py startapp usuariosapp
```

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'usuariosapp',
]
```
# Models.py
```
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)

    def __str__(self):
        return self.user.username

```
# Views.py
```
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def profile(request):
    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            profile = request.user.userprofile
            profile.profile_picture = profile_picture
            profile.save()
    return render(request, 'profile.html')

@login_required
def home(request):
    return render(request, 'home.html')

```
# forms.py
```
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile 

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile 
        fields = ('profile_picture',) 

```
# Templates Profile.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profile</title>
</head>
<body>
    <h2>Profile</h2>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <input type="file" name="profile_picture">
        <button type="submit">Upload Profile Picture</button>
    </form>
</body>
</html>

```
# Templates home.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Perfil</title>
</head>
<body>
    <h2>Perfil de Usuario</h2>
    <div>
        {% if user.is_authenticated %}
            <p>¡Hola, {{ user.username }}!</p>
            {% if user.userprofile.profile_picture %}
                <img src="{{ user.userprofile.profile_picture.url }}" alt="Imagen de perfil" width="50px">
            {% else %}
                <p>No has subido una imagen de perfil todavía.</p>
            {% endif %}
            <a href="{% url 'logout' %}">Cerrar sesión</a>
        {% else %}
            <p>Inicia sesión para ver tu perfil.</p>
            <a href="{% url 'login' %}">Iniciar sesión</a>
        {% endif %}
    </div>
</body>
</html>

```
# Templates/registration login.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <form method="post">
        {% csrf_token %}
        <label for="username">Username:</label>
        <input type="text" id="username" name="username">
        <label for="password">Password:</label>
        <input type="password" id="password" name="password">
        <button type="submit">Login</button>
    </form>
</body>
</html>

```
# Templates/registration signup.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Signup</title>
</head>
<body>
    <h2>Signup</h2>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Sign Up</button>
    </form>
</body>
</html>

```
# urls.py
```
from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('home/', views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```