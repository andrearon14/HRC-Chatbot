# ###
# creado por adrian
#
#
# ###

import mysql.connector
from config import CFG_MYSQL


class Licencia:
    def __init__(self,id,idEmpleado,fecha_comienzo,fecha_final,confirmada,razon_rechazada):
        self.id = id
        self.idempleado = idEmpleado
        self.fecha_comienzo = fecha_comienzo
        self.fecha_final = fecha_final
        self.confirmada = confirmada
        self.razon_rechazada = razon_rechazada
    
    def get_id(self):
        return self.id
    def set_id(self,valor):
        self.id = valor

    def get_idempleado(self):
        return self.idempleado
    def set_idempleado(self,valor):
        self.idempleado = valor

    def get_fecha_comienzo(self):
        return self.fecha_comienzo
    def set_fecha_comienzo(self,valor):
        self.fecha_comienzo = valor

    def set_fecha_final(self,valor):
        self.fecha_final = valor
    def get_fecha_final(self):
        return self.fecha_final

    def set_confirmada(self,valor):
        self.confirmada = valor
    def get_confirmada(self):
        return self.confirmada

    def set_razon_rechazada(self,valor):
        self.razon_rechazada = valor
    def get_razon_rechazada(self):
        return self.razon_rechazada

    def __str__(self):
        return ("id: {} nro: {}, de {} hasta {}").format(int(self.id),int(self.idempleado),self.fecha_comienzo.strftime("%D"),self.fecha_final.strftime("%D"))


class ModuloLicencia:
    @staticmethod   
    def buscar(id_):
        sql_select ="SELECT * FROM licencia WHERE id = {}".format(id_)
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_select)
        result = dr.fetchall()

        licencia = None
        for cnj in result:
            licencia = Licencia(cnj[0],cnj[1],cnj[2],cnj[3],cnj[4],cnj[5])

        dr.close()
        db.close()
        return licencia

    @staticmethod
    def insertar(idempleado,fecha_comienzo,fecha_final,confirmada):
        sql_insert = "INSERT INTO licencia (idempleado,fechaComienzo,fechaFinal,confirmada) VALUES(%s,%s,%s,%s);"
        args =(idempleado,fecha_comienzo,fecha_final,confirmada)
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_insert, args)
        db.commit()
        dr.close()
        db.close()

    @staticmethod
    def modificar(licencia):
        fecha_comienzo = licencia.get_fecha_comienzo()
        fecha_final = licencia.get_fecha_final()
        confirmada = licencia.get_confirmada()
        razon_rechazada = licencia.get_razon_rechazada()
        id_ = licencia.get_id()

        sql_update = "UPDATE licencia SET fechaComienzo = %s,fechaFinal = %s,confirmada = %s,razonRechazada = %s WHERE `id` = {};".format(id_)
        args = (fecha_comienzo,fecha_final,confirmada,razon_rechazada)

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_update, args)
        db.commit()

        dr.close()
        db.close()
        return True

    @staticmethod
    def eliminar(id_):
        sql_delete = "DELETE FROM licencia where id = {} ;".format(id_)
        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_delete)
        db.commit()
        dr.close()
        db.close()
        return True

    @staticmethod
    def listar():
        sql_select = "SELECT * FROM licencia;"

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_select)
        result = dr.fetchall()

        lista = []
        for cnj in result:
            lista.append(Licencia(cnj[0],cnj[1],cnj[2],cnj[3],cnj[4],cnj[5]))

        dr.close()
        db.close()
        return lista

    @staticmethod
    def listar_actual_por_empleado(idempleado):
        sql_select = "SELECT * FROM licencia WHERE idempleado = {} AND fechaFinal >= CURDATE()".format(idempleado)

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_select)
        result = dr.fetchall()
        
        lista = []
        for cnj in result:
            lista.append(Licencia(cnj[0],cnj[1],cnj[2],cnj[3],cnj[4],cnj[5]))

        dr.close()
        db.close()
        return lista

    @staticmethod
    def listar_actual_confirmada():
        sql_select = "SELECT * FROM licencia WHERE confirmada = 1 AND fechaFinal >= CURDATE()"

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_select)
        result = dr.fetchall()

        lista = []
        for cnj in result:
            lista.append(Licencia(cnj[0],cnj[1],cnj[2],cnj[3],cnj[4],cnj[5]))

        dr.close()
        db.close()
        return lista

    @staticmethod
    def listar_actual_solicitadas():
        sql_select = "SELECT * FROM licencia WHERE confirmada = 0 AND razonRechazada IS NULL AND fechaFinal >= CURDATE()"

        db = mysql.connector.connect(**CFG_MYSQL)
        dr = db.cursor()
        dr.execute(sql_select)
        result = dr.fetchall()

        lista = []
        for cnj in result:
            lista.append(Licencia(cnj[0],cnj[1],cnj[2],cnj[3],cnj[4],cnj[5]))

        dr.close()
        db.close()
        return lista

    @staticmethod
    def listar_por_empresa(idempresa):
        pass
        # aca tengo duda de como hacer la consulta
