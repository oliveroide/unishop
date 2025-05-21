from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# --------------------------
# Login y Logout
# --------------------------

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}')
            return redirect('home')  # redirige a la vista con name='home'
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente')
    return redirect('login')  # redirige al login tras cerrar sesión

# --------------------------
# Vistas públicas y privadas
# --------------------------

def product_list(request):
    return render(request, 'products/list.html')

@login_required
def product_detail(request, product_id):
    return render(request, 'products/detail.html', {'product_id': product_id})

# --------------------------
# Registro de usuarios
# --------------------------

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Cuenta creada: {user.username}')
            return redirect('home')
        else:
            messages.error(request, 'Corrige los errores en el formulario')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})
