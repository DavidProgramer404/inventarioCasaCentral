from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('nuevo/', views.nuevo_producto, name='nuevo_producto'),
    path('llegadas/', views.lista_llegadas, name='lista_llegadas'),
    path('llegadas/nueva/', views.nueva_llegada, name='nueva_llegada'),
    path('salidas/', views.lista_salidas, name='lista_salidas'),
    path('salidas/registrar/<int:pk>/', views.registrar_salida, name='registrar_salida'),
    path('salidas/<int:pk>/', views.detalle_salida, name='detalle_salida'),
    path('salidas/<int:pk>/editar/', views.editar_salida, name='editar_salida'),
    path('salidas/<int:pk>/eliminar/', views.eliminar_salida, name='eliminar_salida'),
    path('inventario/', views.inventario_stock, name='inventario_stock'),
]
