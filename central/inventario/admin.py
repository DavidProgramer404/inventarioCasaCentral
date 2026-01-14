from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'codigo_serial', 'fecha_ingreso', 'estado_condicion')
    search_fields = ('nombre', 'codigo_serial')
    list_filter = ('categoria',)

# Panel admin en espanol
admin.site.site_header = 'Panel de Administración de Inventario'
