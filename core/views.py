 from django.shortcuts import render, redirect
  from .cart import Cart

    def home(request):
        return render(request, 'products/list.html')

    def product_list(request):
        return render(request, 'products/detail.html')

    def add_to_cart(request, product_id):
        cart = Cart(request)
        cart.add(product_id)
        return redirect('product_list')

    def remove_from_cart(request, product_id):
        cart = Cart(request)
        cart.remove(product_id)
        return redirect('cart_detail')

    def cart_detail(request):
        cart = Cart(request)
        return render(request, 'cart/detail.html', {'cart': cart})
