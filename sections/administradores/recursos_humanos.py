"""
Recursos Humanos para Administradores
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

try:
    from server.database import crear_conexion, obtener_todos_usuarios
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class RecursosHumanosWindow:
    """Ventana para gestión de recursos humanos"""
    
    def __init__(self, parent, usuarios_data):
        self.parent = parent
        self.usuarios_data = usuarios_data
        self.create_window()

    def create_window(self):
        """Crear ventana principal de recursos humanos"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("👥 Recursos Humanos")
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
        title = tk.Label(scrollable_frame, text="👥 Gestión de Recursos Humanos", 
                        font=("Arial", 18, "bold"), bg="lightsteelblue", fg="darkblue")
        title.pack(pady=15)

        # Panel de estadísticas de personal
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
        """Crear panel de estadísticas de personal"""
        stats_frame = tk.LabelFrame(parent, text="📊 Estadísticas de Personal", 
                                   font=("Arial", 12, "bold"), bg="lightsteelblue", 
                                   fg="darkblue", padx=10, pady=8)
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        # Contar personal por tipo
        docentes = sum(1 for u in self.usuarios_data if u[1] == 'Docente')
        preceptores = sum(1 for u in self.usuarios_data if u[1] == 'Preceptor')
        administrativos = sum(1 for u in self.usuarios_data if u[1] == 'Administrativo')
        total_personal = docentes + preceptores + administrativos

        stats_data = [
            ("👨‍🏫 Docentes", str(docentes), "blue", "Activos"),
            ("👨‍💼 Preceptores", str(preceptores), "green", "Activos"),
            ("🏛️ Administrativos", str(administrativos), "orange", "Activos"),
            ("👥 Total Personal", str(total_personal), "purple", "Institución")
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

        # Pestaña 1: Personal Docente
        self.create_personal_tab(notebook)
        
        # Pestaña 2: Evaluación de Desempeño
        self.create_evaluacion_tab(notebook)
        
        # Pestaña 3: Capacitación
        self.create_capacitacion_tab(notebook)
        
        # Pestaña 4: Licencias y Permisos
        self.create_licencias_tab(notebook)

    def create_personal_tab(self, notebook):
        """Crear pestaña de personal docente"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="👨‍🏫 Personal Docente")

        tk.Label(frame, text="👨‍🏫 Gestión de Personal Docente", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Tabla de personal
        columns = ("Usuario", "Tipo", "Estado", "Última Actividad", "Evaluación")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        # Cargar datos de usuarios
        for usuario in self.usuarios_data:
            if usuario[1] in ['Docente', 'Preceptor']:
                tree.insert("", tk.END, values=(
                    usuario[0],
                    usuario[1],
                    "Activo",
                    "16/01/2025",
                    "Excelente"
                ))

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Botones de acción
        buttons_frame = tk.Frame(frame, bg="lightblue")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="👁️ Ver Perfil", bg="#2196F3", fg="white", font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📊 Evaluar", bg="#FF9800", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📚 Capacitar", bg="#4CAF50", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="➕ Nuevo Personal", bg="#9C27B0", fg="white", font=("Arial", 10), width=15, command=self.crear_personal).pack(side=tk.LEFT, padx=5)

    def create_evaluacion_tab(self, notebook):
        """Crear pestaña de evaluación de desempeño"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="📊 Evaluación")

        tk.Label(frame, text="📊 Evaluación de Desempeño", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Métricas de evaluación
        evaluacion_text = """
        📊 SISTEMA DE EVALUACIÓN DE DESEMPEÑO:
        ═══════════════════════════════════════
        
        🎯 CRITERIOS DE EVALUACIÓN:
        • Rendimiento académico de estudiantes: 40%
        • Metodología pedagógica: 25%
        • Comunicación y trabajo en equipo: 20%
        • Desarrollo profesional continuo: 15%
        
        📈 RESULTADOS GENERALES:
        • Promedio institucional: 8.7/10
        • Docentes destacados: 12 (80%)
        • Necesitan mejora: 2 (13%)
        • En proceso de capacitación: 1 (7%)
        
        🏆 RECONOCIMIENTOS 2024:
        • Docente del Año: Prof. María González
        • Innovación Pedagógica: Prof. Carlos López
        • Mejor Comunicación: Prof. Ana Martínez
        
        📋 PLAN DE DESARROLLO:
        • Capacitaciones programadas: 8
        • Mentorías activas: 3
        • Proyectos de mejora: 5
        """

        tk.Label(frame, text=evaluacion_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_capacitacion_tab(self, notebook):
        """Crear pestaña de capacitación"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="📚 Capacitación")

        tk.Label(frame, text="📚 Capacitación y Desarrollo Profesional", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Programas de capacitación
        capacitacion_frame = tk.LabelFrame(frame, text="🎓 Programas de Capacitación", 
                                          font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        capacitacion_frame.pack(fill=tk.X, padx=20, pady=10)

        programas_data = [
            ("Tecnología Educativa", "40 hs", "En curso", "12 participantes"),
            ("Evaluación por Competencias", "30 hs", "Planificado", "8 inscriptos"),
            ("Neuroeducación", "25 hs", "Completado", "15 certificados"),
            ("Inclusión Educativa", "35 hs", "En curso", "10 participantes")
        ]

        for programa, duracion, estado, participantes in programas_data:
            prog_frame = tk.Frame(capacitacion_frame, bg="white", relief=tk.RAISED, bd=1)
            prog_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(prog_frame, text=programa, font=("Arial", 10, "bold"), 
                    bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            tk.Label(prog_frame, text=duracion, font=("Arial", 10), 
                    bg="white", fg="blue").pack(side=tk.RIGHT, padx=5)
            tk.Label(prog_frame, text=participantes, font=("Arial", 10), 
                    bg="white", fg="green").pack(side=tk.RIGHT, padx=5)
            tk.Label(prog_frame, text=estado, font=("Arial", 10), 
                    bg="white", fg="orange").pack(side=tk.RIGHT, padx=10)

    def create_licencias_tab(self, notebook):
        """Crear pestaña de licencias y permisos"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="💼 Licencias")

        tk.Label(frame, text="💼 Gestión de Licencias y Permisos", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Solicitudes pendientes
        solicitudes_frame = tk.LabelFrame(frame, text="📋 Solicitudes Pendientes", 
                                         font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        solicitudes_frame.pack(fill=tk.X, padx=20, pady=10)

        solicitudes_data = [
            ("Prof. González", "Licencia médica", "3 días", "Pendiente"),
            ("Prof. Martínez", "Permiso personal", "1 día", "Aprobado"),
            ("Prof. López", "Capacitación", "2 días", "En revisión")
        ]

        for docente, tipo, duracion, estado in solicitudes_data:
            sol_frame = tk.Frame(solicitudes_frame, bg="white", relief=tk.RAISED, bd=1)
            sol_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(sol_frame, text=docente, font=("Arial", 10, "bold"), 
                    bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            tk.Label(sol_frame, text=tipo, font=("Arial", 10), 
                    bg="white", fg="blue").pack(side=tk.LEFT, padx=10)
            tk.Label(sol_frame, text=duracion, font=("Arial", 10), 
                    bg="white", fg="green").pack(side=tk.RIGHT, padx=5)
            tk.Label(sol_frame, text=estado, font=("Arial", 10), 
                    bg="white", fg="orange").pack(side=tk.RIGHT, padx=10)

    def crear_personal(self):
        """Crear nuevo registro de personal"""
        CrearPersonalWindow(self.window, self.usuarios_data)

    def evaluar_desempeño(self):
        """Evaluar desempeño del personal"""
        EvaluacionDesempeñoWindow(self.window)

    def gestionar_capacitacion(self):
        """Gestionar programas de capacitación"""
        GestionCapacitacionWindow(self.window)


class CrearPersonalWindow:
    """Ventana para crear nuevo personal"""
    
    def __init__(self, parent, usuarios_data):
        self.parent = parent
        self.usuarios_data = usuarios_data
        self.create_window()

    def create_window(self):
        """Crear ventana de nuevo personal"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("➕ Registrar Nuevo Personal")
        self.window.geometry("600x700")
        self.window.configure(bg="lightblue")

        # Título
        title = tk.Label(self.window, text="➕ Registro de Nuevo Personal", 
                        font=("Arial", 16, "bold"), bg="lightblue", fg="darkblue")
        title.pack(pady=15)

        # Formulario completo
        form_frame = tk.LabelFrame(self.window, text="📝 Datos del Personal", 
                                  font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Campos del formulario
        fields = [
            ("Nombre Completo:", "entry"),
            ("DNI:", "entry"),
            ("Email:", "entry"),
            ("Teléfono:", "entry"),
            ("Cargo:", "combo", ["Docente", "Preceptor", "Administrativo", "Directivo"]),
            ("Especialidad:", "combo", ["Matemáticas", "Lengua", "Ciencias", "Historia", "Geografía", "Educación Física"]),
            ("Fecha de Ingreso:", "entry"),
            ("Título Universitario:", "entry"),
            ("Experiencia (años):", "entry"),
            ("Observaciones:", "text")
        ]

        self.form_widgets = {}
        
        for i, field_data in enumerate(fields):
            label_text = field_data[0]
            field_type = field_data[1]
            
            tk.Label(form_frame, text=label_text, font=("Arial", 10, "bold"), bg="lightblue").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            
            if field_type == "entry":
                widget = tk.Entry(form_frame, width=40)
                if "Fecha" in label_text:
                    widget.insert(0, "16/01/2025")
            elif field_type == "combo":
                values = field_data[2] if len(field_data) > 2 else []
                widget = ttk.Combobox(form_frame, values=values, state="readonly", width=37)
                if values:
                    widget.set(values[0])
            elif field_type == "text":
                widget = tk.Text(form_frame, width=40, height=3)
            
            widget.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            self.form_widgets[label_text] = widget

        # Botones
        buttons_frame = tk.Frame(self.window, bg="lightblue")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="💾 Registrar Personal", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=18, command=self.registrar_personal).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="🗑️ Limpiar", bg="#FF5722", fg="white", 
                 font=("Arial", 10), width=12, command=self.limpiar_formulario).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="❌ Cancelar", bg="#666", fg="white", 
                 font=("Arial", 10), width=12, command=self.window.destroy).pack(side=tk.LEFT, padx=5)

    def registrar_personal(self):
        """Registrar nuevo personal"""
        messagebox.showinfo("Personal Registrado", 
                           "✅ Nuevo personal registrado exitosamente\n"
                           "📧 Se ha enviado email de bienvenida\n"
                           "🔐 Credenciales de acceso generadas")
        self.window.destroy()

    def limpiar_formulario(self):
        """Limpiar todos los campos del formulario"""
        for widget in self.form_widgets.values():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set("")


class EvaluacionDesempeñoWindow:
    """Ventana para evaluación de desempeño"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_window()

    def create_window(self):
        """Crear ventana de evaluación de desempeño"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📊 Evaluación de Desempeño")
        self.window.geometry("800x700")
        self.window.configure(bg="lightgreen")

        # Título
        title = tk.Label(self.window, text="📊 Sistema de Evaluación de Desempeño", 
                        font=("Arial", 16, "bold"), bg="lightgreen", fg="darkgreen")
        title.pack(pady=15)

        # Notebook con tipos de evaluación
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Pestaña 1: Evaluación Individual
        self.create_evaluacion_individual_tab(notebook)
        
        # Pestaña 2: Evaluación 360°
        self.create_evaluacion_360_tab(notebook)
        
        # Pestaña 3: Resultados y Reportes
        self.create_resultados_tab(notebook)

    def create_evaluacion_individual_tab(self, notebook):
        """Crear pestaña de evaluación individual"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="👤 Individual")

        tk.Label(frame, text="👤 Evaluación Individual de Desempeño", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Selección de personal
        selection_frame = tk.Frame(frame, bg="white", relief=tk.RAISED, bd=2)
        selection_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(selection_frame, text="Seleccionar Personal:", font=("Arial", 12, "bold"), bg="white").pack(pady=5)
        personal_combo = ttk.Combobox(selection_frame, values=[
            "Prof. María González (Matemáticas)",
            "Prof. Carlos López (Lengua)",
            "Preceptor Ana Martínez",
            "Admin. Roberto Silva"
        ], state="readonly", width=40)
        personal_combo.set("Prof. María González (Matemáticas)")
        personal_combo.pack(pady=5)

        # Criterios de evaluación
        criterios_frame = tk.LabelFrame(frame, text="📋 Criterios de Evaluación", 
                                       font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        criterios_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        criterios_data = [
            ("Conocimiento de la Materia", 9.0),
            ("Metodología Pedagógica", 8.5),
            ("Comunicación con Estudiantes", 9.2),
            ("Trabajo en Equipo", 8.8),
            ("Puntualidad y Responsabilidad", 9.5),
            ("Innovación y Creatividad", 8.0)
        ]

        for criterio, puntaje in criterios_data:
            crit_frame = tk.Frame(criterios_frame, bg="white", relief=tk.RAISED, bd=1)
            crit_frame.pack(fill=tk.X, padx=10, pady=3)
            
            tk.Label(crit_frame, text=criterio, font=("Arial", 10), bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            # Barra de puntaje
            score_frame = tk.Frame(crit_frame, bg="lightgray", height=15, width=100)
            score_frame.pack(side=tk.RIGHT, padx=10, pady=5)
            score_frame.pack_propagate(False)
            
            color = "green" if puntaje >= 8.5 else "orange" if puntaje >= 7.0 else "red"
            score_bar = tk.Frame(score_frame, bg=color, height=15)
            score_bar.place(x=0, y=0, width=int(100 * puntaje / 10), height=15)
            
            tk.Label(crit_frame, text=f"{puntaje}/10", font=("Arial", 10, "bold"), bg="white", fg=color, width=8).pack(side=tk.RIGHT, padx=5)

    def create_evaluacion_360_tab(self, notebook):
        """Crear pestaña de evaluación 360°"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="🔄 Evaluación 360°")

        tk.Label(frame, text="🔄 Evaluación 360° Integral", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        evaluacion_360_text = """
        🔄 EVALUACIÓN 360° - PROF. MARÍA GONZÁLEZ:
        ═══════════════════════════════════════════
        
        👨‍💼 EVALUACIÓN DEL SUPERVISOR:
        • Cumplimiento de objetivos: 9.2/10
        • Liderazgo pedagógico: 8.8/10
        • Innovación metodológica: 9.0/10
        
        👥 EVALUACIÓN DE PARES:
        • Colaboración: 9.1/10
        • Comunicación: 8.9/10
        • Apoyo mutuo: 9.3/10
        
        🎓 EVALUACIÓN DE ESTUDIANTES:
        • Claridad en explicaciones: 9.4/10
        • Motivación en clase: 9.0/10
        • Disponibilidad para consultas: 9.5/10
        
        👨‍👩‍👧‍👦 EVALUACIÓN DE PADRES:
        • Comunicación: 8.7/10
        • Seguimiento académico: 9.1/10
        • Profesionalismo: 9.2/10
        
        📊 RESULTADO INTEGRAL: 9.1/10 (EXCELENTE)
        
        💡 FORTALEZAS:
        • Excelente relación con estudiantes
        • Metodología innovadora
        • Compromiso institucional
        
        🎯 ÁREAS DE MEJORA:
        • Uso de tecnología educativa
        • Participación en proyectos institucionales
        """

        tk.Label(frame, text=evaluacion_360_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_resultados_tab(self, notebook):
        """Crear pestaña de resultados"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="📊 Resultados")

        tk.Label(frame, text="📊 Resultados de Evaluaciones", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Ranking de desempeño
        ranking_frame = tk.LabelFrame(frame, text="🏆 Ranking de Desempeño", 
                                     font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        ranking_frame.pack(fill=tk.X, padx=20, pady=10)

        ranking_data = [
            ("1º", "Prof. María González", "9.1/10", "Excelente"),
            ("2º", "Prof. Ana Martínez", "8.9/10", "Muy Bueno"),
            ("3º", "Prof. Carlos López", "8.7/10", "Muy Bueno"),
            ("4º", "Preceptor Roberto Silva", "8.5/10", "Bueno"),
            ("5º", "Prof. Laura Díaz", "8.3/10", "Bueno")
        ]

        for posicion, nombre, puntaje, categoria in ranking_data:
            rank_frame = tk.Frame(ranking_frame, bg="white", relief=tk.RAISED, bd=1)
            rank_frame.pack(fill=tk.X, padx=10, pady=3)
            
            tk.Label(rank_frame, text=posicion, font=("Arial", 12, "bold"), bg="white", width=5).pack(side=tk.LEFT, padx=5)
            tk.Label(rank_frame, text=nombre, font=("Arial", 10), bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            color = "gold" if posicion == "1º" else "green" if "Excelente" in categoria or "Muy Bueno" in categoria else "orange"
            tk.Label(rank_frame, text=puntaje, font=("Arial", 10, "bold"), bg="white", fg=color).pack(side=tk.RIGHT, padx=10)
            tk.Label(rank_frame, text=categoria, font=("Arial", 9), bg="white", fg=color).pack(side=tk.RIGHT, padx=5)


class GestionCapacitacionWindow:
    """Ventana para gestión de capacitación"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_window()

    def create_window(self):
        """Crear ventana de gestión de capacitación"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📚 Gestión de Capacitación")
        self.window.geometry("900x700")
        self.window.configure(bg="lightgreen")

        # Título
        title = tk.Label(self.window, text="📚 Centro de Capacitación y Desarrollo", 
                        font=("Arial", 16, "bold"), bg="lightgreen", fg="darkgreen")
        title.pack(pady=15)

        # Notebook
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Pestaña 1: Programas Activos
        self.create_programas_tab(notebook)
        
        # Pestaña 2: Crear Programa
        self.create_crear_programa_tab(notebook)
        
        # Pestaña 3: Certificaciones
        self.create_certificaciones_tab(notebook)

    def create_programas_tab(self, notebook):
        """Crear pestaña de programas activos"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="📚 Programas Activos")

        # Tabla de programas
        columns = ("Programa", "Duración", "Participantes", "Estado", "Progreso")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        # Datos de programas
        programas_data = [
            ("Tecnología Educativa", "40 hs", "12", "En curso", "75%"),
            ("Evaluación por Competencias", "30 hs", "8", "Planificado", "0%"),
            ("Neuroeducación", "25 hs", "15", "Completado", "100%"),
            ("Inclusión Educativa", "35 hs", "10", "En curso", "60%")
        ]

        for programa in programas_data:
            tree.insert("", tk.END, values=programa)

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def create_crear_programa_tab(self, notebook):
        """Crear pestaña para crear programa"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="🆕 Crear Programa")

        tk.Label(frame, text="🆕 Crear Nuevo Programa de Capacitación", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Formulario de programa
        form_frame = tk.LabelFrame(frame, text="📝 Datos del Programa", 
                                  font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        form_frame.pack(fill=tk.X, padx=20, pady=10)

        # Campos básicos
        tk.Label(form_frame, text="Nombre del Programa:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        nombre_entry = tk.Entry(form_frame, width=50)
        nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Duración (horas):", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        duracion_entry = tk.Entry(form_frame, width=20)
        duracion_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(form_frame, text="Modalidad:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        modalidad_combo = ttk.Combobox(form_frame, values=["Presencial", "Virtual", "Mixta"], state="readonly", width=47)
        modalidad_combo.grid(row=2, column=1, padx=10, pady=5)

        # Botones
        buttons_frame = tk.Frame(form_frame, bg="lightgreen")
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=15)

        tk.Button(buttons_frame, text="💾 Crear Programa", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

    def create_certificaciones_tab(self, notebook):
        """Crear pestaña de certificaciones"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="🏆 Certificaciones")

        tk.Label(frame, text="🏆 Certificaciones y Reconocimientos", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Lista de certificaciones
        cert_text = """
        🏆 CERTIFICACIONES OTORGADAS (2024-2025):
        ═══════════════════════════════════════════
        
        ✅ COMPLETADAS:
        • Prof. María González - Tecnología Educativa (40hs)
        • Prof. Ana Martínez - Neuroeducación (25hs)
        • Prof. Carlos López - Evaluación por Competencias (30hs)
        
        🔄 EN PROGRESO:
        • Prof. Laura Díaz - Inclusión Educativa (60% completado)
        • Preceptor Silva - Gestión de Conflictos (40% completado)
        
        📅 PROGRAMADAS:
        • Curso de Liderazgo Educativo (Marzo 2025)
        • Taller de Comunicación Efectiva (Abril 2025)
        • Seminario de Innovación Pedagógica (Mayo 2025)
        
        📊 ESTADÍSTICAS:
        • Total certificaciones: 15
        • Promedio de calificación: 9.2/10
        • Tasa de finalización: 95%
        """

        tk.Label(frame, text=cert_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)