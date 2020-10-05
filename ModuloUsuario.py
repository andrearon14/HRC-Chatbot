# ###
# creado por adrian
#
#
# ###

import mysql.connector
from config import CFG_MYSQL


class Usuario:
    def __init__(self,id,foto,nombre,admin,idempleado):
        self.id = id
        self.foto = foto
        self.nombre = nombre
        self.admin = admin
        self.idempleado = idempleado
    
    def get_id(self):
        return self.id
    def set_id(self,valor):
        self.id = valor

    def get_nombre(self):
        return self.nombre
    def set_nombre(self, valor):
        self.nombre = valor

    def get_foto(self):
        return self.foto

    def set_foto(self, valor):
        self.foto = valor

    def get_admin(self):
        return self.admin
    def set_admin(self, valor):
        self.admin = valor

    def get_idempleado(self):
        return self.idempleado
    def set_empleado(self,valor):
       self.idempleado = valor
       
    def __str__(self):
        return "id {} - nombre {}".format(self.id, self.nombre)


class ModuloUsuario:
    @staticmethod
    def insertar(foto, nombre, admin, idempleado):
        sql_insert = "INSERT INTO usuario(foto,nombre,administrador,idempleado) VALUES (%s,%s,%s,%s);"
        args = (foto,nombre,admin,idempleado)

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_insert,args)
        db.commit()
        dr.close()
        db.close()

    @staticmethod
    def eliminar(id_):
        sql_delete = "DELETE FROM usuario WHERE id = {};".format(id_)
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_delete)
        db.commit()
        dr.close()
        db.close()
        return True

    @staticmethod
    def buscar(id_):
        sql_select = "SELECT * FROM usuario WHERE id = {};".format(id_)

        usuario = None
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_select)
        result = dr.fetchall()

        for cnj in result:
            usuario = Usuario(cnj[0],cnj[1],cnj[2],cnj[3],cnj[4])

        dr.close()
        db.close() 
        return usuario
    
    @staticmethod
    def buscar_por_nombre(nombre):
        sql_select = "SELECT * FROM usuario WHERE nombre = '{}';".format(nombre)

        usuario = None
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_select)
        result = dr.fetchall()

        for cnj in result:
            usuario = Usuario(cnj[0],cnj[1],cnj[2],cnj[3],cnj[4])

        dr.close()
        db.close() 
        return usuario

    @staticmethod
    def listar():
        sql = "SELECT * FROM usuario;"
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql)
        result = dr.fetchall()

        lista = []
        for cnj in result:
            lista.append(Usuario(cnj[0],cnj[1],cnj[2],cnj[3],cnj[4]))

        dr.close()
        db.close()
        return lista


class UsuarioConversor:
    @staticmethod
    def to_dict(usuario):
        return { 'foto' : usuario.get_foto(), 'nombre' : usuario.get_nombre(), 'admin' : usuario.get_admin() }

    @staticmethod
    def from_dict(usuario):
        return Usuario(usuario['id'], usuario['foto'], usuario['nombre'], usuario['admin'], usuario['idempleado'])

    @staticmethod
    def list_to_dict(listt):
        return list(map(UsuarioConversor.to_dict, listt))