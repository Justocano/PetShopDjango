import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()
 
        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd():
    eliminar_tablas()

    crear_usuario(
        username='cevans',
        tipo='Cliente', 
        nombre='Chris', 
        apellido='Evans', 
        correo='cevans@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='15499707-3', 
        direccion='123 Main Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/cevans.jpg')

    crear_usuario(
        username='eolsen',
        tipo='Cliente', 
        nombre='Elizabeth', 
        apellido='Olsen', 
        correo='eolsen@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='19090011-2', 
        direccion='Albert Street, New York, \nNew York 10001 \nEstados Unidos', 
        subscrito=True, 
        imagen='perfiles/eolsen.jpg')

    crear_usuario(
        username='tholland',
        tipo='Cliente', 
        nombre='Tom', 
        apellido='Holland', 
        correo='tholland@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='23548549-0', 
        direccion='105 Apple Park Way, \nCupertino, CA 95014 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/tholland.jpg')

    crear_usuario(
        username='sjohansson',
        tipo='Cliente', 
        nombre='Scarlett', 
        apellido='Johansson', 
        correo='sjohansson@marvel.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='12788999-4', 
        direccion='350 5th Ave, \nNew York, NY 10118 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/sjohansson.jpg')

    crear_usuario(
        username='cpratt',
        tipo='Administrador', 
        nombre='Chris', 
        apellido='Pratt', 
        correo='cpratt@marvel.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='16543210-8', 
        direccion='10 Pine Road, Miami, \nFlorida 33101 \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/cpratt.jpg')
    
    crear_usuario(
        username='mruffalo',
        tipo='Administrador', 
        nombre='Mark', 
        apellido='Ruffalo', 
        correo='mruffalo@marvel.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='21123344-7', 
        direccion='1600 Pennsylvania Avenue NW, \nWashington, D.C. \nEstados Unidos', 
        subscrito=False, 
        imagen='perfiles/mruffalo.jpg')

    crear_usuario(
        username='super',
        tipo='Superusuario',
        nombre='Robert',
        apellido='Downey Jr.',
        correo='rdowneyjr@marvel.com',
        es_superusuario=True,
        es_staff=True,
        rut='18472636-6',
        direccion='15 Oak Street, Los Angeles, \nCalifornia 90001 \nEstados Unidos',
        subscrito=False,
        imagen='perfiles/rdowneyjr.jpg')
    
    categorias_data = [
        { 'id': 1, 'nombre': 'Perros'},
        { 'id': 2, 'nombre': 'Gatos'},
        { 'id': 3, 'nombre': 'Pájaros'},
        { 'id': 4, 'nombre': 'Hamsters'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        # Categoría "Perros"
        {
            'id': 1,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Inaba churu atún con salmon',
            'descripcion': '''Línea: Churu
                                Tipo de golosina para perros y gatos: Snack
                                Peso neto: 56 g
                                Sabor: Salmón
                                Unidades por envase: 4
                                Formato de venta: Unidad
                                Unidades por pack: 1
                                Mascotas recomendadas: Gatos
                                Textura: Húmedo''',
            'precio': 2205,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/Imagen1.png'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Taste of the wild pacific stream',
            'descripcion': '''Especificaciones
                                Sabor: Salmón
                                Peso de la unidad: 5.6 kg
                                Tipo de envase: Bolsa
                                Tipo de comida para mascotas: Seca''',
            'precio': 36990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/Imagen2.png'
        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Belcando | alimento húmedo latas',
            'descripcion': '''Peso de la unidad: 100 g
                                Tipo de envase: Sobre
                                Tipo de comida para mascotas: Húmeda''',
            'precio': 4200,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/Imagen3.png'
        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Belcando mastercraft topping',
            'descripcion': '''Sabor: Pavo
                                Peso de la unidad: 100 g
                                Tipo de envase: Sobre
                                Tipo de comida para mascotas: Humeda''',
            'precio': 3490,
            'descuento_subscriptor': 5,
            'descuento_oferta': 15,
            'imagen': 'productos/Imagen4.png'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Belcando pouch | sobres',
            'descripcion': '''Especificaciones
                                Peso de la unidad: 125 g
                                Tipo de envase: Sobre
                                Tipo de comida para mascotas: Húmeda''',
            'precio': 39900,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/Imagen5.png'
        },
        # Categoría "Gatos"
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=1),
            'nombre': ' Fit formula adulto',
            'descripcion': '''Sabor: Mix
                                Peso de la unidad: 20 kg
                                Tipo de envase: Bolsa
                                Tipo de comida para mascotas: Seca''',
            'precio': 2205,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/Imagen6.png'
        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Nomade adulto 3Kg',
            'descripcion': '''Sabor: Mix
                                Peso de la unidad: 3 kg
                                Tipo de envase: Bolsa
                                Tipo de comida para mascotas: Seca''',
            'precio': 10990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/Imagen8.png'
        },
        {
            'id': 8,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Acana pupy recipe',
            'descripcion': '''Sabor: Mix
                                Peso de la unidad: 11.4 kg
                                Tipo de envase: Bolsa
                                Tipo de comida para mascotas: Seca''',
            'precio': 65800,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/Imagen7.png'
        },
        {
            'id': 9,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Fit formula cahorro',
            'descripcion': '''Sabor: Mix
                                Peso de la unidad: 10 kg
                                Tipo de envase: Bolsa
                                Tipo de comida para mascotas: Seca''',
            'precio': 24990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/Imagen9.png'
        },
        {
            'id': 10,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Fit formula adulto',
            'descripcion': '''Sabor: Pato
                                Peso de la unidad: 11.34 kg
                                Tipo de envase: Bolsa
                                Tipo de comida para mascotas: Seca''',
            'precio': 75100,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/Imagen10.png'
        },
        # Categoría "Pájaros"
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=2),
            'nombre': ' Inaba churu atún con ostiones',
            'descripcion': '''Línea: Snack
                                Tipo de golosina para perros y gatos: Snack
                                Peso neto: 14 g
                                Unidades por envase: 4
                                Formato de venta: Unidad
                                Textura: Húmedo''',
            'precio': 2205,
            'descuento_subscriptor': 5,
            'descuento_oferta': 10,
            'imagen': 'productos/Imagen11.png'
        },
        {
            'id': 12,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Inaba churu pollo ',
            'descripcion': '''Línea: Churu Bites
                                Tipo de golosina para perros y gatos: Snack
                                Peso neto: 30 g
                                Sabor: Pollo y salmón
                                Unidades por envase: 3
                                Formato de venta: Unidad
                                Unidades por pack: 1
                                Mascotas recomendadas: Gatos
                                Textura: Húmedo''',
            'precio': 2500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/Imagen12.png'
        },
        # Categoría "Hamsters"
    ]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Crear carritos')
    for rut in ['15499707-3', '23548549-0']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, 11):
            producto = Producto.objects.get(pk=randint(1, 10))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 11):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 31)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')

