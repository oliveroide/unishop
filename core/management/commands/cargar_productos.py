from django.core.management.base import BaseCommand
from core.models import Product

import os
from django.conf import settings

class Command(BaseCommand):
    help = 'Carga los productos iniciales de UNISON'
    def handle(self, *args, **options):
        productos = [
            {
                'nombre': 'Termo Celcius UNISON',
                'descripcion': 'Termo con logo de la UNISON',
                'precio': 400.00,
                'imagen': 'imagenes/imagen1.jpeg',
                'detalles': ''
            },
            {
                'nombre': 'Porta gafete listón',
                'descripcion': 'Porta gafete con listón universitario',
                'precio': 55.00,
                'imagen': 'imagenes/imagen2.jpeg',
                'detalles': ''
            },
            {
                'nombre': 'Cuaderno media carta',
                'descripcion': 'Cuaderno profesional',
                'precio': 80.00,
                'imagen': 'imagenes/imagen3.jpeg',
                'detalles': 'Cuaderno tamaño media carta profesional, 100 hojas a raya con resorte metálico'
            },
            {
                'nombre': 'Chamarra universitaria',
                'descripcion': 'Chamarra con logo UNISON',
                'precio': 1250.00,
                'imagen': 'imagenes/imagen4.jpeg',
                'detalles': 'Variedad de colores y tallas'
            },
            {
                'nombre': 'Paraguas cuadrado',
                'descripcion': 'Paraguas universitario',
                'precio': 450.00,
                'imagen': 'imagenes/imagen5.jpeg',
                'detalles': 'Medidas: 98 x 98 cm\nColores disponibles: Azul y negro'
            },
            {
                'nombre': 'Lonchera Preston',
                'descripcion': 'Lonchera estilo premium',
                'precio': 235.00,
                'imagen': 'imagenes/imagen6.jpeg',
                'detalles': 'Medidas: 28x20x15 cm\nColores: azul, verde, negro, rojo'
            }
        ]
        
        # Crear directorio de imágenes si no existe
        os.makedirs(os.path.join(settings.MEDIA_ROOT, 'imagenes'), exist_ok=True)
        
        for p in productos:
            # Verificar si la imagen existe físicamente
            img_path = os.path.join(settings.MEDIA_ROOT, p['imagen'])
            if not os.path.exists(img_path):
                self.stdout.write(self.style.WARNING(f"¡Advertencia! Imagen no encontrada: {img_path}"))
                continue
                
            obj, created = Product.objects.get_or_create(
                nombre=p['nombre'],
                defaults={
                    'descripcion': p['descripcion'],
                    'precio': p['precio'],
                    'imagen': p['imagen'],
                    'detalles': p['detalles']
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Producto creado: {p['nombre']}"))
            else:
                self.stdout.write(self.style.NOTICE(f"Producto ya existente: {p['nombre']}"))
        
        self.stdout.write(self.style.SUCCESS('\nProceso completado'))
        self.stdout.write(self.style.NOTICE('\nVerifica que las imágenes estén en:'))
        self.stdout.write(f"{os.path.join(settings.MEDIA_ROOT, 'imagenes')}")