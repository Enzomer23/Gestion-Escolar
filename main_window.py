import tkinter as tk
from PIL import Image, ImageTk
import os
from .auth import AuthManager
from .user_management import UserManager

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.auth_manager = AuthManager(self.root)
        self.user_manager = UserManager(self.root)
        self.setup_window()
        self.load_images()
        self.create_widgets()
    
    def setup_window(self):
        """Configurar la ventana principal"""
        self.root.title("GESJ - Plataforma de Gestión Educativa")
        
        # Obtener el tamaño de la pantalla y establecer la ventana a pantalla completa
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.configure(bg="DarkSeaGreen")
    
    def load_images(self):
        """Cargar las imágenes con manejo de errores"""
        try:
            image_path = r'C:\TFG\TFG-EnzoMerenda-20250627T210914Z-1-001\TFG-EnzoMerenda\GESJ\WhatsApp Image 2024-09-09 at 22.59.55.jpeg'
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((200, 200), Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)
            else:
                self.photo = None
        except Exception as e:
            print(f"Error cargando imagen principal: {e}")
            self.photo = None

        try:
            arg_img_path = r'C:\TFG\TFG-EnzoMerenda-20250627T210914Z-1-001\TFG-EnzoMerenda\GESJ\argentina.jpg'
            if os.path.exists(arg_img_path):
                arg_img = Image.open(arg_img_path)
                arg_img = arg_img.resize((150, 280), Image.Resampling.LANCZOS)
                self.arg_photo = ImageTk.PhotoImage(arg_img)
            else:
                self.arg_photo = None
        except Exception as e:
            print(f"Error cargando imagen de Argentina: {e}")
            self.arg_photo = None
    
    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        self.create_header()
        self.create_main_content()
        self.create_side_image()
        self.create_footer()
    
    def create_header(self):
        """Crear el encabezado con título e imagen"""
        header_frame = tk.Frame(self.root, bg="chartreuse3", padx=10, pady=20)
        header_frame.pack(fill=tk.X)

        if self.photo:
            img_label = tk.Label(header_frame, image=self.photo, bg="chartreuse3")
            img_label.grid(row=0, column=0, rowspan=2)

        title = tk.Label(header_frame, text="     GESJ - Plataforma de Gestión Educativa", 
                        font=("Franklin Gothic Heavy", 40, "bold"), bg="chartreuse3", fg="white", pady=25)
        title.grid(row=0, column=1, padx=20, columnspan=3, sticky="nsew")

        subtitle = tk.Label(header_frame, text="Provincia de San Juan, República Argentina", 
                           font=("Arial", 22), bg="chartreuse3", fg="white")
        subtitle.grid(row=1, column=1, columnspan=3, sticky="nsew")
    
    def create_main_content(self):
        """Crear el contenido principal con botones de roles"""
        roles_frame = tk.Frame(self.root, bg="azure2", padx=20, pady=10)
        roles_frame.pack(pady=20)

        roles_title = tk.Label(roles_frame, text=" ", font=("Arial Rounded MT Bold", 18, "bold"), 
                              bg="azure2", fg="black")
        roles_title.pack()

        roles_title1 = tk.Label(roles_frame, 
                               text="En nuestra institución, cada paso cuenta.\nConectemos juntos las trayectorias escolares hacia un futuro brillante.", 
                               font=("Arial Rounded MT Bold", 14), bg="azure2", fg="black", 
                               wraplength=600, justify="center")
        roles_title1.pack()

        # Recuadro con los botones para los roles
        buttons_frame = tk.Frame(roles_frame, bg="#e0f2f1", padx=10, pady=10, relief=tk.GROOVE, bd=2)
        buttons_frame.pack(pady=10)

        padres_btn = tk.Button(buttons_frame, text="Padres", font=("Arial", 16), width=20, 
                              bg="SeaGreen2", fg="white", command=self.auth_manager.login_padres)
        padres_btn.grid(row=0, column=0, padx=10, pady=5) 

        docentes_btn = tk.Button(buttons_frame, text="Docentes", font=("Arial", 16), width=20, 
                                bg="SeaGreen2", fg="white", command=self.auth_manager.login_docente)
        docentes_btn.grid(row=1, column=0, padx=10, pady=5)

        preceptores_btn = tk.Button(buttons_frame, text="Preceptores", font=("Arial", 16), width=20, 
                                   bg="SeaGreen2", fg="white", command=self.auth_manager.login_preceptor)
        preceptores_btn.grid(row=0, column=1, padx=10, pady=5)

        admin_btn = tk.Button(buttons_frame, text="Administradores", font=("Arial", 16), width=20, 
                             bg="SeaGreen2", fg="white", command=self.auth_manager.login_administrador)
        admin_btn.grid(row=1, column=1, padx=10, pady=5)

        # Frame inferior para opciones de gestión
        gest_frame = tk.Frame(self.root, bg="azure4", padx=20, pady=10)
        gest_frame.pack(pady=10)

        crear_usuario_btn = tk.Button(gest_frame, text="Crear Usuario", font=("Arial", 14), width=20, 
                                     bg="azure4", fg="white", command=self.user_manager.crear_usuario)
        crear_usuario_btn.pack(side=tk.LEFT, padx=10)

        ver_usuarios_btn = tk.Button(gest_frame, text="Ver Usuarios", font=("Arial", 14), width=20, 
                                    bg="azure4", fg="white", command=self.user_manager.ver_usuarios)
        ver_usuarios_btn.pack(side=tk.LEFT, padx=10)

        # Nuevos módulos adicionales
        modulos_adicionales_frame = tk.Frame(self.root, bg="lightsteelblue", padx=20, pady=10)
        modulos_adicionales_frame.pack(pady=10)
        
        tk.Label(modulos_adicionales_frame, text="🎯 Módulos Adicionales", 
                font=("Arial", 14, "bold"), bg="lightsteelblue", fg="darkblue").pack(pady=5)
        
        # Botones para módulos adicionales
        modulos_buttons_frame = tk.Frame(modulos_adicionales_frame, bg="lightsteelblue")
        modulos_buttons_frame.pack()
        
        asistencia_btn = tk.Button(modulos_buttons_frame, text="📅 Asistencia", font=("Arial", 12), width=15, 
                                  bg="teal", fg="white", command=self.abrir_asistencia)
        asistencia_btn.grid(row=0, column=0, padx=5, pady=5)
        
        biblioteca_btn = tk.Button(modulos_buttons_frame, text="📚 Biblioteca", font=("Arial", 12), width=15, 
                                  bg="goldenrod", fg="white", command=self.abrir_biblioteca)
        biblioteca_btn.grid(row=0, column=1, padx=5, pady=5)
        
        eventos_btn = tk.Button(modulos_buttons_frame, text="🎯 Eventos", font=("Arial", 12), width=15, 
                               bg="mediumvioletred", fg="white", command=self.abrir_eventos)
        eventos_btn.grid(row=0, column=2, padx=5, pady=5)
        
        comunicacion_btn = tk.Button(modulos_buttons_frame, text="💬 Comunicación", font=("Arial", 12), width=15, 
                                    bg="steelblue", fg="white", command=self.abrir_comunicacion)
        comunicacion_btn.grid(row=1, column=0, padx=5, pady=5)
        
        evaluaciones_btn = tk.Button(modulos_buttons_frame, text="📊 Evaluaciones", font=("Arial", 12), width=15, 
                                    bg="darkslategray", fg="white", command=self.abrir_evaluaciones)
        evaluaciones_btn.grid(row=1, column=1, padx=5, pady=5)
        
        calificaciones_btn = tk.Button(modulos_buttons_frame, text="📝 Calificaciones", font=("Arial", 12), width=15, 
                                      bg="darkcyan", fg="white", command=self.abrir_calificaciones)
        calificaciones_btn.grid(row=1, column=2, padx=5, pady=5)
        
        salir_btn = tk.Button(gest_frame, text="Salir", font=("Arial", 14), width=20, 
                             bg="azure4", fg="white", command=self.salir_aplicacion)
        salir_btn.pack(side=tk.LEFT, padx=10)
    
    def create_side_image(self):
        """Crear la imagen lateral de Argentina"""
        if self.arg_photo:
            image_frame = tk.Frame(self.root, bg="DarkSeaGreen", bd=5, relief=tk.GROOVE)
            image_frame.place(relx=0.90, rely=0.47, anchor="e") 

            arg_img_label = tk.Label(image_frame, image=self.arg_photo, bg="DarkSeaGreen")
            arg_img_label.pack()
    
    def create_footer(self):
        """Crear el pie de página con derechos reservados"""
        config_frame1 = tk.Frame(self.root, bg="azure4", padx=20, pady=10)
        config_frame1.pack(pady=10)
        nota_derechos = tk.Label(config_frame1, text="Propiedad de la Institución. Todos los derechos reservados.", 
                                font=("Arial", 12), bg="azure4", fg="black")
        nota_derechos.pack()
    
    def salir_aplicacion(self):
        """Salir de la aplicación con confirmación"""
        from tkinter import messagebox
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir de la aplicación?"):
            self.root.quit()
    
    def abrir_asistencia(self):
        """Abrir módulo de asistencia"""
        try:
            from .sections.asistencia import AsistenciaSection
            AsistenciaSection(self.root)
        except ImportError as e:
            messagebox.showerror("Error", f"Error al cargar módulo de asistencia: {e}")
    
    def abrir_biblioteca(self):
        """Abrir módulo de biblioteca"""
        try:
            from .sections.biblioteca import BibliotecaSection
            BibliotecaSection(self.root)
        except ImportError as e:
            messagebox.showerror("Error", f"Error al cargar módulo de biblioteca: {e}")
    
    def abrir_eventos(self):
        """Abrir módulo de eventos"""
        try:
            from .sections.eventos import EventosSection
            EventosSection(self.root)
        except ImportError as e:
            messagebox.showerror("Error", f"Error al cargar módulo de eventos: {e}")
    
    def abrir_comunicacion(self):
        """Abrir módulo de comunicación"""
        try:
            from .sections.comunicacion import ComunicacionSection
            ComunicacionSection(self.root)
        except ImportError as e:
            messagebox.showerror("Error", f"Error al cargar módulo de comunicación: {e}")
    
    def abrir_evaluaciones(self):
        """Abrir módulo de evaluaciones"""
        try:
            from .sections.evaluaciones import EvaluacionesSection
            EvaluacionesSection(self.root)
        except ImportError as e:
            messagebox.showerror("Error", f"Error al cargar módulo de evaluaciones: {e}")
    
    def abrir_calificaciones(self):
        """Abrir módulo de calificaciones"""
        try:
            from .sections.calificaciones import CalificacionesSection
            CalificacionesSection(self.root)
        except ImportError as e:
            messagebox.showerror("Error", f"Error al cargar módulo de calificaciones: {e}")
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()