from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'codigo_serial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código serial'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_cambio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_entrega': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'remitente': forms.TextInput(attrs={'class': 'form-control'}),
            'destinatario': forms.TextInput(attrs={'class': 'form-control'}),
            'hora_salida': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_llegada': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'estado_condicion': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagen_anterior': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imagen_actual': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
