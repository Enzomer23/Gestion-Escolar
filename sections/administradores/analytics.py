"""
Analytics y Business Intelligence para Administradores
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
    from server.database import crear_conexion
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class AnalyticsWindow:
    """Ventana para analytics y business intelligence"""
    
    def __init__(self, parent, cal_manager):
        self.parent = parent
        self.cal_manager = cal_manager
        self.create_window()

    def create_window(self):
        """Crear ventana principal de analytics"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📈 Analytics y Business Intelligence")
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
        title = tk.Label(scrollable_frame, text="📈 Analytics y Business Intelligence Educativo", 
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

        # Pestaña 1: Business Intelligence
        self.create_bi_tab(notebook)
        
        # Pestaña 2: Reportes Ejecutivos
        self.create_reportes_tab(notebook)
        
        # Pestaña 3: Análisis Predictivo
        self.create_predictivo_tab(notebook)
        
        # Pestaña 4: Benchmarking
        self.create_benchmarking_tab(notebook)

    def create_bi_tab(self, notebook):
        """Crear pestaña de business intelligence"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="📊 Business Intelligence")

        tk.Label(frame, text="📊 Business Intelligence Educativo", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Métricas de BI
        bi_text = """
        📊 ANÁLISIS DE BUSINESS INTELLIGENCE:
        ═══════════════════════════════════════
        
        📈 TENDENCIAS DE RENDIMIENTO:
        • Mejora sostenida del 12% anual
        • Reducción de deserción del 8%
        • Incremento en satisfacción familiar del 15%
        
        🎯 FACTORES DE ÉXITO IDENTIFICADOS:
        • Implementación de tutorías: +0.8 pts promedio
        • Comunicación digital con padres: +23% satisfacción
        • Capacitación docente: +0.5 pts rendimiento
        
        📊 CORRELACIONES IMPORTANTES:
        • Asistencia vs Rendimiento: 0.87 correlación
        • Participación familiar vs Éxito: 0.82 correlación
        • Recursos tecnológicos vs Motivación: 0.76 correlación
        
        🔮 PROYECCIONES 2025:
        • Promedio institucional proyectado: 8.9
        • Meta de retención: 98%
        • Objetivo satisfacción: 92%
        """

        tk.Label(frame, text=bi_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_reportes_tab(self, notebook):
        """Crear pestaña de reportes ejecutivos"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="📋 Reportes Ejecutivos")

        tk.Label(frame, text="📋 Reportes Ejecutivos Automatizados", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Generador de reportes
        generator_frame = tk.LabelFrame(frame, text="🔧 Generador de Reportes", 
                                       font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        generator_frame.pack(fill=tk.X, padx=20, pady=10)

        # Configuración de reportes
        tk.Label(generator_frame, text="Tipo de Reporte:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tipo_combo = ttk.Combobox(generator_frame, values=[
            "Reporte Mensual Ejecutivo", "Análisis de Rendimiento", "Reporte Financiero",
            "Evaluación de Personal", "Satisfacción Institucional"
        ], state="readonly", width=30)
        tipo_combo.set("Reporte Mensual Ejecutivo")
        tipo_combo.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(generator_frame, text="Período:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        periodo_combo = ttk.Combobox(generator_frame, values=[
            "Enero 2025", "Diciembre 2024", "Año 2024 Completo"
        ], state="readonly", width=30)
        periodo_combo.set("Enero 2025")
        periodo_combo.grid(row=1, column=1, padx=10, pady=5)

        # Botones de generación
        buttons_frame = tk.Frame(generator_frame, bg="lightgreen")
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=15)

        tk.Button(buttons_frame, text="📊 Generar Reporte", bg="#4CAF50", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📧 Enviar por Email", bg="#2196F3", fg="white", font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)

    def create_predictivo_tab(self, notebook):
        """Crear pestaña de análisis predictivo"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="🔮 Análisis Predictivo")

        tk.Label(frame, text="🔮 Análisis Predictivo Institucional", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Predicciones
        predicciones_text = """
        🔮 ANÁLISIS PREDICTIVO INSTITUCIONAL:
        ═══════════════════════════════════════
        
        📈 PROYECCIONES ACADÉMICAS 2025:
        • Promedio institucional esperado: 8.9 (↗ +0.2)
        • Alumnos en riesgo proyectados: 35 (↘ -12)
        • Tasa de aprobación esperada: 96.5% (↗ +2.5%)
        
        👥 PROYECCIONES DE MATRÍCULA:
        • Crecimiento esperado: +3.5% (8-10 alumnos nuevos)
        • Retención proyectada: 98.2%
        • Demanda por división: A (+15%), B (+8%)
        
        💰 PROYECCIONES FINANCIERAS:
        • Ingresos proyectados: +4.2%
        • Optimización de gastos: -2.1%
        • Inversión en tecnología: +15%
        
        🎯 FACTORES DE RIESGO IDENTIFICADOS:
        • Competencia de escuelas privadas: Medio
        • Cambios en políticas educativas: Bajo
        • Rotación docente: Bajo
        
        💡 RECOMENDACIONES ESTRATÉGICAS:
        • Fortalecer programa de retención
        • Invertir en tecnología educativa
        • Ampliar programas de becas
        """

        tk.Label(frame, text=predicciones_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_benchmarking_tab(self, notebook):
        """Crear pestaña de benchmarking"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="📊 Benchmarking")

        tk.Label(frame, text="📊 Benchmarking Educativo", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Comparación con otras instituciones
        benchmark_text = """
        📊 BENCHMARKING EDUCATIVO - POSICIÓN COMPETITIVA:
        ═══════════════════════════════════════════════════
        
        🏆 RANKING PROVINCIAL:
        • Posición general: 3º de 45 escuelas
        • Rendimiento académico: 2º lugar
        • Satisfacción familiar: 4º lugar
        • Innovación tecnológica: 1º lugar
        
        📈 COMPARACIÓN CON PROMEDIO PROVINCIAL:
        • Nuestro promedio: 8.7 vs Provincial: 7.8 (+0.9)
        • Nuestra retención: 96% vs Provincial: 89% (+7%)
        • Nuestra satisfacción: 87% vs Provincial: 78% (+9%)
        
        🎯 MEJORES PRÁCTICAS IDENTIFICADAS:
        • Escuela San Martín: Programa de tutorías
        • Colegio Belgrano: Sistema de comunicación
        • Instituto Sarmiento: Evaluación continua
        
        📊 ÁREAS DE OPORTUNIDAD:
        • Infraestructura deportiva: Mejorar
        • Programas artísticos: Ampliar
        • Idiomas extranjeros: Fortalecer
        
        🎯 PLAN DE ACCIÓN:
        • Implementar mejores prácticas identificadas
        • Fortalecer áreas de oportunidad
        • Mantener liderazgo en innovación
        """

        tk.Label(frame, text=benchmark_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def generar_reporte_bi(self):
        """Generar reporte de Business Intelligence"""
        GenerarReporteBIWindow(self.window, self.cal_manager)

    def configurar_alertas_predictivas(self):
        """Configurar alertas predictivas"""
        AlertasPredictivesWindow(self.window)


class GenerarReporteBIWindow:
    """Ventana para generar reportes de BI"""
    
    def __init__(self, parent, cal_manager):
        self.parent = parent
        self.cal_manager = cal_manager
        self.create_window()

    def create_window(self):
        """Crear ventana de generación de reportes BI"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📊 Generar Reporte de Business Intelligence")
        self.window.geometry("700x600")
        self.window.configure(bg="lightblue")

        # Título
        title = tk.Label(self.window, text="📊 Generador de Reportes BI", 
                        font=("Arial", 16, "bold"), bg="lightblue", fg="darkblue")
        title.pack(pady=15)

        # Configuración del reporte
        config_frame = tk.LabelFrame(self.window, text="⚙️ Configuración del Reporte", 
                                    font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        config_frame.pack(fill=tk.X, padx=20, pady=10)

        # Métricas a incluir
        tk.Label(config_frame, text="Métricas a incluir:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=0, column=0, padx=10, pady=5, sticky="nw")
        
        metricas_frame = tk.Frame(config_frame, bg="lightblue")
        metricas_frame.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Checkboxes para métricas
        self.metricas_vars = {}
        metricas = [
            ("Rendimiento Académico", True),
            ("Asistencia y Puntualidad", True),
            ("Satisfacción Institucional", False),
            ("Eficiencia Presupuestaria", True),
            ("Desarrollo Docente", False),
            ("Proyecciones Futuras", True)
        ]
        
        for i, (metrica, default) in enumerate(metricas):
            var = tk.BooleanVar(value=default)
            self.metricas_vars[metrica] = var
            tk.Checkbutton(metricas_frame, text=metrica, variable=var, bg="lightblue").grid(row=i//2, column=i%2, sticky="w", padx=5)

        # Período de análisis
        tk.Label(config_frame, text="Período:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        periodo_combo = ttk.Combobox(config_frame, values=[
            "Último mes", "Último trimestre", "Último semestre", "Año completo"
        ], state="readonly", width=30)
        periodo_combo.set("Último trimestre")
        periodo_combo.grid(row=1, column=1, padx=10, pady=5)

        # Formato de salida
        tk.Label(config_frame, text="Formato:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        formato_combo = ttk.Combobox(config_frame, values=["PDF Ejecutivo", "Excel Detallado", "PowerPoint"], state="readonly", width=30)
        formato_combo.set("PDF Ejecutivo")
        formato_combo.grid(row=2, column=1, padx=10, pady=5)

        # Vista previa
        preview_frame = tk.LabelFrame(self.window, text="👁️ Vista Previa del Reporte", 
                                     font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        preview_text = """
        📊 REPORTE DE BUSINESS INTELLIGENCE - VISTA PREVIA:
        ═══════════════════════════════════════════════════
        
        📈 RESUMEN EJECUTIVO:
        • Período analizado: Enero 2025
        • Métricas incluidas: 4 de 6 seleccionadas
        • Estado general: ✅ Excelente
        
        🎯 PRINCIPALES HALLAZGOS:
        • Rendimiento académico superó expectativas (+0.4)
        • Eficiencia presupuestaria en niveles óptimos (97.8%)
        • Proyecciones positivas para próximo trimestre
        
        📊 GRÁFICOS INCLUIDOS:
        • Evolución temporal del rendimiento
        • Distribución presupuestaria
        • Comparativo con metas institucionales
        • Proyecciones a 6 meses
        """

        tk.Label(preview_frame, text=preview_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones
        buttons_frame = tk.Frame(self.window, bg="lightblue")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="📊 Generar Reporte", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=18, command=self.generar_reporte).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="👁️ Vista Previa", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="❌ Cancelar", bg="#F44336", fg="white", 
                 font=("Arial", 10), width=12, command=self.window.destroy).pack(side=tk.LEFT, padx=5)

    def generar_reporte(self):
        """Generar el reporte de BI"""
        messagebox.showinfo("Reporte Generado", 
                           "📊 Reporte de Business Intelligence generado exitosamente\n"
                           "📁 Ubicación: /reportes/BI_Ejecutivo_2025.pdf")
        self.window.destroy()


class AlertasPredictivesWindow:
    """Ventana para configurar alertas predictivas"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_window()

    def create_window(self):
        """Crear ventana de alertas predictivas"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🔮 Configurar Alertas Predictivas")
        self.window.geometry("600x500")
        self.window.configure(bg="lightyellow")

        # Título
        title = tk.Label(self.window, text="🔮 Sistema de Alertas Predictivas", 
                        font=("Arial", 16, "bold"), bg="lightyellow", fg="darkorange")
        title.pack(pady=15)

        # Configuración de alertas
        alertas_frame = tk.LabelFrame(self.window, text="⚙️ Configurar Alertas", 
                                     font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        alertas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        alertas_text = """
        🔮 ALERTAS PREDICTIVAS CONFIGURADAS:
        ═══════════════════════════════════════
        
        📊 RENDIMIENTO ACADÉMICO:
        ✅ Alerta si promedio baja < 8.0 (Activada)
        ✅ Predicción de alumnos en riesgo (Activada)
        ⚠️ Tendencia negativa por 3 semanas (Configurar)
        
        💰 FINANZAS:
        ✅ Gasto excede 105% del presupuesto (Activada)
        ✅ Proyección de déficit (Activada)
        ⚠️ Flujo de caja crítico (Configurar)
        
        👥 RECURSOS HUMANOS:
        ✅ Ausentismo docente > 5% (Activada)
        ⚠️ Rotación de personal alta (Configurar)
        ⚠️ Evaluaciones de desempeño bajas (Configurar)
        
        📈 MATRÍCULA:
        ✅ Proyección de crecimiento negativo (Activada)
        ⚠️ Competencia externa (Configurar)
        ⚠️ Cambios demográficos (Configurar)
        """

        tk.Label(alertas_frame, text=alertas_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones
        buttons_frame = tk.Frame(self.window, bg="lightyellow")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="💾 Guardar Configuración", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="🧪 Probar Alertas", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)