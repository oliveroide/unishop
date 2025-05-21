from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.utils import timezone
from .models import Product, Order, OrderItem
from .cart import Cart

# --------------------------
# Carrito
# --------------------------

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(product)
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
# Autenticación
# --------------------------

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}')
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente')
    return redirect('login')

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

# --------------------------
# Productos
# --------------------------

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
# Órdenes y Confirmación
# --------------------------

@login_required
def checkout_view(request):
    cart = Cart(request)

    if request.method == 'POST':
        address = request.POST.get('address')

        if not address:
            messages.error(request, "Debes ingresar una dirección de entrega.")
            return redirect('checkout')

        order = Order.objects.create(user=request.user, address=address)

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product_id=item['id'],
                quantity=item['quantity'],
                price=item['precio']
            )

        cart.clear()
        request.session['order_id'] = order.id
        messages.success(request, f"Compra realizada exitosamente. Pedido #{order.id}")
        return redirect('confirmacion')

    return render(request, 'checkout.html', {'cart': cart})

@login_required
def confirmacion_compra(request):
    order_id = request.session.get('order_id')
    if not order_id:
        messages.error(request, "No hay una compra reciente.")
        return redirect('home')

    orden = get_object_or_404(Order, id=order_id, user=request.user)

    # Calculamos el total sumando los subtotales de cada producto
    total = sum(item.quantity * item.price for item in orden.items.all())

    return render(request, 'confirmacion.html', {
        'orden': orden,
        'cliente': request.user.username,
        'fecha': orden.date_created,
        'total_pagado': total,
    })


# --------------------------
# Mi cuenta (historial)
# --------------------------

@login_required
def mi_cuenta_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_created')
    return render(request, 'micuenta.html', {'orders': orders})
