import bd
import sys
import mysql.connector
from config import CFG_MYSQL


class Empresa:
    def __init__(self,id,rut,nombre,correo,telefono,direccion):
        self.id = id
        self.rut = rut
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion

    def get_id(self):
        return self.id
    def set_id(self,valor):
        self.id=valor

    def get_rut(self):
        return self.rut
    def set_rut(self,valor):
        self.rut=valor

    def get_nombre(self):
        return self.nombre
    def set_nombre(self,valor):
        self.nombre=valor

    def get_correo(self):
        return self.correo
    def set_correo(self,valor):
        self.correo=valor

    def get_telefono(self):
        return self.telefono
    def set_telefono(self,valor):
        self.telefono=valor

    def get_direccion(self):
        return self.direccion
    def set_direccion(self,valor):
        self.direccion=valor

    def __str__(self):
        return "Nombre: {} / {} ".format(self.rut, self.nombre)


class ModuloEmpresa:
    @staticmethod
    def buscar(id_):
        sql_select = "SELECT * FROM empresa WHERE id = {};".format(id_)

        empresa = None
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_select)
        result = dr.fetchall()

        for cnj in result:
            empresa = Empresa(cnj[0],cnj[1],cnj[2],cnj[3],cnj[4],cnj[5])

        dr.close()
        db.close()
        return empresa

    @staticmethod
    def insertar(empresa):
        rut = empresa.get_rut()
        nombre = empresa.get_nombre()
        correo = empresa.get_correo()
        telefono = empresa.get_telefono()
        direccion = empresa.get_direccion()

        sql_insert = "INSERT INTO empresa(rut,nombre,correo,telefono,direccion) VALUES(%s,%s,%s,%s,%s);"
        args = (rut,nombre,correo,telefono,direccion)

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
        devuelve una lista completa nueva de empresas
        """
        nuevaLista = []
        sql_select = "SELECT * FROM empresa"

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_select)
        result = dr.fetchall()

        for cnj in result:
            emp = Empresa(cnj[0],cnj[1],cnj[2],cnj[3],cnj[4],cnj[5])
            nuevaLista.append(emp)

        dr.close()
        db.close()
        return nuevaLista

    @staticmethod
    def modificar(empresa):
        rut = empresa.get_rut()
        nombre = empresa.get_nombre()
        correo = empresa.get_correo()
        telefono = empresa.get_telefono()
        direccion = empresa.get_direccion()
        id_ = empresa.get_id()

        sql_update = "UPDATE empresa SET rut = %s,nombre = %s,correo = %s,telefono = %s,direccion = %s WHERE id = {};".format(id_)
        args = (rut,nombre,correo,telefono,direccion)

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_update, args)
        db.commit()

        dr.close()
        db.close()
        return True

    @staticmethod
    def eliminar(id_):
        sql_delete = "DELETE FROM empresa WHERE id = {};".format(id_)

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_delete)

        db.commit()
        dr.close()
        db.close()
        return True


class EmpresaConversor:
    @staticmethod
    def to_dict(empresa):
        return { 'id' : empresa.get_id(), 'rut' : empresa.get_rut(), 'nombre' : empresa.get_nombre(), 'correo' : empresa.get_correo(), 'telefono' : empresa.get_telefono(), 'direccion' : empresa.get_direccion() }

    @staticmethod
    def from_dict(empresa):
        id_ = empresa["id"] if "id" in empresa else 0
        return Empresa(id_, empresa["rut"], empresa["nombre"], empresa["correo"], empresa["telefono"], empresa["direccion"])

    @staticmethod
    def list_to_dict(listt):
        return list(map(EmpresaConversor.to_dict, listt))