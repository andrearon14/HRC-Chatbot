$( document ).ready(function() {
    recargar();

    $("#tipo").on("change", recargar);
    $(".search").on("input", recargar);
    from.on("change", recargar);
    to.on("change", recargar);
    $("#empresas").on("change", recargar);

    $("#fromImg").click(function() {
        from.datepicker('show');
    });
    $("#toImg").click(function() {
        to.datepicker('show');
    });
});

function normalize(str) {
    return str.normalize('NFD').replace(/[\u0300-\u036f]/g, "").toLowerCase()
}

var seleccionado = null;
function recargar() {
    var datos = $("#datos");

    datos.html(`
        <div class="row headerrow">
            <div class="col-md-2">
                Fecha
            </div>
            <div class="col-md-2">
                Empleado
            </div>
            <div class="col-md-8">
                Comentario
            </div>
        </div>
    `);

    var tipo = $("#tipo").val();
    var search = normalize($(".search").val());
    var fromDate = getDateVal(dateformat, from.val());
    var toDate = getDateVal(dateformat, to.val());
    var idempresa = $("#empresas").val();
    sugerencias.forEach(function(element) {
        var fecha = getDateVal("m/d/y", element.fecha)
        if (    (tipo == 0 || tipo == element.tipo) &&
                (search.trim().length == 0 || 
                normalize(element.empleado).indexOf(search) != -1 ||
                normalize(element.comentario).indexOf(search) != -1) &&
                (fromDate == null || fecha >= fromDate) &&
                (toDate == null || fecha <= toDate) &&
                (idempresa == 0 || element.idempresa == idempresa)
        ) {
            datos.append(`
                <div class="row datarow">
                    <div class="col-md-2">
                        ${$.datepicker.formatDate(dateformat, fecha)}
                    </div>
                    <div class="col-md-2">
                        ${element.empleado}
                    </div>
                    <div class="col-md-8">
                        ${element.comentario}
                    </div>
                </div>
            `)
        }
    });

    $(".datarow").click(function(element) {
        if (seleccionado != null)
            seleccionado.style.backgroundColor = "";
        seleccionado = element.currentTarget;
        seleccionado.style.backgroundColor = "lightblue";
    });
}