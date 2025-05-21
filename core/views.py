from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .cart import Cart

def galeria_productos(request):
    productos = Product.objects.all()
    return render(request, 'galeria.html', {'productos': productos})
def product_list(request):
    productos = Product.objects.all()
    return render(request, 'products/list.html', {'productos': productos})

def product_detail(request, product_id):
    producto = get_object_or_404(Product, id=product_id)
    return render(request, 'products/detail.html', {'product': producto})

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

def add_to_cart(request, product_id):
    producto = get_object_or_404(Product, id=product_id)
    cart = Cart(request)
    cart.add(producto)
    return redirect('cart_detail')

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart_detail')
