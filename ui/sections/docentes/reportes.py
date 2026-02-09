"""
Reportes y Estadísticas para Docentes
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

class ReportesDocenteWindow:
    """Ventana para reportes y estadísticas de docentes"""
    
    def __init__(self, parent, cal_manager):
        self.parent = parent
        self.cal_manager = cal_manager
        self.create_window()

    def create_window(self):
        """Crear ventana principal de reportes"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📊 Reportes y Estadísticas")
        self.window.geometry("1340x720")
        self.window.configure(bg="lightcyan")

        # Frame principal con scroll
        main_frame = tk.Frame(self.window, bg="lightcyan")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

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

        # Título
        title = tk.Label(scrollable_frame, text="📊 Reportes y Estadísticas Académicas", 
                        font=("Arial", 18, "bold"), bg="lightcyan", fg="darkcyan")
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
        metrics_frame = tk.LabelFrame(parent, text="📈 Métricas de Rendimiento", 
                                     font=("Arial", 12, "bold"), bg="lightcyan", 
                                     fg="darkcyan", padx=10, pady=8)
        metrics_frame.pack(fill=tk.X, pady=(0, 15))

        metrics_data = [
            ("📊 Promedio General", "8.3", "green", "↗ +0.2"),
            ("📝 Calificaciones", "247", "blue", "Total"),
            ("🎯 Aprobación", "94%", "green", "↗ +3%"),
            ("🚨 En Riesgo", "8", "orange", "↘ -2")
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

        # Pestaña 1: Rendimiento por Curso
        self.create_rendimiento_curso_tab(notebook)
        
        # Pestaña 2: Análisis por Materia
        self.create_analisis_materia_tab(notebook)
        
        # Pestaña 3: Estudiantes en Riesgo
        self.create_estudiantes_riesgo_tab(notebook)
        
        # Pestaña 4: Reportes Personalizados
        self.create_reportes_personalizados_tab(notebook)

    def create_rendimiento_curso_tab(self, notebook):
        """Crear pestaña de rendimiento por curso"""
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
        tk.Label(scrollable_frame, text="📊 Rendimiento por Curso", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Tabla de rendimiento
        columns = ("Curso", "División", "Estudiantes", "Promedio", "Aprobados", "En Riesgo")
        tree = ttk.Treeview(scrollable_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        # Datos de ejemplo
        datos_cursos = [
            ("1º Año", "A", "25", "8.4", "23 (92%)", "2"),
            ("1º Año", "B", "24", "8.1", "22 (92%)", "2"),
            ("2º Año", "A", "26", "8.6", "25 (96%)", "1"),
            ("2º Año", "B", "23", "7.9", "21 (91%)", "2"),
            ("3º Año", "A", "22", "8.2", "21 (95%)", "1"),
            ("3º Año", "B", "21", "7.8", "19 (90%)", "2")
        ]

        for dato in datos_cursos:
            tree.insert("", tk.END, values=dato)

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Botones de acción
        buttons_frame = tk.Frame(scrollable_frame, bg="lightblue")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="📊 Generar Reporte", bg="#4CAF50", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📧 Enviar a Directivos", bg="#2196F3", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)

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

        # Análisis detallado por materia
        materias_frame = tk.LabelFrame(scrollable_frame, text="📊 Rendimiento por Materia", 
                                      font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        materias_frame.pack(fill=tk.X, padx=20, pady=10)

        materias_data = [
            ("Matemáticas", "8.2", "92%", "green"),
            ("Lengua y Literatura", "8.5", "96%", "green"),
            ("Ciencias Naturales", "8.0", "88%", "orange"),
            ("Historia", "8.3", "94%", "green"),
            ("Geografía", "7.8", "85%", "orange")
        ]

        for materia, promedio, aprobacion, color in materias_data:
            materia_frame = tk.Frame(materias_frame, bg="white", relief=tk.RAISED, bd=1)
            materia_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(materia_frame, text=materia, font=("Arial", 10, "bold"), 
                    bg="white", width=20, anchor="w").pack(side=tk.LEFT, padx=10)
            
            tk.Label(materia_frame, text=f"Promedio: {promedio}", font=("Arial", 10), 
                    bg="white", fg=color).pack(side=tk.LEFT, padx=20)
            
            tk.Label(materia_frame, text=f"Aprobación: {aprobacion}", font=("Arial", 10), 
                    bg="white", fg=color).pack(side=tk.LEFT, padx=20)

        # Gráfico de tendencias
        tendencias_frame = tk.LabelFrame(scrollable_frame, text="📈 Tendencias Temporales", 
                                        font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        tendencias_frame.pack(fill=tk.X, padx=20, pady=10)

        tendencias_text = """
        📊 EVOLUCIÓN MENSUAL (Últimos 6 meses):
        ═══════════════════════════════════════════
        Agosto:    ████████░░ 8.0  |  Septiembre: ████████░░ 8.1
        Octubre:   ████████░░ 8.2  |  Noviembre:  ████████░░ 8.1
        Diciembre: ████████░░ 8.3  |  Enero:      ████████░░ 8.3
        
        📈 ANÁLISIS DE TENDENCIAS:
        ═══════════════════════════
        • Mejora constante en matemáticas (+0.3)
        • Estabilidad en lengua (8.5 promedio)
        • Leve descenso en ciencias (-0.2)
        • Recuperación en historia (+0.4)
        """

        tk.Label(tendencias_frame, text=tendencias_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_estudiantes_riesgo_tab(self, notebook):
        """Crear pestaña de estudiantes en riesgo"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="🚨 En Riesgo")

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

        tk.Label(scrollable_frame, text="🚨 Estudiantes en Riesgo Académico", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Tabla de estudiantes en riesgo
        riesgo_frame = tk.LabelFrame(scrollable_frame, text="📋 Lista de Estudiantes en Riesgo", 
                                    font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        riesgo_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Estudiante", "Curso", "Promedio", "Materias Críticas", "Última Evaluación", "Acción")
        tree = ttk.Treeview(riesgo_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Estudiante":
                tree.column(col, width=150, anchor="w")
            elif col == "Materias Críticas":
                tree.column(col, width=200, anchor="w")
            else:
                tree.column(col, width=120, anchor="center")

        # Datos de estudiantes en riesgo
        riesgo_data = [
            ("González, Mario", "2º A", "5.8", "Matemáticas, Física", "10/01/2025", "Plan Activo"),
            ("Herrera, Lucas", "3º B", "5.2", "Matemáticas, Química", "08/01/2025", "Crítico"),
            ("Rodríguez, Pedro", "1º B", "5.7", "Lengua, Historia", "12/01/2025", "Seguimiento"),
            ("Martínez, Carlos", "3º A", "6.0", "Física", "15/01/2025", "Mejorando")
        ]

        for data in riesgo_data:
            # Colorear según el nivel de riesgo
            promedio = float(data[2])
            if promedio < 5.5:
                tags = ("critico",)
            elif promedio < 6.0:
                tags = ("alto",)
            else:
                tags = ("moderado",)
            
            tree.insert("", tk.END, values=data, tags=tags)

        # Configurar colores
        tree.tag_configure("critico", background="#FFCDD2")
        tree.tag_configure("alto", background="#FFF3E0")
        tree.tag_configure("moderado", background="#FFF9C4")

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Acciones para estudiantes en riesgo
        acciones_frame = tk.Frame(scrollable_frame, bg="lightyellow")
        acciones_frame.pack(fill=tk.X, pady=10)

        tk.Button(acciones_frame, text="📧 Notificar Preceptores", bg="#FF5722", fg="white", font=("Arial", 10), width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(acciones_frame, text="📞 Contactar Padres", bg="#FF9800", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(acciones_frame, text="📋 Crear Plan", bg="#9C27B0", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_reportes_personalizados_tab(self, notebook):
        """Crear pestaña de reportes personalizados"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="📊 Personalizados")

        # Canvas para scroll
        canvas = tk.Canvas(frame, bg="lightcoral")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="lightcoral")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        tk.Label(scrollable_frame, text="📊 Generador de Reportes Personalizados", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Configurador de reportes
        config_frame = tk.LabelFrame(scrollable_frame, text="⚙️ Configurar Reporte", 
                                    font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        config_frame.pack(fill=tk.X, padx=20, pady=10)

        # Opciones de configuración
        tk.Label(config_frame, text="Tipo de Reporte:", font=("Arial", 10, "bold"), bg="lightcoral").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tipo_combo = ttk.Combobox(config_frame, values=[
            "Rendimiento General", "Por Materia", "Por Período", 
            "Estudiantes en Riesgo", "Comparativo Temporal"
        ], state="readonly", width=25)
        tipo_combo.set("Rendimiento General")
        tipo_combo.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(config_frame, text="Período:", font=("Arial", 10, "bold"), bg="lightcoral").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        periodo_combo = ttk.Combobox(config_frame, values=[
            "Primer Cuatrimestre 2025", "Segundo Cuatrimestre 2024", "Año Completo 2024"
        ], state="readonly", width=25)
        periodo_combo.set("Primer Cuatrimestre 2025")
        periodo_combo.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(config_frame, text="Formato:", font=("Arial", 10, "bold"), bg="lightcoral").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        formato_combo = ttk.Combobox(config_frame, values=["PDF", "Excel", "Word"], state="readonly", width=25)
        formato_combo.set("PDF")
        formato_combo.grid(row=2, column=1, padx=10, pady=5)

        # Botones de generación
        buttons_frame = tk.Frame(config_frame, bg="lightcoral")
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=15)

        tk.Button(buttons_frame, text="📊 Generar Reporte", bg="#4CAF50", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="👁️ Vista Previa", bg="#2196F3", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

        # Plantillas predefinidas
        plantillas_frame = tk.LabelFrame(scrollable_frame, text="📋 Plantillas Predefinidas", 
                                        font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        plantillas_frame.pack(fill=tk.X, padx=20, pady=10)

        plantillas = [
            ("📊 Reporte Mensual Completo", "Incluye todas las métricas del mes"),
            ("🎯 Informe de Rendimiento", "Análisis detallado por curso y materia"),
            ("🚨 Alerta de Riesgo Académico", "Estudiantes que requieren atención"),
            ("📈 Análisis Comparativo", "Comparación con períodos anteriores"),
            ("👨‍👩‍👧‍👦 Reporte para Padres", "Información específica por estudiante")
        ]

        for i, (nombre, descripcion) in enumerate(plantillas):
            plantilla_frame = tk.Frame(plantillas_frame, bg="white", relief=tk.RAISED, bd=1)
            plantilla_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(plantilla_frame, text=nombre, font=("Arial", 10, "bold"), 
                    bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            tk.Label(plantilla_frame, text=descripcion, font=("Arial", 9), 
                    bg="white", fg="gray", anchor="w").pack(side=tk.LEFT, padx=10)
            
            tk.Button(plantilla_frame, text="📄 Usar", bg="#9C27B0", fg="white", 
                     font=("Arial", 8), width=8).pack(side=tk.RIGHT, padx=10, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")