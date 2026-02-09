"""
Módulo de Comunicación Avanzada - GESJ
Plataforma de Gestión Educativa
Provincia de San Juan, República Argentina
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from server.comunicacion_operations import ComunicacionManager
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class ComunicacionSection:
    """Sección principal de comunicación avanzada"""
    
    def __init__(self, root, usuario_id=1, usuario_tipo="Padre"):
        self.root = root
        self.usuario_id = usuario_id
        self.usuario_tipo = usuario_tipo
        self.comunicacion_manager = ComunicacionManager() if DATABASE_AVAILABLE else None
        self.create_comunicacion_window()
    
    def create_comunicacion_window(self):
        """Crear ventana principal de comunicación"""
        self.comunicacion_window = tk.Toplevel(self.root)
        self.comunicacion_window.title("💬 Sistema de Comunicación")
        self.comunicacion_window.geometry("1340x720")
        self.comunicacion_window.configure(bg="lightsteelblue")

        self.create_header()
        self.create_main_content()
        self.create_footer()

    def create_header(self):
        """Crear encabezado"""
        header_frame = tk.Frame(self.comunicacion_window, bg="steelblue", padx=15, pady=8)
        header_frame.pack(fill=tk.X)

        title = tk.Label(header_frame, text="💬 Sistema de Comunicación Integral", 
                        font=("Franklin Gothic Heavy", 18, "bold"), bg="steelblue", fg="white")
        title.pack(pady=5)

        subtitle = tk.Label(header_frame, text="Comunicación Efectiva entre Toda la Comunidad Educativa", 
                           font=("Arial", 11), bg="steelblue", fg="lightsteelblue")
        subtitle.pack()

    def create_main_content(self):
        """Crear contenido principal"""
        # Frame principal con scroll
        main_frame = tk.Frame(self.comunicacion_window, bg="lightsteelblue")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)

        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg="lightsteelblue")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="lightsteelblue")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Panel de estadísticas
        self.create_stats_panel(scrollable_frame)
        
        # Notebook con funcionalidades
        self.create_notebook(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_stats_panel(self, parent):
        """Panel de estadísticas de comunicación"""
        stats_frame = tk.LabelFrame(parent, text="📊 Estadísticas de Comunicación", 
                                   font=("Arial", 12, "bold"), bg="lightsteelblue", 
                                   fg="steelblue", padx=10, pady=8)
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        stats_data = [
            ("📧 Mensajes Hoy", "47", "blue", "Enviados"),
            ("💬 Chat Activo", "12", "green", "Conversaciones"),
            ("📢 Anuncios", "3", "orange", "Publicados"),
            ("📨 Sin Leer", "8", "red", "Pendientes")
        ]

        for i, (label, value, color, info) in enumerate(stats_data):
            stat_frame = tk.Frame(stats_frame, bg="white", relief=tk.RAISED, bd=2)
            stat_frame.grid(row=0, column=i, padx=8, pady=5, sticky="ew")
            
            tk.Label(stat_frame, text=label, font=("Arial", 9, "bold"), bg="white").pack()
            tk.Label(stat_frame, text=value, font=("Arial", 16, "bold"), 
                    bg="white", fg=color).pack()
            tk.Label(stat_frame, text=info, font=("Arial", 8), 
                    bg="white", fg="gray").pack()

        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)

    def create_notebook(self, parent):
        """Crear notebook con funcionalidades"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Pestaña 1: Chat en Tiempo Real
        self.create_chat_tab(notebook)
        
        # Pestaña 2: Mensajería
        self.create_mensajeria_tab(notebook)
        
        # Pestaña 3: Anuncios
        self.create_anuncios_tab(notebook)
        
        # Pestaña 4: Foro
        self.create_foro_tab(notebook)

    def create_chat_tab(self, notebook):
        """Crear pestaña de chat en tiempo real"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="💬 Chat en Tiempo Real")

        tk.Label(frame, text="💬 Chat Institucional en Tiempo Real", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Lista de conversaciones activas
        conversaciones_frame = tk.LabelFrame(frame, text="💬 Conversaciones Activas", 
                                            font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        conversaciones_frame.pack(fill=tk.X, padx=20, pady=10)

        conversaciones_data = [
            ("Prof. González", "Docente", "Consulta sobre Mario", "Hace 5 min", "🟢"),
            ("Preceptor López", "Preceptor", "Reunión de padres", "Hace 12 min", "🟢"),
            ("Madre Díaz", "Padre", "Horarios de tutoría", "Hace 1 hora", "🟡"),
            ("Directora", "Directivo", "Planificación febrero", "Hace 2 horas", "🔴")
        ]

        for i, (nombre, tipo, ultimo_mensaje, tiempo, estado) in enumerate(conversaciones_data):
            conv_frame = tk.Frame(conversaciones_frame, bg="white", relief=tk.RAISED, bd=1)
            conv_frame.pack(fill=tk.X, padx=10, pady=3)
            
            tk.Label(conv_frame, text=estado, font=("Arial", 12), bg="white").pack(side=tk.LEFT, padx=5)
            tk.Label(conv_frame, text=nombre, font=("Arial", 10, "bold"), bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            tk.Label(conv_frame, text=tipo, font=("Arial", 9), bg="white", fg="blue").pack(side=tk.LEFT, padx=5)
            tk.Label(conv_frame, text=tiempo, font=("Arial", 8), bg="white", fg="gray").pack(side=tk.RIGHT, padx=5)

        # Área de chat
        chat_frame = tk.LabelFrame(frame, text="💬 Área de Chat", 
                                  font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Mensajes del chat
        chat_text = tk.Text(chat_frame, height=10, bg="white", state=tk.DISABLED)
        chat_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Área de escritura
        input_frame = tk.Frame(chat_frame, bg="lightblue")
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        mensaje_entry = tk.Entry(input_frame, width=60)
        mensaje_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        tk.Button(input_frame, text="📤 Enviar", bg="#4CAF50", fg="white", font=("Arial", 9)).pack(side=tk.RIGHT, padx=5)

    def create_mensajeria_tab(self, notebook):
        """Crear pestaña de mensajería"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="📧 Mensajería")

        tk.Label(frame, text="📧 Sistema de Mensajería Institucional", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Bandeja de entrada
        bandeja_frame = tk.LabelFrame(frame, text="📥 Bandeja de Entrada", 
                                     font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        bandeja_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Estado", "De", "Asunto", "Fecha", "Prioridad")
        tree = ttk.Treeview(bandeja_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Asunto":
                tree.column(col, width=250, anchor="w")
            elif col == "De":
                tree.column(col, width=120, anchor="w")
            else:
                tree.column(col, width=80, anchor="center")

        # Datos de mensajes
        mensajes_data = [
            ("📧 Nuevo", "Prof. González", "Consulta sobre calificaciones", "16/01/2025", "Normal"),
            ("📖 Leído", "Preceptor López", "Reunión de padres programada", "15/01/2025", "Alta"),
            ("📧 Nuevo", "Directora", "Cambios en el calendario", "14/01/2025", "Urgente"),
            ("📖 Leído", "Madre Díaz", "Agradecimiento por atención", "13/01/2025", "Normal")
        ]

        for mensaje in mensajes_data:
            prioridad = mensaje[4]
            if prioridad == "Urgente":
                tags = ("urgente",)
            elif prioridad == "Alta":
                tags = ("alta",)
            else:
                tags = ()
            
            tree.insert("", tk.END, values=mensaje, tags=tags)

        tree.tag_configure("urgente", background="#FFCDD2")
        tree.tag_configure("alta", background="#FFF3E0")

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def create_anuncios_tab(self, notebook):
        """Crear pestaña de anuncios"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="📢 Anuncios")

        tk.Label(frame, text="📢 Anuncios Institucionales", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Anuncios recientes
        anuncios_frame = tk.LabelFrame(frame, text="📢 Anuncios Recientes", 
                                      font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        anuncios_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        anuncios_text = """
        📢 ANUNCIOS INSTITUCIONALES:
        ═══════════════════════════════════
        
        🔴 URGENTE (16/01/2025):
        "Cambio de horario para reunión de padres"
        La reunión del 20/01 se adelanta a las 17:30 hs.
        
        🟡 IMPORTANTE (15/01/2025):
        "Inicio del período de inscripciones 2025"
        Abiertas las inscripciones para actividades extracurriculares.
        
        🟢 INFORMATIVO (14/01/2025):
        "Nueva biblioteca digital disponible"
        Acceso a 500+ libros digitales para toda la comunidad.
        
        📅 RECORDATORIO (13/01/2025):
        "Entrega de boletines - Febrero 2025"
        Los boletines estarán disponibles a partir del 1º de febrero.
        
        🎉 CELEBRACIÓN (12/01/2025):
        "Felicitaciones a nuestros estudiantes destacados"
        Reconocimiento a los alumnos con mejor rendimiento.
        """

        tk.Label(anuncios_frame, text=anuncios_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones de gestión
        if self.usuario_tipo in ["Administrativo", "Preceptor", "Docente"]:
            buttons_frame = tk.Frame(frame, bg="lightyellow")
            buttons_frame.pack(fill=tk.X, pady=10)

            tk.Button(buttons_frame, text="📝 Crear Anuncio", bg="#4CAF50", fg="white", 
                     font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
            tk.Button(buttons_frame, text="✏️ Editar", bg="#FF9800", fg="white", 
                     font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)

    def create_foro_tab(self, notebook):
        """Crear pestaña de foro"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="🗣️ Foro")

        tk.Label(frame, text="🗣️ Foro de Consultas por Materia", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Temas del foro
        foro_frame = tk.LabelFrame(frame, text="💭 Temas de Discusión", 
                                  font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        foro_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Materia", "Tema", "Autor", "Respuestas", "Última Actividad")
        tree = ttk.Treeview(foro_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Tema":
                tree.column(col, width=200, anchor="w")
            else:
                tree.column(col, width=120, anchor="center")

        # Datos del foro
        foro_data = [
            ("Matemáticas", "Dudas sobre ecuaciones cuadráticas", "Padre González", "5", "Hace 2 horas"),
            ("Lengua", "Análisis de textos literarios", "Prof. Martínez", "8", "Hace 1 día"),
            ("Ciencias", "Experimentos caseros de química", "Alumno Pérez", "12", "Hace 3 horas"),
            ("Historia", "Revolución de Mayo - Recursos", "Prof. López", "3", "Hace 1 semana")
        ]

        for tema in foro_data:
            tree.insert("", tk.END, values=tema)

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Botones del foro
        buttons_frame = tk.Frame(frame, bg="lightcoral")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="💭 Nuevo Tema", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="👁️ Ver Discusión", bg="#2196F3", fg="white", 
                 font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="💬 Responder", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)

    def create_footer(self):
        """Crear pie de página"""
        footer_frame = tk.Frame(self.comunicacion_window, bg="steelblue", padx=15, pady=8)
        footer_frame.pack(fill=tk.X)
        
        tk.Label(footer_frame, text="GESJ - Sistema Integral de Gestión Educativa | Módulo de Comunicación", 
                font=("Arial", 9), bg="steelblue", fg="lightsteelblue").pack()