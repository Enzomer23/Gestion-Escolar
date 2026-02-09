"""
Gestión de Planes de Intervención para Preceptores
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

class PlanesIntervencionWindow:
    """Ventana para gestión de planes de intervención"""
    
    def __init__(self, parent, cal_manager):
        self.parent = parent
        self.cal_manager = cal_manager
        self.create_window()

    def create_window(self):
        """Crear ventana principal de planes de intervención"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📋 Gestión de Planes de Intervención")
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
        title = tk.Label(scrollable_frame, text="📋 Gestión de Planes de Intervención", 
                        font=("Arial", 18, "bold"), bg="lightsteelblue", fg="darkblue")
        title.pack(pady=15)

        # Panel de estadísticas
        self.create_stats_panel(scrollable_frame)
        
        # Panel de filtros
        self.create_filters_panel(scrollable_frame)
        
        # Notebook con pestañas
        self.create_notebook(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_stats_panel(self, parent):
        """Crear panel de estadísticas"""
        stats_frame = tk.LabelFrame(parent, text="📊 Estadísticas de Planes", 
                                   font=("Arial", 12, "bold"), bg="lightsteelblue", 
                                   fg="darkblue", padx=10, pady=8)
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        stats_data = [
            ("📋 Planes Activos", "12", "blue", "En curso"),
            ("✅ Completados", "8", "green", "Este mes"),
            ("🎯 Tasa de Éxito", "85%", "green", "↗ +5%"),
            ("⏱️ Promedio Duración", "6 sem", "orange", "Estándar")
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

    def create_filters_panel(self, parent):
        """Crear panel de filtros"""
        filters_frame = tk.LabelFrame(parent, text="🔍 Filtros", 
                                     font=("Arial", 12, "bold"), bg="lightsteelblue", 
                                     fg="darkblue", padx=10, pady=8)
        filters_frame.pack(fill=tk.X, pady=(0, 15))

        # Filtros
        tk.Label(filters_frame, text="Estado:", font=("Arial", 10), bg="lightsteelblue").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        estado_combo = ttk.Combobox(filters_frame, values=["Todos", "Activo", "Completado", "Suspendido"], state="readonly", width=12)
        estado_combo.set("Todos")
        estado_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filters_frame, text="Prioridad:", font=("Arial", 10), bg="lightsteelblue").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        prioridad_combo = ttk.Combobox(filters_frame, values=["Todas", "Alta", "Media", "Baja"], state="readonly", width=12)
        prioridad_combo.set("Todas")
        prioridad_combo.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(filters_frame, text="Curso:", font=("Arial", 10), bg="lightsteelblue").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        curso_combo = ttk.Combobox(filters_frame, values=["Todos", "1º Año", "2º Año", "3º Año"], state="readonly", width=12)
        curso_combo.set("Todos")
        curso_combo.grid(row=0, column=5, padx=5, pady=5)

        tk.Button(filters_frame, text="🔍 Filtrar", bg="#2196F3", fg="white", font=("Arial", 10), width=10).grid(row=0, column=6, padx=10, pady=5)

    def create_notebook(self, parent):
        """Crear notebook con pestañas"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Pestaña 1: Lista de Planes
        self.create_lista_planes_tab(notebook)
        
        # Pestaña 2: Crear Plan
        self.create_crear_plan_tab(notebook)
        
        # Pestaña 3: Seguimiento
        self.create_seguimiento_tab(notebook)
        
        # Pestaña 4: Evaluación
        self.create_evaluacion_tab(notebook)
        
        # Pestaña 5: Reportes
        self.create_reportes_tab(notebook)

    def create_lista_planes_tab(self, notebook):
        """Crear pestaña de lista de planes"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="📋 Lista de Planes")

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
        tk.Label(scrollable_frame, text="📋 Planes de Intervención Activos", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Tabla de planes
        columns = ("ID", "Estudiante", "Curso", "Tipo", "Prioridad", "Estado", "Progreso", "Acciones")
        tree = ttk.Treeview(scrollable_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "ID":
                tree.column(col, width=50, anchor="center")
            elif col == "Estudiante":
                tree.column(col, width=150, anchor="w")
            elif col == "Acciones":
                tree.column(col, width=120, anchor="center")
            else:
                tree.column(col, width=100, anchor="center")

        # Datos de ejemplo
        planes_data = [
            ("P001", "González, Mario", "2º A", "Académico", "Alta", "Activo", "65%", "Ver | Editar"),
            ("P002", "Herrera, Lucas", "3º B", "Integral", "Crítica", "Activo", "40%", "Ver | Editar"),
            ("P003", "Rodríguez, Pedro", "1º B", "Asistencia", "Alta", "Activo", "80%", "Ver | Editar"),
            ("P004", "Martínez, Carlos", "3º A", "Conductual", "Media", "Seguimiento", "90%", "Ver | Progreso"),
            ("P005", "López, Ana", "2º B", "Académico", "Media", "Completado", "100%", "Ver | Reporte")
        ]

        for plan in planes_data:
            # Colorear filas según prioridad
            prioridad = plan[4]
            if prioridad == "Crítica":
                tags = ("critica",)
            elif prioridad == "Alta":
                tags = ("alta",)
            else:
                tags = ()
            
            tree.insert("", tk.END, values=plan, tags=tags)

        # Configurar colores
        tree.tag_configure("critica", background="#FFCDD2")
        tree.tag_configure("alta", background="#FFF3E0")

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Botones de acción
        buttons_frame = tk.Frame(scrollable_frame, bg="lightblue")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="👁️ Ver Detalle", bg="#2196F3", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="✏️ Editar Plan", bg="#FF9800", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📈 Ver Progreso", bg="#4CAF50", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_crear_plan_tab(self, notebook):
        """Crear pestaña de crear plan"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="🆕 Crear Plan")

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

        tk.Label(scrollable_frame, text="🆕 Crear Nuevo Plan de Intervención", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Formulario de creación
        form_frame = tk.LabelFrame(scrollable_frame, text="📝 Información del Plan", 
                                  font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        form_frame.pack(fill=tk.X, padx=20, pady=10)

        # Campos del formulario
        fields = [
            ("Estudiante:", "combobox", ["González, Mario (2º A)", "Herrera, Lucas (3º B)", "Rodríguez, Pedro (1º B)"]),
            ("Tipo de Plan:", "combobox", ["Académico", "Asistencia", "Conductual", "Integral"]),
            ("Prioridad:", "combobox", ["Baja", "Media", "Alta", "Crítica"]),
            ("Duración (semanas):", "entry", "8"),
            ("Fecha de Inicio:", "entry", "16/01/2025"),
            ("Objetivo Principal:", "text", "Mejorar rendimiento académico en matemáticas y física"),
            ("Estrategias:", "text", "1. Tutorías personalizadas\n2. Apoyo familiar\n3. Seguimiento semanal")
        ]

        for i, (label, field_type, default) in enumerate(fields):
            tk.Label(form_frame, text=label, font=("Arial", 10, "bold"), bg="lightgreen").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            
            if field_type == "combobox":
                widget = ttk.Combobox(form_frame, values=default, state="readonly", width=40)
                if isinstance(default, list) and default:
                    widget.set(default[0])
            elif field_type == "text":
                widget = tk.Text(form_frame, width=50, height=3)
                widget.insert("1.0", default)
            else:
                widget = tk.Entry(form_frame, width=50)
                widget.insert(0, default)
            
            widget.grid(row=i, column=1, padx=10, pady=5, sticky="w")

        # Botones del formulario
        form_buttons_frame = tk.Frame(scrollable_frame, bg="lightgreen")
        form_buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(form_buttons_frame, text="💾 Guardar Plan", bg="#4CAF50", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(form_buttons_frame, text="🗑️ Limpiar", bg="#FF5722", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(form_buttons_frame, text="👁️ Vista Previa", bg="#2196F3", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_seguimiento_tab(self, notebook):
        """Crear pestaña de seguimiento"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="📊 Seguimiento")

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

        tk.Label(scrollable_frame, text="📊 Seguimiento de Progreso", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Selección de plan
        selection_frame = tk.Frame(scrollable_frame, bg="white", relief=tk.RAISED, bd=2)
        selection_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(selection_frame, text="Seleccionar Plan:", font=("Arial", 12, "bold"), bg="white").pack(pady=5)
        plan_combo = ttk.Combobox(selection_frame, values=[
            "P001 - González, Mario (Académico)",
            "P002 - Herrera, Lucas (Integral)",
            "P003 - Rodríguez, Pedro (Asistencia)"
        ], state="readonly", width=50)
        plan_combo.set("P001 - González, Mario (Académico)")
        plan_combo.pack(pady=5)

        # Progreso por objetivos
        progress_frame = tk.LabelFrame(scrollable_frame, text="🎯 Progreso por Objetivos", 
                                      font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        progress_frame.pack(fill=tk.X, padx=20, pady=10)

        objetivos_data = [
            ("Mejorar promedio en Matemáticas", 70, "orange"),
            ("Aumentar asistencia a clases", 85, "green"),
            ("Completar tareas asignadas", 60, "red"),
            ("Participación en clase", 90, "green")
        ]

        for objetivo, progreso, color in objetivos_data:
            obj_frame = tk.Frame(progress_frame, bg="white", relief=tk.RAISED, bd=1)
            obj_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(obj_frame, text=objetivo, font=("Arial", 10), bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            # Barra de progreso
            progress_bar_frame = tk.Frame(obj_frame, bg="lightgray", height=20, width=200)
            progress_bar_frame.pack(side=tk.RIGHT, padx=10, pady=5)
            progress_bar_frame.pack_propagate(False)
            
            progress_bar = tk.Frame(progress_bar_frame, bg=color, height=20)
            progress_bar.place(x=0, y=0, width=int(200 * progreso / 100), height=20)
            
            tk.Label(obj_frame, text=f"{progreso}%", font=("Arial", 10, "bold"), bg="white", fg=color, width=8).pack(side=tk.RIGHT, padx=5)

        # Actividades realizadas
        activities_frame = tk.LabelFrame(scrollable_frame, text="✅ Actividades Realizadas", 
                                        font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        activities_frame.pack(fill=tk.X, padx=20, pady=10)

        activities_text = """
        📅 SEMANA 1 (02-08 Enero):
        • ✅ Tutoría de matemáticas (3 sesiones)
        • ✅ Reunión con padres
        • ✅ Evaluación inicial
        
        📅 SEMANA 2 (09-15 Enero):
        • ✅ Seguimiento de tareas diarias
        • ✅ Apoyo en física
        • ⏳ Evaluación parcial (pendiente)
        
        📅 PRÓXIMAS ACTIVIDADES:
        • 🔄 Evaluación de progreso (20/01)
        • 🔄 Reunión con docentes (22/01)
        • 🔄 Ajuste de estrategias (25/01)
        """

        tk.Label(activities_frame, text=activities_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_evaluacion_tab(self, notebook):
        """Crear pestaña de evaluación"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="📊 Evaluación")

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

        tk.Label(scrollable_frame, text="📊 Evaluación de Efectividad", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Métricas cuantitativas
        metrics_frame = tk.LabelFrame(scrollable_frame, text="📈 Métricas Cuantitativas", 
                                     font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        metrics_frame.pack(fill=tk.X, padx=20, pady=10)

        metrics_text = """
        📊 MEJORAS MEDIBLES:
        ═══════════════════════════════════
        • Promedio Matemáticas: 5.5 → 6.8 (+1.3 pts)
        • Promedio Física: 6.0 → 7.2 (+1.2 pts)
        • Asistencia: 78% → 90% (+12%)
        • Tareas completadas: 60% → 95% (+35%)
        • Participación en clase: 40% → 85% (+45%)
        
        📈 TENDENCIA GENERAL:
        ═══════════════════════════
        • Mejora sostenida durante 4 semanas
        • Pico de rendimiento en semana 3
        • Estabilización en niveles aceptables
        """

        tk.Label(metrics_frame, text=metrics_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Evaluación cualitativa
        qualitative_frame = tk.LabelFrame(scrollable_frame, text="📝 Evaluación Cualitativa", 
                                         font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        qualitative_frame.pack(fill=tk.X, padx=20, pady=10)

        qualitative_text = """
        ✅ LOGROS PRINCIPALES:
        ═══════════════════════════
        • Mayor confianza en matemáticas
        • Mejor organización del tiempo de estudio
        • Comunicación más fluida con docentes
        • Apoyo familiar más estructurado
        
        ⚠️ ÁREAS QUE REQUIEREN ATENCIÓN:
        ═══════════════════════════════════════
        • Mantener constancia en el estudio
        • Reforzar conceptos de física
        • Continuar con apoyo tutorial
        
        💡 RECOMENDACIONES:
        ═══════════════════════════
        • Continuar plan por 4 semanas más
        • Reducir frecuencia de tutorías gradualmente
        • Implementar autoevaluación semanal
        """

        tk.Label(qualitative_frame, text=qualitative_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_reportes_tab(self, notebook):
        """Crear pestaña de reportes"""
        frame = tk.Frame(notebook, bg="lightgray")
        notebook.add(frame, text="📊 Reportes")

        # Canvas para scroll
        canvas = tk.Canvas(frame, bg="lightgray")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="lightgray")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        tk.Label(scrollable_frame, text="📊 Reportes y Estadísticas", 
                font=("Arial", 14, "bold"), bg="lightgray", fg="darkslategray").pack(pady=10)

        # Estadísticas generales
        general_stats_frame = tk.LabelFrame(scrollable_frame, text="📈 Estadísticas Generales", 
                                           font=("Arial", 12, "bold"), bg="lightgray", fg="darkslategray")
        general_stats_frame.pack(fill=tk.X, padx=20, pady=10)

        general_stats_text = """
        📊 RESUMEN EJECUTIVO:
        ═══════════════════════════════════
        • Total de planes creados: 20
        • Planes activos: 12
        • Planes completados exitosamente: 8
        • Tasa de éxito general: 85%
        • Tiempo promedio de duración: 6 semanas
        
        📈 EFECTIVIDAD POR TIPO:
        ═══════════════════════════════
        • Planes Académicos: 90% éxito (9/10)
        • Planes de Asistencia: 85% éxito (6/7)
        • Planes Integrales: 80% éxito (4/5)
        • Planes Conductuales: 75% éxito (3/4)
        
        🎯 FACTORES DE ÉXITO:
        ═══════════════════════════
        • Participación familiar: 0.89 correlación
        • Asistencia regular: 0.85 correlación
        • Apoyo docente: 0.82 correlación
        • Motivación del estudiante: 0.78 correlación
        """

        tk.Label(general_stats_frame, text=general_stats_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones de reportes
        reports_buttons_frame = tk.Frame(scrollable_frame, bg="lightgray")
        reports_buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(reports_buttons_frame, text="📊 Reporte Completo", bg="#4CAF50", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(reports_buttons_frame, text="📧 Enviar a Directivos", bg="#2196F3", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(reports_buttons_frame, text="📈 Análisis Predictivo", bg="#9C27B0", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")