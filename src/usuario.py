from db_connection import get_conn
import hashlib

def hash_password(password: str) -> str:
    if password is None:
        return None
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class Usuario:
    def __init__(self, id_, nombre, correo, role='veterinario'):
        self.id = id_
        self.nombre = nombre
        self.correo = correo
        self.role = role
    
    @classmethod
    def crear(cls, nombre, correo, password, role='veterinario'):
        conn = get_conn()
        try:
            cur = conn.cursor()
            pwd_hash = hash_password(password) if password else None
            cur.execute(
                "INSERT INTO usuarios (nombre, correo, password, role) VALUES (%s, %s, %s, %s)",
                (nombre, correo, pwd_hash, role)
            )
            conn.commit()
            uid = cur.lastrowid
            return cls(uid, nombre, correo, role)
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def listar_todos(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, correo, role FROM usuarios ORDER BY nombre")
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_nombre(cls, nombre):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, correo, role FROM usuarios WHERE nombre = %s", (nombre,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3]) if r else None
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def autenticar(cls, correo, password):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, nombre, correo, role, password FROM usuarios WHERE correo = %s",
                (correo,)
            )
            r = cur.fetchone()
            if not r:
                return None
            stored_hash = r[4]
            if stored_hash is None or hash_password(password) != stored_hash:
                return None
            
            # Devolver Dueno o Veterinario según role
            if r[3] == 'dueno':
                return Dueno.buscar_por_id(r[0])
            elif r[3] == 'veterinario':
                return Veterinario.buscar_por_id(r[0])
            else:
                return cls(r[0], r[1], r[2], r[3])
        finally:
            cur.close()
            conn.close()


class Dueno(Usuario):
    def __init__(self, id_, nombre, correo, role, direccion=None, telefono=None):
        super().__init__(id_, nombre, correo, role)
        self.direccion = direccion
        self.telefono = telefono
    
    @classmethod
    def crear(cls, nombre, correo, password, direccion=None, telefono=None):
        conn = get_conn()
        try:
            cur = conn.cursor()
            pwd_hash = hash_password(password) if password else None
            cur.execute(
                "INSERT INTO usuarios (nombre, correo, password, role, direccion, telefono) VALUES (%s, %s, %s, %s, %s, %s)",
                (nombre, correo, pwd_hash, 'dueno', direccion, telefono)
            )
            conn.commit()
            uid = cur.lastrowid
            return cls(uid, nombre, correo, 'dueno', direccion, telefono)
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_id(cls, id_):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, correo, role, direccion, telefono FROM usuarios WHERE id = %s", (id_,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3], r[4], r[5]) if r else None
        finally:
            cur.close()
            conn.close()
    
    def obtener_mascotas(self):
        from mascota import Mascota
        return Mascota.buscar_por_dueno(self.id)


class Veterinario(Usuario):
    def __init__(self, id_, nombre, correo, role, especialidad=None, anosExperiencia=None):
        super().__init__(id_, nombre, correo, role)
        self.especialidad = especialidad
        self.anosExperiencia = anosExperiencia
    
    @classmethod
    def crear(cls, nombre, correo, password, especialidad=None, anosExperiencia=None):
        conn = get_conn()
        try:
            cur = conn.cursor()
            pwd_hash = hash_password(password) if password else None
            cur.execute(
                "INSERT INTO usuarios (nombre, correo, password, role, especialidad, anosExperiencia) VALUES (%s, %s, %s, %s, %s, %s)",
                (nombre, correo, pwd_hash, 'veterinario', especialidad, anosExperiencia)
            )
            conn.commit()
            uid = cur.lastrowid
            return cls(uid, nombre, correo, 'veterinario', especialidad, anosExperiencia)
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def buscar_por_id(cls, id_):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, correo, role, especialidad, anosExperiencia FROM usuarios WHERE id = %s", (id_,))
            r = cur.fetchone()
            return cls(r[0], r[1], r[2], r[3], r[4], r[5]) if r else None
        finally:
            cur.close()
            conn.close()
    
    @classmethod
    def listar_veterinarios(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, correo, role, especialidad, anosExperiencia FROM usuarios WHERE role = 'veterinario' ORDER BY nombre")
            rows = cur.fetchall()
            return [cls(r[0], r[1], r[2], r[3], r[4], r[5]) for r in rows]
        finally:
            cur.close()
            conn.close()
    
    def obtener_citas(self):
        from cita import Cita
        return Cita.obtener_por_veterinario(self.id)