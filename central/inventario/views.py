from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.dateparse import parse_date

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

def nuevo_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'inventario/nuevo_producto.html', {'form': form})
