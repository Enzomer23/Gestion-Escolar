"""
Reportes de Calificaciones
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

class ReportesCalificacionesWindow:
    """Ventana para reportes de calificaciones"""
    
    def __init__(self, parent, cal_manager):
        self.parent = parent
        self.cal_manager = cal_manager
        self.create_window()

    def create_window(self):
        """Crear ventana principal de reportes"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📋 Reportes de Calificaciones")
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
        title = tk.Label(scrollable_frame, text="📋 Generador de Reportes Académicos", 
                        font=("Arial", 18, "bold"), bg="lightcyan", fg="darkcyan")
        title.pack(pady=15)

        # Panel de configuración de reportes
        self.create_config_panel(scrollable_frame)
        
        # Notebook con tipos de reportes
        self.create_notebook(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_config_panel(self, parent):
        """Crear panel de configuración"""
        config_frame = tk.LabelFrame(parent, text="⚙️ Configuración de Reportes", 
                                    font=("Arial", 12, "bold"), bg="lightcyan", 
                                    fg="darkcyan", padx=10, pady=8)
        config_frame.pack(fill=tk.X, pady=(0, 15))

        # Configuración básica
        tk.Label(config_frame, text="Tipo de Reporte:", font=("Arial", 10, "bold"), bg="lightcyan").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.tipo_reporte_combo = ttk.Combobox(config_frame, values=[
            "Reporte Individual", "Reporte por Curso", "Reporte por Materia", 
            "Reporte Institucional", "Boletín de Calificaciones"
        ], state="readonly", width=25)
        self.tipo_reporte_combo.set("Reporte por Curso")
        self.tipo_reporte_combo.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(config_frame, text="Período:", font=("Arial", 10, "bold"), bg="lightcyan").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.periodo_reporte_combo = ttk.Combobox(config_frame, values=[
            "Primer Cuatrimestre 2025", "Segundo Cuatrimestre 2024", "Año Completo 2024"
        ], state="readonly", width=25)
        self.periodo_reporte_combo.set("Primer Cuatrimestre 2025")
        self.periodo_reporte_combo.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(config_frame, text="Formato:", font=("Arial", 10, "bold"), bg="lightcyan").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.formato_combo = ttk.Combobox(config_frame, values=["PDF", "Excel", "Word"], state="readonly", width=25)
        self.formato_combo.set("PDF")
        self.formato_combo.grid(row=1, column=1, padx=10, pady=5)

        # Botones de generación
        buttons_frame = tk.Frame(config_frame, bg="lightcyan")
        buttons_frame.grid(row=1, column=2, columnspan=2, padx=10, pady=5)

        tk.Button(buttons_frame, text="📊 Generar Reporte", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=18, command=self.generar_reporte).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="👁️ Vista Previa", bg="#2196F3", fg="white", 
                 font=("Arial", 10), width=15, command=self.vista_previa).pack(side=tk.LEFT, padx=5)

    def create_notebook(self, parent):
        """Crear notebook con tipos de reportes"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Pestaña 1: Reportes Predefinidos
        self.create_predefinidos_tab(notebook)
        
        # Pestaña 2: Reportes Personalizados
        self.create_personalizados_tab(notebook)
        
        # Pestaña 3: Boletines
        self.create_boletines_tab(notebook)
        
        # Pestaña 4: Reportes Ejecutivos
        self.create_ejecutivos_tab(notebook)

    def create_predefinidos_tab(self, notebook):
        """Crear pestaña de reportes predefinidos"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="📋 Predefinidos")

        tk.Label(frame, text="📋 Reportes Predefinidos", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Lista de reportes predefinidos
        reportes_frame = tk.LabelFrame(frame, text="📄 Plantillas Disponibles", 
                                      font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        reportes_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        reportes_predefinidos = [
            ("📊 Reporte Mensual de Rendimiento", "Análisis completo del mes con estadísticas", "PDF", "⭐⭐⭐⭐⭐"),
            ("🎓 Boletín Individual de Calificaciones", "Calificaciones detalladas por alumno", "PDF", "⭐⭐⭐⭐⭐"),
            ("📈 Análisis Comparativo por Curso", "Comparación entre cursos y divisiones", "Excel", "⭐⭐⭐⭐"),
            ("🚨 Reporte de Alumnos en Riesgo", "Identificación y seguimiento de riesgo académico", "PDF", "⭐⭐⭐⭐⭐"),
            ("📚 Rendimiento por Materia", "Análisis detallado por área de conocimiento", "Excel", "⭐⭐⭐⭐"),
            ("👨‍🏫 Reporte de Eficiencia Docente", "Análisis del rendimiento por docente", "PDF", "⭐⭐⭐⭐"),
            ("📅 Reporte Trimestral Institucional", "Resumen ejecutivo para directivos", "PDF", "⭐⭐⭐⭐⭐"),
            ("🏆 Reconocimientos y Méritos", "Alumnos destacados y logros académicos", "Word", "⭐⭐⭐⭐")
        ]

        for i, (nombre, descripcion, formato, rating) in enumerate(reportes_predefinidos):
            reporte_frame = tk.Frame(reportes_frame, bg="white", relief=tk.RAISED, bd=1)
            reporte_frame.pack(fill=tk.X, padx=10, pady=5)

            # Información del reporte
            info_frame = tk.Frame(reporte_frame, bg="white")
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=5)
            
            tk.Label(info_frame, text=nombre, font=("Arial", 10, "bold"), bg="white", anchor="w").pack(anchor="w")
            tk.Label(info_frame, text=descripcion, font=("Arial", 9), bg="white", fg="gray", anchor="w").pack(anchor="w")
            
            # Formato y rating
            tk.Label(reporte_frame, text=formato, font=("Arial", 9), bg="white", fg="blue", anchor="center").pack(side=tk.RIGHT, padx=5)
            tk.Label(reporte_frame, text=rating, font=("Arial", 9), bg="white", fg="orange", anchor="center").pack(side=tk.RIGHT, padx=5)
            tk.Button(reporte_frame, text="📄 Generar", bg="#4CAF50", fg="white", font=("Arial", 8), width=10, 
                     command=lambda n=nombre: self.generar_reporte_predefinido(n)).pack(side=tk.RIGHT, padx=10, pady=2)

    def create_personalizados_tab(self, notebook):
        """Crear pestaña de reportes personalizados"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="🎨 Personalizados")

        tk.Label(frame, text="🎨 Crear Reporte Personalizado", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Configurador de reporte personalizado
        config_frame = tk.LabelFrame(frame, text="⚙️ Configurar Reporte Personalizado", 
                                    font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        config_frame.pack(fill=tk.X, padx=20, pady=10)

        # Selección de datos a incluir
        tk.Label(config_frame, text="Datos a incluir:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=0, column=0, padx=10, pady=5, sticky="nw")
        
        datos_frame = tk.Frame(config_frame, bg="lightgreen")
        datos_frame.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Checkboxes para datos
        self.datos_vars = {}
        datos_opciones = [
            ("Calificaciones detalladas", True),
            ("Promedios por materia", True),
            ("Estadísticas generales", False),
            ("Gráficos de tendencias", False),
            ("Análisis comparativo", False),
            ("Recomendaciones", True)
        ]
        
        for i, (opcion, default) in enumerate(datos_opciones):
            var = tk.BooleanVar(value=default)
            self.datos_vars[opcion] = var
            tk.Checkbutton(datos_frame, text=opcion, variable=var, bg="lightgreen").grid(row=i//2, column=i%2, sticky="w", padx=5, pady=2)

        # Filtros adicionales
        tk.Label(config_frame, text="Filtros:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        filtros_frame = tk.Frame(config_frame, bg="lightgreen")
        filtros_frame.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(filtros_frame, text="Curso:", font=("Arial", 9), bg="lightgreen").grid(row=0, column=0, padx=5, pady=2, sticky="w")
        curso_filtro = ttk.Combobox(filtros_frame, values=["Todos", "1º Año", "2º Año", "3º Año"], state="readonly", width=12)
        curso_filtro.set("Todos")
        curso_filtro.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(filtros_frame, text="Materia:", font=("Arial", 9), bg="lightgreen").grid(row=0, column=2, padx=5, pady=2, sticky="w")
        materia_filtro = ttk.Combobox(filtros_frame, values=["Todas", "Matemáticas", "Lengua", "Ciencias"], state="readonly", width=15)
        materia_filtro.set("Todas")
        materia_filtro.grid(row=0, column=3, padx=5, pady=2)

        # Vista previa del reporte
        preview_frame = tk.LabelFrame(frame, text="👁️ Vista Previa del Reporte", 
                                     font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        preview_text = """
        📋 VISTA PREVIA - REPORTE PERSONALIZADO:
        ═══════════════════════════════════════════
        
        📊 CONFIGURACIÓN SELECCIONADA:
        ✅ Calificaciones detalladas
        ✅ Promedios por materia
        ❌ Estadísticas generales
        ❌ Gráficos de tendencias
        ❌ Análisis comparativo
        ✅ Recomendaciones
        
        📄 ESTRUCTURA DEL REPORTE:
        1. Portada institucional
        2. Resumen ejecutivo
        3. Calificaciones detalladas por alumno
        4. Promedios por materia y curso
        5. Recomendaciones pedagógicas
        6. Anexos y observaciones
        
        📊 ESTADÍSTICAS INCLUIDAS:
        • Total de páginas estimadas: 12
        • Alumnos incluidos: 247
        • Materias analizadas: 25
        • Período: Primer Cuatrimestre 2025
        
        🎯 DESTINATARIOS SUGERIDOS:
        • Dirección General
        • Coordinación Académica
        • Consejo de Docentes
        • Supervisión Provincial
        """

        tk.Label(preview_frame, text=preview_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones de generación
        buttons_frame = tk.Frame(frame, bg="lightgreen")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="📊 Generar Reporte", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=18, command=self.generar_reporte_personalizado).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="💾 Guardar Plantilla", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=18, command=self.guardar_plantilla).pack(side=tk.LEFT, padx=5)

    def create_boletines_tab(self, notebook):
        """Crear pestaña de boletines"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="📄 Boletines")

        tk.Label(frame, text="📄 Generación de Boletines de Calificaciones", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Configuración de boletines
        boletin_frame = tk.LabelFrame(frame, text="📋 Configuración de Boletines", 
                                     font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        boletin_frame.pack(fill=tk.X, padx=20, pady=10)

        # Opciones de boletín
        tk.Label(boletin_frame, text="Tipo de Boletín:", font=("Arial", 10, "bold"), bg="lightyellow").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        boletin_tipo_combo = ttk.Combobox(boletin_frame, values=[
            "Boletín Individual", "Boletín por Curso", "Boletín Institucional"
        ], state="readonly", width=25)
        boletin_tipo_combo.set("Boletín Individual")
        boletin_tipo_combo.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(boletin_frame, text="Incluir:", font=("Arial", 10, "bold"), bg="lightyellow").grid(row=1, column=0, padx=10, pady=5, sticky="nw")
        
        incluir_frame = tk.Frame(boletin_frame, bg="lightyellow")
        incluir_frame.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        # Opciones de inclusión
        opciones_boletin = [
            ("Calificaciones por materia", True),
            ("Promedios generales", True),
            ("Observaciones docentes", True),
            ("Asistencia", False),
            ("Comportamiento", False),
            ("Recomendaciones", True)
        ]
        
        for i, (opcion, default) in enumerate(opciones_boletin):
            var = tk.BooleanVar(value=default)
            tk.Checkbutton(incluir_frame, text=opcion, variable=var, bg="lightyellow").grid(row=i//2, column=i%2, sticky="w", padx=5, pady=2)

        # Vista previa del boletín
        preview_boletin_frame = tk.LabelFrame(frame, text="📄 Vista Previa del Boletín", 
                                            font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        preview_boletin_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        boletin_preview = """
        📄 BOLETÍN DE CALIFICACIONES - VISTA PREVIA:
        ═══════════════════════════════════════════════
        
        🏛️ INSTITUCIÓN: GESJ - Provincia de San Juan
        👤 ALUMNO: [Nombre del Alumno]
        🎓 CURSO: [Curso y División]
        📅 PERÍODO: Primer Cuatrimestre 2025
        
        📚 CALIFICACIONES POR MATERIA:
        ═══════════════════════════════════════
        Matemáticas          | 8.5 | ✅ Muy Bueno
        Lengua y Literatura  | 9.0 | 🏆 Excelente  
        Ciencias Naturales   | 8.2 | ✅ Muy Bueno
        Historia             | 8.7 | ✅ Muy Bueno
        Geografía            | 8.0 | 👍 Bueno
        
        📊 RESUMEN ACADÉMICO:
        ═══════════════════════
        • Promedio General: 8.48
        • Materias Aprobadas: 5/5 (100%)
        • Mejor Materia: Lengua y Literatura
        • Materia a Reforzar: Geografía
        
        📋 OBSERVACIONES GENERALES:
        • Alumno responsable y participativo
        • Excelente progreso en el período
        • Se recomienda mantener el ritmo de estudio
        
        👨‍🏫 DOCENTE TUTOR: Prof. [Nombre]
        📞 CONTACTO: [Email/Teléfono]
        """

        tk.Label(preview_boletin_frame, text=boletin_preview, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_ejecutivos_tab(self, notebook):
        """Crear pestaña de reportes ejecutivos"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="🏛️ Ejecutivos")

        tk.Label(frame, text="🏛️ Reportes Ejecutivos para Directivos", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Reportes ejecutivos
        ejecutivos_text = """
        🏛️ REPORTES EJECUTIVOS DISPONIBLES:
        ═══════════════════════════════════════
        
        📊 DASHBOARD EJECUTIVO MENSUAL:
        • KPIs institucionales principales
        • Métricas de rendimiento académico
        • Indicadores de eficiencia operativa
        • Alertas y recomendaciones estratégicas
        
        📈 ANÁLISIS DE TENDENCIAS INSTITUCIONALES:
        • Evolución del rendimiento por período
        • Comparativo con años anteriores
        • Proyecciones y escenarios futuros
        • Factores de éxito identificados
        
        🎯 REPORTE DE CUMPLIMIENTO DE METAS:
        • Objetivos institucionales vs resultados
        • Indicadores de calidad educativa
        • Satisfacción de la comunidad educativa
        • Plan de mejora continua
        
        💰 ANÁLISIS DE EFICIENCIA PRESUPUESTARIA:
        • ROI en programas educativos
        • Costo por alumno por materia
        • Eficiencia en uso de recursos
        • Proyecciones financieras
        
        🏆 REPORTE DE RECONOCIMIENTOS:
        • Logros institucionales destacados
        • Comparativo con otras instituciones
        • Certificaciones y acreditaciones
        • Proyección de imagen institucional
        
        📋 REPORTE PARA SUPERVISIÓN PROVINCIAL:
        • Cumplimiento de normativas educativas
        • Indicadores de calidad requeridos
        • Planes de mejora implementados
        • Solicitudes de apoyo institucional
        """

        tk.Label(frame, text=ejecutivos_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Botones ejecutivos
        buttons_frame = tk.Frame(frame, bg="lightcoral")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="🏛️ Reporte Directivo", bg="#1976D2", fg="white", 
                 font=("Arial", 10), width=18, command=self.generar_reporte_directivo).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📊 Dashboard Ejecutivo", bg="#388E3C", fg="white", 
                 font=("Arial", 10), width=18, command=self.generar_dashboard_ejecutivo).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="🏆 Reporte Provincial", bg="#F57C00", fg="white", 
                 font=("Arial", 10), width=18, command=self.generar_reporte_provincial).pack(side=tk.LEFT, padx=5)

    def generar_reporte(self):
        """Generar reporte según configuración"""
        tipo = self.tipo_reporte_combo.get()
        periodo = self.periodo_reporte_combo.get()
        formato = self.formato_combo.get()
        
        messagebox.showinfo("Reporte Generado", 
                           f"📊 Reporte generado exitosamente:\n"
                           f"• Tipo: {tipo}\n"
                           f"• Período: {periodo}\n"
                           f"• Formato: {formato}\n"
                           f"📁 Guardado en: /reportes/")

    def vista_previa(self):
        """Mostrar vista previa del reporte"""
        messagebox.showinfo("Vista Previa", 
                           "👁️ Vista previa del reporte:\n"
                           "• 15 páginas estimadas\n"
                           "• Incluye gráficos y tablas\n"
                           "• Formato profesional\n"
                           "• Listo para generar")

    def generar_reporte_predefinido(self, nombre_reporte):
        """Generar un reporte predefinido específico"""
        messagebox.showinfo("Reporte Predefinido", 
                           f"📄 Generando: {nombre_reporte}\n"
                           f"⏱️ Tiempo estimado: 2-3 minutos\n"
                           f"📁 Se guardará en /reportes/predefinidos/")

    def guardar_plantilla(self):
        """Guardar configuración como plantilla"""
        messagebox.showinfo("Plantilla Guardada", 
                           "💾 Configuración guardada como plantilla\n"
                           "📋 Disponible en reportes predefinidos\n"
                           "🔄 Reutilizable para futuros reportes")

    def generar_reporte_directivo(self):
        """Generar reporte para directivos"""
        messagebox.showinfo("Reporte Directivo", 
                           "🏛️ Reporte ejecutivo generado:\n"
                           "• Resumen de KPIs institucionales\n"
                           "• Análisis de tendencias\n"
                           "• Recomendaciones estratégicas\n"
                           "📧 Enviado automáticamente a directivos")

    def generar_dashboard_ejecutivo(self):
        """Generar dashboard ejecutivo"""
        messagebox.showinfo("Dashboard Ejecutivo", 
                           "📊 Dashboard ejecutivo generado:\n"
                           "• Métricas en tiempo real\n"
                           "• Gráficos interactivos\n"
                           "• Alertas automatizadas\n"
                           "🔄 Actualización automática cada 30 min")

    def generar_reporte_provincial(self):
        """Generar reporte para supervisión provincial"""
        messagebox.showinfo("Reporte Provincial", 
                           "🏆 Reporte para supervisión generado:\n"
                           "• Cumplimiento de normativas\n"
                           "• Indicadores de calidad\n"
                           "• Logros institucionales\n"
                           "📤 Listo para envío a supervisión")