"""
Seguimiento de Trayectorias Escolares para Preceptores
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

class TrayectoriasEscolaresWindow:
    """Ventana para seguimiento de trayectorias escolares"""
    
    def __init__(self, parent, cal_manager):
        self.parent = parent
        self.cal_manager = cal_manager
        self.create_window()

    def create_window(self):
        """Crear ventana principal de trayectorias escolares"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🎯 Seguimiento de Trayectorias Escolares")
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
        title = tk.Label(scrollable_frame, text="🎯 Seguimiento de Trayectorias Escolares", 
                        font=("Arial", 18, "bold"), bg="lightsteelblue", fg="darkblue")
        title.pack(pady=15)

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

    def create_filters_panel(self, parent):
        """Crear panel de filtros"""
        filters_frame = tk.LabelFrame(parent, text="🔍 Filtros de Búsqueda", 
                                     font=("Arial", 12, "bold"), bg="lightsteelblue", 
                                     fg="darkblue", padx=10, pady=8)
        filters_frame.pack(fill=tk.X, pady=(0, 15))

        # Filtros
        tk.Label(filters_frame, text="Curso:", font=("Arial", 10), bg="lightsteelblue").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        curso_combo = ttk.Combobox(filters_frame, values=["Todos", "1º Año", "2º Año", "3º Año"], state="readonly", width=15)
        curso_combo.set("Todos")
        curso_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filters_frame, text="Estado:", font=("Arial", 10), bg="lightsteelblue").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        estado_combo = ttk.Combobox(filters_frame, values=["Todos", "Excelente", "Bueno", "Regular", "En Riesgo"], state="readonly", width=15)
        estado_combo.set("Todos")
        estado_combo.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(filters_frame, text="🔍 Buscar", bg="#2196F3", fg="white", font=("Arial", 10), width=12).grid(row=0, column=4, padx=10, pady=5)
        tk.Button(filters_frame, text="🔄 Actualizar", bg="#4CAF50", fg="white", font=("Arial", 10), width=12).grid(row=0, column=5, padx=5, pady=5)

    def create_notebook(self, parent):
        """Crear notebook con pestañas"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Pestaña 1: Vista General
        self.create_vista_general_tab(notebook)
        
        # Pestaña 2: Seguimiento Individual
        self.create_seguimiento_individual_tab(notebook)
        
        # Pestaña 3: Alertas y Notificaciones
        self.create_alertas_tab(notebook)

    def create_vista_general_tab(self, notebook):
        """Crear pestaña de vista general"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="👥 Vista General")

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
        tk.Label(scrollable_frame, text="👥 Resumen General de Trayectorias", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Tabla de estudiantes
        columns = ("ID", "Estudiante", "Curso", "Promedio", "Asistencia", "Estado", "Última Actualización")
        tree = ttk.Treeview(scrollable_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "ID":
                tree.column(col, width=50, anchor="center")
            elif col == "Estudiante":
                tree.column(col, width=150, anchor="w")
            else:
                tree.column(col, width=100, anchor="center")

        # Datos de ejemplo
        estudiantes_data = [
            ("001", "Pérez, Juan", "1º A", "8.5", "95%", "Excelente", "15/01/2025"),
            ("002", "Gómez, Ana", "2º A", "8.7", "98%", "Excelente", "15/01/2025"),
            ("003", "Martínez, Carlos", "3º A", "6.9", "85%", "Regular", "14/01/2025"),
            ("004", "Díaz, Laura", "1º A", "9.0", "97%", "Excelente", "15/01/2025"),
            ("005", "González, Mario", "2º A", "6.0", "78%", "En Riesgo", "13/01/2025"),
            ("006", "Ramírez, Sofía", "3º A", "8.3", "92%", "Bueno", "15/01/2025"),
            ("007", "Rodríguez, Pedro", "1º B", "5.7", "72%", "En Riesgo", "12/01/2025"),
            ("008", "Fernández, María", "2º B", "8.0", "89%", "Bueno", "14/01/2025"),
            ("009", "Herrera, Lucas", "3º B", "5.2", "68%", "En Riesgo", "11/01/2025"),
            ("010", "Castro, Julia", "1º B", "8.8", "96%", "Excelente", "15/01/2025")
        ]

        for estudiante in estudiantes_data:
            # Colorear filas según estado
            estado = estudiante[5]
            if estado == "En Riesgo":
                tags = ("riesgo",)
            elif estado == "Excelente":
                tags = ("excelente",)
            else:
                tags = ()
            
            tree.insert("", tk.END, values=estudiante, tags=tags)

        # Configurar colores
        tree.tag_configure("riesgo", background="#FFEBEE")
        tree.tag_configure("excelente", background="#E8F5E8")

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Botones de acción
        buttons_frame = tk.Frame(scrollable_frame, bg="lightblue")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="👁️ Ver Detalle", bg="#2196F3", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📊 Generar Reporte", bg="#FF9800", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📧 Notificar Padres", bg="#4CAF50", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_seguimiento_individual_tab(self, notebook):
        """Crear pestaña de seguimiento individual"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="👤 Individual")

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

        tk.Label(scrollable_frame, text="👤 Seguimiento Individual Detallado", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Selección de estudiante
        selection_frame = tk.Frame(scrollable_frame, bg="white", relief=tk.RAISED, bd=2)
        selection_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(selection_frame, text="Seleccionar Estudiante:", font=("Arial", 12, "bold"), bg="white").pack(pady=5)
        estudiante_combo = ttk.Combobox(selection_frame, values=[
            "Pérez, Juan (1º A)", "Gómez, Ana (2º A)", "Martínez, Carlos (3º A)",
            "Díaz, Laura (1º A)", "González, Mario (2º A) - EN RIESGO"
        ], state="readonly", width=40)
        estudiante_combo.set("González, Mario (2º A) - EN RIESGO")
        estudiante_combo.pack(pady=5)

        # Información detallada del estudiante seleccionado
        info_frame = tk.LabelFrame(scrollable_frame, text="📋 Información Detallada", 
                                  font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        info_frame.pack(fill=tk.X, padx=20, pady=10)

        # Datos del estudiante
        student_info = """
        👤 ESTUDIANTE: Mario González
        📚 CURSO: 2º Año A
        📊 PROMEDIO ACTUAL: 6.0 (En Riesgo)
        📋 ASISTENCIA: 78% (Baja)
        📅 ÚLTIMA ACTUALIZACIÓN: 13/01/2025
        
        📈 EVOLUCIÓN ACADÉMICA:
        ═══════════════════════════
        Marzo 2024: 7.2  |  Abril 2024: 6.8  |  Mayo 2024: 6.5
        Junio 2024: 6.2  |  Julio 2024: 6.0  |  Agosto 2024: 5.8
        
        🎯 MATERIAS CON DIFICULTADES:
        ═══════════════════════════════
        • Matemáticas: 5.5 (Crítico)
        • Física: 6.0 (En Riesgo)
        • Química: 6.2 (Regular)
        
        📋 PLAN DE INTERVENCIÓN ACTIVO:
        ═══════════════════════════════════
        • Tipo: Académico + Asistencia
        • Inicio: 01/12/2024
        • Progreso: 65%
        • Próxima revisión: 20/01/2025
        
        👨‍👩‍👧‍👦 COMUNICACIÓN CON PADRES:
        ═══════════════════════════════════
        • Última reunión: 10/01/2025
        • Próxima cita: 25/01/2025
        • Compromiso familiar: Alto
        """

        tk.Label(info_frame, text=student_info, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones de acción específicos
        actions_frame = tk.Frame(scrollable_frame, bg="lightgreen")
        actions_frame.pack(fill=tk.X, pady=10)

        tk.Button(actions_frame, text="📝 Actualizar Seguimiento", bg="#4CAF50", fg="white", font=("Arial", 10), width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(actions_frame, text="📞 Contactar Padres", bg="#FF9800", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(actions_frame, text="🎯 Ajustar Plan", bg="#9C27B0", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_alertas_tab(self, notebook):
        """Crear pestaña de alertas y notificaciones"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="🚨 Alertas")

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

        tk.Label(scrollable_frame, text="🚨 Sistema de Alertas y Notificaciones", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Panel de alertas activas
        alertas_frame = tk.LabelFrame(scrollable_frame, text="🚨 Alertas Activas", 
                                     font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        alertas_frame.pack(fill=tk.X, padx=20, pady=10)

        alertas_data = [
            ("🔴 CRÍTICO", "Lucas Herrera - Promedio 5.2", "3º B", "Hace 2 días"),
            ("🟡 ALTO", "Mario González - Asistencia 78%", "2º A", "Hace 1 día"),
            ("🟡 ALTO", "Pedro Rodríguez - Promedio 5.7", "1º B", "Hace 3 días"),
            ("🟠 MEDIO", "Carlos Martínez - Tendencia negativa", "3º A", "Hace 1 semana")
        ]

        for i, (nivel, descripcion, curso, tiempo) in enumerate(alertas_data):
            alerta_frame = tk.Frame(alertas_frame, bg="white", relief=tk.RAISED, bd=1)
            alerta_frame.pack(fill=tk.X, padx=10, pady=3)
            
            tk.Label(alerta_frame, text=nivel, font=("Arial", 9, "bold"), bg="white", width=12, anchor="w").pack(side=tk.LEFT, padx=5)
            tk.Label(alerta_frame, text=descripcion, font=("Arial", 9), bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            tk.Label(alerta_frame, text=curso, font=("Arial", 9), bg="white", width=8, anchor="center").pack(side=tk.RIGHT, padx=5)
            tk.Label(alerta_frame, text=tiempo, font=("Arial", 8), bg="white", fg="gray", width=12, anchor="e").pack(side=tk.RIGHT, padx=5)

        # Panel de configuración de alertas
        config_frame = tk.LabelFrame(scrollable_frame, text="⚙️ Configuración de Alertas", 
                                    font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        config_frame.pack(fill=tk.X, padx=20, pady=10)

        config_text = """
        📊 CRITERIOS DE ALERTA CONFIGURADOS:
        ═══════════════════════════════════════
        🔴 CRÍTICO:    Promedio < 5.5 O Asistencia < 70%
        🟡 ALTO:       Promedio < 6.0 O Asistencia < 80%
        🟠 MEDIO:      Tendencia negativa por 3 semanas
        🟢 BAJO:       Mejora después de intervención
        
        📧 NOTIFICACIONES AUTOMÁTICAS:
        ═══════════════════════════════════
        • Padres: Inmediata para alertas críticas
        • Directivos: Resumen semanal
        • Docentes: Notificación de planes activos
        
        🔄 FRECUENCIA DE REVISIÓN:
        ═══════════════════════════════
        • Diaria: Asistencia y comportamiento
        • Semanal: Promedios y tendencias
        • Mensual: Evaluación integral
        """

        tk.Label(config_frame, text=config_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones de gestión de alertas
        alertas_buttons_frame = tk.Frame(scrollable_frame, bg="lightyellow")
        alertas_buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(alertas_buttons_frame, text="🔔 Configurar Alertas", bg="#FF5722", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(alertas_buttons_frame, text="📧 Enviar Notificaciones", bg="#2196F3", fg="white", font=("Arial", 10), width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(alertas_buttons_frame, text="📊 Reporte de Alertas", bg="#9C27B0", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")