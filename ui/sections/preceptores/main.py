"""
Ventana principal para la sección de Preceptores
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# Importar módulos específicos de preceptores
from .tendencias import TendenciasAcademicasWindow
from .trayectorias import TrayectoriasEscolaresWindow
from .planes import PlanesIntervencionWindow
from .reconocimientos import ReconocimientosWindow

try:
    from server.calificaciones import CalificacionesManager
    from server.email_notifier import EmailNotifier
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class PreceptoresSection:
    def __init__(self, root):
        self.root = root
        self.cal_manager = CalificacionesManager() if DATABASE_AVAILABLE else None
        self.email_notifier = EmailNotifier() if DATABASE_AVAILABLE else None
        self.create_preceptores_window()
    
    def create_preceptores_window(self):
        """Crear ventana principal de preceptores"""
        self.preceptores_window = tk.Toplevel(self.root)
        self.preceptores_window.title("GESJ - Panel de Preceptores")
        
        # Optimizado para pantallas 1366x768
        self.preceptores_window.geometry("1340x720+13+24")
        self.preceptores_window.configure(bg="lightsteelblue")

        self.create_header()
        self.create_main_content()
        self.create_footer()

    def create_header(self):
        """Crear encabezado"""
        header_frame = tk.Frame(self.preceptores_window, bg="steelblue", padx=15, pady=8)
        header_frame.pack(fill=tk.X)

        title = tk.Label(header_frame, text="GESJ - Panel Integral de Preceptores", 
                        font=("Franklin Gothic Heavy", 18, "bold"), bg="steelblue", fg="white")
        title.pack(pady=5)

        subtitle = tk.Label(header_frame, text="Sistema de Seguimiento y Gestión Académica", 
                           font=("Arial", 11), bg="steelblue", fg="lightblue")
        subtitle.pack()

    def create_main_content(self):
        """Crear contenido principal con funcionalidades"""
        # Frame principal con scroll
        main_frame = tk.Frame(self.preceptores_window, bg="lightsteelblue")
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
        metrics_frame = tk.LabelFrame(parent, text="📊 Métricas Institucionales", 
                                     font=("Arial", 12, "bold"), bg="lightsteelblue", 
                                     fg="darkblue", padx=10, pady=8)
        metrics_frame.pack(fill=tk.X, pady=(0, 15))

        # Métricas principales
        metrics_data = [
            ("👥 Total Estudiantes", "247", "green", "↗ +3"),
            ("📈 Promedio General", "8.2", "green", "↗ +0.3"),
            ("📋 Asistencia", "89.7%", "orange", "↘ -1.2%"),
            ("🚨 En Riesgo", "12", "red", "↘ -3")
        ]

        for i, (label, value, color, trend) in enumerate(metrics_data):
            metric_frame = tk.Frame(metrics_frame, bg="white", relief=tk.RAISED, bd=2)
            metric_frame.grid(row=0, column=i, padx=8, pady=5, sticky="ew")
            
            tk.Label(metric_frame, text=label, font=("Arial", 9, "bold"), bg="white").pack()
            tk.Label(metric_frame, text=value, font=("Arial", 16, "bold"), 
                    bg="white", fg=color).pack()
            tk.Label(metric_frame, text=trend, font=("Arial", 8), 
                    bg="white", fg="gray").pack()

        # Configurar columnas
        for i in range(4):
            metrics_frame.grid_columnconfigure(i, weight=1)

    def create_functions_panel(self, parent):
        """Panel de funcionalidades principales"""
        functions_frame = tk.LabelFrame(parent, text="🎯 Funcionalidades Principales", 
                                       font=("Arial", 12, "bold"), bg="lightsteelblue", 
                                       fg="darkblue", padx=10, pady=8)
        functions_frame.pack(fill=tk.BOTH, expand=True)

        # Funcionalidades principales
        functions = [
            ("📈 Análisis de Tendencias Académicas", self.abrir_tendencias_academicas,
             "Análisis estadístico del rendimiento por curso y materia", "#1976D2"),
            ("🎯 Seguimiento de Trayectorias Escolares", self.abrir_trayectorias_escolares,
             "Seguimiento integral del progreso de cada estudiante", "#388E3C"),
            ("📋 Gestión de Planes de Intervención", self.abrir_planes_intervencion,
             "Creación y seguimiento de planes personalizados", "#F57C00"),
            ("🏆 Reconocimientos y Méritos", self.abrir_reconocimientos,
             "Gestión de reconocimientos y logros estudiantiles", "#7B1FA2")
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
        footer_frame = tk.Frame(self.preceptores_window, bg="steelblue", padx=15, pady=8)
        footer_frame.pack(fill=tk.X)
        
        tk.Label(footer_frame, text="GESJ - Sistema Integral de Gestión Educativa | Panel de Preceptores", 
                font=("Arial", 9), bg="steelblue", fg="lightblue").pack()

    # Métodos para abrir ventanas específicas
    def abrir_tendencias_academicas(self):
        """Abrir ventana de análisis de tendencias académicas"""
        TendenciasAcademicasWindow(self.preceptores_window, self.cal_manager)

    def abrir_trayectorias_escolares(self):
        """Abrir ventana de seguimiento de trayectorias escolares"""
        TrayectoriasEscolaresWindow(self.preceptores_window, self.cal_manager)

    def abrir_planes_intervencion(self):
        """Abrir ventana de gestión de planes de intervención"""
        PlanesIntervencionWindow(self.preceptores_window, self.cal_manager)

    def abrir_reconocimientos(self):
        """Abrir ventana de reconocimientos y méritos"""
        ReconocimientosWindow(self.preceptores_window, self.cal_manager)