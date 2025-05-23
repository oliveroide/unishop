from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views
from core.views import confirmacion_compra  # Ya está bien importada

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login y Logout
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Productos
    path('', views.product_list, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('register/', views.register_view, name='register'),

    # Carrito
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    path('cart/update/<int:product_id>/', views.update_quantity, name='update_quantity'),

    # Checkout y confirmación
    path('checkout/', views.checkout_view, name='checkout'),
    path('confirmacion/', confirmacion_compra, name='confirmacion'),

    # Cuenta
    path('micuenta/', views.mi_cuenta_view, name='micuenta'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
