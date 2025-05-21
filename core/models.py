from django.db import models
from django.contrib.auth.models import User

# -------------------------------
# Modelo de Producto
# -------------------------------
class Product(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='imagenes/', blank=True, null=True)
    detalles = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

# -------------------------------
# Modelo de Orden
# -------------------------------
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.id} de {self.user.username}"

# -------------------------------
# Modelo de ítems por Orden
# -------------------------------
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.nombre}"
