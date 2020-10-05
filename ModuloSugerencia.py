# ###
# creado por adrian
#
#
# ###

import mysql.connector
import datetime
import ModuloEmpresa
import ModuloEmpleado
from config import CFG_MYSQL

class Sugerencia:
    def __init__(self,id,tipo,fecha,empresa,empleado,comentario):
        self.id = id
        self.tipo = tipo
        self.fecha = fecha
        self.empresa = empresa
        self.empleado = empleado
        self.comentario = comentario

    def get_id(self):
        return self.id
    def set_id(self,valor):
        self.id=valor

    def get_tipo(self):
        return self.tipo
    def set_tipo(self,valor):
        self.tipo=valor

    def get_fecha(self):
        return self.fecha
    def set_fecha(self,valor):
        self.fecha=valor

    def get_empresa(self):
        return self.empresa
    def set_empresa(self,valor):
        self.empresa=valor

    def get_empleado(self):
        return self.empleado
    def set_empleado(self,valor):
        self.empleado=valor
    def get_empleado_nombre(self):
        return self.empleado.get_nombre() if self.empleado else "Anónimo"

    def get_comentario(self):
        return self.comentario
    def set_comentario(self,valor):
        self.comentario=valor

    def __str__(self):
        return "id {} - tipo {} - empresa {} - empleado {} - /{}/ - comentario {} ".format(self.id, self.tipo, self.empresa.get_nombre(), self.get_empleado_nombre(), self.fecha, self.comentario)


class ModuloSugerencia:
    @staticmethod
    def insertar(sugerencia):
        """
        si ya existe el registro lo actualiza sino lo inserta a la bd 
        """
        if sugerencia.get_empleado():
            sql_insert = "INSERT INTO sugerencia(idTipoSugerencia,fecha,idempleado,comentario) values(%s,%s,%s,%s);"
            args = (sugerencia.get_tipo(), sugerencia.get_fecha(), sugerencia.get_empleado().get_id(), sugerencia.get_comentario())
        else:
            sql_insert = "INSERT INTO sugerencia(idTipoSugerencia,fecha,idempresa,comentario) values(%s,%s,%s,%s);"
            args = (sugerencia.get_tipo(), sugerencia.get_fecha(), sugerencia.get_empresa().get_id(), sugerencia.get_comentario())

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_insert,args)
        db.commit()
        dr.close()
        db.close()

    @staticmethod
    def listar():
        nuevaLista = []
        sql_select = "SELECT * FROM sugerencia LEFT JOIN empresa ON sugerencia.idempresa = empresa.id LEFT JOIN empleado ON sugerencia.idempleado = empleado.id LEFT JOIN empresa AS e ON empleado.empresa = e.id;"

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_select)
        result = dr.fetchall()

        #empresa1 = 6
        #empleado = 12
        #empresa2 = 25
        for cnj in result:
            if cnj[3] == None:
                nuevaLista.append(Sugerencia(cnj[0],cnj[1],cnj[2],ModuloEmpresa.Empresa(cnj[25],cnj[26],cnj[27],cnj[28],cnj[29],cnj[30]),ModuloEmpleado.Empleado(cnj[12],cnj[13],cnj[14],cnj[15],cnj[16],cnj[17],cnj[18],cnj[19],cnj[20],cnj[21],cnj[22],cnj[23],cnj[24]),cnj[5]))
            elif cnj[4] == None:
                nuevaLista.append(Sugerencia(cnj[0],cnj[1],cnj[2],ModuloEmpresa.Empresa(cnj[6],cnj[7],cnj[8],cnj[9],cnj[10],cnj[11]),None,cnj[5]))

        dr.close()
        db.close()
        return nuevaLista

    @staticmethod
    def eliminar(id_):
        sql_delete = "DELETE FROM sugerencia WHERE id = {};".format(id_)
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_delete)
        db.commit()
        dr.close()
        db.close()
        return True

class SugerenciaConversor:
    @staticmethod
    def to_dict(sugerencia):
        return { 'id' : sugerencia.get_id(), 'tipo' : sugerencia.get_tipo(), 'fecha' : sugerencia.get_fecha().strftime("%x"), 'idempresa' : sugerencia.get_empresa().get_id(), 'empleado' : sugerencia.get_empleado_nombre(), 'comentario' : sugerencia.get_comentario() }

    @staticmethod
    def from_dict(sugerencia):
        idd = sugerencia['id'] if 'id' in sugerencia else 0
        _empleado = ModuloEmpleado.ModuloEmpleado.buscar(sugerencia['idempleado']) if 'idempleado' in sugerencia else None
        _empresa = ModuloEmpresa.ModuloEmpresa.buscar(sugerencia['idempresa'])
        return Sugerencia(idd, sugerencia['tipo'], sugerencia['fecha'], _empresa, _empleado, sugerencia['comentario'])

    @staticmethod
    def list_to_dict(listt):
        return list(map(SugerenciaConversor.to_dict, listt))