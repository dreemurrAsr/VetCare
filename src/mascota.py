from db_connection import get_conn

class Mascota:
    def __init__(self, id_, idDueno, nombre, especie, raza, edad, sexo, fechaUltimaVacuna=None):
        self.id = id_
        self.idDueno = idDueno
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.edad = edad
        self.sexo = sexo
        self.fechaUltimaVacuna = fechaUltimaVacuna
    
    @classmethod
    def crear(cls, idDueno, nombre, especie, raza, edad, sexo, fechaUltimaVacuna=None):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO mascotas (idDueno, nombre, especie, raza, edad, sexo, fechaUltimaVacuna) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (idDueno, nombre, especie, raza, edad, sexo, fechaUltimaVacuna)
            )
            conn.commit()
            mid = cur.lastrowid
            return cls(mid, idDueno, nombre, especie, raza, edad, sexo, fechaUltimaVacuna)
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def listar_todas(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, idDueno, nombre, especie, raza, edad, sexo, fechaUltimaVacuna FROM mascotas ORDER BY nombre")
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_id(cls, id_):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, idDueno, nombre, especie, raza, edad, sexo, fechaUltimaVacuna FROM mascotas WHERE id = %s", (id_,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]) if r else None
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_dueno(cls, idDueno):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, idDueno, nombre, especie, raza, edad, sexo, fechaUltimaVacuna FROM mascotas WHERE idDueno = %s ORDER BY nombre", (idDueno,))
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def eliminar(cls, id_):
        """Elimina una mascota por ID (DELETE)"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM mascotas WHERE id = %s", (id_,))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
    
    def actualizar(self, nombre=None, especie=None, raza=None, edad=None, sexo=None):
        """Actualiza los datos de la mascota (UPDATE)"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            
            # Actualizar solo los campos proporcionados
            if nombre:
                self.nombre = nombre
            if especie:
                self.especie = especie
            if raza:
                self.raza = raza
            if edad is not None:
                self.edad = edad
            if sexo:
                self.sexo = sexo
            
            cur.execute(
                "UPDATE mascotas SET nombre=%s, especie=%s, raza=%s, edad=%s, sexo=%s WHERE id=%s",
                (self.nombre, self.especie, self.raza, self.edad, self.sexo, self.id)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
    
    def actualizar_vacunas(self, fecha_vacuna):
        """Actualiza la fecha de última vacuna"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("UPDATE mascotas SET fechaUltimaVacuna = %s WHERE id = %s", (fecha_vacuna, self.id))
            conn.commit()
            self.fechaUltimaVacuna = fecha_vacuna
            return True
        finally:
            cur.close()
            conn.close()
    
    def obtener_historial(self):
        """Obtiene el historial médico de esta mascota"""
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, idMascota, idVeterinario, fecha, diagnostico, tratamiento, observaciones FROM historial_medico WHERE idMascota = %s ORDER BY fecha DESC",
                (self.id,)
            )
            rows = cur.fetchall()
            historial = []
            for r in rows:
                historial.append({
                    'id': r[0],
                    'idMascota': r[1],
                    'idVeterinario': r[2],
                    'fecha': r[3],
                    'diagnostico': r[4],
                    'tratamiento': r[5],
                    'observaciones': r[6]
                })
            return historial
        finally:
            cur.close()
            conn.close()
    
    def __str__(self):
        return f"{self.nombre} ({self.especie} - {self.raza}), {self.edad} años"