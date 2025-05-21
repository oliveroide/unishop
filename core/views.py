from django.shortcuts import render
from .models import Product
def home(request):
    return render(request, 'products/list.html') 
def product_list(request):
    productos = Product.objects.all()
    return render(request, 'products/detail.html', {'productos': productos} )
def galeria(request):
    productos = Product.objects.all()
    return render(request, 'galeria.html', {'productos': productos})
