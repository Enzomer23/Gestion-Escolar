"""
Gestión Institucional para Administradores
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

class GestionInstitucionalWindow:
    """Ventana para gestión institucional"""
    
    def __init__(self, parent, cal_manager):
        self.parent = parent
        self.cal_manager = cal_manager
        self.create_window()

    def create_window(self):
        """Crear ventana principal de gestión institucional"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🏛️ Gestión Institucional")
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
        title = tk.Label(scrollable_frame, text="🏛️ Gestión Institucional Integral", 
                        font=("Arial", 18, "bold"), bg="lightsteelblue", fg="darkblue")
        title.pack(pady=15)

        # Notebook con pestañas
        self.create_notebook(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_notebook(self, parent):
        """Crear notebook con pestañas"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Pestaña 1: Planificación Estratégica
        self.create_planificacion_tab(notebook)
        
        # Pestaña 2: Calidad Educativa
        self.create_calidad_tab(notebook)
        
        # Pestaña 3: Auditorías
        self.create_auditorias_tab(notebook)
        
        # Pestaña 4: Proyectos de Innovación
        self.create_innovacion_tab(notebook)

    def create_planificacion_tab(self, notebook):
        """Crear pestaña de planificación estratégica"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="🎯 Planificación Estratégica")

        tk.Label(frame, text="🎯 Planificación Estratégica Institucional", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Objetivos estratégicos
        objetivos_frame = tk.LabelFrame(frame, text="🎯 Objetivos Estratégicos 2025", 
                                       font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        objetivos_frame.pack(fill=tk.X, padx=20, pady=10)

        objetivos_text = """
        🎯 OBJETIVOS ESTRATÉGICOS INSTITUCIONALES:
        ═══════════════════════════════════════════
        
        📚 CALIDAD EDUCATIVA:
        • Mantener promedio institucional > 8.5
        • Reducir alumnos en riesgo a < 5%
        • Implementar nuevas metodologías pedagógicas
        
        👥 DESARROLLO HUMANO:
        • Capacitar 100% del personal docente
        • Implementar evaluación 360° del desempeño
        • Mejorar clima laboral institucional
        
        💰 SOSTENIBILIDAD FINANCIERA:
        • Optimizar uso de recursos en 15%
        • Diversificar fuentes de financiamiento
        • Mantener reservas de emergencia
        
        🌟 INNOVACIÓN TECNOLÓGICA:
        • Digitalizar 90% de procesos administrativos
        • Implementar aulas virtuales
        • Modernizar infraestructura tecnológica
        """

        tk.Label(objetivos_frame, text=objetivos_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_calidad_tab(self, notebook):
        """Crear pestaña de calidad educativa"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="🏆 Calidad Educativa")

        tk.Label(frame, text="🏆 Gestión de Calidad Educativa", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Indicadores de calidad
        calidad_frame = tk.LabelFrame(frame, text="📊 Indicadores de Calidad", 
                                     font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        calidad_frame.pack(fill=tk.X, padx=20, pady=10)

        indicadores_data = [
            ("Rendimiento Académico", "8.7/10", "green"),
            ("Satisfacción Familias", "87%", "green"),
            ("Retención Estudiantil", "96%", "green"),
            ("Eficiencia Docente", "89%", "orange")
        ]

        for i, (indicador, valor, color) in enumerate(indicadores_data):
            ind_frame = tk.Frame(calidad_frame, bg="white", relief=tk.RAISED, bd=1)
            ind_frame.grid(row=i//2, column=i%2, padx=10, pady=5, sticky="ew")
            
            tk.Label(ind_frame, text=indicador, font=("Arial", 10, "bold"), bg="white").pack()
            tk.Label(ind_frame, text=valor, font=("Arial", 14, "bold"), 
                    bg="white", fg=color).pack()

        for i in range(2):
            calidad_frame.grid_columnconfigure(i, weight=1)

    def create_auditorias_tab(self, notebook):
        """Crear pestaña de auditorías"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="📋 Auditorías")

        tk.Label(frame, text="📋 Auditorías y Evaluaciones", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Próximas auditorías
        auditorias_frame = tk.LabelFrame(frame, text="📅 Próximas Auditorías", 
                                        font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        auditorias_frame.pack(fill=tk.X, padx=20, pady=10)

        auditorias_data = [
            ("Auditoría Externa Provincial", "15/03/2025", "Preparación"),
            ("Evaluación Interna de Calidad", "20/02/2025", "Planificación"),
            ("Auditoría Financiera", "10/04/2025", "Pendiente")
        ]

        for auditoria, fecha, estado in auditorias_data:
            aud_frame = tk.Frame(auditorias_frame, bg="white", relief=tk.RAISED, bd=1)
            aud_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(aud_frame, text=auditoria, font=("Arial", 10, "bold"), 
                    bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            tk.Label(aud_frame, text=fecha, font=("Arial", 10), 
                    bg="white", fg="blue").pack(side=tk.RIGHT, padx=10)
            tk.Label(aud_frame, text=estado, font=("Arial", 10), 
                    bg="white", fg="orange").pack(side=tk.RIGHT, padx=10)

    def create_innovacion_tab(self, notebook):
        """Crear pestaña de proyectos de innovación"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="🌟 Innovación")

        tk.Label(frame, text="🌟 Proyectos de Innovación Educativa", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Proyectos activos
        proyectos_frame = tk.LabelFrame(frame, text="🚀 Proyectos Activos", 
                                       font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        proyectos_frame.pack(fill=tk.X, padx=20, pady=10)

        proyectos_data = [
            ("Aulas Digitales Interactivas", "75%", "En desarrollo"),
            ("Sistema de Evaluación Online", "90%", "Implementación"),
            ("Plataforma de Comunicación", "60%", "Desarrollo"),
            ("Biblioteca Digital", "85%", "Testing")
        ]

        for proyecto, progreso, estado in proyectos_data:
            proy_frame = tk.Frame(proyectos_frame, bg="white", relief=tk.RAISED, bd=1)
            proy_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(proy_frame, text=proyecto, font=("Arial", 10, "bold"), 
                    bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            # Barra de progreso
            progress_frame = tk.Frame(proy_frame, bg="lightgray", height=15, width=100)
            progress_frame.pack(side=tk.RIGHT, padx=10, pady=5)
            progress_frame.pack_propagate(False)
            
            progress_bar = tk.Frame(progress_frame, bg="green", height=15)
            progress_bar.place(x=0, y=0, width=int(100 * int(progreso.rstrip('%')) / 100), height=15)
            
            tk.Label(proy_frame, text=progreso, font=("Arial", 10), 
                    bg="white", fg="green").pack(side=tk.RIGHT, padx=5)

    def crear_proyecto_innovacion(self):
        """Crear nuevo proyecto de innovación"""
        CrearProyectoWindow(self.window)

    def evaluar_calidad_educativa(self):
        """Evaluar calidad educativa"""
        EvaluacionCalidadWindow(self.window)


class CrearProyectoWindow:
    """Ventana para crear nuevo proyecto de innovación"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_window()

    def create_window(self):
        """Crear ventana de nuevo proyecto"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🚀 Crear Proyecto de Innovación")
        self.window.geometry("700x600")
        self.window.configure(bg="lightgreen")

        # Título
        title = tk.Label(self.window, text="🚀 Nuevo Proyecto de Innovación", 
                        font=("Arial", 16, "bold"), bg="lightgreen", fg="darkgreen")
        title.pack(pady=15)

        # Formulario
        form_frame = tk.LabelFrame(self.window, text="📝 Datos del Proyecto", 
                                  font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Campos del formulario
        tk.Label(form_frame, text="Nombre del Proyecto:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        nombre_entry = tk.Entry(form_frame, width=50)
        nombre_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Categoría:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        categoria_combo = ttk.Combobox(form_frame, values=[
            "Tecnología Educativa", "Infraestructura", "Metodología Pedagógica", 
            "Comunicación", "Evaluación", "Bienestar Estudiantil"
        ], state="readonly", width=47)
        categoria_combo.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Descripción:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=2, column=0, padx=10, pady=5, sticky="nw")
        descripcion_text = tk.Text(form_frame, width=50, height=6)
        descripcion_text.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Presupuesto:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        presupuesto_entry = tk.Entry(form_frame, width=20)
        presupuesto_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Botones
        buttons_frame = tk.Frame(form_frame, bg="lightgreen")
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=15)

        tk.Button(buttons_frame, text="💾 Crear Proyecto", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=15, command=self.crear_proyecto).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="❌ Cancelar", bg="#F44336", fg="white", 
                 font=("Arial", 10), width=15, command=self.window.destroy).pack(side=tk.LEFT, padx=5)

    def crear_proyecto(self):
        """Crear el proyecto de innovación"""
        messagebox.showinfo("Proyecto Creado", 
                           "✅ Proyecto de innovación creado exitosamente\n"
                           "📊 Se ha agregado al dashboard de seguimiento")
        self.window.destroy()


class EvaluacionCalidadWindow:
    """Ventana para evaluación de calidad educativa"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_window()

    def create_window(self):
        """Crear ventana de evaluación de calidad"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🏆 Evaluación de Calidad Educativa")
        self.window.geometry("800x700")
        self.window.configure(bg="lightgreen")

        # Título
        title = tk.Label(self.window, text="🏆 Evaluación de Calidad Educativa", 
                        font=("Arial", 16, "bold"), bg="lightgreen", fg="darkgreen")
        title.pack(pady=15)

        # Indicadores de calidad
        indicadores_frame = tk.LabelFrame(self.window, text="📊 Indicadores de Calidad", 
                                         font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        indicadores_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        indicadores_text = """
        🏆 EVALUACIÓN DE CALIDAD EDUCATIVA:
        ═══════════════════════════════════════
        
        📊 INDICADORES ACADÉMICOS:
        • Rendimiento promedio: 8.7/10 ✅ (Meta: 8.5)
        • Tasa de aprobación: 94.5% ✅ (Meta: 90%)
        • Alumnos en riesgo: 4.8% ✅ (Meta: <5%)
        • Deserción escolar: 1.2% ✅ (Meta: <2%)
        
        👥 INDICADORES DE SATISFACCIÓN:
        • Satisfacción familias: 87% ⚠️ (Meta: 90%)
        • Satisfacción docentes: 89% ✅ (Meta: 85%)
        • Clima institucional: 8.4/10 ✅ (Meta: 8.0)
        
        🏛️ INDICADORES INSTITUCIONALES:
        • Cumplimiento curricular: 98% ✅
        • Infraestructura: 85% ⚠️ (Necesita mejoras)
        • Tecnología educativa: 92% ✅
        • Capacitación docente: 95% ✅
        
        📈 TENDENCIAS:
        • Mejora sostenida en los últimos 3 años
        • Fortalezas: Rendimiento académico y clima
        • Oportunidades: Infraestructura y satisfacción familias
        
        🎯 PLAN DE MEJORA:
        • Inversión en infraestructura: $300,000
        • Programa de comunicación con familias
        • Modernización de laboratorios
        """

        tk.Label(indicadores_frame, text=indicadores_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones de acción
        buttons_frame = tk.Frame(self.window, bg="lightgreen")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="📊 Generar Reporte", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📧 Enviar a Supervisión", bg="#2196F3", fg="white", 
                 font=("Arial", 10), width=20).pack(side=tk.LEFT, padx=5)