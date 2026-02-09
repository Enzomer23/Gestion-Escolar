"""
Ventana principal para el sistema de Calificaciones
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# Importar módulos específicos de calificaciones
from .registro import RegistroCalificacionesWindow
from .consulta import ConsultaCalificacionesWindow
from .promedios import PromediosAvanzadosWindow
from .estadisticas import EstadisticasWindow
from .reportes import ReportesCalificacionesWindow
from .exportacion import ExportacionWindow
from .alertas import AlertasAcademicasWindow

try:
    from server.calificaciones import CalificacionesManager
    from server.email_notifier import EmailNotifier
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class CalificacionesSection:
    def __init__(self, root, usuario_tipo="Docente", usuario_id=2):
        self.root = root
        self.usuario_tipo = usuario_tipo
        self.usuario_id = usuario_id
        self.cal_manager = CalificacionesManager() if DATABASE_AVAILABLE else None
        self.email_notifier = EmailNotifier() if DATABASE_AVAILABLE else None
        self.create_calificaciones_window()
    
    def create_calificaciones_window(self):
        """Crear ventana principal de calificaciones"""
        self.calificaciones_window = tk.Toplevel(self.root)
        self.calificaciones_window.title("GESJ - Sistema de Calificaciones")
        
        # Optimizado para pantallas 1366x768
        self.calificaciones_window.geometry("1340x720+13+24")
        self.calificaciones_window.configure(bg="lightcyan")

        self.create_header()
        self.create_main_content()
        self.create_footer()

    def create_header(self):
        """Crear encabezado"""
        header_frame = tk.Frame(self.calificaciones_window, bg="darkcyan", padx=15, pady=8)
        header_frame.pack(fill=tk.X)

        title = tk.Label(header_frame, text="📝 Sistema Integral de Calificaciones", 
                        font=("Franklin Gothic Heavy", 18, "bold"), bg="darkcyan", fg="white")
        title.pack(pady=5)

        subtitle = tk.Label(header_frame, text="Gestión Completa de Evaluaciones y Seguimiento Académico", 
                           font=("Arial", 11), bg="darkcyan", fg="lightcyan")
        subtitle.pack()

    def create_main_content(self):
        """Crear contenido principal con funcionalidades"""
        # Frame principal con scroll
        main_frame = tk.Frame(self.calificaciones_window, bg="lightcyan")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)

        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg="lightcyan")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="lightcyan")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Panel de métricas principales
        self.create_metrics_panel(scrollable_frame)
        
        # Panel de funcionalidades principales
        self.create_functions_panel(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_metrics_panel(self, parent):
        """Panel de métricas principales"""
        metrics_frame = tk.LabelFrame(parent, text="📊 Métricas de Calificaciones", 
                                     font=("Arial", 12, "bold"), bg="lightcyan", 
                                     fg="darkcyan", padx=10, pady=8)
        metrics_frame.pack(fill=tk.X, pady=(0, 15))

        # Obtener métricas desde la base de datos
        if DATABASE_AVAILABLE and self.cal_manager:
            try:
                # Aquí podrías obtener métricas reales
                metrics_data = [
                    ("📝 Total Calificaciones", "1,247", "blue", "Registradas"),
                    ("📊 Promedio General", "8.3", "green", "↗ +0.2"),
                    ("🎯 Tasa Aprobación", "94%", "green", "↗ +3%"),
                    ("🚨 Alumnos en Riesgo", "12", "orange", "↘ -3")
                ]
            except:
                metrics_data = [
                    ("📝 Total Calificaciones", "1,247", "blue", "Registradas"),
                    ("📊 Promedio General", "8.3", "green", "↗ +0.2"),
                    ("🎯 Tasa Aprobación", "94%", "green", "↗ +3%"),
                    ("🚨 Alumnos en Riesgo", "12", "orange", "↘ -3")
                ]
        else:
            metrics_data = [
                ("📝 Total Calificaciones", "1,247", "blue", "Registradas"),
                ("📊 Promedio General", "8.3", "green", "↗ +0.2"),
                ("🎯 Tasa Aprobación", "94%", "green", "↗ +3%"),
                ("🚨 Alumnos en Riesgo", "12", "orange", "↘ -3")
            ]

        for i, (label, value, color, info) in enumerate(metrics_data):
            metric_frame = tk.Frame(metrics_frame, bg="white", relief=tk.RAISED, bd=2)
            metric_frame.grid(row=0, column=i, padx=8, pady=5, sticky="ew")
            
            tk.Label(metric_frame, text=label, font=("Arial", 9, "bold"), bg="white").pack()
            tk.Label(metric_frame, text=value, font=("Arial", 16, "bold"), 
                    bg="white", fg=color).pack()
            tk.Label(metric_frame, text=info, font=("Arial", 8), 
                    bg="white", fg="gray").pack()

        # Configurar columnas
        for i in range(4):
            metrics_frame.grid_columnconfigure(i, weight=1)

    def create_functions_panel(self, parent):
        """Panel de funcionalidades principales"""
        functions_frame = tk.LabelFrame(parent, text="🎯 Funcionalidades de Calificaciones", 
                                       font=("Arial", 12, "bold"), bg="lightcyan", 
                                       fg="darkcyan", padx=10, pady=8)
        functions_frame.pack(fill=tk.BOTH, expand=True)

        # Funcionalidades principales
        functions = [
            ("📝 Registro de Calificaciones", self.abrir_registro,
             "Cargar y gestionar calificaciones por materia y período", "#1976D2"),
            ("🔍 Consulta de Calificaciones", self.abrir_consulta,
             "Buscar y revisar calificaciones existentes", "#388E3C"),
            ("📊 Análisis de Promedios", self.abrir_promedios,
             "Análisis avanzado de promedios y estadísticas", "#F57C00"),
            ("📈 Estadísticas Académicas", self.abrir_estadisticas,
             "Estadísticas detalladas por curso y materia", "#7B1FA2"),
            ("📋 Reportes Académicos", self.abrir_reportes,
             "Generación de reportes personalizados", "#D32F2F"),
            ("📤 Exportación de Datos", self.abrir_exportacion,
             "Exportar calificaciones a Excel, PDF y otros formatos", "#455A64"),
            ("🚨 Alertas Académicas", self.abrir_alertas,
             "Sistema de alertas y notificaciones automáticas", "#E65100"),
            ("🎯 Planes de Intervención", self.abrir_planes_intervencion,
             "Crear y gestionar planes para alumnos en riesgo", "#6A1B9A")
        ]

        for i, (title, command, description, color) in enumerate(functions):
            row = i // 2
            col = i % 2
            
            # Frame para cada función
            func_frame = tk.Frame(functions_frame, bg="white", relief=tk.RAISED, bd=2)
            func_frame.grid(row=row, column=col, padx=10, pady=8, sticky="ew")
            
            # Botón principal
            btn = tk.Button(func_frame, text=title, font=("Arial", 11, "bold"),
                           bg=color, fg="white", command=command,
                           width=35, height=2)
            btn.pack(pady=8)
            
            # Descripción
            desc_label = tk.Label(func_frame, text=description, 
                                 font=("Arial", 9), bg="white", fg="gray",
                                 wraplength=280)
            desc_label.pack(pady=(0, 8))

        # Configurar columnas
        for i in range(2):
            functions_frame.grid_columnconfigure(i, weight=1)

    def create_footer(self):
        """Crear pie de página"""
        footer_frame = tk.Frame(self.calificaciones_window, bg="darkcyan", padx=15, pady=8)
        footer_frame.pack(fill=tk.X)
        
        tk.Label(footer_frame, text="GESJ - Sistema Integral de Gestión Educativa | Módulo de Calificaciones", 
                font=("Arial", 9), bg="darkcyan", fg="lightcyan").pack()

    # Métodos para abrir ventanas específicas
    def abrir_registro(self):
        """Abrir ventana de registro de calificaciones"""
        RegistroCalificacionesWindow(self.calificaciones_window, self.cal_manager, self.usuario_id)

    def abrir_consulta(self):
        """Abrir ventana de consulta de calificaciones"""
        ConsultaCalificacionesWindow(self.calificaciones_window, self.cal_manager)

    def abrir_promedios(self):
        """Abrir ventana de análisis de promedios"""
        PromediosAvanzadosWindow(self.calificaciones_window, self.cal_manager)

    def abrir_estadisticas(self):
        """Abrir ventana de estadísticas académicas"""
        EstadisticasWindow(self.calificaciones_window, self.cal_manager)

    def abrir_reportes(self):
        """Abrir ventana de reportes académicos"""
        ReportesCalificacionesWindow(self.calificaciones_window, self.cal_manager)

    def abrir_exportacion(self):
        """Abrir ventana de exportación de datos"""
        ExportacionWindow(self.calificaciones_window, self.cal_manager)

    def abrir_alertas(self):
        """Abrir ventana de alertas académicas"""
        AlertasAcademicasWindow(self.calificaciones_window, self.cal_manager, self.email_notifier)

    def abrir_planes_intervencion(self):
        """Abrir ventana de planes de intervención"""
        from ui.sections.preceptores.planes import PlanesIntervencionWindow
        PlanesIntervencionWindow(self.calificaciones_window, self.cal_manager)