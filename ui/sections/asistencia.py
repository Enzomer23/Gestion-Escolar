"""
Módulo de Asistencia - GESJ
Plataforma de Gestión Educativa
Provincia de San Juan, República Argentina
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date, timedelta
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from server.asistencia_operations import AsistenciaManager
    from server.calificaciones_operations import CalificacionesManager
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class AsistenciaSection:
    """Sección principal de gestión de asistencia"""
    
    def __init__(self, root, usuario_tipo="Docente"):
        self.root = root
        self.usuario_tipo = usuario_tipo
        self.asistencia_manager = AsistenciaManager() if DATABASE_AVAILABLE else None
        self.cal_manager = CalificacionesManager() if DATABASE_AVAILABLE else None
        self.create_asistencia_window()
    
    def create_asistencia_window(self):
        """Crear ventana principal de asistencia"""
        self.asistencia_window = tk.Toplevel(self.root)
        self.asistencia_window.title("📅 Sistema de Asistencia")
        self.asistencia_window.geometry("1340x720")
        self.asistencia_window.configure(bg="lightcyan")

        self.create_header()
        self.create_main_content()
        self.create_footer()

    def create_header(self):
        """Crear encabezado"""
        header_frame = tk.Frame(self.asistencia_window, bg="teal", padx=15, pady=8)
        header_frame.pack(fill=tk.X)

        title = tk.Label(header_frame, text="📅 Sistema Integral de Asistencia", 
                        font=("Franklin Gothic Heavy", 18, "bold"), bg="teal", fg="white")
        title.pack(pady=5)

        subtitle = tk.Label(header_frame, text="Control y Seguimiento de Asistencia Escolar", 
                           font=("Arial", 11), bg="teal", fg="lightcyan")
        subtitle.pack()

    def create_main_content(self):
        """Crear contenido principal"""
        # Frame principal con scroll
        main_frame = tk.Frame(self.asistencia_window, bg="lightcyan")
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
        """Panel de estadísticas de asistencia"""
        stats_frame = tk.LabelFrame(parent, text="📊 Estadísticas de Asistencia", 
                                   font=("Arial", 12, "bold"), bg="lightcyan", 
                                   fg="teal", padx=10, pady=8)
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        stats_data = [
            ("📋 Asistencia General", "89.7%", "orange", "↘ -1.2%"),
            ("👥 Presentes Hoy", "234", "green", "de 247"),
            ("⏰ Llegadas Tarde", "8", "orange", "Hoy"),
            ("🚨 Ausencias Sin Justificar", "5", "red", "Pendientes")
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

        # Pestaña 1: Registro Diario
        self.create_registro_tab(notebook)
        
        # Pestaña 2: Reportes de Asistencia
        self.create_reportes_tab(notebook)
        
        # Pestaña 3: Justificaciones
        self.create_justificaciones_tab(notebook)
        
        # Pestaña 4: Alertas
        self.create_alertas_tab(notebook)

    def create_registro_tab(self, notebook):
        """Crear pestaña de registro diario"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="📝 Registro Diario")

        tk.Label(frame, text="📝 Registro de Asistencia Diaria", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Selección de curso y fecha
        controls_frame = tk.Frame(frame, bg="white", relief=tk.RAISED, bd=2)
        controls_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(controls_frame, text="Curso:", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=0, padx=5, pady=5)
        curso_combo = ttk.Combobox(controls_frame, values=["1º Año A", "1º Año B", "2º Año A", "2º Año B", "3º Año A", "3º Año B"], state="readonly")
        curso_combo.set("1º Año A")
        curso_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(controls_frame, text="Fecha:", font=("Arial", 10, "bold"), bg="white").grid(row=0, column=2, padx=5, pady=5)
        fecha_entry = tk.Entry(controls_frame, width=12)
        fecha_entry.insert(0, date.today().strftime("%d/%m/%Y"))
        fecha_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(controls_frame, text="🔄 Cargar Alumnos", bg="#4CAF50", fg="white", font=("Arial", 9)).grid(row=0, column=4, padx=10, pady=5)

        # Tabla de asistencia
        asistencia_frame = tk.LabelFrame(frame, text="👥 Lista de Asistencia", 
                                        font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        asistencia_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Alumno", "DNI", "Estado", "Hora Llegada", "Observaciones")
        tree = ttk.Treeview(asistencia_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Alumno":
                tree.column(col, width=150, anchor="w")
            elif col == "Observaciones":
                tree.column(col, width=200, anchor="w")
            else:
                tree.column(col, width=100, anchor="center")

        # Datos de ejemplo
        alumnos_data = [
            ("Pérez, Juan", "12345678", "Presente", "07:45", ""),
            ("Gómez, Ana", "87654321", "Presente", "07:50", ""),
            ("González, Mario", "55667788", "Ausente", "--", "Sin justificar"),
            ("Díaz, Laura", "44332211", "Tarde", "08:15", "Justificado"),
            ("Castro, Julia", "14725836", "Presente", "07:40", "")
        ]

        for alumno in alumnos_data:
            estado = alumno[2]
            if estado == "Ausente":
                tags = ("ausente",)
            elif estado == "Tarde":
                tags = ("tarde",)
            else:
                tags = ()
            
            tree.insert("", tk.END, values=alumno, tags=tags)

        # Configurar colores
        tree.tag_configure("ausente", background="#FFCDD2")
        tree.tag_configure("tarde", background="#FFF3E0")

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def create_reportes_tab(self, notebook):
        """Crear pestaña de reportes"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="📊 Reportes")

        tk.Label(frame, text="📊 Reportes de Asistencia", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Generador de reportes
        reportes_frame = tk.LabelFrame(frame, text="📋 Generar Reportes", 
                                      font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        reportes_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(reportes_frame, text="Tipo de Reporte:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tipo_combo = ttk.Combobox(reportes_frame, values=[
            "Asistencia por Alumno", "Asistencia por Curso", "Inasistencias Reiteradas", 
            "Llegadas Tarde", "Resumen Mensual"
        ], state="readonly", width=25)
        tipo_combo.set("Asistencia por Curso")
        tipo_combo.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(reportes_frame, text="📊 Generar", bg="#4CAF50", fg="white", font=("Arial", 10)).grid(row=0, column=2, padx=10, pady=5)

        # Estadísticas generales
        stats_text = """
        📊 ESTADÍSTICAS GENERALES DE ASISTENCIA:
        ═══════════════════════════════════════════
        
        📋 RESUMEN MENSUAL (Enero 2025):
        • Asistencia promedio: 89.7%
        • Días con 100% asistencia: 8
        • Ausencias justificadas: 85%
        • Llegadas tarde promedio: 12/día
        
        🎯 POR CURSO:
        • 1º Año A: 92.3% asistencia
        • 1º Año B: 90.1% asistencia  
        • 2º Año A: 88.9% asistencia
        • 2º Año B: 87.5% asistencia
        • 3º Año A: 89.2% asistencia
        • 3º Año B: 86.8% asistencia
        
        🚨 ALUMNOS CON INASISTENCIAS REITERADAS:
        • González, Mario (2º A): 8 ausencias
        • Herrera, Lucas (3º B): 6 ausencias
        • Rodríguez, Pedro (1º B): 5 ausencias
        """

        tk.Label(frame, text=stats_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_justificaciones_tab(self, notebook):
        """Crear pestaña de justificaciones"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="📝 Justificaciones")

        tk.Label(frame, text="📝 Gestión de Justificaciones", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Justificaciones pendientes
        pendientes_frame = tk.LabelFrame(frame, text="⏳ Justificaciones Pendientes", 
                                        font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        pendientes_frame.pack(fill=tk.X, padx=20, pady=10)

        columns = ("Fecha", "Alumno", "Curso", "Motivo", "Estado", "Acción")
        tree = ttk.Treeview(pendientes_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        # Datos de justificaciones
        justificaciones_data = [
            ("15/01/2025", "González, Mario", "2º A", "Consulta médica", "Pendiente", "Revisar"),
            ("14/01/2025", "Díaz, Laura", "1º A", "Trámite familiar", "Aprobada", "Aprobada"),
            ("13/01/2025", "Herrera, Lucas", "3º B", "Enfermedad", "Pendiente", "Revisar")
        ]

        for justif in justificaciones_data:
            estado = justif[4]
            if estado == "Pendiente":
                tags = ("pendiente",)
            elif estado == "Aprobada":
                tags = ("aprobada",)
            else:
                tags = ()
            
            tree.insert("", tk.END, values=justif, tags=tags)

        tree.tag_configure("pendiente", background="#FFF3E0")
        tree.tag_configure("aprobada", background="#E8F5E8")

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Botones de acción
        buttons_frame = tk.Frame(frame, bg="lightyellow")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="✅ Aprobar", bg="#4CAF50", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="❌ Rechazar", bg="#F44336", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📧 Solicitar Info", bg="#FF9800", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

    def create_alertas_tab(self, notebook):
        """Crear pestaña de alertas"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="🚨 Alertas")

        tk.Label(frame, text="🚨 Alertas de Asistencia", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Alertas automáticas
        alertas_text = """
        🚨 ALERTAS AUTOMÁTICAS DE ASISTENCIA:
        ═══════════════════════════════════════
        
        🔴 CRÍTICAS (Requieren acción inmediata):
        • González, Mario: 8 ausencias en 15 días
        • Herrera, Lucas: 6 ausencias sin justificar
        
        🟡 ATENCIÓN (Seguimiento requerido):
        • Rodríguez, Pedro: 5 llegadas tarde esta semana
        • Martínez, Carlos: Patrón irregular de asistencia
        
        📧 NOTIFICACIONES ENVIADAS:
        • Padres contactados: 5 familias
        • Preceptores notificados: 3 casos
        • Seguimiento programado: 2 reuniones
        
        📊 CONFIGURACIÓN DE ALERTAS:
        • Ausencias consecutivas: ≥ 3 días
        • Ausencias mensuales: ≥ 5 días
        • Llegadas tarde semanales: ≥ 3 veces
        • Porcentaje asistencia: < 80%
        """

        tk.Label(frame, text=alertas_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_footer(self):
        """Crear pie de página"""
        footer_frame = tk.Frame(self.asistencia_window, bg="teal", padx=15, pady=8)
        footer_frame.pack(fill=tk.X)
        
        tk.Label(footer_frame, text="GESJ - Sistema Integral de Gestión Educativa | Módulo de Asistencia", 
                font=("Arial", 9), bg="teal", fg="lightcyan").pack()