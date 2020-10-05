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
            $("#documento").val("");
            $("#sexo").val("");
            $("#direccion").val("");
            $("#correo").val("");
            $("#activo").prop('checked', true);
            $("#empresa").prop('selectIndex', 0);
        }
    });
    $("#guardar").click(function() {
        var d = {};
        if (seleccionado != null)
            d = $(seleccionado).data("elemento");
        d.nombre = $("#nombre").val();
        d.documento = $("#documento").val();
        d.sexo = $("#sexo").val();
        d.direccion = $("#direccion").val();
        d.correo = $("#correo").val();
        d.activo = $("#activo").is(':checked').toString();
        d.empresa = $("#empresa").val();
        $.post("/save_employee", { empleado : JSON.stringify(d) }, function(id) {
            sessionStorage.setItem("id_seleccionado", id);
            location.reload()
        });
    });
    $("#eliminar").click(function() {
        if (seleccionado != null) {
            var d = $(seleccionado).data("elemento");
            $.post("/remove_employee", { id : d.id }, function() {
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
            <div class="col-md-2">
                Documento
            </div>
            <div class="col-md-2">
                Nombre
            </div>
            <div class="col-md-3">
                Correo
            </div>
            <div class="col-md-5">
                Dirección
            </div>
        </div>
    `);

    if (typeof empleados != "undefined") {
        var search = $(".search").val().toLowerCase();
        empleados.forEach(function(element) {
            if (search.trim().length == 0 || 
                element.nombre.toLowerCase().indexOf(search) != -1)
            {
                datos.append(`
                    <div class="row datarow">
                        <div class="col-md-2">
                            ${element.documento}
                        </div>
                        <div class="col-md-2">
                            ${element.nombre}
                        </div>
                        <div class="col-md-3">
                            ${element.correo}
                        </div>
                        <div class="col-md-5">
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
    $("#documento").val(d.documento);
    $("#sexo").val(d.sexo);
    $("#direccion").val(d.direccion);
    $("#correo").val(d.correo);
    $("#activo").prop('checked', d.activo != "false");
    $("#empresa").val(d.empresa);
}

function modificar_habilitado() {
    var confirmar = false;
    if (seleccionado != null) {
        var d = $(seleccionado).data("elemento");
        confirmar = $("#nombre").val() != d.nombre ||
            $("#documento").val() != d.documento ||
            $("#sexo").val() != d.sexo ||
            $("#direccion").val() != d.direccion ||
            $("#correo").val() != d.correo ||
            $("#activo").is(':checked') != (d.activo != "false") ||
            $("#empresa").val() != d.empresa;
    }
    else {
        confirmar = $("#nombre").val() != "" ||
            $("#documento").val() != "" ||
            $("#direccion").val() != "" ||
            $("#correo").val() != "";
    }
    return !confirmar || confirm("Se hicieron modificaciones, desea seguir y descartarlas?");
}