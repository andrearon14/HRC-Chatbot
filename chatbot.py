import dialogflow
import os
import sys
import json
import dateutil.parser
import datetime
import ModuloLicencia
import ModuloEmpleado
import subprocess
from config import CFG_MYSQL


class Global:
    pass

g = Global()
g.vip = 1

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result

def get_chat_response(message, empleado):
    if message.lower() == "reset":
        reiniciar()
        return { "message": "Reiniciado." }
    else:
        if empleado.get_notificaciones():
            ModuloEmpleado.ModuloEmpleado.limpiar_notificaciones(empleado.get_id())

        project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
        query_result = detect_intent_texts(project_id, "unique", message, 'en')
        if query_result.fulfillment_text == "CALENDARIO":
            if empleado.get_dias_licencia_disponibles() == 0:
                detect_intent_texts(project_id, "unique", "cancelar", 'en')
                return { "message": "Tu no tienes días disponibles." }
            else:
                return { "calendar": get_reservados(empleado) }
        elif query_result.fulfillment_text == "FOTOS":
            lista = ModuloEmpleado.EmpleadoConversor.list_to_dict_foto(query_result.parameters['Area'])
            if len(lista) == 0:
                return { "message": "No hay empleados en esta area." }
            else:
                return { "fotos": lista }
        else:
            return { "message": query_result.fulfillment_text }

def reiniciar():
    g.vip = 1
    execute_sql('crearDB.sql')
    execute_sql('initDB.sql')

def execute_sql(filename):
    f = open(filename,'r')
    p = subprocess.Popen(['/Applications/MySQLWorkbench.app/Contents/MacOS/mysql', '--user='+CFG_MYSQL['user'], '--password='+CFG_MYSQL['password'], CFG_MYSQL['database']], stdin=f)
    p.wait()

def get_reservados(empleado):
    #reservados = ['03/14/19','03/15/19','03/18/19']
    reservados = get_reservados_confirmados()
    agregar_lista_fechas(reservados, ModuloLicencia.ModuloLicencia.listar_actual_por_empleado(empleado.get_id()))
    return reservados

def get_reservados_confirmados():
    reservados = []
    agregar_lista_fechas(reservados, ModuloLicencia.ModuloLicencia.listar_actual_confirmada())
    return reservados

def agregar_lista_fechas(reservados,lista_licencias):
    for licencia in lista_licencias:
        if licencia.get_razon_rechazada() == None:
            date = licencia.get_fecha_comienzo()
            while date <= licencia.get_fecha_final():
                reservados.append(date.strftime("%x"))
                date = date + datetime.timedelta(days=1)

def estan_reservados(from_, to):
    for res in get_reservados_confirmados():
        date = dateutil.parser.parse(res)
        if date >= from_.replace(tzinfo=None) and date <= to.replace(tzinfo=None):
            return True
    return False

def cantidad_notificaciones(empleado):
    n = 1
    if empleado.get_id() == g.vip and empleado.get_dias_licencia_disponibles() > 0:
        n += 1
    if empleado.get_notificaciones() != None:
        n += 1
    return n

def texto_notificaciones(empleado):
    s = "Recuerde puedes solicitar adelanto de sueldo entre el 20 y 28 del mes.<br>"
    if empleado.get_id() == g.vip and empleado.get_dias_licencia_disponibles() > 0:
        s += "Debes elegir cuando tomar tu licencia dado que tienes prioridad.<br>"
    if empleado.get_notificaciones() != None:
        s += empleado.get_notificaciones()
    return s

mes = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio',
       'Agosto','Septiembre','Octubre','Noviembre','Diciembre']
def format_date(date):
    return date.strftime("%d de ") + mes[date.month-1] + date.strftime(" de %Y")

def format_dates(from_, to):
    return format_date(from_) + " al " + format_date(to)

def dias_disponibles(empleado):
    if empleado.get_dias_licencia_disponibles() == 1:
        return str(empleado.get_dias_licencia_disponibles()) + " día disponible"
    else:
        return str(empleado.get_dias_licencia_disponibles()) + " días disponibles"

def get_hook_reply(data, empleado):
    intent = data['queryResult']['intent']['displayName']
    print(intent, file=sys.stderr)

    if intent == "CuantosDisponibles":
        if empleado.get_dias_licencia_disponibles() == 0:
            msg = "No tienes días disponibles."
            if empleado.get_id() == g.vip:
                subir_vip_si_corresponde(0)
        else:
            msg = "Tienes " + dias_disponibles(empleado)
    elif intent == "QueTengo":
        tengo = ModuloLicencia.ModuloLicencia.listar_actual_por_empleado(empleado.get_id())
        if len(tengo) == 0:
            msg = "No tienes licencia pedida."
        else:
            n = 1
            msg = "Licencias"
            for licencia in tengo:
                msg += "<BR>" + str(n) + ". del " + format_dates(licencia.get_fecha_comienzo(), licencia.get_fecha_final())
                if licencia.get_confirmada():
                    msg += " esta confirmada"
                elif licencia.get_razon_rechazada():
                    msg += " ha sido rechazada porque " + licencia.get_razon_rechazada()
                else:
                    msg += " solicitada"
                n += 1
    elif intent == "Cuando":
        #print(data, file=sys.stderr)
        range = data['queryResult']['parameters']['RANGO'] #crash when cancelled
        from_ = dateutil.parser.parse(range[0])
        if len(range) > 1:
            to = dateutil.parser.parse(range[1])
        else:
            to = from_
        dias_tomados = (to - from_).days + 1
        print("TOMADOS {}".format(dias_tomados), file=sys.stderr)
        if dias_tomados > empleado.get_dias_licencia_disponibles():
            msg = "Tu solo posees " + dias_disponibles(empleado)
        else:
            if estan_reservados(from_, to):
                msg = "Algunos de los días elegidos estan reservados"
            else:
                confirmada = empleado.get_id() == g.vip
                msg = "Se ha {} tu licencia del ".format("confirmado" if confirmada else "solicitado") + format_dates(from_, to)
                disponibles = ModuloEmpleado.ModuloEmpleado.agregar_dias_licencia_disponibles(empleado.get_id(), -dias_tomados)
                ModuloLicencia.ModuloLicencia.insertar(empleado.get_id(), from_, to, confirmada)

                if confirmada:
                    verificar_si_hace_rechazar_otras_licencias(from_, to)
                    subir_vip_si_corresponde(disponibles)
    elif intent == "AdelantoSueldo":
        if empleado.get_adelanto_permitido() > 0:
            msg = "Tienes pre-aprovado {} para adelantos de sueldo, puede ser pedido entre el 20 y 28 del mes.".format(empleado.get_adelanto_permitido())
        else:
            msg = "No tienes más adelanto de sueldo disponible."
    elif intent == "SolicitoAdelanto":
        if empleado.get_adelanto_permitido() > 0:
            number = data['queryResult']['parameters']['number']
            if number > empleado.get_adelanto_permitido():
                msg = "Tienes solo {} de adelanto permitido.".format(empleado.get_adelanto_permitido())
            else:
                ModuloEmpleado.ModuloEmpleado.cambiar_adelanto_permitido(empleado.get_id(), empleado.get_adelanto_permitido() - number)
                msg = "Tu adelanto de {} ha sido confirmado, será depositado el 30 de este mes.".format(number)
        else:
            msg = "No tienes más adelanto de sueldo disponible."
    return {
        "fulfillmentText": msg
    }

def verificar_si_hace_rechazar_otras_licencias(from_, to):
    for licencia in ModuloLicencia.ModuloLicencia.listar_actual_solicitadas():
        if from_.replace(tzinfo=None) <= licencia.get_fecha_final() and to.replace(tzinfo=None) >= licencia.get_fecha_final():
            razon = "otra persona con más antigüedad pidio la misma fecha."
            licencia.set_razon_rechazada(razon)
            ModuloLicencia.ModuloLicencia.modificar(licencia)
            notificacion = "Su licencia del " + format_dates(licencia.get_fecha_comienzo(), licencia.get_fecha_final()) + " ha sido rechazada porque " + razon
            ModuloEmpleado.ModuloEmpleado.agregar_notificacion(licencia.get_idempleado(), notificacion)
            dias_tomados = (licencia.get_fecha_final() - licencia.get_fecha_comienzo()).days + 1
            ModuloEmpleado.ModuloEmpleado.agregar_dias_licencia_disponibles(licencia.get_idempleado(), dias_tomados)

def subir_vip_si_corresponde(disponibles):
    while disponibles == 0:
        g.vip += 1
        empleadovip = ModuloEmpleado.ModuloEmpleado.buscar(g.vip)
        if empleadovip == None:
            break
        for licencia in ModuloLicencia.ModuloLicencia.listar_actual_por_empleado(empleadovip.get_id()):
            if not licencia.get_confirmada() and licencia.get_razon_rechazada() == None:
                licencia.set_confirmada(True)
                ModuloLicencia.ModuloLicencia.modificar(licencia)
                verificar_si_hace_rechazar_otras_licencias(licencia.get_fecha_comienzo(), licencia.get_fecha_final())
                notificacion = "Su licencia del " + format_dates(licencia.get_fecha_comienzo(), licencia.get_fecha_final()) + " ha sido confirmada."
                ModuloEmpleado.ModuloEmpleado.agregar_notificacion(licencia.get_idempleado(), notificacion)
        disponibles = empleadovip.get_dias_licencia_disponibles()