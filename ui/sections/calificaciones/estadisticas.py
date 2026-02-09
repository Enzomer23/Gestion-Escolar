"""
Estadísticas Académicas
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

class EstadisticasWindow:
    """Ventana para estadísticas académicas"""
    
    def __init__(self, parent, cal_manager):
        self.parent = parent
        self.cal_manager = cal_manager
        self.create_window()

    def create_window(self):
        """Crear ventana principal de estadísticas"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📈 Estadísticas Académicas")
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
        title = tk.Label(scrollable_frame, text="📈 Estadísticas Académicas Institucionales", 
                        font=("Arial", 18, "bold"), bg="lightcyan", fg="darkcyan")
        title.pack(pady=15)

        # Panel de métricas generales
        self.create_general_metrics(scrollable_frame)
        
        # Notebook con estadísticas detalladas
        self.create_notebook(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_general_metrics(self, parent):
        """Crear métricas generales"""
        metrics_frame = tk.LabelFrame(parent, text="📊 Métricas Generales", 
                                     font=("Arial", 12, "bold"), bg="lightcyan", 
                                     fg="darkcyan", padx=10, pady=8)
        metrics_frame.pack(fill=tk.X, pady=(0, 15))

        metrics_data = [
            ("📊 Promedio General", "8.31", "green", "Institucional"),
            ("👥 Total Alumnos", "247", "blue", "Activos"),
            ("📚 Total Materias", "25", "purple", "Activas"),
            ("📝 Total Evaluaciones", "1,247", "orange", "Registradas")
        ]

        for i, (label, value, color, info) in enumerate(metrics_data):
            metric_frame = tk.Frame(metrics_frame, bg="white", relief=tk.RAISED, bd=2)
            metric_frame.grid(row=0, column=i, padx=8, pady=5, sticky="ew")
            
            tk.Label(metric_frame, text=label, font=("Arial", 9, "bold"), bg="white").pack()
            tk.Label(metric_frame, text=value, font=("Arial", 16, "bold"), 
                    bg="white", fg=color).pack()
            tk.Label(metric_frame, text=info, font=("Arial", 8), 
                    bg="white", fg="gray").pack()

        for i in range(4):
            metrics_frame.grid_columnconfigure(i, weight=1)

    def create_notebook(self, parent):
        """Crear notebook con estadísticas"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Pestaña 1: Por Materia
        self.create_por_materia_tab(notebook)
        
        # Pestaña 2: Por Curso
        self.create_por_curso_tab(notebook)
        
        # Pestaña 3: Comparativo Temporal
        self.create_temporal_tab(notebook)
        
        # Pestaña 4: Análisis de Riesgo
        self.create_riesgo_tab(notebook)

    def create_por_materia_tab(self, notebook):
        """Crear pestaña de estadísticas por materia"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="📚 Por Materia")

        tk.Label(frame, text="📚 Estadísticas por Materia", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Tabla de estadísticas por materia
        columns = ("Materia", "Promedio", "Evaluaciones", "Aprobación", "Desv. Estándar", "Estado")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Materia":
                tree.column(col, width=150, anchor="w")
            else:
                tree.column(col, width=120, anchor="center")

        # Datos de materias
        materias_stats = [
            ("Lengua y Literatura", "8.7", "156", "97%", "0.9", "🏆 Excelente"),
            ("Historia", "8.5", "142", "95%", "1.1", "✅ Muy Bueno"),
            ("Matemáticas", "8.3", "189", "92%", "1.3", "✅ Muy Bueno"),
            ("Geografía", "8.1", "134", "90%", "1.2", "👍 Bueno"),
            ("Ciencias Naturales", "8.0", "167", "89%", "1.4", "👍 Bueno"),
            ("Física", "7.8", "98", "85%", "1.6", "⚠️ Regular"),
            ("Química", "7.9", "87", "87%", "1.5", "⚠️ Regular")
        ]

        for materia_data in materias_stats:
            estado = materia_data[5]
            if "🏆" in estado:
                tags = ("excelente",)
            elif "⚠️" in estado:
                tags = ("regular",)
            else:
                tags = ()
            
            tree.insert("", tk.END, values=materia_data, tags=tags)

        # Configurar colores
        tree.tag_configure("excelente", background="#E8F5E8")
        tree.tag_configure("regular", background="#FFF3E0")

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Análisis detallado
        analisis_frame = tk.LabelFrame(frame, text="📊 Análisis Detallado", 
                                      font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        analisis_frame.pack(fill=tk.X, padx=20, pady=10)

        analisis_text = """
        📊 ANÁLISIS ESTADÍSTICO POR MATERIA:
        ═══════════════════════════════════════
        
        🏆 MATERIAS DESTACADAS:
        • Lengua y Literatura: Mejor promedio (8.7) y menor dispersión
        • Historia: Alta tasa de aprobación (95%) y buen promedio
        • Matemáticas: Mayor cantidad de evaluaciones, promedio sólido
        
        ⚠️ MATERIAS QUE REQUIEREN ATENCIÓN:
        • Física: Promedio más bajo (7.8) y mayor dispersión
        • Química: Necesita estrategias de mejora
        
        📈 RECOMENDACIONES:
        • Replicar metodologías exitosas de Lengua en otras materias
        • Reforzar apoyo pedagógico en Física y Química
        • Mantener estándares altos en materias destacadas
        """

        tk.Label(analisis_frame, text=analisis_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_por_curso_tab(self, notebook):
        """Crear pestaña de estadísticas por curso"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="🎓 Por Curso")

        tk.Label(frame, text="🎓 Estadísticas por Curso y División", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Gráfico de barras simulado por curso
        cursos_data = [
            ("1º Año A", 8.4, "green", 25),
            ("1º Año B", 8.1, "green", 24),
            ("2º Año A", 8.7, "gold", 26),
            ("2º Año B", 7.9, "orange", 23),
            ("3º Año A", 8.3, "green", 22),
            ("3º Año B", 7.8, "orange", 21)
        ]

        for curso, promedio, color, alumnos in cursos_data:
            curso_frame = tk.Frame(frame, bg="white", relief=tk.RAISED, bd=1)
            curso_frame.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(curso_frame, text=curso, font=("Arial", 11, "bold"), 
                    bg="white", width=12, anchor="w").pack(side=tk.LEFT, padx=10)
            
            # Barra de progreso simulada
            barra_frame = tk.Frame(curso_frame, bg="lightgray", height=25, width=300)
            barra_frame.pack(side=tk.LEFT, padx=10, pady=5)
            barra_frame.pack_propagate(False)
            
            ancho_barra = int((promedio / 10) * 300)
            barra = tk.Frame(barra_frame, bg=color, height=25)
            barra.place(x=0, y=0, width=ancho_barra, height=25)
            
            tk.Label(curso_frame, text=f"{promedio}", font=("Arial", 11, "bold"), 
                    bg="white", fg=color, width=6).pack(side=tk.LEFT, padx=5)
            
            tk.Label(curso_frame, text=f"({alumnos} alumnos)", font=("Arial", 9), 
                    bg="white", fg="gray", width=12).pack(side=tk.LEFT, padx=5)

    def create_temporal_tab(self, notebook):
        """Crear pestaña de comparativo temporal"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="📅 Temporal")

        tk.Label(frame, text="📅 Evolución Temporal del Rendimiento", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Evolución temporal
        temporal_text = """
        📅 EVOLUCIÓN TEMPORAL DEL RENDIMIENTO:
        ═══════════════════════════════════════
        
        📊 EVOLUCIÓN ANUAL (2020-2025):
        2020: ███████░░░ 7.2  |  2021: ███████░░░ 7.5  |  2022: ████████░░ 7.8
        2023: ████████░░ 8.0  |  2024: ████████░░ 8.2  |  2025: ████████░░ 8.3
        
        📈 ANÁLISIS DE CRECIMIENTO:
        • Crecimiento promedio anual: +0.22 puntos
        • Mejor año de crecimiento: 2022 (+0.3)
        • Crecimiento sostenido: 5 años consecutivos
        • Proyección 2026: 8.5 puntos
        
        🎯 HITOS IMPORTANTES:
        • 2021: Implementación sistema digital
        • 2022: Programa de tutorías
        • 2023: Capacitación docente masiva
        • 2024: Sistema de alertas tempranas
        • 2025: Análisis predictivo
        
        📊 COMPARACIÓN MENSUAL (2025):
        • Marzo: 8.1 (Inicio de año)
        • Abril: 8.2 (↗ +0.1)
        • Mayo: 8.3 (↗ +0.1)
        • Junio: 8.2 (↘ -0.1)
        • Julio: 8.4 (↗ +0.2)
        • Agosto: 8.3 (↘ -0.1)
        
        🔍 FACTORES DE VARIACIÓN:
        • Estacionalidad: Mejor rendimiento en 2º cuatrimestre
        • Eventos institucionales: Impacto mínimo (-0.05)
        • Capacitaciones docentes: Impacto positivo (+0.15)
        • Apoyo familiar: Correlación alta (0.73)
        """

        tk.Label(frame, text=temporal_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_riesgo_tab(self, notebook):
        """Crear pestaña de análisis de riesgo"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="🚨 Análisis de Riesgo")

        tk.Label(frame, text="🚨 Análisis de Riesgo Académico", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Tabla de alumnos en riesgo
        riesgo_frame = tk.LabelFrame(frame, text="🚨 Alumnos en Riesgo Académico", 
                                    font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        riesgo_frame.pack(fill=tk.X, padx=20, pady=10)

        columns = ("Alumno", "Curso", "Promedio", "Materias Críticas", "Nivel Riesgo", "Acción")
        tree = ttk.Treeview(riesgo_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Alumno":
                tree.column(col, width=150, anchor="w")
            elif col == "Materias Críticas":
                tree.column(col, width=180, anchor="w")
            else:
                tree.column(col, width=100, anchor="center")

        # Datos de alumnos en riesgo
        riesgo_data = [
            ("González, Mario", "2º A", "5.8", "Matemáticas, Física", "🔴 Alto", "Plan Activo"),
            ("Herrera, Lucas", "3º B", "5.2", "Matemáticas, Química", "🔴 Crítico", "Intervención"),
            ("Rodríguez, Pedro", "1º B", "5.7", "Lengua, Historia", "🟡 Moderado", "Seguimiento"),
            ("Martínez, Carlos", "3º A", "6.0", "Física", "🟡 Leve", "Monitoreo")
        ]

        for data in riesgo_data:
            nivel = data[4]
            if "🔴" in nivel:
                tags = ("critico",)
            elif "🟡" in nivel:
                tags = ("moderado",)
            else:
                tags = ()
            
            tree.insert("", tk.END, values=data, tags=tags)

        # Configurar colores
        tree.tag_configure("critico", background="#FFCDD2")
        tree.tag_configure("moderado", background="#FFF3E0")

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Análisis de factores de riesgo
        factores_frame = tk.LabelFrame(frame, text="📊 Análisis de Factores de Riesgo", 
                                      font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        factores_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        factores_text = """
        📊 ANÁLISIS DE FACTORES DE RIESGO:
        ═══════════════════════════════════════
        
        🎯 CRITERIOS DE IDENTIFICACIÓN:
        • Promedio < 6.0: Riesgo Alto/Crítico
        • Promedio 6.0-6.5: Riesgo Moderado
        • Tendencia negativa: Riesgo Emergente
        • Asistencia < 80%: Factor agravante
        
        📊 ESTADÍSTICAS DE RIESGO:
        • Total en riesgo: 12 alumnos (4.9%)
        • Riesgo crítico: 3 alumnos (1.2%)
        • Riesgo alto: 4 alumnos (1.6%)
        • Riesgo moderado: 5 alumnos (2.0%)
        
        📈 EVOLUCIÓN DEL RIESGO:
        • Marzo: 18 alumnos en riesgo
        • Abril: 15 alumnos (-3)
        • Mayo: 12 alumnos (-3)
        • Tendencia: ↘ Mejorando (-33%)
        
        🎯 EFECTIVIDAD DE INTERVENCIONES:
        • Planes de intervención activos: 8
        • Tasa de éxito: 75% (6 de 8 mejoraron)
        • Tiempo promedio de recuperación: 6 semanas
        • Satisfacción familiar: 92%
        
        💡 ESTRATEGIAS MÁS EFECTIVAS:
        • Tutorías personalizadas: 85% éxito
        • Apoyo familiar estructurado: 78% éxito
        • Seguimiento semanal: 72% éxito
        • Adaptaciones curriculares: 68% éxito
        """

        tk.Label(factores_frame, text=factores_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones de acción
        buttons_frame = tk.Frame(frame, bg="lightcoral")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="🚨 Generar Alertas", bg="#F44336", fg="white", 
                 font=("Arial", 10), width=15, command=self.generar_alertas_riesgo).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📋 Crear Planes", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=15, command=self.crear_planes_riesgo).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📧 Notificar Padres", bg="#9C27B0", fg="white", 
                 font=("Arial", 10), width=15, command=self.notificar_padres_riesgo).pack(side=tk.LEFT, padx=5)

    def generar_alertas_riesgo(self):
        """Generar alertas para alumnos en riesgo"""
        messagebox.showinfo("Alertas Generadas", 
                           "🚨 Alertas de riesgo generadas:\n"
                           "• 3 alertas críticas enviadas\n"
                           "• 4 alertas de seguimiento\n"
                           "• Preceptores y padres notificados")

    def crear_planes_riesgo(self):
        """Crear planes de intervención para alumnos en riesgo"""
        messagebox.showinfo("Planes Creados", 
                           "📋 Planes de intervención creados:\n"
                           "• 3 planes de recuperación intensiva\n"
                           "• 4 planes de apoyo académico\n"
                           "• Seguimiento programado semanalmente")

    def notificar_padres_riesgo(self):
        """Notificar a padres de alumnos en riesgo"""
        messagebox.showinfo("Padres Notificados", 
                           "📧 Notificaciones enviadas a padres:\n"
                           "• 12 familias contactadas\n"
                           "• Reuniones programadas\n"
                           "• Planes de apoyo compartidos")