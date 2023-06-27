$(document).ready(function(){
    // Agregar método de validación para RUT chileno
    $.validator.addMethod("rutChileno", function(value, element) {
       // Eliminar puntos y guión del RUT
       value = value.replace(/[.-]/g, "");
   
       // Validar que el RUT tenga 8 o 9 dígitos
       if (value.length < 8 || value.length > 9) {
         return false;
       }
   
       // Validar que el último dígito sea un número o una 'K'
       var validChars = "0123456789K";
       var lastChar = value.charAt(value.length - 1).toUpperCase();
       if (validChars.indexOf(lastChar) == -1) {
         return false;
       }
   
       // Calcular el dígito verificador
       var rut = parseInt(value.slice(0, -1), 10);
       var factor = 2;
       var sum = 0;
       var digit;
       while (rut > 0) {
         digit = rut % 10;
         sum += digit * factor;
         rut = Math.floor(rut / 10);
         factor = factor === 7 ? 2 : factor + 1;
       }
       var dv = 11 - (sum % 11);
       dv = dv === 11 ? "0" : dv === 10 ? "K" : dv.toString();
   
       // Validar que el dígito verificador sea correcto
       return dv === lastChar;
     }, "Por favor ingrese un RUT válido."); 
    $('#formulario4').validate({
        "rules": {
            "correo": {
                "required": true,
                "email": true,
            },
            "contraseña": {
                "required": true,
                "minlength": 5,
            },
            "nombre": {
                "required": true,
            },
            "rutChileno":{
                "required": true,
                "rutChileno": true,
            },
            "apellido": {
                "required": true,
            },
            "direccion": {
                "required": true,
            },
            "id": {
                "required": true,
                "number":true,
            },
        },
        "messages": {
            "id": {
                "required": "Este campo es obligatorio",
                "number":"Debe ser numero",
            },
            "correo": {
                "required": "Este campo es obligaorio",
                "email": "Debe tener '@' para avanzar",
            },
            "contraseña": {
                "required": "Este campor es obligatorio",
                "minlength": "Debe tener minimo 5 letras ",
            },
            "nombre": {
                "required": "Este campo es obligatorio",
            },
            "rutChileno":{
                "required": "Este campo es obligatorio",
                "rutChileno": "Tiene que ser de formato rut",
            },
            "apellido": {
                "required": "Este campo es obligatorio",
            },
            "direccion": {
                "required": "Este campo es obligatorio",
            },
        }
    })
});