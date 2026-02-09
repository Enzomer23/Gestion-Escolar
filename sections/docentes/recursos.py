"""
Recursos Pedagógicos para Docentes
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

class RecursosDocenteWindow:
    """Ventana para recursos pedagógicos"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_window()

    def create_window(self):
        """Crear ventana principal de recursos"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📚 Recursos Pedagógicos")
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
        title = tk.Label(scrollable_frame, text="📚 Centro de Recursos Pedagógicos", 
                        font=("Arial", 18, "bold"), bg="lightcyan", fg="darkcyan")
        title.pack(pady=15)

        # Panel de estadísticas
        self.create_stats_panel(scrollable_frame)
        
        # Notebook con pestañas
        self.create_notebook(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_stats_panel(self, parent):
        """Crear panel de estadísticas de recursos"""
        stats_frame = tk.LabelFrame(parent, text="📊 Estadísticas de Recursos", 
                                   font=("Arial", 12, "bold"), bg="lightcyan", 
                                   fg="darkcyan", padx=10, pady=8)
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        stats_data = [
            ("📚 Recursos Disponibles", "247", "blue", "Actualizados"),
            ("📥 Descargas", "89", "green", "Este mes"),
            ("⭐ Favoritos", "23", "orange", "Guardados"),
            ("🆕 Nuevos", "12", "purple", "Esta semana")
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
        """Crear notebook con pestañas"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Pestaña 1: Biblioteca Digital
        self.create_biblioteca_tab(notebook)
        
        # Pestaña 2: Planificaciones
        self.create_planificaciones_tab(notebook)
        
        # Pestaña 3: Herramientas Digitales
        self.create_herramientas_tab(notebook)
        
        # Pestaña 4: Capacitación
        self.create_capacitacion_tab(notebook)

    def create_biblioteca_tab(self, notebook):
        """Crear pestaña de biblioteca digital"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="📚 Biblioteca Digital")

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
        tk.Label(scrollable_frame, text="📚 Biblioteca Digital de Recursos", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Búsqueda y filtros
        search_frame = tk.Frame(scrollable_frame, bg="white", relief=tk.RAISED, bd=2)
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(search_frame, text="🔍 Buscar recursos:", font=("Arial", 10, "bold"), bg="white").pack(side=tk.LEFT, padx=10, pady=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Label(search_frame, text="Materia:", font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=10, pady=5)
        materia_combo = ttk.Combobox(search_frame, values=["Todas", "Matemáticas", "Lengua", "Ciencias", "Historia"], state="readonly", width=12)
        materia_combo.set("Todas")
        materia_combo.pack(side=tk.LEFT, padx=5, pady=5)
        
        tk.Button(search_frame, text="Buscar", bg="#2196F3", fg="white", font=("Arial", 9), width=10).pack(side=tk.LEFT, padx=10, pady=5)

        # Categorías de recursos
        categorias = [
            ("📖 Libros de Texto", [
                ("Matemáticas 1º Año - Santillana", "PDF", "15 MB", "⭐⭐⭐⭐⭐"),
                ("Lengua y Literatura - Kapelusz", "PDF", "22 MB", "⭐⭐⭐⭐"),
                ("Ciencias Naturales - Estrada", "PDF", "18 MB", "⭐⭐⭐⭐⭐")
            ]),
            ("📝 Guías de Ejercicios", [
                ("Ejercicios de Álgebra Básica", "PDF", "3 MB", "⭐⭐⭐⭐"),
                ("Comprensión Lectora - Nivel 1", "PDF", "5 MB", "⭐⭐⭐⭐⭐"),
                ("Experimentos de Química", "PDF", "8 MB", "⭐⭐⭐⭐")
            ]),
            ("🎥 Videos Educativos", [
                ("Fracciones y Decimales", "MP4", "120 MB", "⭐⭐⭐⭐⭐"),
                ("Historia Argentina Siglo XX", "MP4", "95 MB", "⭐⭐⭐⭐"),
                ("El Sistema Solar", "MP4", "78 MB", "⭐⭐⭐⭐⭐")
            ])
        ]

        for categoria, recursos in categorias:
            categoria_frame = tk.LabelFrame(scrollable_frame, text=categoria, 
                                           font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
            categoria_frame.pack(fill=tk.X, padx=20, pady=10)

            for i, (nombre, tipo, tamaño, rating) in enumerate(recursos):
                recurso_frame = tk.Frame(categoria_frame, bg="white", relief=tk.RAISED, bd=1)
                recurso_frame.pack(fill=tk.X, padx=10, pady=5)

                tk.Label(recurso_frame, text=nombre, font=("Arial", 10, "bold"), bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
                tk.Label(recurso_frame, text=f"{tipo} - {tamaño}", font=("Arial", 9), bg="white", fg="gray", anchor="center").pack(side=tk.LEFT, padx=5)
                tk.Label(recurso_frame, text=rating, font=("Arial", 9), bg="white", fg="orange", anchor="center").pack(side=tk.LEFT, padx=5)
                tk.Button(recurso_frame, text="📥 Descargar", bg="#4CAF50", fg="white", font=("Arial", 8), width=12).pack(side=tk.RIGHT, padx=10, pady=2)
                tk.Button(recurso_frame, text="⭐ Favorito", bg="#FF9800", fg="white", font=("Arial", 8), width=10).pack(side=tk.RIGHT, padx=5, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_planificaciones_tab(self, notebook):
        """Crear pestaña de planificaciones"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="📋 Planificaciones")

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

        tk.Label(scrollable_frame, text="📋 Planificaciones y Secuencias Didácticas", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Herramientas de planificación
        herramientas_frame = tk.LabelFrame(scrollable_frame, text="🛠️ Herramientas de Planificación", 
                                          font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        herramientas_frame.pack(fill=tk.X, padx=20, pady=10)

        herramientas = [
            ("📝 Generador de Planificaciones", "Crea planificaciones automáticas basadas en contenidos"),
            ("📅 Calendario Académico", "Organiza fechas importantes y evaluaciones"),
            ("🎯 Objetivos de Aprendizaje", "Base de datos de objetivos por materia y nivel"),
            ("📊 Evaluador de Secuencias", "Analiza la coherencia de tus planificaciones")
        ]

        for herramienta, descripcion in herramientas:
            herr_frame = tk.Frame(herramientas_frame, bg="white", relief=tk.RAISED, bd=1)
            herr_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(herr_frame, text=herramienta, font=("Arial", 10, "bold"), 
                    bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            tk.Label(herr_frame, text=descripcion, font=("Arial", 9), 
                    bg="white", fg="gray", anchor="w").pack(side=tk.LEFT, padx=10)
            
            tk.Button(herr_frame, text="🚀 Usar", bg="#4CAF50", fg="white", 
                     font=("Arial", 8), width=8).pack(side=tk.RIGHT, padx=10, pady=2)

        # Plantillas disponibles
        plantillas_frame = tk.LabelFrame(scrollable_frame, text="📄 Plantillas Disponibles", 
                                        font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        plantillas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        plantillas_text = """
        📋 PLANTILLAS DE PLANIFICACIÓN DISPONIBLES:
        ═══════════════════════════════════════════════════
        
        📚 MATEMÁTICAS:
        • Planificación Anual - 1º Año
        • Secuencia: Números Enteros (15 clases)
        • Proyecto: Geometría en la Vida Cotidiana
        • Evaluación: Álgebra Básica
        
        📖 LENGUA Y LITERATURA:
        • Planificación Anual - 1º Año
        • Secuencia: Comprensión Lectora (20 clases)
        • Proyecto: Taller de Escritura Creativa
        • Evaluación: Análisis de Textos
        
        🔬 CIENCIAS NATURALES:
        • Planificación Anual - 1º Año
        • Secuencia: El Método Científico (12 clases)
        • Proyecto: Feria de Ciencias
        • Evaluación: Experimentos Básicos
        
        🌍 CIENCIAS SOCIALES:
        • Planificación Anual - 1º Año
        • Secuencia: Historia Argentina (25 clases)
        • Proyecto: Investigación Histórica
        • Evaluación: Líneas de Tiempo
        
        📊 ESTADÍSTICAS DE USO:
        ═══════════════════════════
        • Plantillas descargadas: 156
        • Más popular: Matemáticas 1º Año
        • Mejor valorada: Comprensión Lectora
        • Última actualización: 10/01/2025
        """

        tk.Label(plantillas_frame, text=plantillas_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_herramientas_tab(self, notebook):
        """Crear pestaña de herramientas digitales"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="🛠️ Herramientas")

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

        tk.Label(scrollable_frame, text="🛠️ Herramientas Digitales Educativas", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Categorías de herramientas
        categorias_herramientas = [
            ("💻 Herramientas de Presentación", [
                ("Canva Educativo", "Diseño de presentaciones y materiales", "Gratuito", "⭐⭐⭐⭐⭐"),
                ("Genially", "Presentaciones interactivas", "Freemium", "⭐⭐⭐⭐"),
                ("Prezi", "Presentaciones dinámicas", "Freemium", "⭐⭐⭐⭐")
            ]),
            ("🎮 Gamificación", [
                ("Kahoot!", "Cuestionarios interactivos", "Freemium", "⭐⭐⭐⭐⭐"),
                ("Quizizz", "Juegos educativos", "Freemium", "⭐⭐⭐⭐"),
                ("Wordwall", "Actividades interactivas", "Freemium", "⭐⭐⭐⭐")
            ]),
            ("📊 Evaluación Digital", [
                ("Google Forms", "Formularios y encuestas", "Gratuito", "⭐⭐⭐⭐⭐"),
                ("Mentimeter", "Encuestas en tiempo real", "Freemium", "⭐⭐⭐⭐"),
                ("Padlet", "Muros colaborativos", "Freemium", "⭐⭐⭐⭐")
            ]),
            ("🎥 Creación de Contenido", [
                ("Loom", "Grabación de pantalla", "Freemium", "⭐⭐⭐⭐⭐"),
                ("Flipgrid", "Videos colaborativos", "Gratuito", "⭐⭐⭐⭐"),
                ("Screencastify", "Grabación y edición", "Freemium", "⭐⭐⭐⭐")
            ])
        ]

        for categoria, herramientas in categorias_herramientas:
            categoria_frame = tk.LabelFrame(scrollable_frame, text=categoria, 
                                           font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
            categoria_frame.pack(fill=tk.X, padx=20, pady=10)

            for herramienta, descripcion, precio, rating in herramientas:
                herr_frame = tk.Frame(categoria_frame, bg="white", relief=tk.RAISED, bd=1)
                herr_frame.pack(fill=tk.X, padx=10, pady=5)

                # Información de la herramienta
                info_frame = tk.Frame(herr_frame, bg="white")
                info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)
                
                tk.Label(info_frame, text=herramienta, font=("Arial", 10, "bold"), bg="white", anchor="w").pack(anchor="w")
                tk.Label(info_frame, text=descripcion, font=("Arial", 9), bg="white", fg="gray", anchor="w").pack(anchor="w")
                
                # Precio y rating
                tk.Label(herr_frame, text=precio, font=("Arial", 9), bg="white", fg="green", anchor="center").pack(side=tk.RIGHT, padx=5)
                tk.Label(herr_frame, text=rating, font=("Arial", 9), bg="white", fg="orange", anchor="center").pack(side=tk.RIGHT, padx=5)
                tk.Button(herr_frame, text="🔗 Acceder", bg="#2196F3", fg="white", font=("Arial", 8), width=10).pack(side=tk.RIGHT, padx=10, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_capacitacion_tab(self, notebook):
        """Crear pestaña de capacitación"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="🎓 Capacitación")

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

        tk.Label(scrollable_frame, text="🎓 Centro de Capacitación Docente", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Cursos disponibles
        cursos_frame = tk.LabelFrame(scrollable_frame, text="📚 Cursos Disponibles", 
                                    font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        cursos_frame.pack(fill=tk.X, padx=20, pady=10)

        cursos_data = [
            ("Tecnología Educativa", "40 hs", "Disponible", "⭐⭐⭐⭐⭐"),
            ("Evaluación por Competencias", "30 hs", "Inscripción abierta", "⭐⭐⭐⭐"),
            ("Neuroeducación", "25 hs", "Próximamente", "⭐⭐⭐⭐⭐"),
            ("Inclusión Educativa", "35 hs", "Disponible", "⭐⭐⭐⭐"),
            ("Gestión del Aula", "20 hs", "Inscripción abierta", "⭐⭐⭐⭐⭐")
        ]

        for curso, duracion, estado, rating in cursos_data:
            curso_frame = tk.Frame(cursos_frame, bg="white", relief=tk.RAISED, bd=1)
            curso_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(curso_frame, text=curso, font=("Arial", 10, "bold"), bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            tk.Label(curso_frame, text=duracion, font=("Arial", 9), bg="white", fg="blue", anchor="center").pack(side=tk.LEFT, padx=5)
            tk.Label(curso_frame, text=estado, font=("Arial", 9), bg="white", fg="green", anchor="center").pack(side=tk.LEFT, padx=5)
            tk.Label(curso_frame, text=rating, font=("Arial", 9), bg="white", fg="orange", anchor="center").pack(side=tk.LEFT, padx=5)
            tk.Button(curso_frame, text="📝 Inscribirse", bg="#4CAF50", fg="white", font=("Arial", 8), width=12).pack(side=tk.RIGHT, padx=10, pady=2)

        # Progreso personal
        progreso_frame = tk.LabelFrame(scrollable_frame, text="📈 Mi Progreso", 
                                      font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        progreso_frame.pack(fill=tk.X, padx=20, pady=10)

        progreso_text = """
        🎓 MI HISTORIAL DE CAPACITACIÓN:
        ═══════════════════════════════════
        
        ✅ CURSOS COMPLETADOS:
        • Didáctica General (2024) - Certificado
        • TIC en el Aula (2024) - Certificado
        • Evaluación Formativa (2023) - Certificado
        
        📚 CURSOS EN PROGRESO:
        • Tecnología Educativa - 75% completado
        • Gestión del Aula - 30% completado
        
        🎯 PRÓXIMOS OBJETIVOS:
        • Neuroeducación (Inscripción: Feb 2025)
        • Inclusión Educativa (Marzo 2025)
        
        📊 ESTADÍSTICAS:
        ═══════════════════
        • Horas de capacitación: 120 hs
        • Certificados obtenidos: 3
        • Promedio de calificación: 9.2/10
        • Ranking institucional: Top 10%
        """

        tk.Label(progreso_frame, text=progreso_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Recursos de capacitación
        recursos_cap_frame = tk.LabelFrame(scrollable_frame, text="📖 Recursos de Capacitación", 
                                          font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        recursos_cap_frame.pack(fill=tk.X, padx=20, pady=10)

        recursos_cap = [
            ("📚 Biblioteca Pedagógica", "Acceso a libros y artículos especializados"),
            ("🎥 Videoteca Educativa", "Videos de capacitación y conferencias"),
            ("📝 Foro de Docentes", "Intercambio de experiencias y consultas"),
            ("📊 Evaluaciones Online", "Tests de autoevaluación y certificación")
        ]

        for recurso, descripcion in recursos_cap:
            rec_frame = tk.Frame(recursos_cap_frame, bg="white", relief=tk.RAISED, bd=1)
            rec_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(rec_frame, text=recurso, font=("Arial", 10, "bold"), 
                    bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            tk.Label(rec_frame, text=descripcion, font=("Arial", 9), 
                    bg="white", fg="gray", anchor="w").pack(side=tk.LEFT, padx=10)
            
            tk.Button(rec_frame, text="🔗 Acceder", bg="#2196F3", fg="white", 
                     font=("Arial", 8), width=10).pack(side=tk.RIGHT, padx=10, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")