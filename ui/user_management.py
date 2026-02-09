import tkinter as tk
from tkinter import messagebox
import sys
import os

# Agregar el directorio raíz del proyecto al path (método más robusto)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

try:
    from server.database import crear_usuario as db_crear_usuario, obtener_todos_usuarios, inicializar_base_datos
    DATABASE_CONNECTED = inicializar_base_datos()
    print(f"✅ Base de datos conectada en user_management.py: {DATABASE_CONNECTED}")
except ImportError as e:
    DATABASE_CONNECTED = False
    print(f"❌ Error al importar base de datos en user_management.py: {e}")
    print(f"   Directorio actual: {current_dir}")
    print(f"   Directorio raíz: {project_root}")
    def db_crear_usuario(nombre, contrasena, rol):
        print(f"Mock: Creando usuario {nombre} con rol {rol}")
    def obtener_todos_usuarios():
        return []
        return []
# Diccionario para almacenar usuarios localmente (fallback)
usuarios = {}

class UserManager:
    def __init__(self, root):
        self.root = root
    
    def crear_usuario(self):
        def guardar_usuario():
            nombre = nombre_entry.get()
            rol = []
            if padre_var.get():
                rol.append("Padre")
            if docente_var.get():
                rol.append("Docente")
            if preceptor_var.get():
                rol.append("Preceptor")
            if administrador_var.get():
                rol.append("Administrativo")

            contrasena = contrasena_entry.get()
            confirmar_contrasena = confirmar_entry.get()
            email = email_entry.get()

            if nombre and rol and contrasena and confirmar_contrasena == contrasena and email:
                try:
                    if DATABASE_CONNECTED:
                        # Guardar en base de datos (solo un rol por usuario en tu esquema)
                        primer_rol = rol[0] if rol else "Padre"
                        db_crear_usuario(nombre, contrasena, primer_rol)
                    else:
                        # Guardar en diccionario local como fallback
                        usuarios[nombre] = {
                            "contrasena": contrasena,
                            "rol": rol,
                            "email": email
                        }
                    
                    messagebox.showinfo("Usuario Creado", f"Usuario '{nombre}' creado como {', '.join(rol)}.")
                    ventana.destroy()
                except Exception as e:
                    self.mostrar_error(f"No se pudo crear el usuario: {e}")
            else:
                if not nombre:
                    self.mostrar_error("Nombre de usuario no puede estar vacío.")
                elif not rol:
                    self.mostrar_error("Debe seleccionar al menos un rol.")
                elif contrasena != confirmar_contrasena:
                    self.mostrar_error("Las contraseñas no coinciden.")
                elif not email:
                    self.mostrar_error("El correo electrónico no puede estar vacío.")

        def mostrar_error(mensaje):
            self.mostrar_error(mensaje)

        ventana = tk.Toplevel(self.root)
        ventana.title("Crear Usuario")
        ventana.geometry("400x500")
        ventana.configure(bg="#f0f0f0")

        frame_usuario = tk.Frame(ventana, bg="#f0f0f0")
        frame_usuario.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        tk.Label(frame_usuario, text="Ingrese el nombre de usuario:", font=("Arial", 12), bg="#f0f0f0").pack(pady=(10, 0))
        nombre_entry = tk.Entry(frame_usuario, font=("Arial", 14))
        nombre_entry.pack(pady=(0, 10), fill=tk.X)

        tk.Label(frame_usuario, text="Seleccione el rol (puede seleccionar varios):", font=("Arial", 12), bg="#f0f0f0").pack(pady=(10, 0))

        padre_var = tk.BooleanVar()
        docente_var = tk.BooleanVar()
        preceptor_var = tk.BooleanVar()
        administrador_var = tk.BooleanVar()

        roles_frame = tk.Frame(frame_usuario, bg="#f0f0f0")
        roles_frame.pack(pady=(0, 10), fill=tk.X)

        tk.Checkbutton(roles_frame, text="Padre", variable=padre_var, bg="#f0f0f0").pack(anchor='w')
        tk.Checkbutton(roles_frame, text="Docente", variable=docente_var, bg="#f0f0f0").pack(anchor='w')
        tk.Checkbutton(roles_frame, text="Preceptor", variable=preceptor_var, bg="#f0f0f0").pack(anchor='w')
        tk.Checkbutton(roles_frame, text="Administrador", variable=administrador_var, bg="#f0f0f0").pack(anchor='w')

        tk.Label(frame_usuario, text="Ingrese la contraseña:", font=("Arial", 12), bg="#f0f0f0").pack(pady=(10, 0))
        contrasena_entry = tk.Entry(frame_usuario, show='*', font=("Arial", 14))
        contrasena_entry.pack(pady=(0, 10), fill=tk.X)

        tk.Label(frame_usuario, text="Confirme la contraseña:", font=("Arial", 12), bg="#f0f0f0").pack(pady=(10, 0))
        confirmar_entry = tk.Entry(frame_usuario, show='*', font=("Arial", 14))
        confirmar_entry.pack(pady=(0, 10), fill=tk.X)

        tk.Label(frame_usuario, text="Ingrese el correo electrónico:", font=("Arial", 12), bg="#f0f0f0").pack(pady=(10, 0))
        email_entry = tk.Entry(frame_usuario, font=("Arial", 14))
        email_entry.pack(pady=(0, 20), fill=tk.X)

        tk.Button(frame_usuario, text="Guardar", command=guardar_usuario, font=("Arial", 14), 
                 bg="#4caf50", fg="white").pack(pady=10)

    def ver_usuarios(self):
        def mostrar_info(titulo, mensaje):
            info_window = tk.Toplevel(self.root)
            info_window.title(titulo)
            info_window.geometry("400x300")
            info_window.configure(bg="azure4")
            
            info_label = tk.Label(info_window, text=mensaje, font=("Arial", 14), bg="azure4", fg="black")
            info_label.pack(pady=20)
            
            close_button = tk.Button(info_window, text="Cerrar", command=info_window.destroy, 
                                   font=("Arial", 12), bg="forest green", fg="white")
            close_button.pack(pady=10)
        
        # Mostrar usuarios de la base de datos si está conectada
        if DATABASE_CONNECTED:
            usuarios_db = obtener_todos_usuarios()
            if usuarios_db:
                info = "\n".join([f"Usuario: {nombre}, Rol: {rol}, Email: {email}" 
                                 for nombre, rol, email in usuarios_db])
                mostrar_info("Usuarios Registrados (Base de Datos)", info)
            else:
                mostrar_info("Usuarios Registrados", "No hay usuarios en la base de datos.")
        elif usuarios:
            info = "\n".join([f"Usuario: {nombre}, Rol: {', '.join(data['rol'])}, Email: {data['email']}" 
                             for nombre, data in usuarios.items()])
            mostrar_info("Usuarios Registrados (Local)", info)
        else:
            mostrar_info("Usuarios Registrados", "No hay usuarios registrados.")

    def mostrar_error(self, mensaje):
        error_window = tk.Toplevel(self.root)
        error_window.title("Error")
        error_window.geometry("300x150")
        error_window.configure(bg="#ffcccc")

        error_label = tk.Label(error_window, text=mensaje, font=("Arial", 12), bg="#ffcccc", fg="#d8000c")
        error_label.pack(pady=20)

        close_button = tk.Button(error_window, text="Cerrar", command=error_window.destroy, 
                               font=("Arial", 12), bg="#d8000c", fg="white")
        close_button.pack(pady=10)