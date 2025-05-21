from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from core.models import Product
from core.cart import Cart

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product)
    print(f'Agregado: {product.nombre}')
    print(cart.cart)
    return redirect('cart_detail')


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart_detail')

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    messages.info(request, "Carrito vaciado.")
    return redirect('cart_detail')

from django.views.decorators.http import require_POST

@require_POST
def update_quantity(request, product_id):
    cart = Cart(request)
    try:
        quantity = int(request.POST.get('quantity'))
    except (ValueError, TypeError):
        quantity = 1
    cart.update(product_id, quantity)
    return redirect('cart_detail')




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
from .models import Product
from django.db.models import Q

def product_list(request):
    query = request.GET.get('q')
    if query:
        productos = Product.objects.filter(
            Q(nombre__icontains=query) |
            Q(descripcion__icontains=query)
        )
    else:
        productos = Product.objects.all()
    
    return render(request, 'products/list.html', {'productos': productos, 'query': query})

@login_required
def product_detail(request, product_id):
    return render(request, 'products/detail.html', {'product_id': product_id})

# --------------------------
# Registro de usuarios
# --------------------------

from .models import Order
from django.contrib.auth.decorators import login_required

@login_required
def mi_cuenta_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'micuenta.html', {'orders': orders})


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



from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Order, OrderItem
from .cart import Cart

@login_required
def checkout_view(request):
    cart = Cart(request)

    if request.method == 'POST':
        address = request.POST.get('address')

        if not address:
            messages.error(request, "Debes ingresar una dirección de entrega.")
            return redirect('checkout')

        # Crear la orden
        order = Order.objects.create(user=request.user, address=address)

        # Crear los items
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product_id=item['id'],
                quantity=item['quantity'],
                price=item['precio']
            )

        cart.clear()
        messages.success(request, f"Compra realizada exitosamente. Pedido #{order.id}")
        return redirect('home')

    return render(request, 'checkout.html', {'cart': cart})
