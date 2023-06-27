# Create your views here.
from django.shortcuts import  render, redirect
from datetime import date
from .poblar import poblar_bd
from .models import Producto,Perfil,Bodega,DetalleBoleta, Boleta
from .forms import ProductoForm, BodegaForm, RegistroClienteForm, IngresarForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .tools import eliminar_registro, verificar_eliminar_registro
# from .models import Mascota

# Create your views here.

def inicio(request):
    productos = Producto.objects.all().order_by('id')
    datos = { 
        'productos': productos
    }
    return render(request, "core/inicio.html",datos)

def poblar(request):
    poblar_bd()
    return redirect(inicio)

def registro(request):
    form = RegistroClienteForm()
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            rut = form.cleaned_data['rut']
            direccion = form.cleaned_data['direccion']
            subscrito = form.cleaned_data['subscrito']
            Perfil.objects.create(
                usuario=user, 
                tipo_usuario='Cliente', 
                rut=rut, 
                direccion=direccion, 
                subscrito=subscrito,
                imagen=request.FILES['imagen'])
            return redirect(ingresar)
            
    return render(request, "core/registro.html", {'form': form})

def misDatos(request):
    form = RegistroClienteForm()
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            rut = form.cleaned_data['rut']
            direccion = form.cleaned_data['direccion']
            subscrito = form.cleaned_data['subscrito']
            Perfil.objects.create(
                usuario=user, 
                tipo_usuario='Cliente', 
                rut=rut, 
                direccion=direccion, 
                subscrito=subscrito,
                imagen=request.FILES['imagen'])
            return redirect(ingresar)
            
    return render(request, "core/misDatos.html", {'form': form})


def bodega(request):
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        producto = Producto.objects.get(id=producto_id)
        cantidad = int(request.POST.get('cantidad'))
        for cantidad in range(1, cantidad + 1):
            Bodega.objects.create(producto=producto)
        if cantidad == 1:
            messages.success(request, f'Se ha agregado 1 nuevo "{producto.nombre}" a la bodega')
        else:
            messages.success(request, f'Se han agregado {cantidad} productos de "{producto.nombre}" a la bodega')

    registros = Bodega.objects.all()
    lista = []
    for registro in registros:
        vendido = DetalleBoleta.objects.filter(bodega=registro).exists()
        item = {
            'bodega_id': registro.id,
            'nombre_categoria': registro.producto.categoria.nombre,
            'nombre_producto': registro.producto.nombre,
            'estado': 'Vendido' if vendido else 'En bodega',
            'imagen': registro.producto.imagen,
        }
        lista.append(item)

    return render(request, 'core/bodega.html', {
        'form': BodegaForm(),
        'productos': lista,
    })

def eliminar_producto_en_bodega(request, bodega_id):
    
    nombre_producto = Bodega.objects.get(id=bodega_id).producto.nombre
    eliminado, error = verificar_eliminar_registro(Bodega, bodega_id, True)
    
    if eliminado:
        messages.success(request, f'Se ha eliminado el ID {bodega_id} ({nombre_producto}) de la bodega')
    else:
        messages.error(request, error)

    return redirect(bodega)


def boleta(request):
    return render(request, "core/boleta.html")

def carrito(request):
    return render(request, "core/carrito.html")

def ficha(request):
    return render(request, "core/Ficha.html")

def ingresar(request):

    if request.method == "POST":
        form = IngresarForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(inicio)
            messages.error(request, 'La cuenta o la password no son correctos')
    
    return render(request, "core/ingresar.html", {
        'form':  IngresarForm(),
        'perfiles': Perfil.objects.all(),
    })


def miscompras(request):
    return render(request, "core/miscompras.html")


def nosotros(request):
    return render(request, "core/nosotros.html")

def piePagina(request):
    return render(request, "core/piePagina.html")

def _productos(request, accion, id):
    
    if request.method == 'POST':
        
        if accion == 'crear':
            form = ProductoForm(request.POST, request.FILES)

        elif accion == 'actualizar':
            form = ProductoForm(request.POST, request.FILES, instance=Producto.objects.get(id=id))
        
        if form.is_valid():
            producto = form.save()
            form = ProductoForm(instance=producto)
            messages.success(request, f'El producto "{str(producto)}" se logró {accion} correctamente')
            return redirect(_productos, 'actualizar', producto.id)
        else:
            messages.error(request, f'No se pudo {accion} el Producto, pues el formulario no pasó las validaciones básicas')
            return redirect(_productos, 'actualizar', id)

    if request.method == 'GET':

        if accion == 'crear':
            form = ProductoForm()
        
        elif accion == 'actualizar':
            form = ProductoForm(instance=Producto.objects.get(id=id))

        elif accion == 'eliminar':
            messages.success(request, eliminar_registro(Producto, id))
            return redirect(_productos, 'crear', '0')

    productos = Producto.objects.all()

    datos = {
        'form': form,
        'productos': productos
    }
    return render(request, 'core/productos.html', datos)

def ropa(request):
    return render(request, "core/ropa.html")

def usuarios(request):
    return render(request, "core/usuarios.html")

def ventas(request):
    boletas = Boleta.objects.all()
    historial =[]
    for boleta in boletas:
        boleta_historial = {}
        boleta_historial['nro_boleta'] = boleta.nro_boleta
        boleta_historial['nom_cliente'] = f'{boleta.cliente.usuario.first_name} {boleta.cliente.usuario.last_name}'
        boleta_historial['fecha_venta'] = boleta.fecha_venta
        boleta_historial['fecha_despacho'] = boleta.fecha_despacho
        boleta_historial['fecha_entrega'] = boleta.fecha_entrega
        if boleta.cliente.subscrito:
            boleta_historial['subscrito'] = 'Sí'
        else:
            boleta_historial['subscrito'] = 'No'
        boleta_historial['total_a_pagar'] = boleta.total_a_pagar
        boleta_historial['estado'] = boleta.estado
        historial.append(boleta_historial)
    datos = { 'historial': historial }
    return render(request, 'core/ventas.html', datos)

def cambiar_estado_boleta(request, nro_boleta, estado):
    boleta = Boleta.objects.get(nro_boleta=nro_boleta)
    boleta.estado = estado
    if estado == 'Anulado':
        boleta.fecha_venta = date.today()
        boleta.fecha_despacho = None
        boleta.fecha_entrega = None
    else:
        if estado == 'Vendido':
            boleta.fecha_venta = date.today()
            boleta.fecha_despacho = None
            boleta.fecha_entrega = None
        elif estado == 'Despachado':
            boleta.fecha_despacho = date.today()
            boleta.fecha_entrega = None
        elif estado == 'Entregado':
            if boleta.estado == 'Vendido':
                boleta.fecha_despacho = date.today()
                boleta.fecha_entrega = date.today()
            elif boleta.estado == 'Desapachado':
                boleta.fecha_entrega = date.today()
            elif boleta.estado == 'Entregado':
                boleta.fecha_entrega = date.today()
    boleta.save()
    return redirect(ventas)
