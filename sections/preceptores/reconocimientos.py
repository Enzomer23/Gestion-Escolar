"""
Reconocimientos y Méritos para Preceptores
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

class ReconocimientosWindow:
    """Ventana para gestión de reconocimientos y méritos"""
    
    def __init__(self, parent, cal_manager):
        self.parent = parent
        self.cal_manager = cal_manager
        self.create_window()

    def create_window(self):
        """Crear ventana principal de reconocimientos"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🏆 Reconocimientos y Méritos")
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
        title = tk.Label(scrollable_frame, text="🏆 Sistema de Reconocimientos y Méritos", 
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
        stats_frame = tk.LabelFrame(parent, text="📊 Estadísticas de Reconocimientos", 
                                   font=("Arial", 12, "bold"), bg="lightsteelblue", 
                                   fg="darkblue", padx=10, pady=8)
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        stats_data = [
            ("🏆 Total Reconocimientos", "47", "gold", "Este año"),
            ("👥 Estudiantes Reconocidos", "32", "green", "Únicos"),
            ("📈 Promedio Mensual", "8", "blue", "↗ +15%"),
            ("🎯 Meta Anual", "75", "orange", "63% completado")
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
        tk.Label(filters_frame, text="Curso:", font=("Arial", 10), bg="lightsteelblue").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        curso_combo = ttk.Combobox(filters_frame, values=["Todos", "1º Año", "2º Año", "3º Año"], state="readonly", width=12)
        curso_combo.set("Todos")
        curso_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filters_frame, text="Tipo:", font=("Arial", 10), bg="lightsteelblue").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        tipo_combo = ttk.Combobox(filters_frame, values=["Todos", "Académico", "Deportivo", "Artístico", "Social"], state="readonly", width=12)
        tipo_combo.set("Todos")
        tipo_combo.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(filters_frame, text="Período:", font=("Arial", 10), bg="lightsteelblue").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        periodo_combo = ttk.Combobox(filters_frame, values=["2025", "2024", "Todo"], state="readonly", width=12)
        periodo_combo.set("2025")
        periodo_combo.grid(row=0, column=5, padx=5, pady=5)

        tk.Button(filters_frame, text="🔍 Filtrar", bg="#2196F3", fg="white", font=("Arial", 10), width=10).grid(row=0, column=6, padx=10, pady=5)

    def create_notebook(self, parent):
        """Crear notebook con pestañas"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Pestaña 1: Otorgar Reconocimiento
        self.create_otorgar_tab(notebook)
        
        # Pestaña 2: Historial
        self.create_historial_tab(notebook)
        
        # Pestaña 3: Candidatos
        self.create_candidatos_tab(notebook)
        
        # Pestaña 4: Estadísticas
        self.create_estadisticas_tab(notebook)

    def create_otorgar_tab(self, notebook):
        """Crear pestaña para otorgar reconocimientos"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="🏆 Otorgar Reconocimiento")

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
        tk.Label(scrollable_frame, text="🏆 Otorgar Nuevo Reconocimiento", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Formulario
        form_frame = tk.LabelFrame(scrollable_frame, text="📝 Datos del Reconocimiento", 
                                  font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        form_frame.pack(fill=tk.X, padx=20, pady=10)

        # Campos del formulario
        tk.Label(form_frame, text="Estudiante:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        estudiante_combo = ttk.Combobox(form_frame, values=[
            "Pérez, Juan (1º A)", "Gómez, Ana (2º A)", "Díaz, Laura (1º A)",
            "Castro, Julia (1º B)", "Ramírez, Sofía (3º A)"
        ], state="readonly", width=40)
        estudiante_combo.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form_frame, text="Tipo de Reconocimiento:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tipo_combo = ttk.Combobox(form_frame, values=[
            "Excelencia Académica", "Mejor Compañero", "Deportista Destacado",
            "Talento Artístico", "Liderazgo", "Mejora Continua", "Solidaridad"
        ], state="readonly", width=40)
        tipo_combo.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form_frame, text="Motivo:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=2, column=0, padx=10, pady=5, sticky="nw")
        motivo_text = tk.Text(form_frame, width=50, height=4)
        motivo_text.insert("1.0", "Descripción del motivo del reconocimiento...")
        motivo_text.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form_frame, text="Fecha:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        fecha_entry = tk.Entry(form_frame, width=20)
        fecha_entry.insert(0, "16/01/2025")
        fecha_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Botones del formulario
        form_buttons_frame = tk.Frame(scrollable_frame, bg="lightblue")
        form_buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(form_buttons_frame, text="🏆 Otorgar Reconocimiento", bg="#4CAF50", fg="white", font=("Arial", 10), width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(form_buttons_frame, text="🗑️ Limpiar", bg="#FF5722", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)

        # Lista de reconocimientos recientes
        recent_frame = tk.LabelFrame(scrollable_frame, text="📋 Reconocimientos Recientes", 
                                    font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Tabla de reconocimientos recientes
        columns = ("Fecha", "Estudiante", "Tipo", "Motivo")
        tree = ttk.Treeview(recent_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Fecha":
                tree.column(col, width=100, anchor="center")
            elif col == "Estudiante":
                tree.column(col, width=150, anchor="w")
            elif col == "Tipo":
                tree.column(col, width=150, anchor="center")
            else:
                tree.column(col, width=200, anchor="w")

        # Datos recientes
        recent_data = [
            ("15/01/2025", "Díaz, Laura", "Excelencia Académica", "Promedio 9.0 en primer cuatrimestre"),
            ("14/01/2025", "Castro, Julia", "Mejor Compañero", "Ayuda constante a compañeros"),
            ("13/01/2025", "Pérez, Juan", "Mejora Continua", "Progreso notable en matemáticas")
        ]

        for data in recent_data:
            tree.insert("", tk.END, values=data)

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_historial_tab(self, notebook):
        """Crear pestaña de historial"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="📚 Historial")

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

        tk.Label(scrollable_frame, text="📚 Historial Completo de Reconocimientos", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Búsqueda
        search_frame = tk.Frame(scrollable_frame, bg="white", relief=tk.RAISED, bd=2)
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(search_frame, text="🔍 Buscar por estudiante:", font=("Arial", 10, "bold"), bg="white").pack(side=tk.LEFT, padx=10, pady=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(search_frame, text="Buscar", bg="#2196F3", fg="white", font=("Arial", 9), width=10).pack(side=tk.LEFT, padx=5, pady=5)

        # Tabla de historial completo
        historial_frame = tk.LabelFrame(scrollable_frame, text="📋 Todos los Reconocimientos", 
                                       font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        historial_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("ID", "Fecha", "Estudiante", "Curso", "Tipo", "Motivo")
        tree = ttk.Treeview(historial_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "ID":
                tree.column(col, width=50, anchor="center")
            elif col == "Fecha":
                tree.column(col, width=100, anchor="center")
            elif col == "Estudiante":
                tree.column(col, width=150, anchor="w")
            elif col == "Curso":
                tree.column(col, width=80, anchor="center")
            elif col == "Tipo":
                tree.column(col, width=150, anchor="center")
            else:
                tree.column(col, width=200, anchor="w")

        # Datos de historial
        historial_data = [
            ("R047", "15/01/2025", "Díaz, Laura", "1º A", "Excelencia Académica", "Promedio 9.0 en primer cuatrimestre"),
            ("R046", "14/01/2025", "Castro, Julia", "1º B", "Mejor Compañero", "Ayuda constante a compañeros"),
            ("R045", "13/01/2025", "Pérez, Juan", "1º A", "Mejora Continua", "Progreso notable en matemáticas"),
            ("R044", "10/01/2025", "Gómez, Ana", "2º A", "Excelencia Académica", "Mejor promedio del curso"),
            ("R043", "08/01/2025", "Ramírez, Sofía", "3º A", "Liderazgo", "Organización de actividades solidarias"),
            ("R042", "05/01/2025", "Fernández, María", "2º B", "Deportista Destacado", "Campeona inter-escolar de atletismo"),
            ("R041", "03/01/2025", "López, Diego", "1º A", "Talento Artístico", "Presentación destacada en acto escolar"),
            ("R040", "28/12/2024", "Morales, Valentina", "2º A", "Solidaridad", "Campaña de ayuda a compañeros")
        ]

        for data in historial_data:
            tree.insert("", tk.END, values=data)

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_candidatos_tab(self, notebook):
        """Crear pestaña de candidatos"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="⭐ Candidatos")

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

        tk.Label(scrollable_frame, text="⭐ Candidatos para Reconocimientos", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Candidatos por categoría
        categorias = [
            ("🏆 Excelencia Académica", [
                ("Morales, Valentina (2º A)", "Promedio: 9.2", "Todas las materias > 8.5"),
                ("Silva, Mateo (1º A)", "Promedio: 8.9", "Mejora constante"),
                ("Torres, Camila (1º A)", "Promedio: 8.7", "Destacada en ciencias")
            ]),
            ("🤝 Mejor Compañero", [
                ("Vega, Nicolás (1º A)", "Ayuda a compañeros", "Siempre disponible"),
                ("Jiménez, Martina (1º B)", "Integra nuevos alumnos", "Líder natural"),
                ("Sánchez, Emilia (2º A)", "Resuelve conflictos", "Mediadora efectiva")
            ]),
            ("🏃 Deportista Destacado", [
                ("Acosta, Valentino (1º B)", "Atletismo", "Récord escolar en 100m"),
                ("Mendoza, Thiago (1º B)", "Fútbol", "Goleador del torneo"),
                ("Cabrera, Renata (1º B)", "Natación", "Clasificada a provinciales")
            ])
        ]

        for categoria, candidatos in categorias:
            categoria_frame = tk.LabelFrame(scrollable_frame, text=categoria, 
                                           font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
            categoria_frame.pack(fill=tk.X, padx=20, pady=10)

            for i, (nombre, logro, detalle) in enumerate(candidatos):
                candidato_frame = tk.Frame(categoria_frame, bg="white", relief=tk.RAISED, bd=1)
                candidato_frame.pack(fill=tk.X, padx=10, pady=5)

                tk.Label(candidato_frame, text=nombre, font=("Arial", 10, "bold"), bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
                tk.Label(candidato_frame, text=logro, font=("Arial", 9), bg="white", fg="green", anchor="center").pack(side=tk.LEFT, padx=5)
                tk.Label(candidato_frame, text=detalle, font=("Arial", 8), bg="white", fg="gray", anchor="center").pack(side=tk.LEFT, padx=5)
                tk.Button(candidato_frame, text="🏆 Reconocer", bg="#4CAF50", fg="white", font=("Arial", 8), width=12).pack(side=tk.RIGHT, padx=10, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_estadisticas_tab(self, notebook):
        """Crear pestaña de estadísticas"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="📊 Estadísticas")

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

        tk.Label(scrollable_frame, text="📊 Estadísticas de Reconocimientos", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Distribución por tipo
        distribucion_frame = tk.LabelFrame(scrollable_frame, text="📈 Distribución por Tipo", 
                                          font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        distribucion_frame.pack(fill=tk.X, padx=20, pady=10)

        tipos_data = [
            ("Excelencia Académica", 18, "gold"),
            ("Mejor Compañero", 12, "green"),
            ("Deportista Destacado", 8, "blue"),
            ("Mejora Continua", 5, "orange"),
            ("Liderazgo", 3, "purple"),
            ("Solidaridad", 1, "red")
        ]

        for tipo, cantidad, color in tipos_data:
            tipo_frame = tk.Frame(distribucion_frame, bg="white", relief=tk.RAISED, bd=1)
            tipo_frame.pack(fill=tk.X, padx=10, pady=3)
            
            tk.Label(tipo_frame, text=tipo, font=("Arial", 10), bg="white", width=20, anchor="w").pack(side=tk.LEFT, padx=10)
            
            # Barra de progreso
            max_cantidad = 18
            barra_frame = tk.Frame(tipo_frame, bg="lightgray", height=20, width=200)
            barra_frame.pack(side=tk.LEFT, padx=10, pady=5)
            barra_frame.pack_propagate(False)
            
            barra = tk.Frame(barra_frame, bg=color, height=20)
            barra.place(x=0, y=0, width=int(200 * cantidad / max_cantidad), height=20)
            
            tk.Label(tipo_frame, text=f"{cantidad}", font=("Arial", 10, "bold"), bg="white", fg=color, width=5).pack(side=tk.RIGHT, padx=10)

        # Estadísticas por curso
        curso_stats_frame = tk.LabelFrame(scrollable_frame, text="🎓 Estadísticas por Curso", 
                                         font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        curso_stats_frame.pack(fill=tk.X, padx=20, pady=10)

        curso_stats_text = """
        📊 RECONOCIMIENTOS POR CURSO:
        ═══════════════════════════════════
        1º Año A: 18 reconocimientos (38%)
        1º Año B: 12 reconocimientos (26%)
        2º Año A: 10 reconocimientos (21%)
        2º Año B: 5 reconocimientos (11%)
        3º Año A: 2 reconocimientos (4%)
        3º Año B: 0 reconocimientos (0%)
        
        📈 PROYECCIONES ANUALES:
        ═══════════════════════════════
        Meta anual: 75 reconocimientos
        Progreso actual: 47 (63%)
        Proyección: 72 reconocimientos
        Probabilidad de cumplimiento: 92%
        
        📅 TENDENCIAS MENSUALES:
        ═══════════════════════════════
        Enero: 8 reconocimientos (+15%)
        Diciembre: 7 reconocimientos
        Noviembre: 6 reconocimientos
        Promedio mensual: 6.7
        """

        tk.Label(curso_stats_frame, text=curso_stats_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones de reportes
        reports_buttons_frame = tk.Frame(scrollable_frame, bg="lightcoral")
        reports_buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(reports_buttons_frame, text="📊 Generar Reporte Completo", bg="#4CAF50", fg="white", font=("Arial", 10), width=25).pack(side=tk.LEFT, padx=5)
        tk.Button(reports_buttons_frame, text="📧 Enviar a Directivos", bg="#2196F3", fg="white", font=("Arial", 10), width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(reports_buttons_frame, text="🏆 Ceremonia de Reconocimiento", bg="#9C27B0", fg="white", font=("Arial", 10), width=25).pack(side=tk.LEFT, padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")