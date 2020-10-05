$( document ).ready(function() {
    recargar();

    $(".search").on("input", function() {
        seleccionado = null;
        recargar()
    });

    $("#nuevo").click(function() {
        if (modificar_habilitado()) {
            if (seleccionado != null) {
                seleccionado.style.backgroundColor = "";
                seleccionado = null;
            }
            $("#nombre").val("");
            $("#rut").val("");
            $("#direccion").val("");
            $("#telefono").val("");
            $("#correo").val("");
        }
    });
    $("#guardar").click(function() {
        var d = {};
        if (seleccionado != null)
            d = $(seleccionado).data("elemento");
        d.nombre = $("#nombre").val();
        d.rut = $("#rut").val(); 
        d.direccion = $("#direccion").val();
        d.telefono = $("#telefono").val();
        d.correo = $("#correo").val();
        $.post("/save_company", { empresa : JSON.stringify(d) }, function(id) {
            sessionStorage.setItem("id_seleccionado", id);
            location.reload()
        });
    });
    $("#eliminar").click(function() {
        if (seleccionado != null) {
            var d = $(seleccionado).data("elemento");
            $.post("/remove_company", { id : d.id }, function() {
                sessionStorage.setItem("id_seleccionado", "");
                location.reload();
            });
        }
    });
    $("#imprimir").click(function() {
    });
});

var seleccionado = null;
var id_seleccionado = sessionStorage.getItem("id_seleccionado");
function recargar() {
    var datos = $("#datos");

    datos.html(`
        <div class="row headerrow">
            <div class="col-md-3">
                Nombre
            </div>
            <div class="col-md-2">
                Rut
            </div>
            <div class="col-md-2">
                Teléfono
            </div>
            <div class="col-md-2">
                Correo
            </div>
            <div class="col-md-3">
                Dirección
            </div>
        </div>
    `);

    if (typeof empresas != "undefined") {
        var search = $(".search").val().toLowerCase();
        empresas.forEach(function(element) {
            if (search.trim().length == 0 || 
                element.nombre.toLowerCase().indexOf(search) != -1)
            {
                datos.append(`
                    <div class="row datarow">
                        <div class="col-md-3">
                            ${element.nombre}
                        </div>
                        <div class="col-md-2">
                            ${element.rut}
                        </div>
                        <div class="col-md-2">
                            ${element.telefono}
                        </div>
                        <div class="col-md-2">
                            ${element.correo}
                        </div>
                        <div class="col-md-3">
                            ${element.direccion}
                        </div>
                    </div>
                `);
                datos.children().last().data("elemento", element);
                if (id_seleccionado == element.id) {
                    seleccionado = datos.children().last()[0];
                    cargar_seleccionado();  
                }
            }
        });
    }

    id_seleccionado = null;

    $(".datarow").click(function(element) {
        if (modificar_habilitado()) {
            if (seleccionado != null)
                seleccionado.style.backgroundColor = "";
            seleccionado = element.currentTarget;
            cargar_seleccionado();
        }
    });
}

function cargar_seleccionado() {
    seleccionado.style.backgroundColor = "lightblue";
    var d = $(seleccionado).data("elemento");
    $("#nombre").val(d.nombre);
    $("#rut").val(d.rut);
    $("#direccion").val(d.direccion);
    $("#telefono").val(d.telefono);
    $("#correo").val(d.correo);
}

function modificar_habilitado() {
    var confirmar = false;
    if (seleccionado != null) {
        var d = $(seleccionado).data("elemento");
        confirmar = $("#nombre").val() != d.nombre ||
            $("#rut").val() != d.rut ||
            $("#direccion").val() != d.direccion ||
            $("#telefono").val() != d.telefono ||
            $("#correo").val() != d.correo;
    }
    else {
        confirmar = $("#nombre").val() != "" ||
            $("#rut").val() != "" ||
            $("#direccion").val() != "" ||
            $("#telefono").val() != "" ||
            $("#correo").val() != "";
    }
    return !confirmar || confirm("Se hicieron modificaciones, desea seguir y descartarlas?");
}