from django.db import models

class Producto(models.Model):
    CATEGORIAS = [
        ('MON', 'Monitores'),
        ('PER', 'Periféricos'),
        ('HW', 'Hardware'),
    ]

    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    nombre = models.CharField(max_length=100)
    codigo_serial = models.CharField(max_length=100, unique=True)
    modelo = models.CharField(max_length=100)
    fecha_ingreso = models.DateField()
    fecha_cambio = models.DateField(null=True, blank=True)
    fecha_entrega = models.DateField(null=True, blank=True)
    remitente = models.CharField(max_length=100)
    destinatario = models.CharField(max_length=100)
    hora_salida = models.TimeField(verbose_name='Hora de salida')
    hora_llegada = models.TimeField(verbose_name='Hora de llegada')
    estado_condicion = models.CharField(max_length=200)
    descripcion = models.TextField()
    imagen_anterior = models.ImageField(upload_to='productos/', null=True, blank=True)
    imagen_actual = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo_serial})"