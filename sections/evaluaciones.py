"""
Módulo de Evaluaciones Institucionales - GESJ
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
    from server.evaluaciones_operations import EvaluacionesManager
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class EvaluacionesSection:
    """Sección principal de evaluaciones institucionales"""
    
    def __init__(self, root, usuario_id=1, usuario_tipo="Administrativo"):
        self.root = root
        self.usuario_id = usuario_id
        self.usuario_tipo = usuario_tipo
        self.evaluaciones_manager = EvaluacionesManager() if DATABASE_AVAILABLE else None
        self.create_evaluaciones_window()
    
    def create_evaluaciones_window(self):
        """Crear ventana principal de evaluaciones"""
        self.evaluaciones_window = tk.Toplevel(self.root)
        self.evaluaciones_window.title("📊 Sistema de Evaluaciones")
        self.evaluaciones_window.geometry("1340x720")
        self.evaluaciones_window.configure(bg="lightgray")

        self.create_header()
        self.create_main_content()
        self.create_footer()

    def create_header(self):
        """Crear encabezado"""
        header_frame = tk.Frame(self.evaluaciones_window, bg="darkslategray", padx=15, pady=8)
        header_frame.pack(fill=tk.X)

        title = tk.Label(header_frame, text="📊 Sistema de Evaluaciones Institucionales", 
                        font=("Franklin Gothic Heavy", 18, "bold"), bg="darkslategray", fg="white")
        title.pack(pady=5)

        subtitle = tk.Label(header_frame, text="Evaluación Continua y Mejora de la Calidad Educativa", 
                           font=("Arial", 11), bg="darkslategray", fg="lightgray")
        subtitle.pack()

    def create_main_content(self):
        """Crear contenido principal"""
        # Frame principal con scroll
        main_frame = tk.Frame(self.evaluaciones_window, bg="lightgray")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)

        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg="lightgray")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="lightgray")

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
        """Panel de estadísticas de evaluaciones"""
        stats_frame = tk.LabelFrame(parent, text="📊 Estadísticas de Evaluaciones", 
                                   font=("Arial", 12, "bold"), bg="lightgray", 
                                   fg="darkslategray", padx=10, pady=8)
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        stats_data = [
            ("📋 Encuestas Activas", "5", "blue", "En curso"),
            ("👥 Participación", "87%", "green", "Promedio"),
            ("📊 Satisfacción", "8.9/10", "green", "General"),
            ("📈 Mejora Continua", "94%", "green", "Implementada")
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

        # Pestaña 1: Encuestas de Satisfacción
        self.create_encuestas_tab(notebook)
        
        # Pestaña 2: Evaluación de Clima
        self.create_clima_tab(notebook)
        
        # Pestaña 3: Autoevaluación Institucional
        self.create_autoevaluacion_tab(notebook)
        
        # Pestaña 4: Planes de Mejora
        self.create_mejora_tab(notebook)

    def create_encuestas_tab(self, notebook):
        """Crear pestaña de encuestas"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="📋 Encuestas de Satisfacción")

        tk.Label(frame, text="📋 Encuestas de Satisfacción", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Encuestas activas
        encuestas_frame = tk.LabelFrame(frame, text="📊 Encuestas Activas", 
                                       font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        encuestas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Título", "Dirigida a", "Respuestas", "Cierre", "Estado")
        tree = ttk.Treeview(encuestas_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Título":
                tree.column(col, width=200, anchor="w")
            else:
                tree.column(col, width=120, anchor="center")

        # Datos de encuestas
        encuestas_data = [
            ("Satisfacción Docente 2025", "Docentes", "12/15", "31/01/2025", "Activa"),
            ("Clima Institucional", "Toda la comunidad", "89/247", "15/02/2025", "Activa"),
            ("Evaluación de Infraestructura", "Padres", "45/180", "28/01/2025", "Activa")
        ]

        for encuesta in encuestas_data:
            tree.insert("", tk.END, values=encuesta)

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Resultados de encuestas
        resultados_text = """
        📊 RESULTADOS DE ENCUESTAS RECIENTES:
        ═══════════════════════════════════════
        
        👨‍🏫 SATISFACCIÓN DOCENTE (Diciembre 2024):
        • Satisfacción general: 8.7/10
        • Recursos disponibles: 8.2/10
        • Apoyo institucional: 9.1/10
        • Desarrollo profesional: 8.5/10
        
        👨‍👩‍👧‍👦 SATISFACCIÓN FAMILIAS (Noviembre 2024):
        • Comunicación: 8.4/10
        • Calidad educativa: 9.0/10
        • Infraestructura: 7.8/10
        • Atención personalizada: 8.9/10
        
        🎓 SATISFACCIÓN ESTUDIANTES (Octubre 2024):
        • Metodología de enseñanza: 8.6/10
        • Relación con docentes: 9.2/10
        • Actividades extracurriculares: 8.1/10
        • Infraestructura: 7.5/10
        """

        tk.Label(frame, text=resultados_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_clima_tab(self, notebook):
        """Crear pestaña de evaluación de clima"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="🌡️ Clima Institucional")

        tk.Label(frame, text="🌡️ Evaluación de Clima Institucional", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Indicadores de clima
        clima_text = """
        🌡️ EVALUACIÓN DE CLIMA INSTITUCIONAL:
        ═══════════════════════════════════════
        
        📊 INDICADORES PRINCIPALES:
        • Comunicación interna: 8.5/10 ✅
        • Trabajo en equipo: 8.8/10 ✅
        • Liderazgo directivo: 9.0/10 ✅
        • Resolución de conflictos: 8.2/10 ✅
        • Innovación y cambio: 8.4/10 ✅
        
        👥 POR GRUPOS:
        • Docentes: 8.7/10 (Muy satisfecho)
        • Personal administrativo: 8.9/10 (Muy satisfecho)
        • Estudiantes: 8.4/10 (Satisfecho)
        • Familias: 8.6/10 (Muy satisfecho)
        
        🎯 FORTALEZAS IDENTIFICADAS:
        • Excelente liderazgo directivo
        • Comunicación fluida entre niveles
        • Compromiso del personal docente
        • Apoyo a la innovación educativa
        
        ⚠️ ÁREAS DE MEJORA:
        • Infraestructura tecnológica
        • Espacios de recreación
        • Comunicación con familias
        • Actividades extracurriculares
        
        📈 PLAN DE ACCIÓN:
        • Inversión en tecnología: $200,000
        • Mejora de espacios comunes: $150,000
        • Programa de comunicación: En desarrollo
        • Ampliación de actividades: Planificado
        """

        tk.Label(frame, text=clima_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_autoevaluacion_tab(self, notebook):
        """Crear pestaña de autoevaluación"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="🔍 Autoevaluación")

        tk.Label(frame, text="🔍 Autoevaluación Institucional", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Proceso de autoevaluación
        autoevaluacion_text = """
        🔍 PROCESO DE AUTOEVALUACIÓN INSTITUCIONAL:
        ═══════════════════════════════════════════════
        
        📋 DIMENSIONES EVALUADAS:
        • Gestión institucional: 9.1/10 ✅
        • Gestión curricular: 8.8/10 ✅
        • Gestión de recursos: 8.5/10 ✅
        • Gestión del clima: 8.7/10 ✅
        • Gestión de resultados: 9.0/10 ✅
        
        🎯 METODOLOGÍA:
        • Encuestas a todos los actores
        • Análisis de indicadores objetivos
        • Observación de procesos
        • Revisión documental
        • Grupos focales
        
        📊 PARTICIPACIÓN:
        • Docentes: 100% participación
        • Estudiantes: 95% participación
        • Familias: 87% participación
        • Personal administrativo: 100% participación
        
        📈 EVOLUCIÓN HISTÓRICA:
        • 2022: 8.2/10 promedio general
        • 2023: 8.5/10 promedio general (+0.3)
        • 2024: 8.8/10 promedio general (+0.3)
        • Meta 2025: 9.0/10 promedio general
        
        🏆 RECONOCIMIENTOS EXTERNOS:
        • Certificación de Calidad Provincial
        • Premio a la Innovación Educativa
        • Reconocimiento por Inclusión
        """

        tk.Label(frame, text=autoevaluacion_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_mejora_tab(self, notebook):
        """Crear pestaña de planes de mejora"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="📈 Planes de Mejora")

        tk.Label(frame, text="📈 Planes de Mejora Continua", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Planes de mejora activos
        mejora_text = """
        📈 PLANES DE MEJORA CONTINUA 2025:
        ═══════════════════════════════════════
        
        🎯 PLAN 1: MEJORA DE INFRAESTRUCTURA
        • Objetivo: Modernizar aulas y laboratorios
        • Presupuesto: $300,000
        • Plazo: 6 meses
        • Progreso: 25% completado
        • Responsable: Dirección General
        
        📚 PLAN 2: FORTALECIMIENTO PEDAGÓGICO
        • Objetivo: Capacitación docente en nuevas metodologías
        • Presupuesto: $75,000
        • Plazo: 12 meses
        • Progreso: 60% completado
        • Responsable: Coordinación Académica
        
        💻 PLAN 3: DIGITALIZACIÓN EDUCATIVA
        • Objetivo: Implementar aulas virtuales
        • Presupuesto: $150,000
        • Plazo: 8 meses
        • Progreso: 40% completado
        • Responsable: Coordinación TIC
        
        👥 PLAN 4: COMUNICACIÓN INSTITUCIONAL
        • Objetivo: Mejorar comunicación con familias
        • Presupuesto: $25,000
        • Plazo: 4 meses
        • Progreso: 80% completado
        • Responsable: Secretaría Académica
        
        📊 INDICADORES DE SEGUIMIENTO:
        • Reuniones de seguimiento: Mensuales
        • Reportes de progreso: Quincenales
        • Evaluación de impacto: Trimestral
        • Ajustes de planes: Según necesidad
        """

        tk.Label(frame, text=mejora_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_footer(self):
        """Crear pie de página"""
        footer_frame = tk.Frame(self.evaluaciones_window, bg="darkslategray", padx=15, pady=8)
        footer_frame.pack(fill=tk.X)
        
        tk.Label(footer_frame, text="GESJ - Sistema Integral de Gestión Educativa | Módulo de Evaluaciones", 
                font=("Arial", 9), bg="darkslategray", fg="lightgray").pack()