from django.urls import path
from .views import inicio,registro,bodega,boleta,carrito,ficha,ingresar,miscompras,misDatos,nosotros,_productos,ropa,usuarios,ventas,poblar,cambiar_estado_boleta
from .views import eliminar_producto_en_bodega, eliminar_producto_en_bodega,  eliminar_producto_en_carrito, agregar_producto_al_carrito

urlpatterns = [
    path('', inicio, name="inicio"),
    path('registro',registro,name="registro"),
    path('bodega',bodega ,name="bodega"),
    path('boleta/<nro_boleta>', boleta,name="boleta"),
    path('carrito', carrito,name="carrito"),
    path('ficha/<producto_id>',ficha ,name="ficha"),
    path('ingresar',ingresar ,name="ingresar"),
    path('miscompras',miscompras ,name="miscompras"),
    path('misDatos',misDatos ,name="misDatos"),
    path('nosotros',nosotros ,name="nosotros"),
    path('_productos/<accion>/<id>',_productos ,name="_productos"),
    path('ropa',ropa ,name="ropa"),
    path('usuarios', usuarios,name="usuarios"),
    path('ventas',ventas ,name="ventas"),
    path('poblar',poblar,name="poblar"),
    path('cambiar_estado_boleta/<nro_boleta>/<estado>', cambiar_estado_boleta, name='cambiar_estado_boleta'),
    path('eliminar_producto_en_bodega/<bodega_id>', eliminar_producto_en_bodega, name='eliminar_producto_en_bodega'),
        path('eliminar_producto_en_carrito/<carrito_id>', eliminar_producto_en_carrito, name='eliminar_producto_en_carrito'),
    path('agregar_producto_al_carrito/<producto_id>', agregar_producto_al_carrito, name='agregar_producto_al_carrito'),
]
