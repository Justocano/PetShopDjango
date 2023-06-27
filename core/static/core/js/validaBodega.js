$(document).ready(function(){
    $('#formulario6').validate({
        rules:{
            "cantidad":{
                required:true,
                number: true,
            },
            "categoria":{
                required:true,
            },
        },
        messages:{
            "cantidad":{
                required:"El campo es obligaorio",
                number: "Debe ser numero",
            },
            "categoria":{
                required:"El campo es obligaorio",
            },
        },
        errorPlacement: function(error, element) {
            error.insertAfter(element); // Inserta el mensaje de error después del elemento
            error.addClass('error-message'); // Aplica una clase al mensaje de error
        },
    })
})