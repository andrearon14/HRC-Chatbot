# ###
# creado por adrian
#
#
# ###

import mysql.connector
from config import CFG_MYSQL


class TipoSugerencia:
    def __init__(self,idd,texto):
        self.id = idd
        self.texto = texto

    def set_id(self,valor):
        self.id=valor
    def get_id(self):
        return self.id

    def set_texto(self,valor):
        self.texto=valor
    def get_texto(self):
        return self.texto
    
    def __str__(self):
        return (" Id : {} - {} ").format(self.get_id(),self.get_texto())


class ModuloTipoSugerencia:
    @staticmethod
    def existe_id(id_):
        sql_select = "SELECT * FROM tiposugerencia WHERE id = '{}';".format(id_)
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_select)
        result = dr.fetchall()
        existe = len(result) > 0
        dr.close()
        db.close()
        return existe

    @staticmethod
    def insertar(id_, texto):
        """
        si ya existe el registro lo actualiza sino lo inserta a la BD
        """
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        if ModuloTipoSugerencia.existe_id(id_):
            sql_update = "UPDATE tiposugerencia SET text = '{}' WHERE id = '{}';".format(texto,id_)
            dr.execute(sql_update)
        else:
            sql_insert = "INSERT INTO tiposugerencia(id,text) VALUES(%s,%s);"
            args = (id_,texto)
            dr.execute(sql_insert, args)
        db.commit()
        dr.close()
        db.close()

    @staticmethod
    def listar():
        nuevaLista = []
        sql_select = "SELECT * FROM tiposugerencia;"

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_select)
        result = dr.fetchall()

        for cnj in result:
            nuevaLista.append(TipoSugerencia(cnj[0], cnj[1]))

        dr.close()
        db.close()
        return nuevaLista

    @staticmethod
    def eliminar(id_):
        sql_delete="DELETE FROM tiposugerencia WHERE id = '{}';".format(id_)
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_delete)
        db.commit()
        dr.close()
        db.close()
        return True


class TipoSugerenciaConversor:
    @staticmethod
    def to_dict(tipo):
        return { 'id' : tipo.get_id(), 'texto' : tipo.get_texto() }

    @staticmethod
    def from_dict(tipo):
        return TipoSugerencia(tipo['id'], tipo['texto'])

    @staticmethod
    def list_to_dict(listt):
        return list(map(TipoSugerenciaConversor.to_dict, listt))