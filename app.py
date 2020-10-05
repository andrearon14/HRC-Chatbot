from flask import Flask, render_template, jsonify, request
import chatbot
import ModuloEmpresa
import ModuloEmpleado
import ModuloTipoSugerencia
import ModuloSugerencia
import ModuloUsuario
import json
import sys
import ast
from datetime import datetime
    
app = Flask(__name__)
#FLASK_DEBUG=1 flask run

app.usuario_actual = ModuloUsuario.ModuloUsuario.buscar(1)

# Arma estructura de usuario actual mas lista del resto
def usr():
    userlista = []
    for user in ModuloUsuario.ModuloUsuario.listar():
        if user.get_id() != app.usuario_actual.get_id():
            otro = ModuloUsuario.UsuarioConversor.to_dict(user)
            userlista.append(otro)
    data = ModuloUsuario.UsuarioConversor.to_dict(app.usuario_actual).copy()
    data["lista"] = userlista
    data["notificacion"] = chatbot.cantidad_notificaciones(get_actual_empleado())
    data["notificacion_texto"] = chatbot.texto_notificaciones(get_actual_empleado())
    return data

def get_actual_empleado():
    return ModuloEmpleado.ModuloEmpleado.buscar(app.usuario_actual.get_idempleado())

def get_actual_empleado_json():
    return json.dumps(ModuloEmpleado.EmpleadoConversor.to_dict(get_actual_empleado()))

## PUNTOS DE ENTRADA ##
@app.route("/")
def main():
    return render_template('index.html', usr = usr())

@app.route("/datos_empresa")
def datos_empresa():
    if app.usuario_actual.get_admin() == True:
        return render_template('datos_empresa.html', usr = usr(), pag = "datos_empresa", empresas = list_companies_json())
    else:
        return render_template('index.html', usr = usr(), pag = "datos_empresa")

@app.route("/datos_empleado")
def datos_empleado():
    if app.usuario_actual.get_admin() == True:
        return render_template('datos_empleado.html', usr = usr(), pag = "datos_empleado", empresas = list_companies(), empleados = list_employees_json())
    else:
        return render_template('datos_empleado_me.html', usr = usr(), pag = "datos_empleado", empleado = get_actual_empleado_json())

@app.route("/sugerencias")
def solicitudes():
    if app.usuario_actual.get_admin() == True:
        return render_template('sugerencias_admin.html', usr = usr(), pag = "sugerencias", tipos = list_suggestion_types(), empresas = list_companies(), sugerencias = list_suggestions_json())
    else:
        return render_template('sugerencias_empleado.html', usr = usr(), pag = "sugerencias", tipos = list_suggestion_types())

@app.route("/solicitudes")
def sugerencias():
    return render_template('chatbot.html', usr = usr(), pag = "solicitudes")

## CHATBOT ##
@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    return jsonify(chatbot.get_chat_response(message, get_actual_empleado()))

@app.route('/hook', methods=['POST'])
def hook():
    data = request.get_json(silent=True)
    reply = chatbot.get_hook_reply(data, get_actual_empleado())
    return jsonify(reply)

## SUGERENCIAS ##
def list_suggestion_types():
    return ModuloTipoSugerencia.TipoSugerenciaConversor.list_to_dict(ModuloTipoSugerencia.ModuloTipoSugerencia.listar())

def list_suggestions_json():
    return json.dumps(ModuloSugerencia.SugerenciaConversor.list_to_dict(ModuloSugerencia.ModuloSugerencia.listar()))

@app.route('/send_suggestion', methods=['POST'])
def send_suggestion():
    d = request.form.to_dict()
    anonimo = 'anonimo' in d and d['anonimo'] == 'on'
    empleado_actual = get_actual_empleado()
    empleado = None if anonimo else empleado_actual
    empresa = ModuloEmpresa.ModuloEmpresa.buscar(empleado_actual.get_idempresa())
    sugerencia = ModuloSugerencia.Sugerencia(0, d["tipo"], datetime.now(), empresa, empleado, d["comentario"])
    ModuloSugerencia.ModuloSugerencia.insertar(sugerencia)
    return render_template('sugerencias_empleado_ok.html', usr = usr(), pag = "sugerencias")

## USUARIOS ##
@app.route('/set_user', methods=['POST'])
def set_user():
    nombre = request.args.get('nombre')
    usuario = ModuloUsuario.ModuloUsuario.buscar_por_nombre(nombre)
    if usuario:
        app.usuario_actual = usuario
    return "Done"

## EMPLEADOS ##
def list_employees_json():
    return json.dumps(ModuloEmpleado.EmpleadoConversor.list_to_dict(ModuloEmpleado.ModuloEmpleado.listar()))  

@app.route('/save_employee', methods=['POST'])
def save_employee():
    empleado = ast.literal_eval(request.form["empleado"])
    obj = ModuloEmpleado.EmpleadoConversor.from_dict(empleado)
    if "id" in empleado:
        ModuloEmpleado.ModuloEmpleado.modificar(obj)
        return str(empleado["id"])
    else:
        id_ = ModuloEmpleado.ModuloEmpleado.insertar(obj)
        ModuloUsuario.ModuloUsuario.insertar(obj.get_foto(), obj.get_nombre(), False, id_)
        return str(id_)
    return ""

@app.route('/remove_employee', methods=['POST'])
def remove_employee():
    id_ = request.form["id"]
    ModuloEmpleado.ModuloEmpleado.eliminar(id_)
    return ""

## EMPRESAS ##
def list_companies():
    return ModuloEmpresa.EmpresaConversor.list_to_dict(ModuloEmpresa.ModuloEmpresa.listar())

def list_companies_json():
    return json.dumps(list_companies())

@app.route('/save_company', methods=['POST'])
def save_company():
    empresa = ast.literal_eval(request.form["empresa"])
    obj = ModuloEmpresa.EmpresaConversor.from_dict(empresa)
    if "id" in empresa:
        ModuloEmpresa.ModuloEmpresa.modificar(obj)
        return str(empresa["id"])
    else:
        id_ = ModuloEmpresa.ModuloEmpresa.insertar(obj)
        return str(id_)
    return ""

@app.route('/remove_company', methods=['POST'])
def remove_company():
    id_ = request.form["id"]
    ModuloEmpresa.ModuloEmpresa.eliminar(id_)
    return ""

####
if __name__ == "__main__":
    app.run()