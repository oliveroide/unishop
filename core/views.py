from django.shortcuts import render

def home(request):
    return render(request, 'products/list.html') 
def product_list(request):
    return render(request, 'products/detail.html')