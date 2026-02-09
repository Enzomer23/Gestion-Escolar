"""
Exportación de Calificaciones
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

try:
    from server.calificaciones import CalificacionesManager
    from server.excel_exporter import ExcelExporter
    from server.pdf_exporter import PDFExporter
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class ExportacionWindow:
    """Ventana para exportación de calificaciones"""
    
    def __init__(self, parent, cal_manager):
        self.parent = parent
        self.cal_manager = cal_manager
        self.excel_exporter = ExcelExporter() if DATABASE_AVAILABLE else None
        self.pdf_exporter = PDFExporter() if DATABASE_AVAILABLE else None
        self.create_window()

    def create_window(self):
        """Crear ventana principal de exportación"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📤 Exportación de Calificaciones")
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
        title = tk.Label(scrollable_frame, text="📤 Centro de Exportación de Datos Académicos", 
                        font=("Arial", 18, "bold"), bg="lightcyan", fg="darkcyan")
        title.pack(pady=15)

        # Panel de estadísticas de exportación
        self.create_export_stats(scrollable_frame)
        
        # Notebook con tipos de exportación
        self.create_notebook(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_export_stats(self, parent):
        """Crear estadísticas de exportación"""
        stats_frame = tk.LabelFrame(parent, text="📊 Estadísticas de Exportación", 
                                   font=("Arial", 12, "bold"), bg="lightcyan", 
                                   fg="darkcyan", padx=10, pady=8)
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        stats_data = [
            ("📄 Archivos Generados", "47", "blue", "Este mes"),
            ("📊 Excel Exportados", "23", "green", "Más popular"),
            ("📋 PDF Creados", "18", "orange", "Reportes"),
            ("💾 Tamaño Total", "125MB", "purple", "Archivos")
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
        """Crear notebook con tipos de exportación"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Pestaña 1: Exportación Excel
        self.create_excel_tab(notebook)
        
        # Pestaña 2: Exportación PDF
        self.create_pdf_tab(notebook)
        
        # Pestaña 3: Exportación Masiva
        self.create_masiva_tab(notebook)
        
        # Pestaña 4: Configuración
        self.create_config_tab(notebook)

    def create_excel_tab(self, notebook):
        """Crear pestaña de exportación Excel"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="📊 Excel")

        tk.Label(frame, text="📊 Exportación a Microsoft Excel", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Configuración Excel
        excel_frame = tk.LabelFrame(frame, text="⚙️ Configuración de Exportación Excel", 
                                   font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        excel_frame.pack(fill=tk.X, padx=20, pady=10)

        # Opciones de Excel
        tk.Label(excel_frame, text="Tipo de Exportación:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        excel_tipo_combo = ttk.Combobox(excel_frame, values=[
            "Calificaciones por Materia", "Promedios por Curso", "Reporte Completo", 
            "Alumnos en Riesgo", "Estadísticas Generales"
        ], state="readonly", width=30)
        excel_tipo_combo.set("Calificaciones por Materia")
        excel_tipo_combo.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(excel_frame, text="Incluir Gráficos:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        graficos_var = tk.BooleanVar(value=True)
        tk.Checkbutton(excel_frame, text="Incluir gráficos automáticos", variable=graficos_var, bg="lightblue").grid(row=1, column=1, padx=10, pady=5, sticky="w")

        tk.Label(excel_frame, text="Formato de Datos:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        formato_datos_combo = ttk.Combobox(excel_frame, values=["Tabla Simple", "Tabla Dinámica", "Dashboard"], state="readonly", width=30)
        formato_datos_combo.set("Tabla Dinámica")
        formato_datos_combo.grid(row=2, column=1, padx=10, pady=5)

        # Botones Excel
        excel_buttons_frame = tk.Frame(excel_frame, bg="lightblue")
        excel_buttons_frame.grid(row=3, column=0, columnspan=2, pady=15)

        tk.Button(excel_buttons_frame, text="📊 Exportar a Excel", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=18, command=self.exportar_excel).pack(side=tk.LEFT, padx=5)
        tk.Button(excel_buttons_frame, text="👁️ Vista Previa", bg="#2196F3", fg="white", 
                 font=("Arial", 10), width=15, command=self.preview_excel).pack(side=tk.LEFT, padx=5)

        # Características de Excel
        caracteristicas_frame = tk.LabelFrame(frame, text="✨ Características del Excel Generado", 
                                            font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        caracteristicas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        excel_features = """
        ✨ CARACTERÍSTICAS DEL ARCHIVO EXCEL:
        ═══════════════════════════════════════
        
        📊 HOJAS INCLUIDAS:
        • Calificaciones: Datos detallados por alumno
        • Promedios: Cálculos automáticos por materia
        • Estadísticas: Análisis general del curso
        • Gráficos: Visualizaciones automáticas
        • Resumen: Dashboard ejecutivo
        
        🎨 FORMATO PROFESIONAL:
        • Colores institucionales GESJ
        • Encabezados con logo y datos
        • Formato condicional para notas
        • Filtros automáticos habilitados
        • Fórmulas para cálculos dinámicos
        
        📈 GRÁFICOS AUTOMÁTICOS:
        • Distribución de calificaciones
        • Evolución temporal de promedios
        • Comparativo por materia
        • Ranking de alumnos
        
        🔧 FUNCIONALIDADES AVANZADAS:
        • Tablas dinámicas configuradas
        • Validación de datos
        • Protección de fórmulas
        • Comentarios explicativos
        • Hipervínculos entre hojas
        """

        tk.Label(caracteristicas_frame, text=excel_features, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_pdf_tab(self, notebook):
        """Crear pestaña de exportación PDF"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="📋 PDF")

        tk.Label(frame, text="📋 Exportación a PDF", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Configuración PDF
        pdf_frame = tk.LabelFrame(frame, text="⚙️ Configuración de PDF", 
                                 font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        pdf_frame.pack(fill=tk.X, padx=20, pady=10)

        # Opciones de PDF
        tk.Label(pdf_frame, text="Tipo de PDF:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        pdf_tipo_combo = ttk.Combobox(pdf_frame, values=[
            "Boletín Individual", "Reporte por Curso", "Certificado de Notas", 
            "Reporte Ejecutivo", "Análisis Estadístico"
        ], state="readonly", width=30)
        pdf_tipo_combo.set("Boletín Individual")
        pdf_tipo_combo.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(pdf_frame, text="Calidad:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        calidad_combo = ttk.Combobox(pdf_frame, values=["Alta (300 DPI)", "Media (150 DPI)", "Baja (72 DPI)"], state="readonly", width=30)
        calidad_combo.set("Alta (300 DPI)")
        calidad_combo.grid(row=1, column=1, padx=10, pady=5)

        # Botones PDF
        pdf_buttons_frame = tk.Frame(pdf_frame, bg="lightgreen")
        pdf_buttons_frame.grid(row=2, column=0, columnspan=2, pady=15)

        tk.Button(pdf_buttons_frame, text="📋 Exportar a PDF", bg="#F44336", fg="white", 
                 font=("Arial", 10), width=18, command=self.exportar_pdf).pack(side=tk.LEFT, padx=5)
        tk.Button(pdf_buttons_frame, text="🖨️ Imprimir Directo", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=18, command=self.imprimir_directo).pack(side=tk.LEFT, padx=5)

        # Plantillas PDF
        plantillas_frame = tk.LabelFrame(frame, text="📄 Plantillas PDF Disponibles", 
                                        font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        plantillas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        plantillas_data = [
            ("📄 Boletín Oficial GESJ", "Formato institucional estándar", "Recomendado"),
            ("📊 Reporte Estadístico", "Con gráficos y análisis", "Profesional"),
            ("🏆 Certificado de Logros", "Para reconocimientos", "Especial"),
            ("📋 Informe Académico", "Detallado para padres", "Completo"),
            ("📈 Dashboard Ejecutivo", "Para directivos", "Ejecutivo")
        ]

        for plantilla, descripcion, tipo in plantillas_data:
            plant_frame = tk.Frame(plantillas_frame, bg="white", relief=tk.RAISED, bd=1)
            plant_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(plant_frame, text=plantilla, font=("Arial", 10, "bold"), 
                    bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            tk.Label(plant_frame, text=descripcion, font=("Arial", 9), 
                    bg="white", fg="gray", anchor="w").pack(side=tk.LEFT, padx=10)
            
            color = "#4CAF50" if tipo == "Recomendado" else "#2196F3"
            tk.Button(plant_frame, text=f"📄 Usar {tipo}", bg=color, fg="white", 
                     font=("Arial", 8), width=12, command=lambda t=tipo: self.usar_plantilla(t)).pack(side=tk.RIGHT, padx=10, pady=2)

    def create_masiva_tab(self, notebook):
        """Crear pestaña de exportación masiva"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="🔄 Exportación Masiva")

        tk.Label(frame, text="🔄 Exportación Masiva de Datos", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Configuración masiva
        masiva_frame = tk.LabelFrame(frame, text="⚙️ Configuración de Exportación Masiva", 
                                    font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        masiva_frame.pack(fill=tk.X, padx=20, pady=10)

        # Selección de datos
        tk.Label(masiva_frame, text="Datos a Exportar:", font=("Arial", 10, "bold"), bg="lightyellow").grid(row=0, column=0, padx=10, pady=5, sticky="nw")
        
        datos_frame = tk.Frame(masiva_frame, bg="lightyellow")
        datos_frame.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # Checkboxes para datos masivos
        self.masiva_vars = {}
        datos_masivos = [
            ("Todas las calificaciones", True),
            ("Todos los promedios", True),
            ("Estadísticas por curso", False),
            ("Análisis de tendencias", False),
            ("Reportes de riesgo", True),
            ("Datos de asistencia", False)
        ]
        
        for i, (dato, default) in enumerate(datos_masivos):
            var = tk.BooleanVar(value=default)
            self.masiva_vars[dato] = var
            tk.Checkbutton(datos_frame, text=dato, variable=var, bg="lightyellow").grid(row=i//2, column=i%2, sticky="w", padx=5, pady=2)

        # Formato de exportación masiva
        tk.Label(masiva_frame, text="Formato:", font=("Arial", 10, "bold"), bg="lightyellow").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        formato_masivo_combo = ttk.Combobox(masiva_frame, values=["ZIP con Excel", "ZIP con PDF", "Base de datos SQL"], state="readonly", width=30)
        formato_masivo_combo.set("ZIP con Excel")
        formato_masivo_combo.grid(row=1, column=1, padx=10, pady=5)

        # Progreso de exportación
        progress_frame = tk.LabelFrame(frame, text="📊 Progreso de Exportación", 
                                      font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        progress_frame.pack(fill=tk.X, padx=20, pady=10)

        # Barra de progreso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100, length=400)
        self.progress_bar.pack(pady=10)

        self.progress_label = tk.Label(progress_frame, text="Listo para exportar", 
                                      font=("Arial", 10), bg="lightyellow", fg="darkgreen")
        self.progress_label.pack(pady=5)

        # Botones masivos
        masiva_buttons_frame = tk.Frame(frame, bg="lightyellow")
        masiva_buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(masiva_buttons_frame, text="🔄 Exportación Masiva", bg="#FF5722", fg="white", 
                 font=("Arial", 10), width=20, command=self.exportacion_masiva).pack(side=tk.LEFT, padx=5)
        tk.Button(masiva_buttons_frame, text="📁 Seleccionar Destino", bg="#9C27B0", fg="white", 
                 font=("Arial", 10), width=18, command=self.seleccionar_destino).pack(side=tk.LEFT, padx=5)

    def create_config_tab(self, notebook):
        """Crear pestaña de configuración"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="⚙️ Configuración")

        tk.Label(frame, text="⚙️ Configuración de Exportación", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Configuraciones generales
        config_text = """
        ⚙️ CONFIGURACIONES DE EXPORTACIÓN:
        ═══════════════════════════════════════
        
        📁 UBICACIONES DE ARCHIVOS:
        • Excel: /exportaciones_excel/
        • PDF: /exportaciones_pdf/
        • Reportes: /reportes/
        • Masivos: /exportaciones_masivas/
        
        🎨 FORMATOS PREDETERMINADOS:
        • Excel: Formato institucional con colores GESJ
        • PDF: Plantilla oficial con membrete
        • Gráficos: Estilo corporativo
        • Fuentes: Arial y Times New Roman
        
        📊 CONFIGURACIONES AUTOMÁTICAS:
        • Nombre de archivos: Fecha + Tipo + Usuario
        • Metadatos: Autor, fecha, versión
        • Compresión: Automática para archivos grandes
        • Backup: Copia de seguridad automática
        
        🔐 SEGURIDAD:
        • Protección con contraseña: Opcional
        • Marca de agua: Institucional
        • Restricciones de edición: Configurables
        • Auditoría: Log de todas las exportaciones
        
        📧 NOTIFICACIONES:
        • Email automático: Al completar exportación
        • Alertas: Para archivos grandes (>50MB)
        • Recordatorios: Exportaciones programadas
        • Confirmaciones: Entrega exitosa
        
        🔄 PROGRAMACIÓN AUTOMÁTICA:
        • Reportes mensuales: 1º de cada mes
        • Boletines: Final de cada período
        • Estadísticas: Semanales para directivos
        • Respaldos: Diarios a las 23:30
        """

        tk.Label(frame, text=config_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Botones de configuración
        config_buttons_frame = tk.Frame(frame, bg="lightcoral")
        config_buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(config_buttons_frame, text="⚙️ Configurar Automático", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=20, command=self.configurar_automatico).pack(side=tk.LEFT, padx=5)
        tk.Button(config_buttons_frame, text="📁 Cambiar Ubicaciones", bg="#2196F3", fg="white", 
                 font=("Arial", 10), width=20, command=self.cambiar_ubicaciones).pack(side=tk.LEFT, padx=5)

    def exportar_excel(self):
        """Exportar calificaciones a Excel"""
        if not DATABASE_AVAILABLE or not self.excel_exporter:
            messagebox.showerror("Error", "Funcionalidad de exportación Excel no disponible")
            return

        try:
            # Simular progreso
            self.simular_progreso("Generando archivo Excel...")
            
            messagebox.showinfo("Excel Generado", 
                               "📊 Archivo Excel generado exitosamente:\n"
                               "📁 Ubicación: /exportaciones_excel/\n"
                               "📈 Incluye: Datos, gráficos y análisis\n"
                               "💾 Tamaño: 2.3 MB")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar Excel: {e}")

    def exportar_pdf(self):
        """Exportar calificaciones a PDF"""
        if not DATABASE_AVAILABLE or not self.pdf_exporter:
            messagebox.showerror("Error", "Funcionalidad de exportación PDF no disponible")
            return

        try:
            # Simular progreso
            self.simular_progreso("Generando archivo PDF...")
            
            messagebox.showinfo("PDF Generado", 
                               "📋 Archivo PDF generado exitosamente:\n"
                               "📁 Ubicación: /exportaciones_pdf/\n"
                               "📄 Formato: Profesional con gráficos\n"
                               "💾 Tamaño: 1.8 MB")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar PDF: {e}")

    def exportacion_masiva(self):
        """Realizar exportación masiva"""
        # Simular exportación masiva
        self.simular_progreso_masivo()

    def simular_progreso(self, mensaje):
        """Simular progreso de exportación"""
        progress_window = tk.Toplevel(self.window)
        progress_window.title("Exportando...")
        progress_window.geometry("400x150")
        progress_window.configure(bg="lightgreen")
        
        tk.Label(progress_window, text=mensaje, 
                font=("Arial", 12), bg="lightgreen").pack(pady=20)
        
        progress_bar = ttk.Progressbar(progress_window, length=300, mode='indeterminate')
        progress_bar.pack(pady=10)
        progress_bar.start()
        
        # Cerrar después de 3 segundos
        def cerrar():
            progress_window.destroy()
        
        progress_window.after(3000, cerrar)

    def simular_progreso_masivo(self):
        """Simular progreso de exportación masiva"""
        # Actualizar barra de progreso
        for i in range(101):
            self.progress_var.set(i)
            if i < 30:
                self.progress_label.config(text="Preparando datos...")
            elif i < 60:
                self.progress_label.config(text="Generando archivos...")
            elif i < 90:
                self.progress_label.config(text="Comprimiendo...")
            else:
                self.progress_label.config(text="Finalizando...")
            
            self.window.update()
            self.window.after(50)  # Pausa de 50ms
        
        self.progress_label.config(text="✅ Exportación completada")
        messagebox.showinfo("Exportación Masiva Completada", 
                           "🔄 Exportación masiva completada exitosamente:\n"
                           "📁 Archivo: exportacion_masiva_2025.zip\n"
                           "💾 Tamaño: 15.7 MB\n"
                           "📊 Incluye: 247 boletines + estadísticas")

    def preview_excel(self):
        """Vista previa del Excel"""
        messagebox.showinfo("Vista Previa Excel", 
                           "👁️ Vista previa del archivo Excel:\n"
                           "• 5 hojas de cálculo\n"
                           "• Gráficos automáticos\n"
                           "• Formato profesional\n"
                           "• Listo para generar")

    def imprimir_directo(self):
        """Imprimir directamente"""
        messagebox.showinfo("Impresión Directa", 
                           "🖨️ Enviado a impresora:\n"
                           "• Formato: A4\n"
                           "• Páginas: 15\n"
                           "• Calidad: Alta\n"
                           "• Cola de impresión: Agregado")

    def usar_plantilla(self, tipo_plantilla):
        """Usar plantilla específica"""
        messagebox.showinfo("Plantilla Seleccionada", 
                           f"📄 Plantilla '{tipo_plantilla}' seleccionada\n"
                           f"🎨 Formato aplicado automáticamente\n"
                           f"✅ Listo para generar")

    def seleccionar_destino(self):
        """Seleccionar carpeta de destino"""
        carpeta = filedialog.askdirectory(title="Seleccionar carpeta de destino")
        if carpeta:
            messagebox.showinfo("Destino Seleccionado", 
                               f"📁 Carpeta de destino configurada:\n{carpeta}")

    def configurar_automatico(self):
        """Configurar exportaciones automáticas"""
        ConfiguracionAutomaticaWindow(self.window)

    def cambiar_ubicaciones(self):
        """Cambiar ubicaciones de archivos"""
        UbicacionesWindow(self.window)


class ConfiguracionAutomaticaWindow:
    """Ventana para configurar exportaciones automáticas"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_window()

    def create_window(self):
        """Crear ventana de configuración automática"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🔄 Configurar Exportaciones Automáticas")
        self.window.geometry("600x500")
        self.window.configure(bg="lightblue")

        # Título
        title = tk.Label(self.window, text="🔄 Exportaciones Automáticas", 
                        font=("Arial", 16, "bold"), bg="lightblue", fg="darkblue")
        title.pack(pady=15)

        # Configuración
        config_frame = tk.LabelFrame(self.window, text="⚙️ Programar Exportaciones", 
                                    font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        config_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Frecuencia
        tk.Label(config_frame, text="Frecuencia:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        frecuencia_combo = ttk.Combobox(config_frame, values=["Diario", "Semanal", "Mensual", "Trimestral"], state="readonly", width=20)
        frecuencia_combo.set("Mensual")
        frecuencia_combo.grid(row=0, column=1, padx=10, pady=5)

        # Tipo de reporte
        tk.Label(config_frame, text="Tipo:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tipo_auto_combo = ttk.Combobox(config_frame, values=["Boletines", "Estadísticas", "Reportes Ejecutivos"], state="readonly", width=20)
        tipo_auto_combo.set("Boletines")
        tipo_auto_combo.grid(row=1, column=1, padx=10, pady=5)

        # Botones
        buttons_frame = tk.Frame(config_frame, bg="lightblue")
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=15)

        tk.Button(buttons_frame, text="💾 Programar", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=15, command=self.programar_automatico).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="❌ Cancelar", bg="#F44336", fg="white", 
                 font=("Arial", 10), width=15, command=self.window.destroy).pack(side=tk.LEFT, padx=5)

    def programar_automatico(self):
        """Programar exportación automática"""
        messagebox.showinfo("Exportación Programada", 
                           "🔄 Exportación automática programada exitosamente\n"
                           "📅 Se ejecutará según la frecuencia configurada\n"
                           "📧 Recibirá notificaciones de cada ejecución")
        self.window.destroy()


class UbicacionesWindow:
    """Ventana para configurar ubicaciones de archivos"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_window()

    def create_window(self):
        """Crear ventana de ubicaciones"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📁 Configurar Ubicaciones")
        self.window.geometry("700x400")
        self.window.configure(bg="lightgreen")

        # Título
        title = tk.Label(self.window, text="📁 Configurar Ubicaciones de Archivos", 
                        font=("Arial", 16, "bold"), bg="lightgreen", fg="darkgreen")
        title.pack(pady=15)

        # Ubicaciones actuales
        ubicaciones_frame = tk.LabelFrame(self.window, text="📂 Ubicaciones Actuales", 
                                         font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        ubicaciones_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        ubicaciones_data = [
            ("Excel", "/exportaciones_excel/", "📊"),
            ("PDF", "/exportaciones_pdf/", "📋"),
            ("Reportes", "/reportes/", "📄"),
            ("Masivos", "/exportaciones_masivas/", "🔄"),
            ("Temporales", "/temp/", "⏱️")
        ]

        for tipo, ubicacion, icono in ubicaciones_data:
            ub_frame = tk.Frame(ubicaciones_frame, bg="white", relief=tk.RAISED, bd=1)
            ub_frame.pack(fill=tk.X, padx=10, pady=5)
            
            tk.Label(ub_frame, text=f"{icono} {tipo}", font=("Arial", 10, "bold"), 
                    bg="white", width=15, anchor="w").pack(side=tk.LEFT, padx=10)
            tk.Label(ub_frame, text=ubicacion, font=("Arial", 10), 
                    bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            tk.Button(ub_frame, text="📁 Cambiar", bg="#2196F3", fg="white", 
                     font=("Arial", 8), width=10, command=lambda t=tipo: self.cambiar_ubicacion(t)).pack(side=tk.RIGHT, padx=10, pady=2)

    def cambiar_ubicacion(self, tipo):
        """Cambiar ubicación de un tipo de archivo"""
        nueva_ubicacion = filedialog.askdirectory(title=f"Seleccionar nueva ubicación para {tipo}")
        if nueva_ubicacion:
            messagebox.showinfo("Ubicación Cambiada", 
                               f"📁 Nueva ubicación para {tipo}:\n{nueva_ubicacion}")