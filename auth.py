import tkinter as tk
from tkinter import messagebox
import sys
import os

# Agregar el directorio raíz del proyecto al path (método más robusto)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from .sections.padres import PadresSection
from .sections.docentes.main import DocentesSection
from .sections.preceptores.main import PreceptoresSection
from .sections.administradores.main import AdministradoresSection

try:
    from server.database import verificar_usuario, inicializar_base_datos
    DATABASE_CONNECTED = inicializar_base_datos()
    print(f"✅ Base de datos conectada exitosamente en auth.py: {DATABASE_CONNECTED}")
except ImportError as e:
    DATABASE_CONNECTED = False
    print(f"❌ Error al importar módulo de base de datos en auth.py: {e}")
    print(f"   Directorio actual: {current_dir}")
    print(f"   Directorio raíz: {project_root}")
    def verificar_usuario(usuario, contrasena):
        if usuario == "test" and contrasena == "test":
            return ("Padre",)
        return None
except Exception as e:
    DATABASE_CONNECTED = False
    print(f"❌ Error de conexión a base de datos en auth.py: {e}")
    def verificar_usuario(usuario, contrasena):
        if usuario == "test" and contrasena == "test":
            return ("Padre",)
        return None

# Diccionario para almacenar usuarios localmente (fallback)
usuarios = {}

class AuthManager:
    def __init__(self, root):
        self.root = root
    
    def create_login_window(self, title, role):
        """Crear ventana de login genérica"""
        login_window = tk.Toplevel(self.root)
        login_window.title(f"Login {title}")
        login_window.geometry("400x400")
        login_window.configure(bg="azure4")

        frame_login = tk.Frame(login_window, bg="azure4", padx=20, pady=20)
        frame_login.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(frame_login, text="Iniciar Sesión", font=("Arial", 24, "bold"), 
                              bg="azure4", fg="white")
        title_label.pack(pady=20)

        user_label = tk.Label(frame_login, text="Usuario:", font=("Arial", 14), bg="azure4", fg="white")
        user_label.pack(pady=5)
        user_entry = tk.Entry(frame_login, font=("Arial", 14))
        user_entry.pack(pady=10)

        pass_label = tk.Label(frame_login, text="Contraseña:", font=("Arial", 14), bg="azure4", fg="white")
        pass_label.pack(pady=5)
        pass_entry = tk.Entry(frame_login, show="*", font=("Arial", 14))
        pass_entry.pack(pady=10)

        def verificar_login():
            usuario = user_entry.get()
            contrasena = pass_entry.get()

            if DATABASE_CONNECTED:
                resultado = verificar_usuario(usuario, contrasena)
                if resultado and resultado[0] == role:
                    messagebox.showinfo("Login Exitoso", f"Bienvenido a la gestión de {title}")
                    login_window.destroy()
                    self.open_section(role, usuario)
                elif resultado:
                    messagebox.showerror("Rol Incorrecto", f"Este usuario no tiene rol '{role}', sino '{resultado[0]}'.")
                else:
                    messagebox.showerror("Error de Login", "Usuario o Contraseña incorrectos.")
            else:
                if usuario in usuarios and usuarios[usuario]["contrasena"] == contrasena:
                    if role in usuarios[usuario]["rol"]:
                        messagebox.showinfo("Login Exitoso", f"Bienvenido a la gestión de {title}")
                        login_window.destroy()
                        self.open_section(role, usuario)
                    else:
                        messagebox.showerror("Rol Incorrecto", f"Este usuario no tiene rol '{role}'.")
                else:
                    messagebox.showerror("Error de Login", "Usuario o Contraseña incorrectos.")

        login_button = tk.Button(frame_login, text="Ingresar", font=("Arial", 14), bg="green", 
                               fg="white", command=verificar_login)
        login_button.pack(pady=20)
    
    def open_section(self, role, usuario=None):
        """Abrir la sección correspondiente según el rol"""
        if role == "Padre":
            PadresSection(self.root, usuario)
        elif role == "Docente":
            DocentesSection(self.root)
        elif role == "Preceptor":
            PreceptoresSection(self.root)
        elif role == "Administrativo":
            AdministradoresSection(self.root)
    
    def login_padres(self):
        self.create_login_window("Padres", "Padre")
    
    def login_docente(self):
        self.create_login_window("Docentes", "Docente")
    
    def login_preceptor(self):
        self.create_login_window("Preceptores", "Preceptor")
    
    def login_administrador(self):
        self.create_login_window("Administradores", "Administrativo")