"""
Módulo de Eventos y Actividades - GESJ
Plataforma de Gestión Educativa
Provincia de San Juan, República Argentina
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from server.eventos_operations import EventosManager
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class EventosSection:
    """Sección principal de gestión de eventos"""
    
    def __init__(self, root, usuario_tipo="Administrativo"):
        self.root = root
        self.usuario_tipo = usuario_tipo
        self.eventos_manager = EventosManager() if DATABASE_AVAILABLE else None
        self.create_eventos_window()
    
    def create_eventos_window(self):
        """Crear ventana principal de eventos"""
        self.eventos_window = tk.Toplevel(self.root)
        self.eventos_window.title("🎯 Sistema de Eventos")
        self.eventos_window.geometry("1340x720")
        self.eventos_window.configure(bg="lightpink")

        self.create_header()
        self.create_main_content()
        self.create_footer()

    def create_header(self):
        """Crear encabezado"""
        header_frame = tk.Frame(self.eventos_window, bg="mediumvioletred", padx=15, pady=8)
        header_frame.pack(fill=tk.X)

        title = tk.Label(header_frame, text="🎯 Sistema de Eventos y Actividades", 
                        font=("Franklin Gothic Heavy", 18, "bold"), bg="mediumvioletred", fg="white")
        title.pack(pady=5)

        subtitle = tk.Label(header_frame, text="Organización y Gestión de Actividades Institucionales", 
                           font=("Arial", 11), bg="mediumvioletred", fg="lightpink")
        subtitle.pack()

    def create_main_content(self):
        """Crear contenido principal"""
        # Frame principal con scroll
        main_frame = tk.Frame(self.eventos_window, bg="lightpink")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)

        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg="lightpink")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="lightpink")

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
        """Panel de estadísticas de eventos"""
        stats_frame = tk.LabelFrame(parent, text="📊 Estadísticas de Eventos", 
                                   font=("Arial", 12, "bold"), bg="lightpink", 
                                   fg="mediumvioletred", padx=10, pady=8)
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        stats_data = [
            ("🎯 Eventos Este Mes", "12", "blue", "Programados"),
            ("👥 Participación", "89%", "green", "Promedio"),
            ("📅 Próximos", "5", "orange", "Esta semana"),
            ("🏆 Completados", "8", "green", "Exitosos")
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

        # Pestaña 1: Calendario
        self.create_calendario_tab(notebook)
        
        # Pestaña 2: Crear Evento
        self.create_crear_evento_tab(notebook)
        
        # Pestaña 3: Actividades Extracurriculares
        self.create_extracurriculares_tab(notebook)
        
        # Pestaña 4: Reuniones
        self.create_reuniones_tab(notebook)

    def create_calendario_tab(self, notebook):
        """Crear pestaña de calendario"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="📅 Calendario")

        tk.Label(frame, text="📅 Calendario Institucional", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Eventos próximos
        proximos_frame = tk.LabelFrame(frame, text="📅 Próximos Eventos", 
                                      font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        proximos_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Fecha", "Evento", "Hora", "Tipo", "Dirigido a", "Estado")
        tree = ttk.Treeview(proximos_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Evento":
                tree.column(col, width=200, anchor="w")
            else:
                tree.column(col, width=100, anchor="center")

        # Datos de eventos
        eventos_data = [
            ("20/01/2025", "Reunión de Padres 1º Año", "18:00", "Reunión", "Padres", "Confirmado"),
            ("22/01/2025", "Acto de Inicio de Clases", "08:00", "Ceremonia", "Toda la comunidad", "Programado"),
            ("25/01/2025", "Taller de Matemáticas", "14:00", "Académico", "Estudiantes", "Programado"),
            ("28/01/2025", "Feria de Ciencias", "09:00", "Educativo", "Toda la comunidad", "Preparación")
        ]

        for evento in eventos_data:
            tree.insert("", tk.END, values=evento)

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def create_crear_evento_tab(self, notebook):
        """Crear pestaña para crear eventos"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="🆕 Crear Evento")

        tk.Label(frame, text="🆕 Crear Nuevo Evento", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Formulario de evento
        form_frame = tk.LabelFrame(frame, text="📝 Datos del Evento", 
                                  font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        form_frame.pack(fill=tk.X, padx=20, pady=10)

        # Campos del formulario
        tk.Label(form_frame, text="Título:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        titulo_entry = tk.Entry(form_frame, width=50)
        titulo_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Tipo:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tipo_combo = ttk.Combobox(form_frame, values=[
            "Académico", "Deportivo", "Cultural", "Reunión", "Ceremonia", "Taller"
        ], state="readonly", width=47)
        tipo_combo.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Fecha:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        fecha_entry = tk.Entry(form_frame, width=20)
        fecha_entry.insert(0, "20/01/2025")
        fecha_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form_frame, text="Descripción:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
        descripcion_text = tk.Text(form_frame, width=50, height=4)
        descripcion_text.grid(row=3, column=1, padx=10, pady=5)

        # Botones
        buttons_frame = tk.Frame(form_frame, bg="lightgreen")
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=15)

        tk.Button(buttons_frame, text="💾 Crear Evento", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📧 Notificar", bg="#2196F3", fg="white", 
                 font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)

    def create_extracurriculares_tab(self, notebook):
        """Crear pestaña de actividades extracurriculares"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="🏃 Extracurriculares")

        tk.Label(frame, text="🏃 Actividades Extracurriculares", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Actividades disponibles
        actividades_text = """
        🏃 ACTIVIDADES EXTRACURRICULARES DISPONIBLES:
        ═══════════════════════════════════════════════
        
        🏃 DEPORTES:
        • Fútbol: Lunes y Miércoles 15:00-17:00 (25 inscriptos)
        • Básquet: Martes y Jueves 15:00-17:00 (18 inscriptos)
        • Atletismo: Viernes 15:00-17:00 (12 inscriptos)
        • Natación: Sábados 09:00-11:00 (15 inscriptos)
        
        🎨 ARTE Y CULTURA:
        • Coro escolar: Miércoles 16:00-18:00 (22 inscriptos)
        • Teatro: Jueves 16:00-18:00 (16 inscriptos)
        • Artes plásticas: Viernes 14:00-16:00 (20 inscriptos)
        • Danza folklórica: Martes 17:00-19:00 (14 inscriptos)
        
        🔬 CIENCIA Y TECNOLOGÍA:
        • Club de ciencias: Lunes 16:00-18:00 (18 inscriptos)
        • Robótica: Miércoles 17:00-19:00 (12 inscriptos)
        • Programación: Viernes 16:00-18:00 (10 inscriptos)
        
        📚 APOYO ACADÉMICO:
        • Tutorías de matemáticas: Diario 15:00-16:00
        • Apoyo en lengua: Martes y Jueves 15:00-16:00
        • Preparación para exámenes: Según demanda
        """

        tk.Label(frame, text=actividades_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_reuniones_tab(self, notebook):
        """Crear pestaña de reuniones"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="👥 Reuniones")

        tk.Label(frame, text="👥 Gestión de Reuniones", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Próximas reuniones
        reuniones_frame = tk.LabelFrame(frame, text="📅 Próximas Reuniones", 
                                       font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        reuniones_frame.pack(fill=tk.X, padx=20, pady=10)

        columns = ("Fecha", "Tipo", "Participantes", "Tema", "Estado")
        tree = ttk.Treeview(reuniones_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Tema":
                tree.column(col, width=200, anchor="w")
            else:
                tree.column(col, width=120, anchor="center")

        # Datos de reuniones
        reuniones_data = [
            ("20/01/2025", "Padres", "1º Año A", "Inicio de clases y expectativas", "Confirmada"),
            ("22/01/2025", "Docentes", "Todos", "Planificación curricular", "Programada"),
            ("25/01/2025", "Directivos", "Equipo directivo", "Evaluación trimestral", "Programada")
        ]

        for reunion in reuniones_data:
            tree.insert("", tk.END, values=reunion)

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Calendario de reuniones
        calendario_frame = tk.LabelFrame(frame, text="📅 Calendario de Reuniones", 
                                        font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        calendario_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        calendario_text = """
        📅 CALENDARIO DE REUNIONES - ENERO 2025:
        ═══════════════════════════════════════════
        
        📋 REUNIONES PROGRAMADAS:
        • 20/01 - Reunión Padres 1º Año (18:00)
        • 22/01 - Consejo Docente (14:00)
        • 25/01 - Reunión Directivos (10:00)
        • 28/01 - Evaluación Institucional (16:00)
        
        📊 ESTADÍSTICAS:
        • Asistencia promedio: 87%
        • Reuniones completadas: 8
        • Reuniones pendientes: 4
        • Satisfacción: 9.2/10
        
        📝 PRÓXIMAS FECHAS IMPORTANTES:
        • 01/02 - Inicio período lectivo
        • 05/02 - Reunión con supervisión
        • 10/02 - Jornada pedagógica
        """

        tk.Label(calendario_frame, text=calendario_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_footer(self):
        """Crear pie de página"""
        footer_frame = tk.Frame(self.eventos_window, bg="mediumvioletred", padx=15, pady=8)
        footer_frame.pack(fill=tk.X)
        
        tk.Label(footer_frame, text="GESJ - Sistema Integral de Gestión Educativa | Módulo de Eventos", 
                font=("Arial", 9), bg="mediumvioletred", fg="lightpink").pack()