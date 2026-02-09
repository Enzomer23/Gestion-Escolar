"""
Módulo de Biblioteca - GESJ
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
    from server.biblioteca_operations import BibliotecaManager
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class BibliotecaSection:
    """Sección principal de gestión de biblioteca"""
    
    def __init__(self, root, usuario_tipo="Docente"):
        self.root = root
        self.usuario_tipo = usuario_tipo
        self.biblioteca_manager = BibliotecaManager() if DATABASE_AVAILABLE else None
        self.create_biblioteca_window()
    
    def create_biblioteca_window(self):
        """Crear ventana principal de biblioteca"""
        self.biblioteca_window = tk.Toplevel(self.root)
        self.biblioteca_window.title("📚 Sistema de Biblioteca")
        self.biblioteca_window.geometry("1340x720")
        self.biblioteca_window.configure(bg="lightyellow")

        self.create_header()
        self.create_main_content()
        self.create_footer()

    def create_header(self):
        """Crear encabezado"""
        header_frame = tk.Frame(self.biblioteca_window, bg="goldenrod", padx=15, pady=8)
        header_frame.pack(fill=tk.X)

        title = tk.Label(header_frame, text="📚 Sistema Integral de Biblioteca", 
                        font=("Franklin Gothic Heavy", 18, "bold"), bg="goldenrod", fg="white")
        title.pack(pady=5)

        subtitle = tk.Label(header_frame, text="Gestión de Recursos Didácticos y Biblioteca Digital", 
                           font=("Arial", 11), bg="goldenrod", fg="lightyellow")
        subtitle.pack()

    def create_main_content(self):
        """Crear contenido principal"""
        # Frame principal con scroll
        main_frame = tk.Frame(self.biblioteca_window, bg="lightyellow")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)

        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg="lightyellow")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="lightyellow")

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
        """Panel de estadísticas de biblioteca"""
        stats_frame = tk.LabelFrame(parent, text="📊 Estadísticas de Biblioteca", 
                                   font=("Arial", 12, "bold"), bg="lightyellow", 
                                   fg="goldenrod", padx=10, pady=8)
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        stats_data = [
            ("📚 Total Libros", "1,247", "blue", "Catálogo"),
            ("📖 Disponibles", "1,089", "green", "87%"),
            ("📋 Préstamos Activos", "158", "orange", "Vigentes"),
            ("⏰ Vencidos", "12", "red", "Pendientes")
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

        # Pestaña 1: Catálogo
        self.create_catalogo_tab(notebook)
        
        # Pestaña 2: Préstamos
        self.create_prestamos_tab(notebook)
        
        # Pestaña 3: Inventario
        self.create_inventario_tab(notebook)
        
        # Pestaña 4: Recursos Digitales
        self.create_digitales_tab(notebook)

    def create_catalogo_tab(self, notebook):
        """Crear pestaña de catálogo"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="📖 Catálogo")

        tk.Label(frame, text="📖 Catálogo de Biblioteca", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Búsqueda
        search_frame = tk.Frame(frame, bg="white", relief=tk.RAISED, bd=2)
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(search_frame, text="🔍 Buscar:", font=("Arial", 10, "bold"), bg="white").pack(side=tk.LEFT, padx=10, pady=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5, pady=5)

        tk.Label(search_frame, text="Categoría:", font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=10, pady=5)
        categoria_combo = ttk.Combobox(search_frame, values=[
            "Todas", "Matemáticas", "Lengua", "Ciencias", "Historia", "Literatura"
        ], state="readonly", width=12)
        categoria_combo.set("Todas")
        categoria_combo.pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(search_frame, text="Buscar", bg="#2196F3", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=10, pady=5)

        # Catálogo de libros
        catalogo_frame = tk.LabelFrame(frame, text="📚 Libros Disponibles", 
                                      font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        catalogo_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Título", "Autor", "Categoría", "Editorial", "Disponibles", "Acción")
        tree = ttk.Treeview(catalogo_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Título":
                tree.column(col, width=200, anchor="w")
            elif col == "Autor":
                tree.column(col, width=150, anchor="w")
            else:
                tree.column(col, width=100, anchor="center")

        # Datos de libros
        libros_data = [
            ("Matemáticas 1º Año", "Santillana", "Matemáticas", "Santillana", "15/20", "Prestar"),
            ("Lengua y Literatura", "Kapelusz", "Lengua", "Kapelusz", "8/15", "Prestar"),
            ("Historia Argentina", "Estrada", "Historia", "Estrada", "12/18", "Prestar"),
            ("Ciencias Naturales", "Aique", "Ciencias", "Aique", "0/10", "Agotado")
        ]

        for libro in libros_data:
            disponibles = libro[4]
            if "0/" in disponibles:
                tags = ("agotado",)
            else:
                tags = ()
            
            tree.insert("", tk.END, values=libro, tags=tags)

        tree.tag_configure("agotado", background="#FFCDD2")

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def create_prestamos_tab(self, notebook):
        """Crear pestaña de préstamos"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="📋 Préstamos")

        tk.Label(frame, text="📋 Gestión de Préstamos", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Préstamos activos
        prestamos_frame = tk.LabelFrame(frame, text="📚 Préstamos Activos", 
                                       font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        prestamos_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Alumno", "Libro", "Fecha Préstamo", "Vencimiento", "Estado", "Acción")
        tree = ttk.Treeview(prestamos_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Libro":
                tree.column(col, width=200, anchor="w")
            elif col == "Alumno":
                tree.column(col, width=150, anchor="w")
            else:
                tree.column(col, width=100, anchor="center")

        # Datos de préstamos
        prestamos_data = [
            ("Pérez, Juan", "Matemáticas 1º Año", "10/01/2025", "17/01/2025", "Vigente", "Devolver"),
            ("Gómez, Ana", "Historia Argentina", "08/01/2025", "15/01/2025", "Vencido", "Contactar"),
            ("Díaz, Laura", "Lengua y Literatura", "12/01/2025", "19/01/2025", "Vigente", "Devolver")
        ]

        for prestamo in prestamos_data:
            estado = prestamo[4]
            if estado == "Vencido":
                tags = ("vencido",)
            else:
                tags = ()
            
            tree.insert("", tk.END, values=prestamo, tags=tags)

        tree.tag_configure("vencido", background="#FFCDD2")

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def create_inventario_tab(self, notebook):
        """Crear pestaña de inventario"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="📦 Inventario")

        tk.Label(frame, text="📦 Inventario de Recursos", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Inventario por categorías
        inventario_text = """
        📦 INVENTARIO DE RECURSOS EDUCATIVOS:
        ═══════════════════════════════════════
        
        📚 LIBROS DE TEXTO:
        • Matemáticas: 85 ejemplares (15 disponibles)
        • Lengua: 67 ejemplares (8 disponibles)
        • Ciencias: 52 ejemplares (12 disponibles)
        • Historia: 48 ejemplares (18 disponibles)
        
        💻 RECURSOS TECNOLÓGICOS:
        • Proyectores: 8 unidades (6 disponibles)
        • Laptops educativas: 25 unidades (20 disponibles)
        • Tablets: 15 unidades (12 disponibles)
        • Equipos de audio: 5 unidades (4 disponibles)
        
        🔬 MATERIAL DE LABORATORIO:
        • Microscopios: 12 unidades (10 disponibles)
        • Material de química: Completo
        • Material de física: 85% disponible
        • Modelos anatómicos: 8 unidades
        
        🎨 MATERIAL ARTÍSTICO:
        • Instrumentos musicales: 25 unidades
        • Material de dibujo: Stock completo
        • Materiales de manualidades: 90% disponible
        """

        tk.Label(frame, text=inventario_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_digitales_tab(self, notebook):
        """Crear pestaña de recursos digitales"""
        frame = tk.Frame(notebook, bg="lightgray")
        notebook.add(frame, text="💻 Recursos Digitales")

        tk.Label(frame, text="💻 Biblioteca Digital", 
                font=("Arial", 14, "bold"), bg="lightgray", fg="darkslategray").pack(pady=10)

        # Recursos digitales
        digitales_text = """
        💻 BIBLIOTECA DIGITAL GESJ:
        ═══════════════════════════════════
        
        📱 PLATAFORMAS EDUCATIVAS:
        • Khan Academy: Acceso institucional
        • Coursera for Schools: 50 licencias
        • Duolingo for Schools: Idiomas
        • Google Workspace: Toda la institución
        
        📚 LIBROS DIGITALES:
        • Biblioteca Nacional Digital: Acceso completo
        • Libros de texto digitales: 150 títulos
        • Revistas educativas: 25 suscripciones
        • Enciclopedias online: Britannica, Wikipedia
        
        🎥 CONTENIDO MULTIMEDIA:
        • Videos educativos: 500+ videos
        • Documentales: 80 títulos
        • Simuladores interactivos: 25 programas
        • Juegos educativos: 40 aplicaciones
        
        📊 ESTADÍSTICAS DE USO:
        • Accesos diarios: 156 promedio
        • Recurso más usado: Khan Academy
        • Tiempo promedio de sesión: 45 minutos
        • Satisfacción de usuarios: 92%
        """

        tk.Label(frame, text=digitales_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_footer(self):
        """Crear pie de página"""
        footer_frame = tk.Frame(self.biblioteca_window, bg="goldenrod", padx=15, pady=8)
        footer_frame.pack(fill=tk.X)
        
        tk.Label(footer_frame, text="GESJ - Sistema Integral de Gestión Educativa | Módulo de Biblioteca", 
                font=("Arial", 9), bg="goldenrod", fg="lightyellow").pack()