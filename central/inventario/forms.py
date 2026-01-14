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

# Formulario para registrar llegada (sin fecha_entrega)
class LlegadaForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'categoria', 'nombre', 'codigo_serial', 'modelo',
            'fecha_ingreso', 'remitente', 'destinatario',
            'hora_salida', 'hora_llegada',
            'estado_condicion', 'descripcion',
            'imagen_anterior', 'imagen_actual',
        ]
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_serial': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'remitente': forms.TextInput(attrs={'class': 'form-control'}),
            'destinatario': forms.TextInput(attrs={'class': 'form-control'}),
            'hora_salida': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_llegada': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'estado_condicion': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagen_anterior': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imagen_actual': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# Formulario para registrar salida y actualizar datos de llegada
class SalidaForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            # Datos que se pueden actualizar de la llegada
            'categoria', 'nombre', 'modelo', 'fecha_ingreso', 'remitente', 'hora_llegada',
            # Datos propios de la salida
            'destinatario', 'hora_salida', 'fecha_entrega',
            # Estado/descrición e imagen
            'estado_condicion', 'descripcion', 'imagen_actual',
        ]
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'remitente': forms.TextInput(attrs={'class': 'form-control'}),
            'hora_llegada': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'destinatario': forms.TextInput(attrs={'class': 'form-control'}),
            'hora_salida': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'fecha_entrega': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estado_condicion': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagen_actual': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class IngresoSimpleForm(forms.Form):
    fecha_ingreso = forms.DateField(
        label='Fecha de ingreso',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

class InventarioIngresoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'categoria', 'nombre', 'codigo_serial', 'modelo',
            'fecha_ingreso',
            'remitente',
            'estado_condicion', 'descripcion',
            'imagen_anterior', 'imagen_actual',
        ]
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_serial': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'remitente': forms.TextInput(attrs={'class': 'form-control'}),
            'estado_condicion': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'imagen_anterior': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'imagen_actual': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_codigo_serial(self):
        codigo = self.cleaned_data.get('codigo_serial', '').strip()
        if not codigo:
            raise forms.ValidationError('El código serial es requerido.')
        from .models import Producto
        if Producto.objects.filter(codigo_serial=codigo).exists():
            raise forms.ValidationError('Ya existe un producto con este código serial.')
        return codigo
