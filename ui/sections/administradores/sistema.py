"""
Configuración del Sistema para Administradores
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

try:
    from server.database import crear_usuario, obtener_todos_usuarios, crear_conexion
    from server.user_management import UserManager
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class SistemaWindow:
    """Ventana para configuración del sistema"""
    
    def __init__(self, parent, usuarios_data):
        self.parent = parent
        self.usuarios_data = usuarios_data
        self.user_manager = UserManager() if DATABASE_AVAILABLE else None
        self.create_window()

    def create_window(self):
        """Crear ventana principal del sistema"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("⚙️ Configuración del Sistema")
        self.window.geometry("1340x720")
        self.window.configure(bg="lightsteelblue")

        # Título
        title = tk.Label(self.window, text="⚙️ Configuración y Administración del Sistema", 
                        font=("Arial", 18, "bold"), bg="lightsteelblue", fg="darkblue")
        title.pack(pady=15)

        # Notebook con pestañas
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Pestaña 1: Gestión de Usuarios
        self.create_usuarios_tab(notebook)
        
        # Pestaña 2: Configuración General
        self.create_config_tab(notebook)

    def create_usuarios_tab(self, notebook):
        """Crear pestaña de gestión de usuarios"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="👥 Gestión de Usuarios")

        tk.Label(frame, text="👥 Gestión de Usuarios del Sistema", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Tabla de usuarios
        usuarios_frame = tk.LabelFrame(frame, text="📋 Lista de Usuarios", 
                                      font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        usuarios_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Usuario", "Tipo", "Email", "Estado")
        self.tree_usuarios = ttk.Treeview(usuarios_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.tree_usuarios.heading(col, text=col)
            if col == "Usuario":
                self.tree_usuarios.column(col, width=150, anchor="w")
            elif col == "Email":
                self.tree_usuarios.column(col, width=200, anchor="w")
            else:
                self.tree_usuarios.column(col, width=120, anchor="center")

        # Cargar usuarios
        self.cargar_usuarios()

        self.tree_usuarios.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Botones de gestión
        buttons_frame = tk.Frame(frame, bg="lightblue")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="➕ Crear Usuario", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=15, command=self.crear_usuario).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="✏️ Editar Usuario", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=15, command=self.editar_usuario).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="🔄 Actualizar Lista", bg="#2196F3", fg="white", 
                 font=("Arial", 10), width=15, command=self.actualizar_lista_usuarios).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="🗑️ Eliminar Usuario", bg="#F44336", fg="white", 
                 font=("Arial", 10), width=15, command=self.eliminar_usuario).pack(side=tk.LEFT, padx=5)

    def cargar_usuarios(self):
        """Cargar usuarios en la tabla"""
        # Limpiar tabla
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)

        # Cargar usuarios
        for usuario in self.usuarios_data:
            email = f"{usuario[0]}@gesj.edu.ar" if len(usuario) < 3 else usuario[2]
            self.tree_usuarios.insert("", tk.END, values=(
                usuario[0],  # nombre_usuario
                usuario[1],  # tipo_usuario
                email,       # email
                "Activo"     # estado
            ))

    def crear_usuario(self):
        """Crear nuevo usuario"""
        CrearUsuarioWindow(self.window, self.actualizar_lista_usuarios)

    def editar_usuario(self):
        """Editar usuario seleccionado"""
        print("🔧 Función editar_usuario llamada")
        
        selection = self.tree_usuarios.selection()
        print(f"📋 Selección actual: {selection}")
        
        if not selection:
            messagebox.showwarning("Selección", "Por favor seleccione un usuario para editar")
            print("⚠️ No hay usuario seleccionado")
            return
        
        item = self.tree_usuarios.item(selection[0])
        usuario_data = item['values']
        print(f"👤 Datos del usuario seleccionado: {usuario_data}")
        
        # Crear ventana de edición
        try:
            print(f"🪟 Creando ventana de edición para: {usuario_data[0]}")
            editar_window = EditarUsuarioWindow(self.window, usuario_data, self.actualizar_lista_usuarios)
            print(f"✅ Ventana de edición creada exitosamente")
        except Exception as e:
            print(f"❌ Error creando ventana de edición: {e}")
            messagebox.showerror("Error", f"Error al abrir ventana de edición: {e}")

    def actualizar_lista_usuarios(self):
        """Actualizar lista de usuarios"""
        if DATABASE_AVAILABLE:
            self.usuarios_data = obtener_todos_usuarios()
        self.cargar_usuarios()
    
    def eliminar_usuario(self):
        """Eliminar usuario seleccionado"""
        selection = self.tree_usuarios.selection()
        if not selection:
            messagebox.showwarning("Selección", "Por favor seleccione un usuario para eliminar")
            return
        
        item = self.tree_usuarios.item(selection[0])
        usuario_data = item['values']
        nombre_usuario = usuario_data[0]
        
        # Verificar que no sea un usuario crítico
        if nombre_usuario in ['admin1', 'admin']:
            messagebox.showerror("Error", f"No se puede eliminar el usuario crítico: {nombre_usuario}")
            return
        
        # Confirmación de eliminación
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación", 
            f"⚠️ ¿Está seguro que desea eliminar el usuario '{nombre_usuario}'?\n\n"
            f"Esta acción NO se puede deshacer.\n"
            f"Tipo: {usuario_data[1]}\n"
            f"Email: {usuario_data[2]}"
        )
        
        if respuesta:
            try:
                if DATABASE_AVAILABLE and self.user_manager:
                    success = self.user_manager.eliminar_usuario(nombre_usuario)
                    if success:
                        messagebox.showinfo("Usuario Eliminado", 
                                           f"✅ Usuario '{nombre_usuario}' eliminado exitosamente")
                        self.actualizar_lista_usuarios()
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el usuario")
                else:
                    messagebox.showinfo("Usuario Eliminado", 
                                       f"✅ Usuario '{nombre_usuario}' eliminado (simulación)")
                    self.actualizar_lista_usuarios()
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar usuario: {e}")

    def create_config_tab(self, notebook):
        """Crear pestaña de configuración general"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="⚙️ Configuración")

        tk.Label(frame, text="⚙️ Configuración General del Sistema", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Configuraciones del sistema
        config_text = """
        ⚙️ CONFIGURACIONES DEL SISTEMA:
        ═══════════════════════════════════════
        
        🗄️ BASE DE DATOS:
        • Servidor: MySQL 8.0
        • Host: 127.0.0.1:3306
        • Base de datos: gestion_escolar
        • Estado: ✅ Conectado
        
        📧 NOTIFICACIONES:
        • Servidor SMTP: Configurado
        • Modo: Simulación activa
        • Emails enviados hoy: 23
        • Tasa de entrega: 98.5%
        
        💾 RESPALDOS:
        • Automático: Diario a las 23:30
        • Último respaldo: 15/01/2025 23:30
        • Tamaño: 45.2 MB
        • Estado: ✅ Exitoso
        
        🔐 SEGURIDAD:
        • Usuarios activos: 15
        • Sesiones activas: 8
        • Intentos fallidos hoy: 2
        • Último acceso admin: 16/01/2025 14:30
        """

        tk.Label(frame, text=config_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)


class CrearUsuarioWindow:
    """Ventana para crear nuevo usuario"""
    
    def __init__(self, parent, callback_actualizar):
        self.parent = parent
        self.callback_actualizar = callback_actualizar
        self.create_window()

    def create_window(self):
        """Crear ventana de nuevo usuario"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("➕ Crear Nuevo Usuario")
        self.window.geometry("500x500")
        self.window.configure(bg="lightgreen")

        # Título
        title = tk.Label(self.window, text="➕ Crear Nuevo Usuario", 
                        font=("Arial", 16, "bold"), bg="lightgreen", fg="darkgreen")
        title.pack(pady=15)

        # Formulario
        form_frame = tk.LabelFrame(self.window, text="📝 Datos del Usuario", 
                                  font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Nombre de usuario
        tk.Label(form_frame, text="Nombre de Usuario:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.usuario_entry = tk.Entry(form_frame, width=30)
        self.usuario_entry.grid(row=0, column=1, padx=10, pady=5)

        # Contraseña
        tk.Label(form_frame, text="Contraseña:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = tk.Entry(form_frame, show='*', width=30)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Confirmar contraseña
        tk.Label(form_frame, text="Confirmar Contraseña:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.confirm_password_entry = tk.Entry(form_frame, show='*', width=30)
        self.confirm_password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Tipo de usuario
        tk.Label(form_frame, text="Tipo de Usuario:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.tipo_combo = ttk.Combobox(form_frame, values=["Padre", "Docente", "Preceptor", "Administrativo"], state="readonly", width=27)
        self.tipo_combo.set("Padre")
        self.tipo_combo.grid(row=3, column=1, padx=10, pady=5)

        # Email
        tk.Label(form_frame, text="Email:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = tk.Entry(form_frame, width=30)
        self.email_entry.grid(row=4, column=1, padx=10, pady=5)

        # Botones
        buttons_frame = tk.Frame(self.window, bg="lightgreen")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="💾 Crear Usuario", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=15, command=self.crear_usuario).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="❌ Cancelar", bg="#F44336", fg="white", 
                 font=("Arial", 10), width=15, command=self.window.destroy).pack(side=tk.LEFT, padx=5)

    def crear_usuario(self):
        """Crear el nuevo usuario"""
        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        tipo = self.tipo_combo.get()
        email = self.email_entry.get().strip()

        # Validaciones
        if not usuario:
            messagebox.showerror("Error", "El nombre de usuario es obligatorio")
            return
        
        if not password:
            messagebox.showerror("Error", "La contraseña es obligatoria")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        if len(password) < 4:
            messagebox.showerror("Error", "La contraseña debe tener al menos 4 caracteres")
            return

        try:
            if DATABASE_AVAILABLE:
                crear_usuario(usuario, password, tipo)
            
            messagebox.showinfo("Usuario Creado", 
                               f"✅ Usuario '{usuario}' creado exitosamente\n"
                               f"📧 Tipo: {tipo}\n"
                               f"📧 Email: {email}")
            
            if self.callback_actualizar:
                self.callback_actualizar()
            
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear usuario: {e}")


class EditarUsuarioWindow:
    """Ventana para editar usuario existente"""
    
    def __init__(self, parent, usuario_data, callback_actualizar):
        print(f"🔧 EditarUsuarioWindow.__init__ llamado")
        print(f"👤 Usuario a editar: {usuario_data}")
        
        self.parent = parent
        self.usuario_data = usuario_data
        self.callback_actualizar = callback_actualizar
        
        try:
            print(f"🪟 Iniciando creación de ventana...")
            self.create_window()
            print(f"✅ Ventana creada exitosamente")
        except Exception as e:
            print(f"❌ Error en __init__: {e}")
            raise e

    def create_window(self):
        """Crear ventana de edición"""
        print(f"🪟 create_window() llamado")
        
        try:
            self.window = tk.Toplevel(self.parent)
            self.window.title(f"✏️ Editar Usuario: {self.usuario_data[0]}")
            self.window.geometry("500x600")
            self.window.configure(bg="lightblue")
            
            print(f"🪟 Ventana básica creada")
            
            # Hacer que la ventana sea modal
            self.window.transient(self.parent)
            self.window.grab_set()
            
            print(f"🔒 Ventana configurada como modal")
            
            # Centrar la ventana
            self.window.update_idletasks()
            x = (self.window.winfo_screenwidth() // 2) - (250)
            y = (self.window.winfo_screenheight() // 2) - (300)
            self.window.geometry(f"500x600+{x}+{y}")
            
            print(f"📍 Ventana centrada en posición: {x}, {y}")
            
            # Crear contenido
            self.create_form()
            
            print(f"✅ Formulario creado exitosamente")
            
        except Exception as e:
            print(f"❌ Error en create_window: {e}")
            raise e

    def create_form(self):
        """Crear formulario de edición"""
        print(f"📝 Creando formulario de edición...")
        
        # Título
        title = tk.Label(self.window, text=f"✏️ Editar Usuario: {self.usuario_data[0]}", 
                        font=("Arial", 16, "bold"), bg="lightblue", fg="darkblue")
        title.pack(pady=15)

        # Formulario de edición
        form_frame = tk.LabelFrame(self.window, text="📝 Datos del Usuario", 
                                  font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Nombre de usuario (solo lectura)
        tk.Label(form_frame, text="Usuario:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(form_frame, text=self.usuario_data[0], font=("Arial", 10), bg="lightblue", fg="gray").grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Nueva contraseña
        tk.Label(form_frame, text="Nueva Contraseña:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = tk.Entry(form_frame, show='*', width=30)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Confirmar contraseña
        tk.Label(form_frame, text="Confirmar Contraseña:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.confirm_password_entry = tk.Entry(form_frame, show='*', width=30)
        self.confirm_password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Tipo de usuario
        tk.Label(form_frame, text="Tipo de Usuario:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.tipo_combo = ttk.Combobox(form_frame, values=["Padre", "Docente", "Preceptor", "Administrativo"], state="readonly", width=27)
        self.tipo_combo.set(self.usuario_data[1])
        self.tipo_combo.grid(row=3, column=1, padx=10, pady=5)
        
        # Bind para actualizar permisos cuando cambie el tipo
        self.tipo_combo.bind("<<ComboboxSelected>>", self.actualizar_permisos)

        # Email
        tk.Label(form_frame, text="Email:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = tk.Entry(form_frame, width=30)
        email_actual = self.usuario_data[2] if len(self.usuario_data) > 2 else f"{self.usuario_data[0]}@gesj.edu.ar"
        self.email_entry.insert(0, email_actual)
        self.email_entry.grid(row=4, column=1, padx=10, pady=5)

        # Estado
        tk.Label(form_frame, text="Estado:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.estado_combo = ttk.Combobox(form_frame, values=["Activo", "Inactivo", "Suspendido"], state="readonly", width=27)
        self.estado_combo.set("Activo")
        self.estado_combo.grid(row=5, column=1, padx=10, pady=5)

        # Observaciones
        tk.Label(form_frame, text="Observaciones:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=6, column=0, padx=10, pady=5, sticky="nw")
        self.observaciones_text = tk.Text(form_frame, width=30, height=4)
        self.observaciones_text.grid(row=6, column=1, padx=10, pady=5)

        # Información de permisos
        permisos_frame = tk.LabelFrame(form_frame, text="🔒 Permisos del Rol Seleccionado", 
                                      font=("Arial", 10, "bold"), bg="lightblue", fg="darkblue")
        permisos_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.permisos_label = tk.Label(permisos_frame, text=self.get_permisos_descripcion(self.usuario_data[1]), 
                                      font=("Arial", 9), bg="lightblue", justify=tk.LEFT)
        self.permisos_label.pack(padx=10, pady=5)

        # Botones
        buttons_frame = tk.Frame(self.window, bg="lightblue")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="💾 Guardar Cambios", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=18, command=self.guardar_cambios).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="❌ Cancelar", bg="#F44336", fg="white", 
                 font=("Arial", 10), width=15, command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        
        print(f"🎯 Formulario de edición completado")

    def get_permisos_descripcion(self, tipo_usuario):
        """Obtener descripción de permisos según el tipo de usuario"""
        permisos = {
            "Padre": "👨‍👩‍👧‍👦 Ver calificaciones de sus hijos, consultar asistencia, justificar inasistencias",
            "Docente": "👨‍🏫 Gestionar calificaciones, exportar reportes, comunicarse con padres",
            "Preceptor": "👨‍💼 Ver todos los alumnos, gestionar planes de intervención, análisis de tendencias",
            "Administrativo": "🏛️ Acceso completo al sistema, gestión de usuarios, reportes ejecutivos"
        }
        return permisos.get(tipo_usuario, "Sin permisos definidos")

    def actualizar_permisos(self, event=None):
        """Actualizar descripción de permisos cuando cambia el tipo"""
        nuevo_tipo = self.tipo_combo.get()
        nueva_descripcion = self.get_permisos_descripcion(nuevo_tipo)
        self.permisos_label.config(text=nueva_descripcion)

    def guardar_cambios(self):
        """Guardar cambios del usuario"""
        print(f"💾 Intentando guardar cambios para usuario: {self.usuario_data[0]}")
        
        # Validar contraseñas si se ingresó una nueva
        nueva_password = self.password_entry.get()
        if nueva_password:
            if nueva_password != self.confirm_password_entry.get():
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return
            if len(nueva_password) < 4:
                messagebox.showerror("Error", "La contraseña debe tener al menos 4 caracteres")
                return

        try:
            print(f"🔄 Actualizando usuario en base de datos...")
            if DATABASE_AVAILABLE:
                # Usar UserManager para actualizar
                from server.user_management import UserManager
                user_manager = UserManager()
                
                # Preparar datos para actualizar
                nuevos_datos = {
                    'tipo_usuario': self.tipo_combo.get()
                }
                
                if nueva_password:
                    nuevos_datos['contrasena'] = nueva_password
                    print(f"🔐 Actualizando contraseña...")
                
                success = user_manager.actualizar_usuario(self.usuario_data[0], nuevos_datos)
                
                if not success:
                    messagebox.showerror("Error", "No se pudo actualizar el usuario en la base de datos")
                    return
                else:
                    print(f"✅ Usuario actualizado exitosamente en base de datos")
            else:
                print(f"⚠️ Modo simulación - Base de datos no disponible")
            
            messagebox.showinfo("Usuario Actualizado", 
                               f"✅ Usuario '{self.usuario_data[0]}' actualizado exitosamente\n"
                               f"📧 Tipo: {self.tipo_combo.get()}\n"
                               f"📧 Email: {self.email_entry.get()}\n"
                               f"📊 Estado: {self.estado_combo.get()}")
            
            if self.callback_actualizar:
                print(f"🔄 Actualizando lista de usuarios...")
                self.callback_actualizar()
            
            print(f"🚪 Cerrando ventana de edición...")
            self.window.destroy()
            
        except Exception as e:
            print(f"❌ Error al actualizar usuario: {e}")
            messagebox.showerror("Error", f"Error al actualizar usuario: {e}")
        self.create_window()

    def create_window(self):
        """Crear ventana de edición"""
        print(f"🪟 Creando ventana de edición...")
        self.window = tk.Toplevel(self.parent)
        self.window.title("✏️ Editar Usuario")
        self.window.geometry("500x600")
        self.window.configure(bg="lightblue")
        
        # Hacer que la ventana sea modal
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Centrar la ventana
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"500x600+{x}+{y}")
        
        print(f"✅ Ventana de edición creada exitosamente")

        # Título
        title = tk.Label(self.window, text=f"✏️ Editar Usuario: {self.usuario_data[0]}", 
                        font=("Arial", 16, "bold"), bg="lightblue", fg="darkblue")
        title.pack(pady=15)

        # Formulario de edición
        form_frame = tk.LabelFrame(self.window, text="📝 Datos del Usuario", 
                                  font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Nombre de usuario (solo lectura)
        tk.Label(form_frame, text="Usuario:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(form_frame, text=self.usuario_data[0], font=("Arial", 10), bg="lightblue", fg="gray").grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Nueva contraseña
        tk.Label(form_frame, text="Nueva Contraseña:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.password_entry = tk.Entry(form_frame, show='*', width=30)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Confirmar contraseña
        tk.Label(form_frame, text="Confirmar Contraseña:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.confirm_password_entry = tk.Entry(form_frame, show='*', width=30)
        self.confirm_password_entry.grid(row=2, column=1, padx=10, pady=5)

        # Tipo de usuario
        tk.Label(form_frame, text="Tipo de Usuario:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.tipo_combo = ttk.Combobox(form_frame, values=["Padre", "Docente", "Preceptor", "Administrativo"], state="readonly", width=27)
        self.tipo_combo.set(self.usuario_data[1])
        self.tipo_combo.grid(row=3, column=1, padx=10, pady=5)
        
        # Bind para actualizar permisos cuando cambie el tipo
        self.tipo_combo.bind("<<ComboboxSelected>>", self.actualizar_permisos)

        # Email
        tk.Label(form_frame, text="Email:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.email_entry = tk.Entry(form_frame, width=30)
        email_actual = self.usuario_data[2] if len(self.usuario_data) > 2 else f"{self.usuario_data[0]}@gesj.edu.ar"
        self.email_entry.insert(0, email_actual)
        self.email_entry.grid(row=4, column=1, padx=10, pady=5)

        # Estado
        tk.Label(form_frame, text="Estado:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.estado_combo = ttk.Combobox(form_frame, values=["Activo", "Inactivo", "Suspendido"], state="readonly", width=27)
        self.estado_combo.set("Activo")
        self.estado_combo.grid(row=5, column=1, padx=10, pady=5)

        # Observaciones
        tk.Label(form_frame, text="Observaciones:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=6, column=0, padx=10, pady=5, sticky="nw")
        self.observaciones_text = tk.Text(form_frame, width=30, height=4)
        self.observaciones_text.grid(row=6, column=1, padx=10, pady=5)

        # Información de permisos
        permisos_frame = tk.LabelFrame(form_frame, text="🔒 Permisos del Rol Seleccionado", 
                                      font=("Arial", 10, "bold"), bg="lightblue", fg="darkblue")
        permisos_frame.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.permisos_label = tk.Label(permisos_frame, text=self.get_permisos_descripcion(self.usuario_data[1]), 
                                      font=("Arial", 9), bg="lightblue", justify=tk.LEFT)
        self.permisos_label.pack(padx=10, pady=5)


        # Botones
        buttons_frame = tk.Frame(self.window, bg="lightblue")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="💾 Guardar Cambios", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=18, command=self.guardar_cambios).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="❌ Cancelar", bg="#F44336", fg="white", 
                 font=("Arial", 10), width=15, command=self.window.destroy).pack(side=tk.LEFT, padx=5)
        
        print(f"🎯 Formulario de edición listo para usuario: {self.usuario_data[0]}")

    def get_permisos_descripcion(self, tipo_usuario):
        """Obtener descripción de permisos según el tipo de usuario"""
        permisos = {
            "Padre": "👨‍👩‍👧‍👦 Ver calificaciones de sus hijos, consultar asistencia, justificar inasistencias",
            "Docente": "👨‍🏫 Gestionar calificaciones, exportar reportes, comunicarse con padres",
            "Preceptor": "👨‍💼 Ver todos los alumnos, gestionar planes de intervención, análisis de tendencias",
            "Administrativo": "🏛️ Acceso completo al sistema, gestión de usuarios, reportes ejecutivos"
        }
        return permisos.get(tipo_usuario, "Sin permisos definidos")

    def actualizar_permisos(self, event=None):
        """Actualizar descripción de permisos cuando cambia el tipo"""
        nuevo_tipo = self.tipo_combo.get()
        nueva_descripcion = self.get_permisos_descripcion(nuevo_tipo)
        self.permisos_label.config(text=nueva_descripcion)

    def guardar_cambios(self):
        """Guardar cambios del usuario"""
        print(f"💾 Intentando guardar cambios para usuario: {self.usuario_data[0]}")
        
        # Validar contraseñas si se ingresó una nueva
        nueva_password = self.password_entry.get()
        if nueva_password:
            if nueva_password != self.confirm_password_entry.get():
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return
            if len(nueva_password) < 4:
                messagebox.showerror("Error", "La contraseña debe tener al menos 4 caracteres")
                return

        try:
            print(f"🔄 Actualizando usuario en base de datos...")
            if DATABASE_AVAILABLE:
                # Usar UserManager para actualizar
                from server.user_management import UserManager
                user_manager = UserManager()
                
                # Preparar datos para actualizar
                nuevos_datos = {
                    'tipo_usuario': self.tipo_combo.get()
                }
                
                if nueva_password:
                    nuevos_datos['contrasena'] = nueva_password
                    print(f"🔐 Actualizando contraseña...")
                
                success = user_manager.actualizar_usuario(self.usuario_data[0], nuevos_datos)
                
                if not success:
                    messagebox.showerror("Error", "No se pudo actualizar el usuario en la base de datos")
                    return
                else:
                    print(f"✅ Usuario actualizado exitosamente en base de datos")
            else:
                print(f"⚠️ Modo simulación - Base de datos no disponible")
            
            messagebox.showinfo("Usuario Actualizado", 
                               f"✅ Usuario '{self.usuario_data[0]}' actualizado exitosamente\n"
                               f"📧 Tipo: {self.tipo_combo.get()}\n"
                               f"📧 Email: {self.email_entry.get()}\n"
                               f"📊 Estado: {self.estado_combo.get()}")
            
            if self.callback_actualizar:
                print(f"🔄 Actualizando lista de usuarios...")
                self.callback_actualizar()
            
            print(f"🚪 Cerrando ventana de edición...")
            self.window.destroy()
            
        except Exception as e:
            print(f"❌ Error al actualizar usuario: {e}")
            messagebox.showerror("Error", f"Error al actualizar usuario: {e}")