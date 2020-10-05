# ###
# creado por adrian
#
#
# ###

import bd
import sys
import mysql.connector
from config import CFG_MYSQL


class Empleado:
    def __init__(self,id,idempresa,documento,nombre,direccion,correo,activo,dias_licencia_disponibles,notificaciones,adelanto_permitido,foto,cargo,sexo):
        self.id = id
        self.idempresa = idempresa
        self.documento = documento
        self.nombre = nombre
        self.direccion = direccion
        self.correo = correo
        self.activo = activo
        self.dias_licencia_disponibles = dias_licencia_disponibles
        self.notificaciones = notificaciones
        self.adelanto_permitido = adelanto_permitido
        self.foto = foto
        self.cargo = cargo
        self.sexo = sexo

    def get_id(self):
        return self.id
    def set_id(self,valor):
        self.id=valor

    def get_idempresa(self):
        return self.idempresa
    def set_idempresa(self,valor):
        self.idempresa=valor

    def get_documento(self):
        return self.documento
    def set_documento(self,valor):
        self.documento=valor

    def get_nombre(self):
        return self.nombre
    def set_nombre(self,valor):
        self.nombre=valor

    def get_direccion(self):
        return self.direccion
    def set_direccion(self,valor):
        self.direccion=valor

    def get_correo(self):
        return self.correo
    def set_correo(self,valor):
        self.correo=valor

    def get_activo(self):
        return self.activo
    def set_activo(self,valor):
        self.activo=valor

    def get_dias_licencia_disponibles(self):
        return self.dias_licencia_disponibles
    def set_dias_licencia_disponibles(self,valor):
        self.dias_licencia_disponibles=valor

    def get_notificaciones(self):
        return self.notificaciones
    def set_notificaciones(self,valor):
        self.notificaciones=valor

    def get_adelanto_permitido(self):
        return self.adelanto_permitido
    def set_adelanto_permitido(self,valor):
        self.adelanto_permitido=valor

    def get_foto(self):
        return self.foto
    def set_foto(self,valor):
        self.foto=valor

    def get_cargo(self):
        return self.cargo
    def set_cargo(self,valor):
        self.cargo=valor

    def get_sexo(self):
        return self.sexo
    def set_sexo(self,valor):
        self.sexo=valor

    def __str__(self):
        return "Nombre: {} / {} ".format(self.documento, self.nombre)


class ModuloEmpleado:
    @staticmethod
    def buscar(id_):
        sql_select = "SELECT * FROM empleado WHERE id = {};".format(id_)

        empleado = None
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_select)
        result = dr.fetchall()

        for cnj in result:
            empleado = Empleado(cnj[0],cnj[1],cnj[2],cnj[3],cnj[4],cnj[5],cnj[6],cnj[7],cnj[8],cnj[9],cnj[10],cnj[11],cnj[12])

        dr.close()
        db.close()
        return empleado

    @staticmethod
    def insertar(empleado):
        idempresa = empleado.get_idempresa()
        documento = empleado.get_documento()
        nombre = empleado.get_nombre()
        direccion = empleado.get_direccion()
        correo = empleado.get_correo()
        activo = empleado.get_activo()
        dias_licencia_disponibles = empleado.get_dias_licencia_disponibles()
        notificaciones = empleado.get_notificaciones()
        adelanto_permitido = empleado.get_adelanto_permitido()
        foto = empleado.get_foto()
        cargo = empleado.get_cargo()
        sexo = empleado.get_sexo()

        sql_insert = "INSERT INTO empleado(empresa,documento,nombre,direccion,correo,activo,diasLicenciaDisponibles,notificaciones,adelantoPermitido,foto,cargo,sexo) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
        args = (idempresa,documento,nombre,direccion,correo,activo,dias_licencia_disponibles,notificaciones,adelanto_permitido,foto,cargo,sexo)

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_insert,args)
        db.commit()
        id_ = dr.lastrowid
        dr.close()
        db.close()
        return id_

    @staticmethod
    def listar():
        """
        devuelve una lista completa nueva de empleados
        """
        nuevaLista = []
        sql_select = "SELECT * FROM empleado"

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_select)
        result = dr.fetchall()

        for cnj in result:
            emp = Empleado(cnj[0],cnj[1],cnj[2],cnj[3],cnj[4],cnj[5],cnj[6],cnj[7],cnj[8],cnj[9],cnj[10],cnj[11],cnj[12])
            nuevaLista.append(emp)

        dr.close()
        db.close()
        return nuevaLista

    @staticmethod
    def listar_area(area):
        nuevaLista = []
        sql_select = 'SELECT empleado.* FROM area JOIN areaempleado ON area.id = areaempleado.idarea JOIN empleado ON empleado.id = areaempleado.idempleado WHERE area.nombre = "{}";'.format(area)

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_select)
        result = dr.fetchall()

        for cnj in result:
            emp = Empleado(cnj[0],cnj[1],cnj[2],cnj[3],cnj[4],cnj[5],cnj[6],cnj[7],cnj[8],cnj[9],cnj[10],cnj[11],cnj[12])
            nuevaLista.append(emp)

        dr.close()
        db.close()
        return nuevaLista

    @staticmethod
    def modificar(empleado):
        idempresa = empleado.get_idempresa()
        documento = empleado.get_documento()
        nombre = empleado.get_nombre()
        direccion = empleado.get_direccion()
        correo = empleado.get_correo()
        activo = empleado.get_activo()
        dias_licencia_disponibles = empleado.get_dias_licencia_disponibles()
        notificaciones = empleado.get_notificaciones()
        adelanto_permitido = empleado.get_adelanto_permitido()
        foto = empleado.get_foto()
        cargo = empleado.get_cargo()
        sexo = empleado.get_sexo()
        id_ = empleado.get_id()

        sql_update = "UPDATE empleado SET empresa = %s,documento = %s,nombre = %s,direccion = %s,correo = %s,activo = %s,diasLicenciaDisponibles = %s,notificaciones = %s,adelantoPermitido = %s,foto = %s,cargo = %s,sexo = %s WHERE id = {};".format(id_)
        args = (idempresa,documento,nombre,direccion,correo,activo,dias_licencia_disponibles,notificaciones,adelanto_permitido,foto,cargo,sexo)

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_update, args)
        db.commit()

        dr.close()
        db.close()
        return True

    @staticmethod
    def agregar_dias_licencia_disponibles(id_,dias):
        sql_select = "SELECT diasLicenciaDisponibles FROM empleado WHERE id = {};".format(id_)
        sql_update = "UPDATE empleado SET diasLicenciaDisponibles = %s WHERE id = {};".format(id_)
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()

        dr.execute(sql_select)
        disponibles = dr.fetchone()[0] + dias

        args = (disponibles,)
        dr.execute(sql_update,args)
        db.commit()
        dr.close()
        db.close()
        return disponibles

    @staticmethod
    def agregar_notificacion(id_,notificacion):
        sql_select = "SELECT notificaciones FROM empleado WHERE id = {};".format(id_)
        sql_update = "UPDATE empleado SET notificaciones = %s WHERE id = {};".format(id_)
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()

        dr.execute(sql_select)
        notificacion_anterior = dr.fetchone()[0]
        if notificacion_anterior == None:
            notificacion_nueva = notificacion
        else:
            notificacion_nueva = notificacion_anterior + "<BR>" + notificacion

        args = (notificacion_nueva,)
        dr.execute(sql_update,args)
        db.commit()
        dr.close()
        db.close()
        return notificacion_nueva

    @staticmethod
    def limpiar_notificaciones(id_):
        sql_update = "UPDATE empleado SET notificaciones = NULL WHERE id = {};".format(id_)
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_update)
        db.commit()
        dr.close()
        db.close()

    @staticmethod
    def cambiar_adelanto_permitido(id_, valor):
        sql_update = "UPDATE empleado SET adelantoPermitido = {} WHERE id = {};".format(valor, id_)
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_update)
        db.commit()
        dr.close()
        db.close()

    @staticmethod
    def eliminar(id_):
        sql_delete = "DELETE FROM empleado WHERE id = {};".format(id_)

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_delete)

        db.commit()
        dr.close()
        db.close()
        return True


class EmpleadoConversor:
    @staticmethod
    def to_dict(empleado):
        return { 'id' : empleado.get_id(), 'empresa' : empleado.get_idempresa(), 'documento' : empleado.get_documento(), 'nombre' : empleado.get_nombre(), 'direccion' : empleado.get_direccion(), 'correo' : empleado.get_correo(), 'activo' : empleado.get_activo(), 'sexo' : empleado.get_sexo() }

    @staticmethod
    def from_dict(empleado):
        id_ = empleado["id"] if "id" in empleado else 0
        return Empleado(id_, empleado["empresa"], empleado["documento"], empleado["nombre"], empleado["direccion"], empleado["correo"], empleado["activo"], 10, None, 15000, "mujer.png" if empleado["sexo"] == "F" else "hombre.png", "", empleado["sexo"])

    @staticmethod
    def list_to_dict(listt):
        return list(map(EmpleadoConversor.to_dict, listt))

    @staticmethod
    def to_dict_foto(empleado):
        return { 'foto' : empleado.get_foto(), 'nombre' : empleado.get_nombre(), 'cargo' : empleado.get_cargo() }

    @staticmethod
    def list_to_dict_foto(area):
        return list(map(EmpleadoConversor.to_dict_foto, ModuloEmpleado.listar_area(area)))