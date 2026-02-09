"""
Sistema de Comunicación para Docentes
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

try:
    from server.email_notifier import EmailNotifier
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class ComunicacionDocenteWindow:
    """Ventana para comunicación con padres y preceptores"""
    
    def __init__(self, parent, email_notifier):
        self.parent = parent
        self.email_notifier = email_notifier
        self.create_window()

    def create_window(self):
        """Crear ventana principal de comunicación"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📧 Sistema de Comunicación")
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
        title = tk.Label(scrollable_frame, text="📧 Sistema de Comunicación Integral", 
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
        """Crear panel de estadísticas de comunicación"""
        stats_frame = tk.LabelFrame(parent, text="📊 Estadísticas de Comunicación", 
                                   font=("Arial", 12, "bold"), bg="lightcyan", 
                                   fg="darkcyan", padx=10, pady=8)
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        stats_data = [
            ("📧 Mensajes Enviados", "47", "blue", "Este mes"),
            ("📨 Respuestas", "32", "green", "68% tasa"),
            ("🚨 Alertas Activas", "5", "orange", "Pendientes"),
            ("👥 Contactos", "89", "purple", "Activos")
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

        # Pestaña 1: Enviar Mensaje
        self.create_enviar_mensaje_tab(notebook)
        
        # Pestaña 2: Bandeja de Entrada
        self.create_bandeja_entrada_tab(notebook)
        
        # Pestaña 3: Notificaciones Automáticas
        self.create_notificaciones_tab(notebook)
        
        # Pestaña 4: Contactos
        self.create_contactos_tab(notebook)

    def create_enviar_mensaje_tab(self, notebook):
        """Crear pestaña para enviar mensajes"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="📤 Enviar Mensaje")

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
        tk.Label(scrollable_frame, text="📤 Redactar Nuevo Mensaje", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Formulario de mensaje
        form_frame = tk.LabelFrame(scrollable_frame, text="✉️ Datos del Mensaje", 
                                  font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        form_frame.pack(fill=tk.X, padx=20, pady=10)

        # Destinatarios
        tk.Label(form_frame, text="Para:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        destinatario_combo = ttk.Combobox(form_frame, values=[
            "Todos los Padres", "Padres de 1º A", "Padres de 2º A", "Preceptores", 
            "Padre específico", "Directivos"
        ], state="readonly", width=40)
        destinatario_combo.set("Padres de 1º A")
        destinatario_combo.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Asunto
        tk.Label(form_frame, text="Asunto:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        asunto_entry = tk.Entry(form_frame, width=50)
        asunto_entry.insert(0, "Información sobre calificaciones del primer cuatrimestre")
        asunto_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Prioridad
        tk.Label(form_frame, text="Prioridad:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        prioridad_combo = ttk.Combobox(form_frame, values=["Normal", "Alta", "Urgente"], state="readonly", width=15)
        prioridad_combo.set("Normal")
        prioridad_combo.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Mensaje
        tk.Label(form_frame, text="Mensaje:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
        mensaje_text = tk.Text(form_frame, width=60, height=8)
        mensaje_text.insert("1.0", """Estimados padres,

Me dirijo a ustedes para informarles sobre el progreso académico de sus hijos durante el primer cuatrimestre.

En general, el rendimiento del curso ha sido satisfactorio, con un promedio general de 8.3 puntos.

Adjunto encontrarán el detalle de las calificaciones por materia.

Cualquier consulta, no duden en contactarme.

Saludos cordiales,
Prof. [Nombre del Docente]""")
        mensaje_text.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Adjuntos
        tk.Label(form_frame, text="Adjuntos:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        adjuntos_frame = tk.Frame(form_frame, bg="lightblue")
        adjuntos_frame.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        
        tk.Button(adjuntos_frame, text="📎 Adjuntar Archivo", bg="#9C27B0", fg="white", font=("Arial", 9), width=15).pack(side=tk.LEFT, padx=5)
        tk.Label(adjuntos_frame, text="Calificaciones_1A_Enero.xlsx", font=("Arial", 9), bg="lightblue", fg="green").pack(side=tk.LEFT, padx=10)

        # Botones de acción
        buttons_frame = tk.Frame(scrollable_frame, bg="lightblue")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="📤 Enviar Mensaje", bg="#4CAF50", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="💾 Guardar Borrador", bg="#FF9800", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="👁️ Vista Previa", bg="#2196F3", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_bandeja_entrada_tab(self, notebook):
        """Crear pestaña de bandeja de entrada"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="📥 Bandeja de Entrada")

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

        tk.Label(scrollable_frame, text="📥 Mensajes Recibidos", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Tabla de mensajes
        mensajes_frame = tk.LabelFrame(scrollable_frame, text="📨 Lista de Mensajes", 
                                      font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        mensajes_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Estado", "De", "Asunto", "Fecha", "Prioridad")
        tree = ttk.Treeview(mensajes_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Estado":
                tree.column(col, width=80, anchor="center")
            elif col == "De":
                tree.column(col, width=150, anchor="w")
            elif col == "Asunto":
                tree.column(col, width=300, anchor="w")
            elif col == "Fecha":
                tree.column(col, width=120, anchor="center")
            else:
                tree.column(col, width=100, anchor="center")

        # Datos de mensajes
        mensajes_data = [
            ("📧 Nuevo", "Padre González", "Consulta sobre calificaciones de Mario", "15/01/2025", "Normal"),
            ("📖 Leído", "Preceptor López", "Informe de asistencia - 1º A", "14/01/2025", "Normal"),
            ("📧 Nuevo", "Madre Díaz", "Reunión para hablar sobre Laura", "13/01/2025", "Alta"),
            ("📖 Leído", "Directora", "Reunión de docentes - Viernes", "12/01/2025", "Normal"),
            ("📧 Nuevo", "Padre Herrera", "Preocupación por rendimiento de Lucas", "11/01/2025", "Urgente"),
            ("📖 Leído", "Preceptor Martín", "Plan de intervención aprobado", "10/01/2025", "Normal")
        ]

        for mensaje in mensajes_data:
            # Colorear según prioridad
            prioridad = mensaje[4]
            if prioridad == "Urgente":
                tags = ("urgente",)
            elif prioridad == "Alta":
                tags = ("alta",)
            else:
                tags = ()
            
            tree.insert("", tk.END, values=mensaje, tags=tags)

        # Configurar colores
        tree.tag_configure("urgente", background="#FFCDD2")
        tree.tag_configure("alta", background="#FFF3E0")

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Botones de acción
        buttons_frame = tk.Frame(scrollable_frame, bg="lightgreen")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="👁️ Leer Mensaje", bg="#2196F3", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="↩️ Responder", bg="#4CAF50", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="🗑️ Eliminar", bg="#F44336", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_notificaciones_tab(self, notebook):
        """Crear pestaña de notificaciones automáticas"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="🔔 Notificaciones")

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

        tk.Label(scrollable_frame, text="🔔 Sistema de Notificaciones Automáticas", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Configuración de notificaciones
        config_frame = tk.LabelFrame(scrollable_frame, text="⚙️ Configurar Notificaciones", 
                                    font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        config_frame.pack(fill=tk.X, padx=20, pady=10)

        # Tipos de notificaciones
        notif_types = [
            ("📝 Calificaciones subidas", True, "Notificar cuando se cargan nuevas notas"),
            ("🚨 Estudiante en riesgo", True, "Alertar cuando un estudiante baja de 6.0"),
            ("📋 Asistencia baja", False, "Notificar cuando la asistencia es < 80%"),
            ("📊 Fin de período", True, "Recordar cierre de calificaciones"),
            ("👥 Reunión de padres", False, "Recordatorios de reuniones programadas")
        ]

        for i, (tipo, activo, descripcion) in enumerate(notif_types):
            notif_frame = tk.Frame(config_frame, bg="white", relief=tk.RAISED, bd=1)
            notif_frame.pack(fill=tk.X, padx=10, pady=5)
            
            var = tk.BooleanVar(value=activo)
            tk.Checkbutton(notif_frame, text=tipo, variable=var, font=("Arial", 10, "bold"), 
                          bg="white").pack(side=tk.LEFT, padx=10, pady=5)
            
            tk.Label(notif_frame, text=descripcion, font=("Arial", 9), 
                    bg="white", fg="gray").pack(side=tk.LEFT, padx=20)

        # Historial de notificaciones
        historial_frame = tk.LabelFrame(scrollable_frame, text="📋 Historial de Notificaciones", 
                                       font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        historial_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        historial_text = """
        📧 NOTIFICACIONES ENVIADAS (Últimos 7 días):
        ═══════════════════════════════════════════════════
        
        15/01/2025 - 14:30
        ✅ Calificaciones de Matemáticas cargadas
        📧 Enviado a: 25 padres + 2 preceptores
        
        14/01/2025 - 16:45
        🚨 Alerta: Mario González en riesgo académico
        📧 Enviado a: Padres + Preceptor López
        
        13/01/2025 - 09:15
        📊 Recordatorio: Cierre de período el 20/01
        📧 Enviado a: Todos los docentes
        
        12/01/2025 - 11:20
        ✅ Calificaciones de Lengua cargadas
        📧 Enviado a: 24 padres + 2 preceptores
        
        11/01/2025 - 15:30
        🚨 Alerta: Lucas Herrera - Promedio crítico (5.2)
        📧 Enviado a: Padres + Directivos
        
        📊 ESTADÍSTICAS:
        ═══════════════════
        • Total enviadas: 47 notificaciones
        • Tasa de entrega: 98.5%
        • Respuestas recibidas: 32 (68%)
        • Tiempo promedio de respuesta: 4.2 horas
        """

        tk.Label(historial_frame, text=historial_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_contactos_tab(self, notebook):
        """Crear pestaña de contactos"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="👥 Contactos")

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

        tk.Label(scrollable_frame, text="👥 Directorio de Contactos", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Búsqueda de contactos
        search_frame = tk.Frame(scrollable_frame, bg="white", relief=tk.RAISED, bd=2)
        search_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(search_frame, text="🔍 Buscar contacto:", font=("Arial", 10, "bold"), bg="white").pack(side=tk.LEFT, padx=10, pady=5)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.pack(side=tk.LEFT, padx=5, pady=5)
        tk.Button(search_frame, text="Buscar", bg="#2196F3", fg="white", font=("Arial", 9), width=10).pack(side=tk.LEFT, padx=5, pady=5)

        # Filtros
        filtros_frame = tk.Frame(search_frame, bg="white")
        filtros_frame.pack(side=tk.RIGHT, padx=10, pady=5)

        tk.Label(filtros_frame, text="Filtrar:", font=("Arial", 9), bg="white").pack(side=tk.LEFT, padx=5)
        filtro_combo = ttk.Combobox(filtros_frame, values=["Todos", "Padres", "Preceptores", "Directivos"], state="readonly", width=12)
        filtro_combo.set("Todos")
        filtro_combo.pack(side=tk.LEFT, padx=5)

        # Lista de contactos
        contactos_frame = tk.LabelFrame(scrollable_frame, text="📞 Lista de Contactos", 
                                       font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        contactos_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Nombre", "Tipo", "Email", "Teléfono", "Estudiante", "Última Comunicación")
        tree = ttk.Treeview(contactos_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Nombre":
                tree.column(col, width=150, anchor="w")
            elif col == "Email":
                tree.column(col, width=200, anchor="w")
            elif col == "Estudiante":
                tree.column(col, width=150, anchor="w")
            else:
                tree.column(col, width=120, anchor="center")

        # Datos de contactos
        contactos_data = [
            ("González, María", "Padre", "maria.gonzalez@gmail.com", "264-123-4567", "Mario González", "15/01/2025"),
            ("López, Juan", "Preceptor", "j.lopez@escuela.edu", "264-234-5678", "1º A", "14/01/2025"),
            ("Díaz, Carmen", "Padre", "carmen.diaz@hotmail.com", "264-345-6789", "Laura Díaz", "13/01/2025"),
            ("Martín, Roberto", "Preceptor", "r.martin@escuela.edu", "264-456-7890", "2º A", "12/01/2025"),
            ("Herrera, Ana", "Padre", "ana.herrera@yahoo.com", "264-567-8901", "Lucas Herrera", "11/01/2025"),
            ("Directora", "Directivo", "direccion@escuela.edu", "264-678-9012", "Institución", "10/01/2025")
        ]

        for contacto in contactos_data:
            tree.insert("", tk.END, values=contacto)

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Botones de acción
        buttons_frame = tk.Frame(scrollable_frame, bg="lightcoral")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="📧 Enviar Email", bg="#4CAF50", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📞 Llamar", bg="#FF9800", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="✏️ Editar", bg="#9C27B0", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")