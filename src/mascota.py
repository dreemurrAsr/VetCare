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
    
    def __str__(self):
        return f"{self.nombre} ({self.especie} - {self.raza}), {self.edad} años"