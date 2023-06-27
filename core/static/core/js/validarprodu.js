$(document).ready(function () {
    $('#formulario3').validate({
        rules: {
            'categoria': {
                required: true,
            },
            'nombre': {
                required: true,
            },
            'descripcion': {
                required: true,
            },
            'precio': {
                required: true,
                digits: true,
                number: true,
            },
            'descuento_subscriptor': {
                required: true,
                digits: true,
                number: true,
                range: [0, 100],
            },
            'descuento_oferta': {
                required: true,
                digits: true,
                number: true,
                range: [0, 100],
            },
        },
        messages: {
            'categoria': {
                required: 'Debe ingresar la categoría del producto',
            },
            'nombre': {
                required: 'Debe ingresar el nombre del producto',
            },
            'descripcion': {
                required: 'Debe ingresar la descripción del producto',
            },
            'precio': {
                required: 'Debe ingresar el precio del producto',
                number: 'Debe ingresar un número',
                digits: 'Debe ingresar un número entero',
            },
            'descuento_subscriptor': {
                required: 'Debe ingresar el % de descuento para subscriptores',
                number: 'Debe ingresar un número',
                digits: 'Debe ingresar un número entero',
                
                range: 'El descuento debe ser un número entre 0 y 100',
            },
            'descuento_oferta': {
                required: 'Debe ingresar el % de descuento para ofertas',
                number: 'Debe ingresar un número',
                digits: 'Debe ingresar un número entero',
                range: 'El descuento debe ser un número entre 0 y 100',
            },
        },
        errorPlacement: function(error, element) {
            error.insertAfter(element); // Inserta el mensaje de error después del elemento
            error.addClass('error-message'); // Aplica una clase al mensaje de error
            element.after('<br>'); 
        },
    })
});