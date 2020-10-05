$( document ).ready(function() {
    var d = empleado;
    $("#nombre").val(d.nombre);
    $("#documento").val(d.documento);
    $("#direccion").val(d.direccion);
    $("#correo").val(d.correo);

    $("#guardar").click(function() {
        d.nombre = $("#nombre").val();
        d.documento = $("#documento").val(); 
        d.direccion = $("#direccion").val();
        d.correo = $("#correo").val();
        $.post("/save_employee", { empleado : JSON.stringify(d) }, function(id) {
            location.reload()
        });
    });
});