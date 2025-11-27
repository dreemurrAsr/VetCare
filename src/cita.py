from db_connection import get_conn

class Cita:
    def __init__(self, id_, idMascota, idVeterinario, fecha, hora, motivo, estado='pendiente'):
        self.id = id_
        self.idMascota = idMascota
        self.idVeterinario = idVeterinario
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo
        self.estado = estado
    
    @classmethod
    def crear(cls, idMascota, idVeterinario, fecha, hora, motivo=None, estado='pendiente'):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO citas (idMascota, idVeterinario, fecha, hora, motivo, estado) VALUES (%s, %s, %s, %s, %s, %s)",
                (idMascota, idVeterinario, fecha, hora, motivo, estado)
            )
            conn.commit()
            cid = cur.lastrowid
            return cls(cid, idMascota, idVeterinario, fecha, hora, motivo, estado)
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def listar_todas(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, idMascota, idVeterinario, fecha, hora, motivo, estado FROM citas ORDER BY fecha DESC, hora DESC")
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_id(cls, id_):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, idMascota, idVeterinario, fecha, hora, motivo, estado FROM citas WHERE id = %s", (id_,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) if r else None
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def obtener_por_veterinario(cls, idVeterinario):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, idMascota, idVeterinario, fecha, hora, motivo, estado FROM citas WHERE idVeterinario = %s ORDER BY fecha DESC, hora DESC", (idVeterinario,))
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def obtener_por_mascota(cls, idMascota):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, idMascota, idVeterinario, fecha, hora, motivo, estado FROM citas WHERE idMascota = %s ORDER BY fecha DESC, hora DESC", (idMascota,))
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def obtener_por_dueno(cls, idDueno):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                """SELECT c.id, c.idMascota, c.idVeterinario, c.fecha, c.hora, c.motivo, c.estado 
                   FROM citas c
                   JOIN mascotas m ON c.idMascota = m.id
                   WHERE m.idDueno = %s 
                   ORDER BY c.fecha DESC, c.hora DESC""",
                (idDueno,)
            )
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4], r[5], r[6]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    def actualizar_estado(self, nuevo_estado):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("UPDATE citas SET estado = %s WHERE id = %s", (nuevo_estado, self.id))
            conn.commit()
            self.estado = nuevo_estado
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
    
    def confirmar(self):
        return self.actualizar_estado('confirmada')
    
    def cancelar(self):
        return self.actualizar_estado('cancelada')
    
    def completar(self):
        return self.actualizar_estado('completada')
    
    def __str__(self):
        return f"Cita #{self.id} - {self.fecha} {self.hora} - Estado: {self.estado}"