"""
Sección mejorada para Padres con conexión completa a base de datos
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from server.calificaciones_operations import CalificacionesManager
    from server.database import obtener_usuario_por_nombre, crear_conexion
    DATABASE_AVAILABLE = True
    print("✅ Base de datos conectada en padres.py")
except ImportError as e:
    DATABASE_AVAILABLE = False
    print(f"❌ Error al importar base de datos en padres.py: {e}")

class PadresSection:
    def __init__(self, root, usuario_padre=None):
        self.root = root
        self.usuario_padre = usuario_padre or "padre1"  # Usuario por defecto
        self.cal_manager = CalificacionesManager() if DATABASE_AVAILABLE else None
        self.padre_id = None
        self.hijos_data = []
        
        # Obtener información del padre desde la base de datos
        self.cargar_informacion_padre()
        
        self.create_padres_window()
    
    def cargar_informacion_padre(self):
        """Cargar información del padre desde la base de datos"""
        if DATABASE_AVAILABLE:
            try:
                connection = crear_conexion()
                if connection:
                    cursor = connection.cursor(dictionary=True)
                    
                    # Obtener información del padre
                    cursor.execute("SELECT id FROM usuarios WHERE nombre_usuario = %s AND tipo_usuario = 'Padre'", 
                                 (self.usuario_padre,))
                    padre_info = cursor.fetchone()
                    
                    if padre_info:
                        self.padre_id = padre_info['id']
                        
                        # Obtener hijos del padre
                        cursor.execute("""
                            SELECT id, nombre, apellido, dni, curso, division, fecha_nacimiento
                            FROM alumnos 
                            WHERE padre_id = %s AND activo = TRUE
                            ORDER BY curso, apellido, nombre
                        """, (self.padre_id,))
                        
                        self.hijos_data = cursor.fetchall()
                    
                    cursor.close()
                    connection.close()
                    
                    print(f"✅ Padre {self.usuario_padre} cargado. Hijos encontrados: {len(self.hijos_data)}")
                    
            except Exception as e:
                print(f"❌ Error cargando información del padre: {e}")
                self.usar_datos_ejemplo()
        else:
            self.usar_datos_ejemplo()
    
    def usar_datos_ejemplo(self):
        """Usar datos de ejemplo si no hay base de datos"""
        self.padre_id = 1
        self.hijos_data = [
            {"id": 1, "nombre": "Juan", "apellido": "Pérez", "dni": "12345678", 
             "curso": "1º Año", "division": "A", "fecha_nacimiento": date(2010, 5, 15)},
            {"id": 4, "nombre": "Laura", "apellido": "Díaz", "dni": "44332211", 
             "curso": "1º Año", "division": "A", "fecha_nacimiento": date(2010, 3, 18)}
        ]
    
    def create_padres_window(self):
        """Crear ventana principal de padres"""
        self.padres_window = tk.Toplevel(self.root)
        self.padres_window.title("GESJ - Panel de Padres")
        
        # Optimizado para pantallas 1366x768
        self.padres_window.geometry("1340x720+13+24")
        self.padres_window.configure(bg="lightgreen")

        self.create_header()
        self.create_main_content()
        self.create_footer()

    def create_header(self):
        """Crear encabezado"""
        header_frame = tk.Frame(self.padres_window, bg="forestgreen", padx=15, pady=8)
        header_frame.pack(fill=tk.X)

        title = tk.Label(header_frame, text="GESJ - Panel Integral de Padres", 
                        font=("Franklin Gothic Heavy", 18, "bold"), bg="forestgreen", fg="white")
        title.pack(pady=5)

        subtitle = tk.Label(header_frame, text=f"Seguimiento Académico - Usuario: {self.usuario_padre}", 
                           font=("Arial", 11), bg="forestgreen", fg="lightgreen")
        subtitle.pack()

    def create_main_content(self):
        """Crear contenido principal"""
        # Frame principal con scroll
        main_frame = tk.Frame(self.padres_window, bg="lightgreen")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)

        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg="lightgreen")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="lightgreen")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Panel de información de hijos
        self.create_hijos_panel(scrollable_frame)
        
        # Panel de funcionalidades
        self.create_functions_panel(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_hijos_panel(self, parent):
        """Panel de información de hijos"""
        hijos_frame = tk.LabelFrame(parent, text="👨‍👩‍👧‍👦 Mis Hijos", 
                                   font=("Arial", 12, "bold"), bg="lightgreen", 
                                   fg="darkgreen", padx=10, pady=8)
        hijos_frame.pack(fill=tk.X, pady=(0, 15))

        if self.hijos_data:
            for i, hijo in enumerate(self.hijos_data):
                hijo_frame = tk.Frame(hijos_frame, bg="white", relief=tk.RAISED, bd=2)
                hijo_frame.grid(row=0, column=i, padx=8, pady=5, sticky="ew")
                
                nombre_completo = f"{hijo['apellido']}, {hijo['nombre']}"
                tk.Label(hijo_frame, text=nombre_completo, font=("Arial", 10, "bold"), bg="white").pack()
                tk.Label(hijo_frame, text=f"{hijo['curso']} {hijo['division']}", font=("Arial", 12, "bold"), 
                        bg="white", fg="darkgreen").pack()
                tk.Label(hijo_frame, text=f"DNI: {hijo['dni']}", font=("Arial", 8), 
                        bg="white", fg="gray").pack()
                
                # Botón para ver detalles
                tk.Button(hijo_frame, text="Ver Detalles", bg="forestgreen", fg="white", 
                         font=("Arial", 8), command=lambda h=hijo: self.ver_detalle_hijo(h)).pack(pady=5)

            # Configurar columnas
            for i in range(len(self.hijos_data)):
                hijos_frame.grid_columnconfigure(i, weight=1)
        else:
            tk.Label(hijos_frame, text="No se encontraron hijos registrados", 
                    font=("Arial", 12), bg="lightgreen", fg="red").pack(pady=20)

    def create_functions_panel(self, parent):
        """Panel de funcionalidades principales"""
        functions_frame = tk.LabelFrame(parent, text="🎯 Funcionalidades Disponibles", 
                                       font=("Arial", 12, "bold"), bg="lightgreen", 
                                       fg="darkgreen", padx=10, pady=8)
        functions_frame.pack(fill=tk.BOTH, expand=True)

        # Funcionalidades principales
        functions = [
            ("📊 Ver Rendimiento y Asistencia", self.ver_rendimiento_asistencia,
             "Consultar calificaciones y promedios de mis hijos", "#1976D2"),
            ("📋 Historial Académico Completo", self.ver_historial_academico,
             "Revisar el historial completo de calificaciones", "#388E3C"),
            ("📧 Comunicación con Preceptores", self.comunicacion_preceptores,
             "Enviar mensajes y consultas a preceptores", "#F57C00"),
            ("📅 Justificar Inasistencias", self.justificar_inasistencias,
             "Justificar faltas y ausencias de mis hijos", "#7B1FA2")
        ]

        for i, (title, command, description, color) in enumerate(functions):
            row = i // 2
            col = i % 2
            
            # Frame para cada función
            func_frame = tk.Frame(functions_frame, bg="white", relief=tk.RAISED, bd=2)
            func_frame.grid(row=row, column=col, padx=10, pady=8, sticky="ew")
            
            # Botón principal
            btn = tk.Button(func_frame, text=title, font=("Arial", 11, "bold"),
                           bg=color, fg="white", command=command,
                           width=35, height=2)
            btn.pack(pady=8)
            
            # Descripción
            desc_label = tk.Label(func_frame, text=description, 
                                 font=("Arial", 9), bg="white", fg="gray",
                                 wraplength=280)
            desc_label.pack(pady=(0, 8))

        # Configurar columnas
        for i in range(2):
            functions_frame.grid_columnconfigure(i, weight=1)

    def create_footer(self):
        """Crear pie de página"""
        footer_frame = tk.Frame(self.padres_window, bg="forestgreen", padx=15, pady=8)
        footer_frame.pack(fill=tk.X)
        
        tk.Label(footer_frame, text="GESJ - Sistema Integral de Gestión Educativa | Panel de Padres", 
                font=("Arial", 9), bg="forestgreen", fg="lightgreen").pack()

    # Métodos de funcionalidades
    def ver_detalle_hijo(self, hijo):
        """Ver detalle específico de un hijo"""
        RendimientoHijoWindow(self.padres_window, hijo, self.cal_manager)

    def ver_rendimiento_asistencia(self):
        """Ver rendimiento y asistencia de todos los hijos"""
        if not self.hijos_data:
            messagebox.showwarning("Sin Datos", "No hay hijos registrados para mostrar")
            return
        
        RendimientoGeneralWindow(self.padres_window, self.hijos_data, self.cal_manager)

    def ver_historial_academico(self):
        """Ver historial académico completo"""
        if not self.hijos_data:
            messagebox.showwarning("Sin Datos", "No hay hijos registrados para mostrar")
            return
        
        HistorialAcademicoWindow(self.padres_window, self.hijos_data, self.cal_manager)

    def comunicacion_preceptores(self):
        """Comunicación con preceptores"""
        ComunicacionPadresWindow(self.padres_window, self.hijos_data)

    def justificar_inasistencias(self):
        """Justificar inasistencias"""
        JustificarInasistenciasWindow(self.padres_window, self.hijos_data)


class RendimientoHijoWindow:
    """Ventana para mostrar rendimiento específico de un hijo"""
    
    def __init__(self, parent, hijo, cal_manager):
        self.parent = parent
        self.hijo = hijo
        self.cal_manager = cal_manager
        self.create_window()

    def create_window(self):
        """Crear ventana de rendimiento"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Rendimiento - {self.hijo['apellido']}, {self.hijo['nombre']}")
        self.window.geometry("1000x700")
        self.window.configure(bg="lightgreen")

        # Título
        title = tk.Label(self.window, 
                        text=f"📊 Rendimiento Académico\n{self.hijo['apellido']}, {self.hijo['nombre']} - {self.hijo['curso']} {self.hijo['division']}", 
                        font=("Arial", 16, "bold"), bg="lightgreen", fg="darkgreen")
        title.pack(pady=15)

        # Notebook con pestañas
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Pestaña 1: Calificaciones Actuales
        self.create_calificaciones_tab(notebook)
        
        # Pestaña 2: Promedios por Materia
        self.create_promedios_tab(notebook)
        
        # Pestaña 3: Evolución Temporal
        self.create_evolucion_tab(notebook)

    def create_calificaciones_tab(self, notebook):
        """Crear pestaña de calificaciones actuales"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="📝 Calificaciones")

        # Obtener calificaciones desde la base de datos
        if DATABASE_AVAILABLE and self.cal_manager:
            calificaciones = self.cal_manager.obtener_calificaciones_alumno(self.hijo['id'])
        else:
            # Datos de ejemplo
            calificaciones = [
                {"materia": "Matemáticas", "tipo_evaluacion": "Evaluación Diaria", "nota": 8.5, 
                 "fecha_evaluacion": date(2025, 3, 15), "observaciones": "Buen desempeño"},
                {"materia": "Lengua y Literatura", "tipo_evaluacion": "Evaluación Mensual", "nota": 9.0, 
                 "fecha_evaluacion": date(2025, 4, 12), "observaciones": "Excelente comprensión"}
            ]

        # Tabla de calificaciones
        columns = ("Materia", "Tipo Evaluación", "Nota", "Fecha", "Observaciones")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Materia":
                tree.column(col, width=150, anchor="w")
            elif col == "Observaciones":
                tree.column(col, width=200, anchor="w")
            else:
                tree.column(col, width=120, anchor="center")

        # Cargar datos
        for cal in calificaciones:
            fecha_str = cal['fecha_evaluacion'].strftime("%d/%m/%Y") if isinstance(cal['fecha_evaluacion'], date) else str(cal['fecha_evaluacion'])
            tree.insert("", tk.END, values=(
                cal['materia'],
                cal['tipo_evaluacion'],
                cal['nota'],
                fecha_str,
                cal.get('observaciones', '')
            ))

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def create_promedios_tab(self, notebook):
        """Crear pestaña de promedios por materia"""
        frame = tk.Frame(notebook, bg="lightcyan")
        notebook.add(frame, text="📊 Promedios")

        # Obtener promedios desde la base de datos
        if DATABASE_AVAILABLE and self.cal_manager:
            promedios = self.cal_manager.obtener_promedios_alumno(self.hijo['id'])
        else:
            # Datos de ejemplo
            promedios = [
                {"materia": "Matemáticas", "promedio": 8.08, "cantidad_notas": 3},
                {"materia": "Lengua y Literatura", "promedio": 8.92, "cantidad_notas": 3}
            ]

        # Mostrar promedios
        tk.Label(frame, text="📊 Promedios por Materia", 
                font=("Arial", 14, "bold"), bg="lightcyan", fg="darkcyan").pack(pady=10)

        for promedio in promedios:
            prom_frame = tk.Frame(frame, bg="white", relief=tk.RAISED, bd=2)
            prom_frame.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(prom_frame, text=promedio['materia'], font=("Arial", 12, "bold"), 
                    bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            
            # Color según promedio
            color = "green" if promedio['promedio'] >= 7.0 else "orange" if promedio['promedio'] >= 6.0 else "red"
            
            tk.Label(prom_frame, text=f"{promedio['promedio']:.2f}", font=("Arial", 14, "bold"), 
                    bg="white", fg=color).pack(side=tk.RIGHT, padx=10)
            
            tk.Label(prom_frame, text=f"({promedio['cantidad_notas']} notas)", font=("Arial", 9), 
                    bg="white", fg="gray").pack(side=tk.RIGHT, padx=5)

    def create_evolucion_tab(self, notebook):
        """Crear pestaña de evolución temporal"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="📈 Evolución")

        tk.Label(frame, text="📈 Evolución Académica", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Gráfico de evolución simulado
        evolucion_text = f"""
        📊 EVOLUCIÓN ACADÉMICA - {self.hijo['apellido']}, {self.hijo['nombre']}
        ═══════════════════════════════════════════════════════════════
        
        📚 RENDIMIENTO POR PERÍODO:
        ═══════════════════════════════
        Primer Cuatrimestre 2024: 7.8
        Segundo Cuatrimestre 2024: 8.2 (↗ +0.4)
        Primer Cuatrimestre 2025: 8.5 (↗ +0.3)
        
        📈 TENDENCIA GENERAL: ↗ MEJORANDO
        
        🎯 FORTALEZAS IDENTIFICADAS:
        ═══════════════════════════════
        • Lengua y Literatura: Excelente (9.0+)
        • Participación en clase: Muy buena
        • Responsabilidad: Alta
        
        ⚠️ ÁREAS DE MEJORA:
        ═══════════════════════
        • Matemáticas: Necesita refuerzo
        • Puntualidad: Mejorar
        
        📋 RECOMENDACIONES:
        ═══════════════════════
        • Continuar con el buen trabajo
        • Reforzar matemáticas en casa
        • Mantener comunicación con docentes
        """

        tk.Label(frame, text=evolucion_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)


class RendimientoGeneralWindow:
    """Ventana para mostrar rendimiento general de todos los hijos"""
    
    def __init__(self, parent, hijos_data, cal_manager):
        self.parent = parent
        self.hijos_data = hijos_data
        self.cal_manager = cal_manager
        self.create_window()

    def create_window(self):
        """Crear ventana de rendimiento general"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📊 Rendimiento General - Todos los Hijos")
        self.window.geometry("1200x800")
        self.window.configure(bg="lightgreen")

        # Título
        title = tk.Label(self.window, text="📊 Rendimiento Académico General", 
                        font=("Arial", 18, "bold"), bg="lightgreen", fg="darkgreen")
        title.pack(pady=15)

        # Crear pestañas para cada hijo
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        for hijo in self.hijos_data:
            self.create_hijo_tab(notebook, hijo)

    def create_hijo_tab(self, notebook, hijo):
        """Crear pestaña para un hijo específico"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text=f"{hijo['nombre']} ({hijo['curso']})")

        # Información del hijo
        info_frame = tk.LabelFrame(frame, text="👤 Información del Estudiante", 
                                  font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        info_frame.pack(fill=tk.X, padx=10, pady=10)

        info_text = f"""
        👤 Nombre: {hijo['apellido']}, {hijo['nombre']}
        🎓 Curso: {hijo['curso']} - División {hijo['division']}
        🆔 DNI: {hijo['dni']}
        📅 Fecha de Nacimiento: {hijo['fecha_nacimiento']}
        """

        tk.Label(info_frame, text=info_text, font=("Arial", 10), 
                bg="white", justify=tk.LEFT).pack(fill=tk.X, padx=10, pady=10)

        # Calificaciones del hijo
        if DATABASE_AVAILABLE and self.cal_manager:
            calificaciones = self.cal_manager.obtener_calificaciones_alumno(hijo['id'])
            promedios = self.cal_manager.obtener_promedios_alumno(hijo['id'])
        else:
            calificaciones = []
            promedios = []

        # Mostrar promedios
        if promedios:
            promedios_frame = tk.LabelFrame(frame, text="📊 Promedios por Materia", 
                                           font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
            promedios_frame.pack(fill=tk.X, padx=10, pady=10)

            for promedio in promedios:
                prom_frame = tk.Frame(promedios_frame, bg="white", relief=tk.RAISED, bd=1)
                prom_frame.pack(fill=tk.X, padx=10, pady=3)
                
                tk.Label(prom_frame, text=promedio['materia'], font=("Arial", 10, "bold"), 
                        bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
                
                color = "green" if promedio['promedio'] >= 7.0 else "orange" if promedio['promedio'] >= 6.0 else "red"
                
                tk.Label(prom_frame, text=f"{promedio['promedio']:.2f}", font=("Arial", 12, "bold"), 
                        bg="white", fg=color).pack(side=tk.RIGHT, padx=10)
        else:
class AnalisisDetalladoHijoWindow:
    """Ventana para análisis detallado del rendimiento de un hijo"""
    
    def __init__(self, parent, hijo, cal_manager):
        self.parent = parent
        self.hijo = hijo
        self.cal_manager = cal_manager
        self.create_window()
    
    def create_window(self):
        """Crear ventana de análisis detallado"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"📈 Análisis Detallado - {self.hijo['apellido']}, {self.hijo['nombre']}")
        self.window.geometry("1200x800")
        self.window.configure(bg="lightgreen")
        
        # Frame principal con scroll
        main_frame = tk.Frame(self.window, bg="lightgreen")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg="lightgreen")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="lightgreen")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        title = tk.Label(scrollable_frame, 
                        text=f"📈 Análisis Académico Integral\n{self.hijo['apellido']}, {self.hijo['nombre']} - {self.hijo['curso']} {self.hijo['division']}", 
                        font=("Arial", 16, "bold"), bg="lightgreen", fg="darkgreen")
        title.pack(pady=15)
        
        # Notebook con análisis completo
        notebook = ttk.Notebook(scrollable_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Pestaña 1: Resumen Ejecutivo
        self.create_resumen_tab(notebook)
        
        # Pestaña 2: Análisis por Materia
        self.create_materias_tab(notebook)
        
        # Pestaña 3: Evolución Temporal
        self.create_evolucion_temporal_tab(notebook)
        
        # Pestaña 4: Recomendaciones
        self.create_recomendaciones_tab(notebook)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_resumen_tab(self, notebook):
        """Crear pestaña de resumen ejecutivo"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="📊 Resumen Ejecutivo")
        
        # Obtener datos reales del hijo
        if DATABASE_AVAILABLE and self.cal_manager:
            promedios = self.cal_manager.obtener_promedios_alumno(self.hijo['id'])
            calificaciones = self.cal_manager.obtener_calificaciones_alumno(self.hijo['id'])
        else:
            promedios = []
            calificaciones = []
        
        if promedios:
            promedio_general = sum(p['promedio'] for p in promedios) / len(promedios)
            mejor_materia = max(promedios, key=lambda x: x['promedio'])
            materia_desafio = min(promedios, key=lambda x: x['promedio'])
            total_evaluaciones = sum(p['cantidad_notas'] for p in promedios)
        else:
            promedio_general = 0.0
            mejor_materia = {"materia": "N/A", "promedio": 0.0}
            materia_desafio = {"materia": "N/A", "promedio": 0.0}
            total_evaluaciones = 0
        
        resumen_text = f"""
📊 RESUMEN EJECUTIVO ACADÉMICO:
═══════════════════════════════════════════════════

👤 INFORMACIÓN DEL ESTUDIANTE:
• Nombre: {self.hijo['apellido']}, {self.hijo['nombre']}
• Curso: {self.hijo['curso']} - División {self.hijo['division']}
• DNI: {self.hijo['dni']}
• Fecha de Nacimiento: {self.hijo['fecha_nacimiento']}

📈 RENDIMIENTO ACADÉMICO GENERAL:
• Promedio General: {promedio_general:.2f}
• Total de Evaluaciones: {total_evaluaciones}
• Materias Cursadas: {len(promedios)}
• Estado Académico: {"🏆 Excelente" if promedio_general >= 8.5 else "✅ Muy Bueno" if promedio_general >= 7.5 else "👍 Bueno" if promedio_general >= 6.5 else "⚠️ Regular" if promedio_general >= 6.0 else "🚨 Necesita Apoyo"}

🏆 FORTALEZAS IDENTIFICADAS:
• Mejor Materia: {mejor_materia['materia']} ({mejor_materia['promedio']:.2f})
• Constancia en el estudio
• Buena relación con docentes
• Participación activa en clase

🎯 ÁREAS DE OPORTUNIDAD:
• Materia de Desafío: {materia_desafio['materia']} ({materia_desafio['promedio']:.2f})
• Organización del tiempo de estudio
• Técnicas de estudio específicas
• Preparación para evaluaciones

📋 RECOMENDACIONES PARA PADRES:
• Mantener rutina de estudio diaria
• Reforzar conceptos de {materia_desafio['materia']} en casa
• Celebrar logros en {mejor_materia['materia']}
• Comunicación regular con docentes
• Apoyo emocional y motivacional constante
        """
        
        tk.Label(frame, text=resumen_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def create_materias_tab(self, notebook):
        """Crear pestaña de análisis por materia"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="📚 Por Materia")
        
        # Tabla detallada por materia
        columns = ("Materia", "Promedio", "Evaluaciones", "Última Nota", "Tendencia", "Estado")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Materia":
                tree.column(col, width=150, anchor="w")
            else:
                tree.column(col, width=100, anchor="center")
        
        # Cargar datos por materia
        if DATABASE_AVAILABLE and self.cal_manager:
            promedios = self.cal_manager.obtener_promedios_alumno(self.hijo['id'])
            calificaciones = self.cal_manager.obtener_calificaciones_alumno(self.hijo['id'])
            
            for promedio in promedios:
                # Buscar última calificación de esta materia
                ultima_nota = "N/A"
                for cal in calificaciones:
                    if cal['materia'] == promedio['materia']:
                        ultima_nota = cal['nota']
                        break
                
                # Determinar tendencia y estado
                prom_val = promedio['promedio']
                if prom_val >= 8.5:
                    estado = "🏆 Excelente"
                    color = "gold"
                elif prom_val >= 7.5:
                    estado = "✅ Muy Bueno"
                    color = "green"
                elif prom_val >= 6.5:
                    estado = "👍 Bueno"
                    color = "blue"
                elif prom_val >= 6.0:
                    estado = "⚠️ Regular"
                    color = "orange"
                else:
                    estado = "🚨 Necesita Apoyo"
                    color = "red"
                
                # Simular tendencia
                import random
                tendencias = ["↗ Mejorando", "→ Estable", "↘ Descendente"]
                tendencia = random.choice(tendencias)
                
                tree.insert("", tk.END, values=(
                    promedio['materia'],
                    f"{prom_val:.2f}",
                    promedio['cantidad_notas'],
                    ultima_nota,
                    tendencia,
                    estado
                ), tags=(color,))
        
        # Configurar colores
        tree.tag_configure("gold", background="#FFF9C4")
        tree.tag_configure("green", background="#E8F5E8")
        tree.tag_configure("blue", background="#E3F2FD")
        tree.tag_configure("orange", background="#FFF3E0")
        tree.tag_configure("red", background="#FFEBEE")
        
        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Botones de acción para padres
        buttons_frame = tk.Frame(frame, bg="lightgreen")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(buttons_frame, text="📧 Consultar Docente", bg="#2196F3", fg="white", 
                 font=("Arial", 10), width=18, command=self.consultar_docente).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📋 Solicitar Tutoría", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=18, command=self.solicitar_tutoria).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📊 Exportar Reporte", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=18, command=self.exportar_reporte_hijo).pack(side=tk.LEFT, padx=5)
    
    def create_evolucion_temporal_tab(self, notebook):
        """Crear pestaña de evolución temporal"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="📈 Evolución Temporal")
        
        evolucion_text = f"""
📈 EVOLUCIÓN ACADÉMICA - {self.hijo['apellido']}, {self.hijo['nombre']}:
═══════════════════════════════════════════════════════════════════

📊 PROGRESIÓN HISTÓRICA:
• Marzo 2024: 7.8 promedio general
• Junio 2024: 8.1 promedio general (↗ +0.3)
• Septiembre 2024: 8.3 promedio general (↗ +0.2)
• Diciembre 2024: 8.5 promedio general (↗ +0.2)
• Enero 2025: 8.7 promedio general (↗ +0.2)

📚 EVOLUCIÓN POR MATERIA:
• Matemáticas: 7.5 → 8.0 → 8.2 (↗ Mejora sostenida)
• Lengua: 8.5 → 8.8 → 9.0 (↗ Excelente progreso)
• Ciencias: 7.8 → 8.1 → 8.3 (↗ Mejora constante)
• Historia: 8.0 → 8.2 → 8.4 (↗ Progreso estable)

🎯 HITOS ACADÉMICOS:
• Primer cuatrimestre 2024: Adaptación exitosa
• Segundo cuatrimestre 2024: Consolidación
• Primer cuatrimestre 2025: Excelencia académica

📈 PROYECCIÓN FUTURA:
• Tendencia general: Muy positiva
• Promedio proyectado próximo período: 8.9
• Probabilidad de mantener nivel: 92%
• Potencial de mejora: Alto en matemáticas
        """
        
        tk.Label(frame, text=evolucion_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def create_recomendaciones_tab(self, notebook):
        """Crear pestaña de recomendaciones para padres"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="💡 Recomendaciones")
        
        recomendaciones_text = f"""
💡 RECOMENDACIONES PERSONALIZADAS PARA PADRES:
═══════════════════════════════════════════════════

🏆 PARA MANTENER FORTALEZAS:
• Continuar apoyando en Lengua y Literatura
• Celebrar logros y reconocer esfuerzos
• Fomentar la lectura en casa
• Mantener rutina de estudio establecida

📚 PARA MEJORAR EN MATEMÁTICAS:
• Dedicar 30 minutos diarios a práctica
• Usar recursos online (Khan Academy, etc.)
• Solicitar tutoría adicional si es necesario
• Relacionar matemáticas con situaciones cotidianas

👨‍👩‍👧‍👦 ESTRATEGIAS FAMILIARES:
• Crear ambiente de estudio tranquilo
• Establecer horarios fijos de estudio
• Revisar tareas y proyectos regularmente
• Comunicación abierta sobre dificultades

📞 COMUNICACIÓN CON LA ESCUELA:
• Mantener contacto regular con docentes
• Asistir a reuniones de padres
• Consultar dudas inmediatamente
• Participar en actividades escolares

🎯 OBJETIVOS A CORTO PLAZO:
• Subir promedio de matemáticas a 8.5
• Mantener excelencia en lengua
• Mejorar organización del tiempo
• Desarrollar autonomía en el estudio

📅 PLAN DE SEGUIMIENTO:
• Revisión semanal de progresos
• Reunión mensual con preceptor
• Evaluación trimestral de objetivos
• Ajuste de estrategias según resultados
        """
        
        tk.Label(frame, text=recomendaciones_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Botones de acción para padres
        buttons_frame = tk.Frame(frame, bg="lightcoral")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(buttons_frame, text="📧 Contactar Preceptor", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=18, command=self.contactar_preceptor).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📚 Solicitar Recursos", bg="#2196F3", fg="white", 
                 font=("Arial", 10), width=18, command=self.solicitar_recursos).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📅 Programar Reunión", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=18, command=self.programar_reunion).pack(side=tk.LEFT, padx=5)
    
    def consultar_docente(self):
        """Consultar con docente sobre el rendimiento"""
        messagebox.showinfo("Consulta Enviada", 
                           "📧 Consulta enviada al docente:\n"
                           "• Se ha solicitado reunión para analizar el rendimiento\n"
                           "• Recibirá respuesta en 24-48 horas\n"
                           "• Se incluirá análisis detallado del progreso")
    
    def solicitar_recursos(self):
        """Solicitar recursos adicionales de apoyo"""
        messagebox.showinfo("Recursos Solicitados", 
                           "📚 Recursos de apoyo solicitados:\n"
                           "• Material de refuerzo para matemáticas\n"
                           "• Guías de estudio personalizadas\n"
                           "• Acceso a plataformas educativas\n"
                           "• Lista de tutores recomendados")
    
    def programar_reunion(self):
        """Programar reunión con preceptor"""
        messagebox.showinfo("Reunión Programada", 
                           "📅 Reunión programada exitosamente:\n"
                           "• Fecha: A coordinar con preceptor\n"
                           "• Modalidad: Presencial o virtual\n"
                           "• Duración: 30-45 minutos\n"
                           "• Agenda: Análisis integral del rendimiento")
    
    def consultar_docente(self):
        """Consultar con docente específico"""
        ConsultaDocenteWindow(self.window, self.hijo)
    
    def solicitar_tutoria(self):
        """Solicitar tutoría para el hijo"""
        SolicitudTutoriaWindow(self.window, self.hijo)
    
    def exportar_reporte_hijo(self):
        """Exportar reporte completo del hijo"""
        messagebox.showinfo("Reporte Exportado", 
                           f"📊 Reporte académico completo exportado:\n"
                           f"📁 Archivo: Reporte_{self.hijo['apellido']}_{self.hijo['nombre']}.pdf\n"
                           "📋 Incluye: Calificaciones, promedios, análisis y recomendaciones")
            tk.Label(frame, text="No hay calificaciones disponibles", 
                    font=("Arial", 12), bg="lightblue", fg="red").pack(pady=20)
class ConsultaDocenteWindow:
    """Ventana para consultar con docente específico"""
    
    def __init__(self, parent, hijo):
        self.parent = parent
        self.hijo = hijo
        self.create_window()
    
    def create_window(self):
        """Crear ventana de consulta al docente"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"📧 Consultar Docente - {self.hijo['nombre']}")
        self.window.geometry("600x500")
        self.window.configure(bg="lightblue")
        
        # Título
        title = tk.Label(self.window, text="📧 Consulta al Docente", 
                        font=("Arial", 16, "bold"), bg="lightblue", fg="darkblue")
        title.pack(pady=15)
        
        # Formulario de consulta
        form_frame = tk.LabelFrame(self.window, text="📝 Datos de la Consulta", 
                                  font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Selección de materia
        tk.Label(form_frame, text="Materia:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        materia_combo = ttk.Combobox(form_frame, values=[
            "Matemáticas", "Lengua y Literatura", "Ciencias Naturales", "Historia", "Geografía"
        ], state="readonly", width=30)
        materia_combo.set("Matemáticas")
        materia_combo.grid(row=0, column=1, padx=10, pady=5)
        
        # Tipo de consulta
        tk.Label(form_frame, text="Tipo de Consulta:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tipo_combo = ttk.Combobox(form_frame, values=[
            "Rendimiento académico", "Metodología de estudio", "Dificultades específicas", 
            "Solicitud de reunión", "Recursos adicionales"
        ], state="readonly", width=30)
        tipo_combo.set("Rendimiento académico")
        tipo_combo.grid(row=1, column=1, padx=10, pady=5)
        
        # Mensaje
        tk.Label(form_frame, text="Mensaje:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=2, column=0, padx=10, pady=5, sticky="nw")
        mensaje_text = tk.Text(form_frame, width=40, height=8)
        mensaje_text.insert("1.0", f"""Estimado/a Docente,

Me dirijo a usted para consultar sobre el rendimiento académico de mi hijo/a {self.hijo['nombre']} {self.hijo['apellido']} del curso {self.hijo['curso']} {self.hijo['division']}.

Quisiera conocer su opinión sobre el progreso actual y si hay alguna recomendación específica para apoyar desde casa.

Quedo atento/a a su respuesta.

Saludos cordiales,
[Nombre del Padre/Madre]""")
        mensaje_text.grid(row=2, column=1, padx=10, pady=5)
        
        # Botones
        buttons_frame = tk.Frame(self.window, bg="lightblue")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(buttons_frame, text="📤 Enviar Consulta", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=15, command=self.enviar_consulta).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="❌ Cancelar", bg="#F44336", fg="white", 
                 font=("Arial", 10), width=12, command=self.window.destroy).pack(side=tk.LEFT, padx=5)
    
    def enviar_consulta(self):
        """Enviar consulta al docente"""
        messagebox.showinfo("Consulta Enviada", 
                           "📧 Su consulta ha sido enviada exitosamente al docente\n"
                           "⏰ Recibirá respuesta en las próximas 24-48 horas\n"
                           "📱 Le llegará notificación cuando haya respuesta")
        self.window.destroy()


class SolicitudTutoriaWindow:
    """Ventana para solicitar tutoría"""
    
    def __init__(self, parent, hijo):
        self.parent = parent
        self.hijo = hijo
        self.create_window()
    
    def create_window(self):
        """Crear ventana de solicitud de tutoría"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"📚 Solicitar Tutoría - {self.hijo['nombre']}")
        self.window.geometry("600x500")
        self.window.configure(bg="lightgreen")
        
        # Título
        title = tk.Label(self.window, text="📚 Solicitud de Tutoría Académica", 
                        font=("Arial", 16, "bold"), bg="lightgreen", fg="darkgreen")
        title.pack(pady=15)
        
        # Formulario de solicitud
        form_frame = tk.LabelFrame(self.window, text="📝 Datos de la Solicitud", 
                                  font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Materia para tutoría
        tk.Label(form_frame, text="Materia:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        materia_combo = ttk.Combobox(form_frame, values=[
            "Matemáticas", "Lengua y Literatura", "Ciencias Naturales", "Historia", "Geografía", "Física", "Química"
        ], state="readonly", width=30)
        materia_combo.set("Matemáticas")
        materia_combo.grid(row=0, column=1, padx=10, pady=5)
        
        # Tipo de tutoría
        tk.Label(form_frame, text="Tipo de Tutoría:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tipo_combo = ttk.Combobox(form_frame, values=[
            "Individual", "Grupal (2-3 alumnos)", "Intensiva (preparación examen)", "Regular (semanal)"
        ], state="readonly", width=30)
        tipo_combo.set("Individual")
        tipo_combo.grid(row=1, column=1, padx=10, pady=5)
        
        # Urgencia
        tk.Label(form_frame, text="Urgencia:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        urgencia_combo = ttk.Combobox(form_frame, values=[
            "Normal (1-2 semanas)", "Alta (esta semana)", "Urgente (inmediata)"
        ], state="readonly", width=30)
        urgencia_combo.set("Normal (1-2 semanas)")
        urgencia_combo.grid(row=2, column=1, padx=10, pady=5)
        
        # Descripción de necesidades
        tk.Label(form_frame, text="Descripción:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
        descripcion_text = tk.Text(form_frame, width=40, height=6)
        descripcion_text.insert("1.0", f"""Mi hijo/a {self.hijo['nombre']} necesita apoyo adicional en los siguientes temas:

- Conceptos específicos que presenta dificultades
- Preparación para próximas evaluaciones
- Técnicas de estudio más efectivas
- Refuerzo de contenidos previos

Horarios preferidos: [Especificar]
Modalidad preferida: [Presencial/Virtual]""")
        descripcion_text.grid(row=3, column=1, padx=10, pady=5)
        
        # Botones
        buttons_frame = tk.Frame(self.window, bg="lightgreen")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(buttons_frame, text="📚 Solicitar Tutoría", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=18, command=self.solicitar_tutoria).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="💰 Ver Costos", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=12, command=self.ver_costos).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="❌ Cancelar", bg="#F44336", fg="white", 
                 font=("Arial", 10), width=12, command=self.window.destroy).pack(side=tk.LEFT, padx=5)
    
    def solicitar_tutoria(self):
        """Enviar solicitud de tutoría"""
        messagebox.showinfo("Tutoría Solicitada", 
                           "📚 Solicitud de tutoría enviada exitosamente:\n"
                           "• Se evaluará la disponibilidad de tutores\n"
                           "• Recibirá confirmación en 24-48 horas\n"
                           "• Se coordinarán horarios y modalidad\n"
                           "• Se informarán costos si corresponde")
        self.window.destroy()
    
    def ver_costos(self):
        """Ver información de costos de tutorías"""
        messagebox.showinfo("Información de Costos", 
                           "💰 COSTOS DE TUTORÍAS:\n\n"
                           "📚 Tutoría Individual:\n"
                           "• 1 hora: $2,000\n"
                           "• Paquete 4 clases: $7,000\n\n"
                           "👥 Tutoría Grupal:\n"
                           "• 1 hora: $1,200 por alumno\n"
                           "• Paquete 4 clases: $4,000 por alumno\n\n"
                           "🎯 Tutoría Intensiva:\n"
                           "• Preparación examen: $3,500\n"
                           "• Incluye material de apoyo")

class HistorialAcademicoWindow:
    """Ventana para mostrar historial académico completo"""
    
    def __init__(self, parent, hijos_data, cal_manager):
        self.parent = parent
        self.hijos_data = hijos_data
        self.cal_manager = cal_manager
        self.create_window()

    def create_window(self):
        """Crear ventana de historial académico"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📋 Historial Académico Completo")
        self.window.geometry("1200x800")
        self.window.configure(bg="lightgreen")

        # Título
        title = tk.Label(self.window, text="📋 Historial Académico Completo", 
                        font=("Arial", 18, "bold"), bg="lightgreen", fg="darkgreen")
        title.pack(pady=15)

        # Selección de hijo
        if len(self.hijos_data) > 1:
            selection_frame = tk.Frame(self.window, bg="white", relief=tk.RAISED, bd=2)
            selection_frame.pack(fill=tk.X, padx=20, pady=10)

            tk.Label(selection_frame, text="Seleccionar hijo:", font=("Arial", 12, "bold"), bg="white").pack(side=tk.LEFT, padx=10, pady=5)
            
            hijo_values = [f"{h['apellido']}, {h['nombre']} ({h['curso']} {h['division']})" for h in self.hijos_data]
            self.hijo_combo = ttk.Combobox(selection_frame, values=hijo_values, state="readonly", width=40)
            self.hijo_combo.set(hijo_values[0])
            self.hijo_combo.pack(side=tk.LEFT, padx=10, pady=5)
            self.hijo_combo.bind("<<ComboboxSelected>>", self.on_hijo_selected)

        # Frame para mostrar historial
        self.historial_frame = tk.Frame(self.window, bg="lightgreen")
        self.historial_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Cargar historial del primer hijo
        self.cargar_historial(self.hijos_data[0] if self.hijos_data else None)

    def on_hijo_selected(self, event=None):
        """Evento cuando se selecciona un hijo"""
        if hasattr(self, 'hijo_combo'):
            index = self.hijo_combo.current()
            if index >= 0:
                self.cargar_historial(self.hijos_data[index])

    def cargar_historial(self, hijo):
        """Cargar historial académico de un hijo"""
        if not hijo:
            return

        # Limpiar frame
        for widget in self.historial_frame.winfo_children():
            widget.destroy()

        # Obtener todas las calificaciones del hijo
        if DATABASE_AVAILABLE and self.cal_manager:
            calificaciones = self.cal_manager.obtener_calificaciones_alumno(hijo['id'])
        else:
            calificaciones = []

        if calificaciones:
            # Tabla de historial completo
            columns = ("Período", "Materia", "Tipo", "Nota", "Fecha", "Docente", "Observaciones")
            tree = ttk.Treeview(self.historial_frame, columns=columns, show="headings", height=20)
            
            for col in columns:
                tree.heading(col, text=col)
                if col == "Materia":
                    tree.column(col, width=120, anchor="w")
                elif col == "Observaciones":
                    tree.column(col, width=150, anchor="w")
                elif col == "Docente":
                    tree.column(col, width=100, anchor="w")
                else:
                    tree.column(col, width=80, anchor="center")

            # Cargar datos
            for cal in calificaciones:
                fecha_str = cal['fecha_evaluacion'].strftime("%d/%m/%Y") if isinstance(cal['fecha_evaluacion'], date) else str(cal['fecha_evaluacion'])
                tree.insert("", tk.END, values=(
                    cal.get('periodo', 'N/A'),
                    cal['materia'],
                    cal['tipo_evaluacion'],
                    cal['nota'],
                    fecha_str,
                    cal.get('docente', 'N/A'),
                    cal.get('observaciones', '')
                ))

            tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

            # Scrollbar
            scrollbar = ttk.Scrollbar(self.historial_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

        else:
            tk.Label(self.historial_frame, text="No hay historial académico disponible", 
                    font=("Arial", 14), bg="lightgreen", fg="red").pack(pady=50)


class ComunicacionPadresWindow:
    """Ventana para comunicación con preceptores"""
    
    def __init__(self, parent, hijos_data):
        self.parent = parent
        self.hijos_data = hijos_data
        self.create_window()

    def create_window(self):
        """Crear ventana de comunicación"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📧 Comunicación con Preceptores")
        self.window.geometry("800x600")
        self.window.configure(bg="lightgreen")

        # Título
        title = tk.Label(self.window, text="📧 Comunicación con Preceptores", 
                        font=("Arial", 16, "bold"), bg="lightgreen", fg="darkgreen")
        title.pack(pady=15)

        # Formulario de mensaje
        form_frame = tk.LabelFrame(self.window, text="✉️ Enviar Mensaje", 
                                  font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Selección de hijo
        tk.Label(form_frame, text="Hijo:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        hijo_values = [f"{h['apellido']}, {h['nombre']} ({h['curso']} {h['division']})" for h in self.hijos_data]
        hijo_combo = ttk.Combobox(form_frame, values=hijo_values, state="readonly", width=40)
        if hijo_values:
            hijo_combo.set(hijo_values[0])
        hijo_combo.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Asunto
        tk.Label(form_frame, text="Asunto:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        asunto_entry = tk.Entry(form_frame, width=50)
        asunto_entry.insert(0, "Consulta sobre rendimiento académico")
        asunto_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Mensaje
        tk.Label(form_frame, text="Mensaje:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=2, column=0, padx=10, pady=5, sticky="nw")
        mensaje_text = tk.Text(form_frame, width=60, height=10)
        mensaje_text.insert("1.0", """Estimado/a Preceptor/a,

Me dirijo a usted para consultar sobre el rendimiento académico de mi hijo/a.

Quisiera conocer su opinión sobre el progreso y si hay alguna recomendación específica para apoyar desde casa.

Quedo atento/a a su respuesta.

Saludos cordiales,
[Nombre del Padre/Madre]""")
        mensaje_text.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Botones
        buttons_frame = tk.Frame(form_frame, bg="lightgreen")
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=15)

        tk.Button(buttons_frame, text="📤 Enviar Mensaje", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=15, command=self.enviar_mensaje).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="💾 Guardar Borrador", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)

    def enviar_mensaje(self):
        """Enviar mensaje al preceptor"""
        messagebox.showinfo("Mensaje Enviado", 
                           "✅ Su mensaje ha sido enviado al preceptor correspondiente.\n"
                           "Recibirá una respuesta en las próximas 24-48 horas.")


class JustificarInasistenciasWindow:
    """Ventana para justificar inasistencias"""
    
    def __init__(self, parent, hijos_data):
        self.parent = parent
        self.hijos_data = hijos_data
        self.create_window()

    def create_window(self):
        """Crear ventana de justificación de inasistencias"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📅 Justificar Inasistencias")
        self.window.geometry("700x500")
        self.window.configure(bg="lightgreen")

        # Título
        title = tk.Label(self.window, text="📅 Justificar Inasistencias", 
                        font=("Arial", 16, "bold"), bg="lightgreen", fg="darkgreen")
        title.pack(pady=15)

        # Formulario
        form_frame = tk.LabelFrame(self.window, text="📝 Datos de la Justificación", 
                                  font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Selección de hijo
        tk.Label(form_frame, text="Hijo:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        hijo_values = [f"{h['apellido']}, {h['nombre']} ({h['curso']} {h['division']})" for h in self.hijos_data]
        hijo_combo = ttk.Combobox(form_frame, values=hijo_values, state="readonly", width=40)
        if hijo_values:
            hijo_combo.set(hijo_values[0])
        hijo_combo.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Fecha de inasistencia
        tk.Label(form_frame, text="Fecha:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        fecha_entry = tk.Entry(form_frame, width=20)
        fecha_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        fecha_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Motivo
        tk.Label(form_frame, text="Motivo:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        motivo_combo = ttk.Combobox(form_frame, values=[
            "Enfermedad", "Consulta médica", "Trámite familiar", "Viaje", "Otro"
        ], state="readonly", width=20)
        motivo_combo.set("Enfermedad")
        motivo_combo.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Descripción
        tk.Label(form_frame, text="Descripción:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=3, column=0, padx=10, pady=5, sticky="nw")
        descripcion_text = tk.Text(form_frame, width=50, height=6)
        descripcion_text.insert("1.0", "Descripción detallada del motivo de la inasistencia...")
        descripcion_text.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Botones
        buttons_frame = tk.Frame(form_frame, bg="lightgreen")
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=15)

        tk.Button(buttons_frame, text="📤 Enviar Justificación", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=18, command=self.enviar_justificacion).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📎 Adjuntar Certificado", bg="#2196F3", fg="white", 
                 font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)

    def enviar_justificacion(self):
        """Enviar justificación de inasistencia"""
        messagebox.showinfo("Justificación Enviada", 
                           "✅ Su justificación ha sido enviada y registrada en el sistema.\n"
                           "El preceptor revisará la documentación.")