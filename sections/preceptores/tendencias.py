"""
Análisis de Tendencias Académicas para Preceptores
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

try:
    from server.calificaciones import CalificacionesManager
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class TendenciasAcademicasWindow:
    """Ventana para análisis de tendencias académicas"""
    
    def __init__(self, parent, cal_manager):
        self.parent = parent
        self.cal_manager = cal_manager
        self.create_window()

    def create_window(self):
        """Crear ventana principal de tendencias académicas"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📈 Análisis de Tendencias Académicas")
        self.window.geometry("1340x720")
        self.window.configure(bg="lightsteelblue")

        # Frame principal con scroll
        main_frame = tk.Frame(self.window, bg="lightsteelblue")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

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

        # Título
        title = tk.Label(scrollable_frame, text="📈 Análisis de Tendencias Académicas", 
                        font=("Arial", 18, "bold"), bg="lightsteelblue", fg="darkblue")
        title.pack(pady=15)

        # Panel de métricas
        self.create_metrics_panel(scrollable_frame)
        
        # Notebook con pestañas
        self.create_notebook(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_metrics_panel(self, parent):
        """Crear panel de métricas principales"""
        metrics_frame = tk.LabelFrame(parent, text="📊 Métricas Generales", 
                                     font=("Arial", 12, "bold"), bg="lightsteelblue", 
                                     fg="darkblue", padx=10, pady=8)
        metrics_frame.pack(fill=tk.X, pady=(0, 15))

        metrics_data = [
            ("📈 Promedio General", "8.2", "green", "↗ +0.3"),
            ("📋 Asistencia", "89.7%", "orange", "↘ -1.2%"),
            ("🎯 Aprobación", "94.5%", "green", "↗ +2.1%"),
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

        for i in range(4):
            metrics_frame.grid_columnconfigure(i, weight=1)

    def create_notebook(self, parent):
        """Crear notebook con pestañas"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Pestaña 1: Tendencias por Curso
        self.create_tendencias_curso_tab(notebook)
        
        # Pestaña 2: Análisis por Materia
        self.create_analisis_materia_tab(notebook)
        
        # Pestaña 3: Comparativo Temporal
        self.create_comparativo_temporal_tab(notebook)

    def create_tendencias_curso_tab(self, notebook):
        """Crear pestaña de tendencias por curso"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="📊 Por Curso")

        # Canvas para scroll en la pestaña
        canvas = tk.Canvas(frame, bg="lightblue")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="lightblue")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Contenido
        tk.Label(scrollable_frame, text="📊 Tendencias por Curso y División", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Tabla de tendencias
        columns = ("Curso", "División", "Promedio", "Tendencia", "Asistencia", "En Riesgo")
        tree = ttk.Treeview(scrollable_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        # Datos de ejemplo
        datos_cursos = [
            ("1º Año", "A", "8.4", "↗ +0.2", "92%", "2"),
            ("1º Año", "B", "8.1", "↗ +0.1", "89%", "3"),
            ("2º Año", "A", "8.6", "↗ +0.4", "91%", "1"),
            ("2º Año", "B", "7.9", "↘ -0.1", "87%", "4"),
            ("3º Año", "A", "8.2", "→ 0.0", "88%", "2"),
            ("3º Año", "B", "7.8", "↘ -0.2", "85%", "3")
        ]

        for dato in datos_cursos:
            tree.insert("", tk.END, values=dato)

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_analisis_materia_tab(self, notebook):
        """Crear pestaña de análisis por materia"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="📚 Por Materia")

        # Canvas para scroll
        canvas = tk.Canvas(frame, bg="lightgreen")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="lightgreen")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        tk.Label(scrollable_frame, text="📚 Análisis por Materia", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Gráfico de barras simulado
        materias_data = [
            ("Matemáticas", 8.2, "green"),
            ("Lengua", 8.5, "green"),
            ("Historia", 8.0, "orange"),
            ("Geografía", 7.8, "orange"),
            ("Ciencias", 8.3, "green"),
            ("Física", 7.5, "red"),
            ("Química", 7.7, "orange")
        ]

        for materia, promedio, color in materias_data:
            materia_frame = tk.Frame(scrollable_frame, bg="white", relief=tk.RAISED, bd=1)
            materia_frame.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(materia_frame, text=materia, font=("Arial", 10, "bold"), 
                    bg="white", width=15, anchor="w").pack(side=tk.LEFT, padx=10)
            
            # Barra de progreso simulada
            barra_frame = tk.Frame(materia_frame, bg="lightgray", height=20)
            barra_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)
            
            ancho_barra = int((promedio / 10) * 300)
            barra = tk.Frame(barra_frame, bg=color, height=20, width=ancho_barra)
            barra.pack(side=tk.LEFT)
            
            tk.Label(materia_frame, text=f"{promedio}", font=("Arial", 10, "bold"), 
                    bg="white", fg=color).pack(side=tk.RIGHT, padx=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_comparativo_temporal_tab(self, notebook):
        """Crear pestaña de comparativo temporal"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="📅 Temporal")

        # Canvas para scroll
        canvas = tk.Canvas(frame, bg="lightyellow")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="lightyellow")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        tk.Label(scrollable_frame, text="📅 Evolución Temporal", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Gráfico temporal simulado
        temporal_text = """
        📊 EVOLUCIÓN DEL RENDIMIENTO ACADÉMICO (2024-2025):
        ═══════════════════════════════════════════════════════
        
        Marzo 2024:    ████████░░ 8.0  |  Abril 2024:    ████████░░ 8.1
        Mayo 2024:     ████████░░ 8.2  |  Junio 2024:    ████████░░ 8.0
        Julio 2024:    ████████░░ 8.3  |  Agosto 2024:   ████████░░ 8.1
        Sept 2024:     ████████░░ 8.4  |  Oct 2024:      ████████░░ 8.2
        Nov 2024:      ████████░░ 8.3  |  Dic 2024:      ████████░░ 8.5
        
        📈 TENDENCIAS IDENTIFICADAS:
        ═══════════════════════════════
        • Mejora constante en el segundo cuatrimestre
        • Pico de rendimiento en diciembre (8.5)
        • Estabilidad en el rango 8.0-8.5
        • Proyección 2025: 8.7 (optimista)
        
        🎯 FACTORES DE ÉXITO:
        ═══════════════════════
        • Implementación de planes de intervención: +0.3 pts
        • Mejora en asistencia: +0.2 pts
        • Apoyo familiar: +0.2 pts
        • Recursos tecnológicos: +0.1 pts
        """

        tk.Label(scrollable_frame, text=temporal_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Botones de acción
        buttons_frame = tk.Frame(scrollable_frame, bg="lightyellow")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="📊 Generar Reporte Completo", 
                 bg="#FF9800", fg="white", font=("Arial", 10), width=25).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="📧 Enviar a Directivos", 
                 bg="#2196F3", fg="white", font=("Arial", 10), width=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="📈 Análisis Predictivo", 
                 bg="#9C27B0", fg="white", font=("Arial", 10), width=20).pack(side=tk.LEFT, padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")