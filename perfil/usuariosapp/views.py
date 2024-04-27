from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm, CustomUserChangeForm


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            # Autenticar al usuario después de registrarse
            authenticated_user = authenticate(request, username=user.username, password=form.cleaned_data['password1'])
            if authenticated_user is not None:
                login(request, authenticated_user)
            return redirect('home') 
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  
#             return redirect('home') 
#     else:
#         form = SignUpForm()
#     return render(request, 'registration/signup.html', {'form': form})

# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('profile')
#     else:
#         form = LoginForm()
#     return render(request, 'registration/login.html', {'form': form})
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirige al usuario al perfil
                return redirect('profile')
            else:
                # Si la autenticación falla, muestra un mensaje de error
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')  


@login_required
def profile(request):
    user = request.user
    return render(request, 'index.html', {'user': user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})
