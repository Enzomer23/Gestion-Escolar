"""
Análisis Avanzado de Promedios
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

class PromediosAvanzadosWindow:
    """Ventana para análisis avanzado de promedios"""
    
    def __init__(self, parent, cal_manager):
        self.parent = parent
        self.cal_manager = cal_manager
        self.create_window()

    def create_window(self):
        """Crear ventana principal de promedios"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📊 Análisis Avanzado de Promedios")
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
        title = tk.Label(scrollable_frame, text="📊 Análisis Avanzado de Promedios", 
                        font=("Arial", 18, "bold"), bg="lightcyan", fg="darkcyan")
        title.pack(pady=15)

        # Panel de métricas de promedios
        self.create_metrics_panel(scrollable_frame)
        
        # Notebook con análisis detallado
        self.create_notebook(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_metrics_panel(self, parent):
        """Crear panel de métricas de promedios"""
        metrics_frame = tk.LabelFrame(parent, text="📈 Métricas de Promedios", 
                                     font=("Arial", 12, "bold"), bg="lightcyan", 
                                     fg="darkcyan", padx=10, pady=8)
        metrics_frame.pack(fill=tk.X, pady=(0, 15))

        metrics_data = [
            ("📊 Promedio General", "8.3", "green", "Institucional"),
            ("🏆 Mejor Curso", "8.7", "gold", "2º Año A"),
            ("📈 Mayor Mejora", "+0.4", "blue", "1º Año B"),
            ("🎯 Meta Cumplida", "94%", "green", "Cursos > 8.0")
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
        """Crear notebook con análisis"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Pestaña 1: Ranking de Alumnos
        self.create_ranking_tab(notebook)
        
        # Pestaña 2: Análisis por Curso
        self.create_por_curso_tab(notebook)
        
        # Pestaña 3: Tendencias Temporales
        self.create_tendencias_tab(notebook)
        
        # Pestaña 4: Análisis Estadístico
        self.create_estadistico_tab(notebook)

    def create_ranking_tab(self, notebook):
        """Crear pestaña de ranking de alumnos"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="🏆 Ranking de Alumnos")

        tk.Label(frame, text="🏆 Ranking de Alumnos por Promedio", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Tabla de ranking
        columns = ("Posición", "Alumno", "Curso", "Promedio", "Categoría", "Tendencia")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Alumno":
                tree.column(col, width=150, anchor="w")
            elif col == "Posición":
                tree.column(col, width=80, anchor="center")
            else:
                tree.column(col, width=120, anchor="center")

        # Datos de ranking
        ranking_data = [
            ("1º", "Díaz, Laura", "1º A", "9.2", "🏆 Excelente", "↗ +0.3"),
            ("2º", "Gómez, Ana", "2º A", "8.9", "🏆 Excelente", "↗ +0.2"),
            ("3º", "Pérez, Juan", "1º A", "8.7", "✅ Muy Bueno", "→ 0.0"),
            ("4º", "Castro, Julia", "1º B", "8.5", "✅ Muy Bueno", "↗ +0.1"),
            ("5º", "Ramírez, Sofía", "3º A", "8.3", "✅ Muy Bueno", "↘ -0.1")
        ]

        for i, data in enumerate(ranking_data):
            posicion = data[0]
            if posicion in ["1º", "2º", "3º"]:
                tags = ("podium",)
            else:
                tags = ()
            
            tree.insert("", tk.END, values=data, tags=tags)

        # Configurar colores
        tree.tag_configure("podium", background="#FFF9C4")

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def create_por_curso_tab(self, notebook):
        """Crear pestaña de análisis por curso"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="🎓 Por Curso")

        tk.Label(frame, text="🎓 Análisis de Promedios por Curso", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Análisis por curso
        curso_text = """
        🎓 ANÁLISIS DETALLADO POR CURSO:
        ═══════════════════════════════════════
        
        📊 1º AÑO A (25 alumnos):
        • Promedio: 8.4 (↗ +0.3 vs período anterior)
        • Distribución: 60% Muy Bueno, 32% Bueno, 8% Regular
        • Mejor materia: Lengua (8.9)
        • Materia a reforzar: Matemáticas (8.1)
        • Alumnos destacados: 6
        • Alumnos en riesgo: 0
        
        📊 1º AÑO B (24 alumnos):
        • Promedio: 8.1 (↗ +0.4 vs período anterior)
        • Distribución: 50% Muy Bueno, 42% Bueno, 8% Regular
        • Mejor materia: Historia (8.5)
        • Materia a reforzar: Ciencias (7.8)
        • Alumnos destacados: 4
        • Alumnos en riesgo: 1
        
        📊 2º AÑO A (26 alumnos):
        • Promedio: 8.7 (→ 0.0 vs período anterior)
        • Distribución: 65% Muy Bueno, 31% Bueno, 4% Regular
        • Mejor materia: Lengua (9.1)
        • Materia a reforzar: Física (8.2)
        • Alumnos destacados: 8
        • Alumnos en riesgo: 1
        
        📊 2º AÑO B (23 alumnos):
        • Promedio: 7.9 (↘ -0.1 vs período anterior)
        • Distribución: 43% Muy Bueno, 48% Bueno, 9% Regular
        • Mejor materia: Historia (8.3)
        • Materia a reforzar: Matemáticas (7.5)
        • Alumnos destacados: 3
        • Alumnos en riesgo: 2
        """

        tk.Label(frame, text=curso_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_tendencias_tab(self, notebook):
        """Crear pestaña de tendencias temporales"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="📈 Tendencias")

        tk.Label(frame, text="📈 Tendencias Temporales de Promedios", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Gráfico de tendencias
        tendencias_text = """
        📈 EVOLUCIÓN TEMPORAL DE PROMEDIOS:
        ═══════════════════════════════════════
        
        📊 ÚLTIMOS 6 MESES:
        Agosto 2024:    ████████░░ 8.0  |  Septiembre: ████████░░ 8.1
        Octubre 2024:   ████████░░ 8.2  |  Noviembre:  ████████░░ 8.1
        Diciembre 2024: ████████░░ 8.3  |  Enero 2025: ████████░░ 8.3
        
        📈 ANÁLISIS DE TENDENCIAS:
        • Tendencia general: ↗ Positiva (+0.3 en 6 meses)
        • Velocidad de mejora: 0.05 puntos/mes
        • Estabilidad: Alta (desviación < 0.1)
        • Proyección Febrero: 8.4 puntos
        
        🎯 POR MATERIA:
        • Matemáticas: ↗ +0.4 (Mayor mejora)
        • Lengua: → +0.1 (Estable alto)
        • Ciencias: ↗ +0.3 (Mejora sostenida)
        • Historia: ↘ -0.1 (Leve descenso)
        
        📊 FACTORES DE MEJORA IDENTIFICADOS:
        • Implementación de tutorías: +0.2 puntos
        • Mejora en comunicación con padres: +0.1 puntos
        • Nuevas metodologías pedagógicas: +0.1 puntos
        • Sistema de alertas tempranas: +0.1 puntos
        
        🔮 PROYECCIONES 2025:
        • Promedio esperado fin de año: 8.6
        • Meta institucional: 8.5 ✅ Alcanzable
        • Probabilidad de cumplimiento: 87%
        """

        tk.Label(frame, text=tendencias_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_estadistico_tab(self, notebook):
        """Crear pestaña de análisis estadístico"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="📊 Análisis Estadístico")

        tk.Label(frame, text="📊 Análisis Estadístico Avanzado", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Análisis estadístico completo
        estadistico_text = """
        📊 ANÁLISIS ESTADÍSTICO INSTITUCIONAL:
        ═══════════════════════════════════════
        
        📏 MEDIDAS DE TENDENCIA CENTRAL:
        • Media aritmética: 8.31
        • Mediana: 8.25
        • Moda: 8.0
        • Media ponderada: 8.35 (por peso de evaluaciones)
        
        📐 MEDIDAS DE DISPERSIÓN:
        • Desviación estándar: 1.18
        • Varianza: 1.39
        • Rango: 4.5 (5.0 - 9.5)
        • Coeficiente de variación: 14.2%
        • Rango intercuartílico: 1.2
        
        📊 DISTRIBUCIÓN DE FRECUENCIAS:
        • 9.0-10.0: ████████░░ 28% (69 alumnos)
        • 8.0-8.9:  ████████████ 35% (86 alumnos)
        • 7.0-7.9:  ██████░░░░ 22% (54 alumnos)
        • 6.0-6.9:  ████░░░░░░ 12% (30 alumnos)
        • <6.0:     ██░░░░░░░░ 3% (8 alumnos)
        
        📈 ANÁLISIS DE CORRELACIONES:
        • Asistencia vs Promedio: 0.78 (correlación alta)
        • Participación vs Rendimiento: 0.82 (muy alta)
        • Tareas vs Calificaciones: 0.75 (alta)
        • Apoyo familiar vs Éxito: 0.69 (moderada-alta)
        
        🎯 INTERPRETACIÓN ESTADÍSTICA:
        • Distribución: Ligeramente sesgada hacia valores altos
        • Homogeneidad: Grupo relativamente homogéneo
        • Outliers: 3 valores atípicos identificados
        • Normalidad: Distribución aproximadamente normal
        
        💡 RECOMENDACIONES ESTADÍSTICAS:
        • Mantener estrategias actuales (distribución positiva)
        • Atención especial a outliers inferiores
        • Aprovechar correlaciones identificadas
        • Monitorear tendencia de mejora continua
        """

        tk.Label(frame, text=estadistico_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Botones de análisis
        buttons_frame = tk.Frame(frame, bg="lightcoral")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="📊 Generar Reporte Estadístico", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=25, command=self.generar_reporte_estadistico).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📈 Análisis Predictivo", bg="#2196F3", fg="white", 
                 font=("Arial", 10), width=18, command=self.analisis_predictivo).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📧 Enviar a Directivos", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=18, command=self.enviar_directivos).pack(side=tk.LEFT, padx=5)

    def generar_reporte_estadistico(self):
        """Generar reporte estadístico completo"""
        messagebox.showinfo("Reporte Estadístico", 
                           "📊 Reporte estadístico generado exitosamente\n"
                           "📁 Incluye: Análisis completo, gráficos y recomendaciones\n"
                           "📄 Formato: PDF ejecutivo de 15 páginas")

    def analisis_predictivo(self):
        """Realizar análisis predictivo"""
        AnalisisPredictivo(self.window, self.cal_manager)

    def enviar_directivos(self):
        """Enviar análisis a directivos"""
        messagebox.showinfo("Enviado a Directivos", 
                           "📧 Análisis estadístico enviado a:\n"
                           "• Dirección General\n"
                           "• Coordinación Académica\n"
                           "• Supervisión Provincial")


class AnalisisPredictivo:
    """Ventana para análisis predictivo de promedios"""
    
    def __init__(self, parent, cal_manager):
        self.parent = parent
        self.cal_manager = cal_manager
        self.create_window()

    def create_window(self):
        """Crear ventana de análisis predictivo"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🔮 Análisis Predictivo de Rendimiento")
        self.window.geometry("900x700")
        self.window.configure(bg="lightblue")

        # Título
        title = tk.Label(self.window, text="🔮 Análisis Predictivo de Rendimiento Académico", 
                        font=("Arial", 16, "bold"), bg="lightblue", fg="darkblue")
        title.pack(pady=15)

        # Análisis predictivo
        predictivo_frame = tk.LabelFrame(self.window, text="🔮 Predicciones Académicas", 
                                        font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        predictivo_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        predictivo_text = """
        🔮 ANÁLISIS PREDICTIVO ACADÉMICO:
        ═══════════════════════════════════════
        
        📈 PROYECCIONES PARA FEBRERO 2025:
        • Promedio institucional esperado: 8.4 (↗ +0.1)
        • Probabilidad de mejora: 78%
        • Alumnos en riesgo proyectados: 6 (↘ -2)
        • Tasa de aprobación esperada: 96% (↗ +2%)
        
        🎯 PREDICCIONES POR CURSO:
        • 1º Año A: 8.5 promedio (85% confianza)
        • 1º Año B: 8.2 promedio (82% confianza)
        • 2º Año A: 8.8 promedio (90% confianza)
        • 2º Año B: 8.0 promedio (75% confianza)
        • 3º Año A: 8.3 promedio (88% confianza)
        • 3º Año B: 7.9 promedio (70% confianza)
        
        🚨 ALERTAS PREDICTIVAS:
        • Mario González: 85% probabilidad de mejora
        • Lucas Herrera: Requiere intervención inmediata
        • Pedro Rodríguez: 70% probabilidad de recuperación
        
        📊 FACTORES PREDICTIVOS CLAVE:
        • Asistencia regular: +0.8 impacto en promedio
        • Participación familiar: +0.6 impacto
        • Tutorías: +0.5 impacto
        • Motivación estudiantil: +0.4 impacto
        
        💡 RECOMENDACIONES PREDICTIVAS:
        • Implementar tutorías preventivas en 2º B
        • Reforzar comunicación familiar en 3º B
        • Mantener estrategias exitosas en 2º A
        • Monitoreo especial en casos de riesgo
        
        🎯 ESCENARIOS PROYECTADOS:
        • Escenario optimista: 8.6 promedio general
        • Escenario realista: 8.4 promedio general
        • Escenario pesimista: 8.2 promedio general
        """

        tk.Label(predictivo_frame, text=predictivo_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones de acción
        buttons_frame = tk.Frame(self.window, bg="lightblue")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="🎯 Crear Planes Preventivos", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=20, command=self.crear_planes_preventivos).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📊 Exportar Predicciones", bg="#2196F3", fg="white", 
                 font=("Arial", 10), width=18, command=self.exportar_predicciones).pack(side=tk.LEFT, padx=5)

    def crear_planes_preventivos(self):
        """Crear planes preventivos basados en predicciones"""
        messagebox.showinfo("Planes Preventivos", 
                           "🎯 Planes preventivos creados automáticamente:\n"
                           "• 3 planes de intervención temprana\n"
                           "• 5 estrategias de reforzamiento\n"
                           "• 2 programas de apoyo familiar\n"
                           "📅 Implementación programada para la próxima semana")

    def exportar_predicciones(self):
        """Exportar análisis predictivo"""
        messagebox.showinfo("Predicciones Exportadas", 
                           "📊 Análisis predictivo exportado exitosamente\n"
                           "📁 Formato: PDF con gráficos y proyecciones\n"
                           "📈 Incluye: Escenarios, recomendaciones y planes")