from db_connection import create_connection, close_connection

def create_table_usuarios(conn):
    query = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(100) NOT NULL,
            correo VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255),
            tipoUsuario ENUM('dueno', 'veterinario', 'admin') NOT NULL,
            direccion VARCHAR(200),
            telefono VARCHAR(20),
            especialidad VARCHAR(100),
            anosExperiencia INT,
            horario VARCHAR(100),
            role VARCHAR(50) DEFAULT 'dueno',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    print("Table 'usuarios' created.")
    cursor.close()


def create_table_mascotas(conn):
    query = """
        CREATE TABLE IF NOT EXISTS mascotas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            idDueno INT NOT NULL,
            nombre VARCHAR(100) NOT NULL,
            especie VARCHAR(50) NOT NULL,
            raza VARCHAR(100),
            edad INT,
            sexo ENUM('macho', 'hembra') NOT NULL,
            fechaUltimaVacuna DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (idDueno) REFERENCES usuarios(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    print("Table 'mascotas' created.")
    cursor.close()


def create_table_citas(conn):
    query = """
        CREATE TABLE IF NOT EXISTS citas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            idMascota INT NOT NULL,
            idVeterinario INT NOT NULL,
            fecha DATE NOT NULL,
            hora TIME NOT NULL,
            motivo TEXT,
            estado ENUM('pendiente', 'confirmada', 'cancelada', 'completada') 
                DEFAULT 'pendiente',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (idMascota) REFERENCES mascotas(id) ON DELETE CASCADE,
            FOREIGN KEY (idVeterinario) REFERENCES usuarios(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    print("Table 'citas' created.")
    cursor.close()


def create_table_historial(conn):
    query = """
        CREATE TABLE IF NOT EXISTS historial_medico (
            id INT AUTO_INCREMENT PRIMARY KEY,
            idMascota INT NOT NULL,
            idVeterinario INT NOT NULL,
            fecha DATE NOT NULL,
            diagnostico TEXT,
            tratamiento TEXT,
            observaciones TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (idMascota) REFERENCES mascotas(id) ON DELETE CASCADE,
            FOREIGN KEY (idVeterinario) REFERENCES usuarios(id) ON DELETE CASCADE
        ) ENGINE=InnoDB;
    """
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    print("Table 'historial_medico' created.")
    cursor.close()



def main():
    conn = create_connection()
    if conn:
        # Crear tablas
        create_table_usuarios(conn)
        create_table_mascotas(conn)
        create_table_citas(conn)
        create_table_historial(conn)
        close_connection(conn)

if __name__ == "__main__":
    main()