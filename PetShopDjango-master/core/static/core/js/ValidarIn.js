$(document).ready(function() {
  $('#formulario2').validate({ 
      rules: {
        'username': {
          required: true,
        },
        'password': {
          required: true,
        },
      },
      messages: {
        'username': {
          required: 'Debe ingresar un nombre de usuario',
        },
        'password': {
          required: 'Debe ingresar una contraseña',
        },
      },
      errorPlacement: function(error, element) {
        error.insertAfter(element); // Inserta el mensaje de error después del elemento
        error.addClass('error-message'); // Aplica una clase al mensaje de error
      },
  });
});
