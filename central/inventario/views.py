from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm, LlegadaForm, SalidaForm, InventarioIngresoForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.utils import timezone
from uuid import uuid4
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

# Importar formularios específicos para llegada y salida
from .forms import LlegadaForm, SalidaForm, IngresoSimpleForm

def lista_productos(request):
    q = request.GET.get('q', '').strip()
    categoria = request.GET.get('categoria', '').strip()
    fecha_desde = request.GET.get('fecha_desde', '').strip()
    fecha_hasta = request.GET.get('fecha_hasta', '').strip()
    estado = request.GET.get('estado', '').strip()
    queryset = Producto.objects.all()
    if q:
        queryset = queryset.filter(
            Q(nombre__icontains=q) |
            Q(codigo_serial__icontains=q) |
            Q(modelo__icontains=q) |
            Q(remitente__icontains=q) |
            Q(destinatario__icontains=q) |
            Q(estado_condicion__icontains=q)
        )
    if categoria:
        queryset = queryset.filter(categoria=categoria)
    if fecha_desde:
        d = parse_date(fecha_desde)
        if d:
            queryset = queryset.filter(fecha_ingreso__gte=d)
    if fecha_hasta:
        h = parse_date(fecha_hasta)
        if h:
            queryset = queryset.filter(fecha_ingreso__lte=h)
    if estado:
        queryset = queryset.filter(estado_condicion__icontains=estado)
    total = queryset.count()
    paginator = Paginator(queryset.order_by('id'), 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    params = request.GET.copy()
    params.pop('page', None)
    querystring = params.urlencode()
    return render(request, 'inventario/lista_productos.html', {
        'page_obj': page_obj,
        'q': q,
        'categoria': categoria,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'estado': estado,
        'total': total,
        'querystring': querystring,
    })

@login_required
@permission_required('inventario.add_producto', raise_exception=True)
def nuevo_producto(request):
    if request.method == 'POST':
        form = InventarioIngresoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.fecha_entrega = None
            producto.destinatario = ''
            producto.save()
            messages.success(request, 'Producto registrado en inventario correctamente.')
            return redirect('inventario:lista_productos')
        else:
            messages.error(request, 'Por favor, corrige los errores del formulario.')
    else:
        form = InventarioIngresoForm()
    return render(request, 'inventario/nuevo_producto.html', {'form': form})


def lista_llegadas(request):
    q = request.GET.get('q', '').strip()
    categoria = request.GET.get('categoria', '').strip()
    fecha_desde = request.GET.get('fecha_desde', '').strip()
    fecha_hasta = request.GET.get('fecha_hasta', '').strip()
    estado = request.GET.get('estado', '').strip()
    queryset = Producto.objects.filter(fecha_entrega__isnull=True)
    if q:
        queryset = queryset.filter(
            Q(nombre__icontains=q) |
            Q(codigo_serial__icontains=q) |
            Q(modelo__icontains=q) |
            Q(remitente__icontains=q) |
            Q(destinatario__icontains=q) |
            Q(estado_condicion__icontains=q)
        )
    if categoria:
        queryset = queryset.filter(categoria=categoria)
    if fecha_desde:
        d = parse_date(fecha_desde)
        if d:
            queryset = queryset.filter(fecha_ingreso__gte=d)
    if fecha_hasta:
        h = parse_date(fecha_hasta)
        if h:
            queryset = queryset.filter(fecha_ingreso__lte=h)
    if estado:
        queryset = queryset.filter(estado_condicion__icontains=estado)
    total = queryset.count()
    paginator = Paginator(queryset.order_by('-fecha_ingreso', 'id'), 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    params = request.GET.copy(); params.pop('page', None)
    querystring = params.urlencode()
    return render(request, 'inventario/lista_productos.html', {
        'page_obj': page_obj,
        'q': q,
        'categoria': categoria,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'estado': estado,
        'total': total,
        'querystring': querystring,
        'page_title': '📥 Productos de llegada',
        'section': 'llegadas',
    })


def lista_salidas(request):
    q = request.GET.get('q', '').strip()
    categoria = request.GET.get('categoria', '').strip()
    fecha_desde = request.GET.get('fecha_desde', '').strip()
    fecha_hasta = request.GET.get('fecha_hasta', '').strip()
    estado = request.GET.get('estado', '').strip()
    queryset = Producto.objects.filter(fecha_entrega__isnull=False)
    if q:
        queryset = queryset.filter(
            Q(nombre__icontains=q) |
            Q(codigo_serial__icontains=q) |
            Q(modelo__icontains=q) |
            Q(remitente__icontains=q) |
            Q(destinatario__icontains=q) |
            Q(estado_condicion__icontains=q)
        )
    if categoria:
        queryset = queryset.filter(categoria=categoria)
    if fecha_desde:
        d = parse_date(fecha_desde)
        if d:
            queryset = queryset.filter(fecha_entrega__gte=d)
    if fecha_hasta:
        h = parse_date(fecha_hasta)
        if h:
            queryset = queryset.filter(fecha_entrega__lte=h)
    if estado:
        queryset = queryset.filter(estado_condicion__icontains=estado)
    total = queryset.count()
    paginator = Paginator(queryset.order_by('-fecha_entrega', 'id'), 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    params = request.GET.copy(); params.pop('page', None)
    querystring = params.urlencode()
    return render(request, 'inventario/lista_productos.html', {
        'page_obj': page_obj,
        'q': q,
        'categoria': categoria,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'estado': estado,
        'total': total,
        'querystring': querystring,
        'page_title': '📤 Productos de salida',
        'section': 'salidas',
    })


def inventario_stock(request):
    q = request.GET.get('q', '').strip()
    categoria = request.GET.get('categoria', '').strip()
    fecha_desde = request.GET.get('fecha_desde', '').strip()
    fecha_hasta = request.GET.get('fecha_hasta', '').strip()
    estado = request.GET.get('estado', '').strip()
    queryset = Producto.objects.filter(fecha_entrega__isnull=True)
    if q:
        queryset = queryset.filter(
            Q(nombre__icontains=q) |
            Q(codigo_serial__icontains=q) |
            Q(modelo__icontains=q) |
            Q(remitente__icontains=q) |
            Q(destinatario__icontains=q) |
            Q(estado_condicion__icontains=q)
        )
    if categoria:
        queryset = queryset.filter(categoria=categoria)
    if fecha_desde:
        d = parse_date(fecha_desde)
        if d:
            queryset = queryset.filter(fecha_ingreso__gte=d)
    if fecha_hasta:
        h = parse_date(fecha_hasta)
        if h:
            queryset = queryset.filter(fecha_ingreso__lte=h)
    if estado:
        queryset = queryset.filter(estado_condicion__icontains=estado)
    total = queryset.count()
    paginator = Paginator(queryset.order_by('id'), 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    params = request.GET.copy(); params.pop('page', None)
    querystring = params.urlencode()
    return render(request, 'inventario/lista_productos.html', {
        'page_obj': page_obj,
        'q': q,
        'categoria': categoria,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'estado': estado,
        'total': total,
        'querystring': querystring,
        'page_title': '📦 Inventario (en stock)',
        'section': 'inventario',
    })


# Registrar nueva llegada (solo sección de sede)
def nueva_llegada(request):
    if request.method == 'POST':
        form = LlegadaForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            # Asegurar que no se fije fecha_entrega en llegada
            producto.fecha_entrega = None
            producto.save()
            return redirect('lista_llegadas')
    else:
        form = LlegadaForm()
    return render(request, 'inventario/nueva_llegada.html', {'form': form})

# Registrar salida a partir de una llegada (solo sección de sede)
def registrar_salida(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return redirect('lista_llegadas')

    if request.method == 'POST':
        form = SalidaForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_salidas')
    else:
        form = SalidaForm(instance=producto)

    return render(request, 'inventario/registrar_salida.html', {
        'form': form,
        'producto': producto,
    })

# Ver detalle de salida (entrega) de un producto
def detalle_salida(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return redirect('lista_salidas')
    # Solo mostrar detalles si tiene fecha_entrega (es una salida)
    if not producto.fecha_entrega:
        return redirect('lista_llegadas')
    return render(request, 'inventario/salida_detalle.html', {
        'producto': producto,
    })

# Editar salida de un producto (actualiza datos de llegada y de salida)
def editar_salida(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return redirect('lista_salidas')

    if request.method == 'POST':
        form = SalidaForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_salidas')
    else:
        form = SalidaForm(instance=producto)

    return render(request, 'inventario/registrar_salida.html', {
        'form': form,
        'producto': producto,
    })

# Eliminar salida (revertir entrega) de un producto
def eliminar_salida(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return redirect('lista_salidas')

    if request.method == 'POST':
        # Revertir la entrega: dejar fecha_entrega sin valor
        producto.fecha_entrega = None
        producto.save()
        return redirect('lista_llegadas')

    return render(request, 'inventario/eliminar_salida.html', {
        'producto': producto,
    })
