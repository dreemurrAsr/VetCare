import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from usuario import Usuario, Dueno, Veterinario, hash_password

current_user = None  


CODIGO_ADMIN = "ADMIN2025"

# --------------------------
# Funciones de la aplicación
# --------------------------

def login_inicial():
    """Solicita credenciales al iniciar la aplicación.
     registrarse si el usuario no tiene cuenta: dueno, veterinario o admin.
    """
    global current_user

    tiene = messagebox.askyesno("Bienvenido a VetCare", "¿Tienes una cuenta en el sistema?")
    if tiene is None:
        salir()
        return

    if not tiene:
        
        try:
            u = registrar_usuario_publico()
            if u:
                current_user = u
                lbl_help.config(text=f"Usuario conectado: {current_user.nombre} ({current_user.role})")
                ajustar_menu_por_rol()
                
                if current_user.role == 'dueno':
                    mostrar_mis_mascotas()
                else:
                    listar_usuarios()
                return
            else:
                messagebox.showinfo("Info", "Registro cancelado. Se solicitará inicio de sesión.")
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el registro:\n{e}")

    for _ in range(3):
        correo = simpledialog.askstring("Inicio de sesión", "Correo electrónico:")
        if correo is None:
            salir()
            return
        pwd = simpledialog.askstring("Inicio de sesión", "Contraseña:", show='*')
        if pwd is None:
            salir()
            return
        usuario = Usuario.autenticar(correo.strip(), pwd)
        if usuario:
            current_user = usuario
            lbl_help.config(text=f"Usuario conectado: {current_user.nombre} ({current_user.role})")
            ajustar_menu_por_rol()
         
            if current_user.role == 'dueno':
                mostrar_mis_mascotas()
            elif current_user.role == 'veterinario':
                mostrar_mis_citas()
            else:
                listar_usuarios()
            return
        else:
            retry = messagebox.askretrycancel("Error", "Credenciales incorrectas. ¿Deseas intentar de nuevo?")
            if not retry:
                
                want_reg = messagebox.askyesno("Registro", "¿Deseas registrarte ahora?")
                if want_reg:
                    try:
                        u = registrar_usuario_publico()
                        if u:
                            current_user = u
                            lbl_help.config(text=f"Usuario conectado: {current_user.nombre} ({current_user.role})")
                            ajustar_menu_por_rol()
                            if current_user.role == 'dueno':
                                mostrar_mis_mascotas()
                            elif current_user.role == 'veterinario':
                                mostrar_mis_citas()
                            else:
                                listar_usuarios()
                            return
                    except Exception as e:
                        messagebox.showerror("Error", f"Error durante el registro:\n{e}")
                # si no se registra, seguir al siguiente intento (o salir si no quedan intentos)
    messagebox.showerror("Error", "Demasiados intentos fallidos. Saliendo.")
    salir()


def requiere_admin(func):
    """Decorador simple para funciones que requieren rol 'admin'."""
    def wrapper(*args, **kwargs):
        if current_user is None or current_user.role != 'admin':
            messagebox.showerror("Permisos", "Acción restringida: se requiere usuario admin.")
            return
        return func(*args, **kwargs)
    return wrapper



def registrar_usuario_publico():
    """Permite registrar un usuario desde la pantalla de inicio (roles: dueno, veterinario, admin).
    Si se selecciona admin, se solicita un código adicional.
    """
    nombre = simpledialog.askstring("Registrar usuario", "Nombre completo:")
    if not nombre:
        return None
    
    correo = simpledialog.askstring("Registrar usuario", "Correo electrónico:")
    if not correo:
        return None
    
    role = simpledialog.askstring("Registrar usuario", "Rol (dueno/veterinario/admin):", initialvalue="dueno")
    if role is None:
        return None
    role = role.strip().lower()
    if role not in ('dueno', 'veterinario', 'admin'):
        messagebox.showwarning("Rol inválido", "Rol inválido. Se usará 'dueno'.")
        role = 'dueno'
    
    
    if role == 'admin':
        codigo = simpledialog.askstring("Código Admin", "Ingrese el código de administrador:", show='*')
        if codigo != CODIGO_ADMIN:
            messagebox.showerror("Código incorrecto", "El código de administrador es incorrecto. No se puede crear la cuenta.")
            return None
    
    pwd = simpledialog.askstring("Registrar usuario", "Contraseña:", show='*')
    if not pwd:
        messagebox.showwarning("Contraseña requerida", "La contraseña es obligatoria.")
        return None
    
    
    try:
        if role == 'dueno':
            direccion = simpledialog.askstring("Datos del dueño", "Dirección:")
            telefono = simpledialog.askstring("Datos del dueño", "Teléfono:")
            u = Dueno.crear(nombre.strip(), correo.strip(), pwd, direccion, telefono)
        elif role == 'veterinario':
            especialidad = simpledialog.askstring("Datos del veterinario", "Especialidad:")
            anos = simpledialog.askinteger("Datos del veterinario", "Años de experiencia:", minvalue=0)
            u = Veterinario.crear(nombre.strip(), correo.strip(), pwd, especialidad, anos)
        else:  
            u = Usuario.crear(nombre.strip(), correo.strip(), pwd, 'admin')
        
        messagebox.showinfo("OK", f"Usuario registrado: {u.nombre} (role={u.role})")
        return u
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar usuario:\n{e}")
        return None




@requiere_admin
def registrar_usuario():
    nombre = simpledialog.askstring("Registrar usuario", "Nombre completo:")
    if not nombre:
        return
    
    correo = simpledialog.askstring("Registrar usuario", "Correo electrónico:")
    if not correo:
        return
    
    role = simpledialog.askstring("Registrar usuario", "Rol (dueno/veterinario/admin):", initialvalue="dueno")
    
    if role and role.strip().lower() == 'admin':
        codigo = simpledialog.askstring("Código Admin", "Ingrese el código de administrador:", show='*')
        if codigo != CODIGO_ADMIN:
            messagebox.showerror("Código incorrecto", "El código de administrador es incorrecto. No se puede crear la cuenta admin.")
            return
    
    pwd = simpledialog.askstring("Registrar usuario", "Contraseña:", show='*')
    
    try:
        role = role.strip().lower() if role else 'dueno'
        
        if role == 'dueno':
            direccion = simpledialog.askstring("Datos del dueño", "Dirección:")
            telefono = simpledialog.askstring("Datos del dueño", "Teléfono:")
            u = Dueno.crear(nombre.strip(), correo.strip(), pwd, direccion, telefono)
        elif role == 'veterinario':
            especialidad = simpledialog.askstring("Datos del veterinario", "Especialidad:")
            anos = simpledialog.askinteger("Datos del veterinario", "Años de experiencia:", minvalue=0)
            u = Veterinario.crear(nombre.strip(), correo.strip(), pwd, especialidad, anos)
        else:
            u = Usuario.crear(nombre.strip(), correo.strip(), pwd, 'admin')
        
        messagebox.showinfo("OK", f"Usuario registrado: {u.nombre} (id={u.id})")
        listar_usuarios()
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar usuario:\n{e}")


@requiere_admin
def eliminar_usuario():
    nombre = simpledialog.askstring("Eliminar usuario", "Nombre del usuario a eliminar:")
    if not nombre:
        return
    usr = Usuario.buscar_por_nombre(nombre.strip())
    if usr is None:
        messagebox.showwarning("No encontrado", "Usuario no encontrado.")
        return
    if messagebox.askyesno("Confirmar", f"¿Eliminar al usuario '{usr.nombre}' (id={usr.id})?"):
        try:
            conn = __import__('db_connection').get_conn()
            cur = conn.cursor()
            cur.execute("DELETE FROM usuarios WHERE id = %s", (usr.id,))
            conn.commit()
            cur.close()
            conn.close()
            messagebox.showinfo("OK", "Usuario eliminado.")
            listar_usuarios()
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar usuario:\n{e}")


def registrar_mascota():
    """Permite al dueño registrar una mascota"""
    if current_user is None or current_user.role != 'dueno':
        messagebox.showerror("Permisos", "Solo los dueños pueden registrar mascotas.")
        return
    
    from mascota import Mascota
    
    nombre = simpledialog.askstring("Registrar mascota", "Nombre de la mascota:")
    if not nombre:
        return
    
    especie = simpledialog.askstring("Registrar mascota", "Especie (perro/gato/ave/etc.):")
    if not especie:
        return
    
    raza = simpledialog.askstring("Registrar mascota", "Raza:")
    edad = simpledialog.askinteger("Registrar mascota", "Edad (años):", minvalue=0)
    
    sexo = simpledialog.askstring("Registrar mascota", "Sexo (macho/hembra):", initialvalue="macho")
    if sexo not in ('macho', 'hembra'):
        sexo = 'macho'
    
    try:
        m = Mascota.crear(current_user.id, nombre.strip(), especie.strip(), raza, edad, sexo)
        messagebox.showinfo("OK", f"Mascota registrada: {m.nombre} (id={m.id})")
        mostrar_mis_mascotas()
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar mascota:\n{e}")


def mostrar_mis_mascotas():
    """Muestra las mascotas del dueño actual"""
    if current_user is None or current_user.role != 'dueno':
        return
    
    try:
        mascotas = current_user.obtener_mascotas()
        lb_output.delete(0, tk.END)
        lb_output.insert(tk.END, f"Mis mascotas ({current_user.nombre}):")
        if not mascotas:
            lb_output.insert(tk.END, "  (No tienes mascotas registradas)")
            return
        for m in mascotas:
            lb_output.insert(tk.END, f"  [{m.id}] {m.nombre} - {m.especie} ({m.raza}), {m.edad} años")
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener mascotas:\n{e}")


def agendar_cita():
    """Permite al dueño agendar una cita para su mascota"""
    if current_user is None or current_user.role != 'dueno':
        messagebox.showerror("Permisos", "Solo los dueños pueden agendar citas.")
        return
    
    from cita import Cita
    from mascota import Mascota
    

    mascotas = current_user.obtener_mascotas()
    if not mascotas:
        messagebox.showwarning("Sin mascotas", "Primero debes registrar una mascota.")
        return
    

    nombres_mascotas = [f"{m.id} - {m.nombre}" for m in mascotas]
    mascota_selec = simpledialog.askstring("Agendar cita", 
                                           f"Mascotas disponibles:\n" + "\n".join(nombres_mascotas) + 
                                           "\n\nIngresa el ID de la mascota:")
    if not mascota_selec:
        return
    
    try:
        id_mascota = int(mascota_selec)
    except:
        messagebox.showerror("Error", "ID inválido.")
        return
    
    veterinarios = Veterinario.listar_veterinarios()
    if not veterinarios:
        messagebox.showwarning("Sin veterinarios", "No hay veterinarios disponibles.")
        return
    
    nombres_vets = [f"{v.id} - Dr. {v.nombre} ({v.especialidad})" for v in veterinarios]
    vet_selec = simpledialog.askstring("Seleccionar veterinario",
                                      f"Veterinarios disponibles:\n" + "\n".join(nombres_vets) +
                                      "\n\nIngresa el ID del veterinario:")
    if not vet_selec:
        return
    
    try:
        id_vet = int(vet_selec)
    except:
        messagebox.showerror("Error", "ID inválido.")
        return
    
    
    fecha = simpledialog.askstring("Agendar cita", "Fecha (YYYY-MM-DD):")
    if not fecha:
        return
    
    hora = simpledialog.askstring("Agendar cita", "Hora (HH:MM):")
    if not hora:
        return
    
    motivo = simpledialog.askstring("Agendar cita", "Motivo de la consulta:")
    
    try:
        cita = Cita.crear(id_mascota, id_vet, fecha, hora, motivo)
        messagebox.showinfo("OK", f"Cita agendada para {fecha} a las {hora}")
        mostrar_mis_citas()
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except Exception as e:
        messagebox.showerror("Error", f"Error al agendar cita:\n{e}")


def mostrar_mis_citas():
    """Muestra las citas del usuario actual (veterinario o dueño)"""
    if current_user is None:
        return
    
    from cita import Cita
    
    try:
        if current_user.role == 'veterinario':
            citas = current_user.obtener_citas()
            titulo = f"Citas asignadas (Dr. {current_user.nombre}):"
        elif current_user.role == 'dueno':
            citas = Cita.obtener_por_dueno(current_user.id)
            titulo = f"Mis citas ({current_user.nombre}):"
        else:
            return
        
        lb_output.delete(0, tk.END)
        lb_output.insert(tk.END, titulo)
        if not citas:
            lb_output.insert(tk.END, "  (No hay citas)")
            return
        for c in citas:
            lb_output.insert(tk.END, f"  [{c.id}] {c.fecha} {c.hora} - {c.estado}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener citas:\n{e}")


def completar_cita():
    """Permite al veterinario completar una cita y registrar diagnóstico"""
    if current_user is None or current_user.role != 'veterinario':
        messagebox.showerror("Permisos", "Solo los veterinarios pueden completar citas.")
        return
    
    from cita import Cita
    
    
    id_cita = simpledialog.askinteger("Completar cita", "Ingresa el ID de la cita:")
    if not id_cita:
        return
    
    
    cita = Cita.buscar_por_id(id_cita)
    if not cita:
        messagebox.showerror("Error", "Cita no encontrada.")
        return
    
    if cita.idVeterinario != current_user.id:
        messagebox.showerror("Error", "Esta cita no está asignada a ti.")
        return
    
    if cita.estado not in ('pendiente', 'confirmada'):
        messagebox.showerror("Error", f"Esta cita ya está en estado: {cita.estado}")
        return

    diagnostico = simpledialog.askstring("Diagnóstico", "Ingresa el diagnóstico:")
    if not diagnostico:
        return
    
    tratamiento = simpledialog.askstring("Tratamiento", "Ingresa el tratamiento:")
    if not tratamiento:
        return
    
    observaciones = simpledialog.askstring("Observaciones", "Observaciones adicionales (opcional):")
    
    try:
        cita.completar(diagnostico, tratamiento, observaciones)
        messagebox.showinfo("OK", "Cita completada y registrada en historial médico.")
        mostrar_mis_citas()
    except Exception as e:
        messagebox.showerror("Error", f"Error al completar cita:\n{e}")


def ver_historial_mascota():
    """Permite ver el historial médico de una mascota"""
    if current_user is None:
        messagebox.showerror("Permisos", "Debe iniciar sesión.")
        return
    
    from mascota import Mascota
    
    id_mascota = simpledialog.askinteger("Ver historial", "Ingresa el ID de la mascota:")
    if not id_mascota:
        return
    
    try:
        mascota = Mascota.buscar_por_id(id_mascota)
        if not mascota:
            messagebox.showerror("Error", "Mascota no encontrada.")
            return
        
        if current_user.role == 'dueno' and mascota.idDueno != current_user.id:
            messagebox.showerror("Permisos", "No puedes ver el historial de esta mascota.")
            return
        
        historial = mascota.obtener_historial()
        
        lb_output.delete(0, tk.END)
        lb_output.insert(tk.END, f"Historial Médico de {mascota.nombre}:")
        if not historial:
            lb_output.insert(tk.END, "  (Sin historial médico)")
            return
        
        for h in historial:
            lb_output.insert(tk.END, f"\n  Fecha: {h['fecha']}")
            lb_output.insert(tk.END, f"  Diagnóstico: {h['diagnostico']}")
            lb_output.insert(tk.END, f"  Tratamiento: {h['tratamiento']}")
            if h['observaciones']:
                lb_output.insert(tk.END, f"  Observaciones: {h['observaciones']}")
            lb_output.insert(tk.END, "  " + "-"*50)
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener historial:\n{e}")




def listar_usuarios():
    try:
        usuarios = Usuario.listar_todos()
        lb_output.delete(0, tk.END)
        if not usuarios:
            lb_output.insert(tk.END, "No hay usuarios registrados.")
            return
        lb_output.insert(tk.END, "Usuarios:")
        for u in usuarios:
            lb_output.insert(tk.END, f"  [{u.id}] {u.nombre} – {u.role}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar usuarios:\n{e}")


def listar_mascotas():
    """Lista todas las mascotas del sistema (admin/veterinario)"""
    if current_user is None or current_user.role == 'dueno':
        messagebox.showerror("Permisos", "Acción no permitida.")
        return
    
    from mascota import Mascota
    
    try:
        mascotas = Mascota.listar_todas()
        lb_output.delete(0, tk.END)
        if not mascotas:
            lb_output.insert(tk.END, "No hay mascotas registradas.")
            return
        lb_output.insert(tk.END, "Mascotas:")
        for m in mascotas:
            lb_output.insert(tk.END, f"  [{m.id}] {m.nombre} - {m.especie} (Dueño ID: {m.idDueno})")
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar mascotas:\n{e}")

def eliminar_mascota():
    """Permite al dueño o admin eliminar una mascota"""
    if current_user is None:
        messagebox.showerror("Permisos", "Debe iniciar sesión.")
        return
    
    from mascota import Mascota
    
    id_mascota = simpledialog.askinteger("Eliminar mascota", "Ingresa el ID de la mascota:")
    if not id_mascota:
        return
    
    try:
        mascota = Mascota.buscar_por_id(id_mascota)
        if not mascota:
            messagebox.showerror("Error", "Mascota no encontrada.")
            return
        
        
        if current_user.role == 'dueno' and mascota.idDueno != current_user.id:
            messagebox.showerror("Permisos", "No puedes eliminar esta mascota.")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar a {mascota.nombre}?"):
            Mascota.eliminar(id_mascota)
            messagebox.showinfo("OK", "Mascota eliminada.")
            if current_user.role == 'dueno':
                mostrar_mis_mascotas()
            else:
                listar_mascotas()
    except Exception as e:
        messagebox.showerror("Error", f"Error al eliminar mascota:\n{e}")

def listar_citas():
    """Lista todas las citas del sistema (admin/veterinario)"""
    if current_user is None or current_user.role == 'dueno':
        messagebox.showerror("Permisos", "Acción no permitida.")
        return
    
    from cita import Cita
    
    try:
        citas = Cita.listar_todas()
        lb_output.delete(0, tk.END)
        if not citas:
            lb_output.insert(tk.END, "No hay citas registradas.")
            return
        lb_output.insert(tk.END, "Citas:")
        for c in citas:
            lb_output.insert(tk.END, f"  [{c.id}] {c.fecha} {c.hora} - Estado: {c.estado}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al listar citas:\n{e}")


def salir():
    root.destroy()
    sys.exit(0)


def ajustar_menu_por_rol():
    """Habilita/deshabilita opciones del menú según el rol del usuario actual."""
    if current_user is None:
        
        for i in range(acciones_menu.index(tk.END) + 1):
            try:
                acciones_menu.entryconfig(i, state="disabled")
            except:
                pass
        return

    if current_user.role == 'admin':
    
        acciones_menu.entryconfig("Registrar usuario", state="normal")
        acciones_menu.entryconfig("Eliminar usuario", state="normal")
        acciones_menu.entryconfig("Listar usuarios", state="normal")
        acciones_menu.entryconfig("Listar mascotas", state="normal")
        acciones_menu.entryconfig("Listar citas", state="normal")
        acciones_menu.entryconfig("Registrar mascota", state="disabled")
        acciones_menu.entryconfig("Agendar cita", state="disabled")
        acciones_menu.entryconfig("Mis mascotas", state="disabled")
        acciones_menu.entryconfig("Mis citas", state="disabled")
        acciones_menu.entryconfig("Eliminar mascota", state="normal")
        
        
    elif current_user.role == 'veterinario':
        
        acciones_menu.entryconfig("Registrar usuario", state="disabled")
        acciones_menu.entryconfig("Eliminar usuario", state="disabled")
        acciones_menu.entryconfig("Listar usuarios", state="normal")
        acciones_menu.entryconfig("Listar mascotas", state="normal")
        acciones_menu.entryconfig("Listar citas", state="normal")
        acciones_menu.entryconfig("Registrar mascota", state="disabled")
        acciones_menu.entryconfig("Agendar cita", state="disabled")
        acciones_menu.entryconfig("Mis mascotas", state="disabled")
        acciones_menu.entryconfig("Mis citas", state="normal")
        acciones_menu.entryconfig("Eliminar mascota", state="disabled")
        
    else:  
      
        acciones_menu.entryconfig("Registrar usuario", state="disabled")
        acciones_menu.entryconfig("Eliminar usuario", state="disabled")
        acciones_menu.entryconfig("Listar usuarios", state="disabled")
        acciones_menu.entryconfig("Listar mascotas", state="disabled")
        acciones_menu.entryconfig("Listar citas", state="disabled")
        acciones_menu.entryconfig("Registrar mascota", state="normal")
        acciones_menu.entryconfig("Agendar cita", state="normal")
        acciones_menu.entryconfig("Mis mascotas", state="normal")
        acciones_menu.entryconfig("Mis citas", state="normal")
        acciones_menu.entryconfig("Eliminar mascota", state="normal")


# ==================== INTERFAZ GRÁFICA ====================

root = tk.Tk()
root.title("VetCare - Sistema de Gestión Veterinaria")
root.geometry("800x480")
root.minsize(700, 420)

# Menú principal
menubar = tk.Menu(root)

# Menú "Acciones" con las opciones
acciones_menu = tk.Menu(menubar, tearoff=0)
acciones_menu.add_command(label="Registrar usuario", command=registrar_usuario)
acciones_menu.add_command(label="Eliminar usuario", command=eliminar_usuario)
acciones_menu.add_command(label="Eliminar mascota", command=eliminar_mascota)
acciones_menu.add_separator()
acciones_menu.add_command(label="Registrar mascota", command=registrar_mascota)
acciones_menu.add_command(label="Agendar cita", command=agendar_cita)
acciones_menu.add_command(label="Completar cita", command=completar_cita)
acciones_menu.add_separator()
acciones_menu.add_command(label="Listar usuarios", command=listar_usuarios)
acciones_menu.add_command(label="Listar mascotas", command=listar_mascotas)
acciones_menu.add_command(label="Listar citas", command=listar_citas)
acciones_menu.add_separator()
acciones_menu.add_command(label="Mis mascotas", command=mostrar_mis_mascotas)
acciones_menu.add_command(label="Mis citas", command=mostrar_mis_citas)
acciones_menu.add_command(label="Ver historial médico", command=ver_historial_mascota)
menubar.add_cascade(label="Acciones", menu=acciones_menu)

# Menú "Archivo" con Salir
archivo_menu = tk.Menu(menubar, tearoff=0)
archivo_menu.add_command(label="Salir", command=salir)
menubar.add_cascade(label="Archivo", menu=archivo_menu)

root.config(menu=menubar)

# Frame principal para salida / resultados
frame_output = ttk.Frame(root, padding=(12, 12))
frame_output.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

lbl_output = ttk.Label(frame_output, text="Sistema VetCare", font=("Segoe UI", 12, "bold"))
lbl_output.pack(anchor="w")


frame_list = ttk.Frame(frame_output)
frame_list.pack(fill=tk.BOTH, expand=True, pady=(6, 0))

sb = ttk.Scrollbar(frame_list, orient=tk.VERTICAL)
lb_output = tk.Listbox(frame_list, yscrollcommand=sb.set, font=("Consolas", 10))
sb.config(command=lb_output.yview)
sb.pack(side=tk.RIGHT, fill=tk.Y)
lb_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


lbl_help = ttk.Label(frame_output, text="Iniciando sistema...", font=("Segoe UI", 9))
lbl_help.pack(anchor="w", pady=(8, 0))


root.after(100, login_inicial)

root.mainloop()