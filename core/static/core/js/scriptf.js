$(document).ready(function () {
    $('#ver_productost').click(function(event){
        event.preventDefault();
        $.get('https://fakestoreapi.com/products',
        function (data) {
            $('#producto').empty();
            $.each(data, function (i, item) {
                var fila = ` 
                <div class="col-sm-12 col-md-6 col-lg-4 col-xl-3">
                    <div class="card mb-4 box-shadow">
                        <div class="text-center">
                            <img src="${item.image}" class="card-img-top producto-tamaño" alt="">
                        </div>
                        <div class="card-body">
                            <p class="card-text">
                            <div class="lead text-secondary fw-bold">
                                DISPONIBLE
                            </div>
                            <div class="lead text-danger">
                                <span class="precio-oferta fw-bold">
                                    ${item.price}
                                </span>
                            </div>
                            <br>
                            ${item.title}
                            <br>
                            <b>Descipción</b>
                            <div class="text-truncate">
                                ${item.description}
                            </div>
                        </div>
                    </div>
                </div>
                `;
                $('#producto').append(fila);
            });
        });
    })
});
