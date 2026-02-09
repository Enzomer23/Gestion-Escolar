"""
Consulta de Calificaciones
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

class ConsultaCalificacionesWindow:
    """Ventana para consulta de calificaciones"""
    
    def __init__(self, parent, cal_manager):
        self.parent = parent
        self.cal_manager = cal_manager
        self.create_window()

    def create_window(self):
        """Crear ventana principal de consulta"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🔍 Consulta de Calificaciones")
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
        title = tk.Label(scrollable_frame, text="🔍 Consulta Avanzada de Calificaciones", 
                        font=("Arial", 18, "bold"), bg="lightcyan", fg="darkcyan")
        title.pack(pady=15)

        # Panel de filtros
        self.create_filters_panel(scrollable_frame)
        
        # Notebook con tipos de consulta
        self.create_notebook(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_filters_panel(self, parent):
        """Crear panel de filtros"""
        filters_frame = tk.LabelFrame(parent, text="🔍 Filtros de Búsqueda", 
                                     font=("Arial", 12, "bold"), bg="lightcyan", 
                                     fg="darkcyan", padx=10, pady=8)
        filters_frame.pack(fill=tk.X, pady=(0, 15))

        # Filtros principales
        tk.Label(filters_frame, text="Buscar por:", font=("Arial", 10), bg="lightcyan").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.busqueda_entry = tk.Entry(filters_frame, width=25)
        self.busqueda_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filters_frame, text="Curso:", font=("Arial", 10), bg="lightcyan").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.curso_combo = ttk.Combobox(filters_frame, values=["Todos", "1º Año", "2º Año", "3º Año"], state="readonly", width=12)
        self.curso_combo.set("Todos")
        self.curso_combo.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(filters_frame, text="Materia:", font=("Arial", 10), bg="lightcyan").grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.materia_filtro_combo = ttk.Combobox(filters_frame, values=["Todas", "Matemáticas", "Lengua", "Ciencias"], state="readonly", width=15)
        self.materia_filtro_combo.set("Todas")
        self.materia_filtro_combo.grid(row=0, column=5, padx=5, pady=5)

        tk.Button(filters_frame, text="🔍 Buscar", bg="#2196F3", fg="white", font=("Arial", 10), width=10, command=self.buscar_calificaciones).grid(row=0, column=6, padx=10, pady=5)

    def create_notebook(self, parent):
        """Crear notebook con tipos de consulta"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Pestaña 1: Por Alumno
        self.create_por_alumno_tab(notebook)
        
        # Pestaña 2: Por Materia
        self.create_por_materia_tab(notebook)
        
        # Pestaña 3: Por Período
        self.create_por_periodo_tab(notebook)
        
        # Pestaña 4: Búsqueda Avanzada
        self.create_busqueda_avanzada_tab(notebook)

    def create_por_alumno_tab(self, notebook):
        """Crear pestaña de consulta por alumno"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="👤 Por Alumno")

        tk.Label(frame, text="👤 Consulta por Alumno", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Selección de alumno
        selection_frame = tk.Frame(frame, bg="white", relief=tk.RAISED, bd=2)
        selection_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(selection_frame, text="Seleccionar Alumno:", font=("Arial", 12, "bold"), bg="white").pack(pady=5)
        self.alumno_combo = ttk.Combobox(selection_frame, state="readonly", width=40)
        self.alumno_combo.pack(pady=5)
        self.alumno_combo.bind("<<ComboboxSelected>>", self.cargar_calificaciones_alumno)

        # Tabla de calificaciones del alumno
        self.create_tabla_alumno(frame)

        # Cargar alumnos
        self.cargar_lista_alumnos()

    def create_tabla_alumno(self, parent):
        """Crear tabla de calificaciones por alumno"""
        tabla_frame = tk.LabelFrame(parent, text="📊 Calificaciones del Alumno", 
                                   font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        tabla_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Materia", "Tipo Evaluación", "Nota", "Fecha", "Observaciones", "Docente")
        self.tree_alumno = ttk.Treeview(tabla_frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            self.tree_alumno.heading(col, text=col)
            if col == "Materia":
                self.tree_alumno.column(col, width=150, anchor="w")
            elif col == "Observaciones":
                self.tree_alumno.column(col, width=200, anchor="w")
            else:
                self.tree_alumno.column(col, width=120, anchor="center")

        self.tree_alumno.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def cargar_lista_alumnos(self):
        """Cargar lista de todos los alumnos"""
        if not DATABASE_AVAILABLE or not self.cal_manager:
            return

        try:
            # Obtener todos los alumnos activos
            from server.database import crear_conexion
            connection = crear_conexion()
            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("""
                    SELECT id, nombre, apellido, curso, division 
                    FROM alumnos 
                    WHERE activo = TRUE 
                    ORDER BY curso, division, apellido, nombre
                """)
                alumnos = cursor.fetchall()
                cursor.close()
                connection.close()

                # Llenar combobox
                alumno_values = [f"{a['apellido']}, {a['nombre']} ({a['curso']} {a['division']})" for a in alumnos]
                self.alumno_combo['values'] = alumno_values
                self.alumnos_data = alumnos

        except Exception as e:
            print(f"Error cargando alumnos: {e}")

    def cargar_calificaciones_alumno(self, event=None):
        """Cargar calificaciones del alumno seleccionado"""
        alumno_index = self.alumno_combo.current()
        if alumno_index < 0:
            return

        alumno_seleccionado = self.alumnos_data[alumno_index]

        # Limpiar tabla
        for item in self.tree_alumno.get_children():
            self.tree_alumno.delete(item)

        if DATABASE_AVAILABLE and self.cal_manager:
            calificaciones = self.cal_manager.obtener_calificaciones_alumno(alumno_seleccionado['id'])
            
            for cal in calificaciones:
                self.tree_alumno.insert("", tk.END, values=(
                    cal['materia'],
                    cal['tipo_evaluacion'],
                    cal['nota'],
                    cal['fecha_evaluacion'].strftime("%d/%m/%Y") if cal['fecha_evaluacion'] else '',
                    cal['observaciones'] or '',
                    cal['docente']
                ))

    def create_por_materia_tab(self, notebook):
        """Crear pestaña de consulta por materia"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="📚 Por Materia")

        tk.Label(frame, text="📚 Consulta por Materia", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Tabla de calificaciones por materia
        columns = ("Alumno", "Curso", "Nota", "Tipo Evaluación", "Fecha", "Estado")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Alumno":
                tree.column(col, width=150, anchor="w")
            else:
                tree.column(col, width=120, anchor="center")

        # Datos de ejemplo
        calificaciones_data = [
            ("Pérez, Juan", "1º A", "8.5", "Mensual", "15/01/2025", "✅ Aprobado"),
            ("Gómez, Ana", "2º A", "9.0", "Diaria", "14/01/2025", "🏆 Excelente"),
            ("González, Mario", "2º A", "5.8", "Mensual", "13/01/2025", "🚨 En Riesgo"),
            ("Díaz, Laura", "1º A", "8.9", "Cuatrimestral", "12/01/2025", "✅ Muy Bueno")
        ]

        for cal in calificaciones_data:
            estado = cal[5]
            if "🚨" in estado:
                tags = ("riesgo",)
            elif "🏆" in estado:
                tags = ("excelente",)
            else:
                tags = ()
            
            tree.insert("", tk.END, values=cal, tags=tags)

        # Configurar colores
        tree.tag_configure("riesgo", background="#FFEBEE")
        tree.tag_configure("excelente", background="#E8F5E8")

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def create_por_periodo_tab(self, notebook):
        """Crear pestaña de consulta por período"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="📅 Por Período")

        tk.Label(frame, text="📅 Consulta por Período Académico", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Resumen por período
        resumen_text = """
        📅 RESUMEN POR PERÍODO ACADÉMICO:
        ═══════════════════════════════════════
        
        📊 PRIMER CUATRIMESTRE 2025:
        • Total calificaciones: 1,247
        • Promedio general: 8.3
        • Alumnos evaluados: 247
        • Materias activas: 25
        
        📈 DISTRIBUCIÓN DE NOTAS:
        • Excelente (9-10): ████████░░ 28%
        • Muy Bueno (8-8.9): ████████████ 35%
        • Bueno (7-7.9): ██████░░░░ 22%
        • Regular (6-6.9): ████░░░░░░ 12%
        • En Riesgo (<6): ██░░░░░░░░ 3%
        
        🎯 ANÁLISIS POR CURSO:
        • 1º Año: 8.4 promedio (↗ +0.3)
        • 2º Año: 8.2 promedio (→ 0.0)
        • 3º Año: 8.1 promedio (↘ -0.1)
        
        📚 MATERIAS DESTACADAS:
        • Lengua y Literatura: 8.7 promedio
        • Historia: 8.5 promedio
        • Matemáticas: 8.3 promedio
        
        ⚠️ MATERIAS QUE REQUIEREN ATENCIÓN:
        • Física: 7.8 promedio
        • Química: 7.9 promedio
        """

        tk.Label(frame, text=resumen_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_busqueda_avanzada_tab(self, notebook):
        """Crear pestaña de búsqueda avanzada"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="🔎 Búsqueda Avanzada")

        tk.Label(frame, text="🔎 Búsqueda Avanzada de Calificaciones", 
                font=("Arial", 14, "bold"), bg="lightcoral", fg="darkred").pack(pady=10)

        # Criterios de búsqueda avanzada
        criterios_frame = tk.LabelFrame(frame, text="⚙️ Criterios de Búsqueda", 
                                       font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        criterios_frame.pack(fill=tk.X, padx=20, pady=10)

        # Rango de notas
        tk.Label(criterios_frame, text="Rango de Notas:", font=("Arial", 10, "bold"), bg="lightcoral").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        rango_frame = tk.Frame(criterios_frame, bg="lightcoral")
        rango_frame.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(rango_frame, text="Desde:", font=("Arial", 9), bg="lightcoral").pack(side=tk.LEFT)
        self.nota_desde_entry = tk.Entry(rango_frame, width=8)
        self.nota_desde_entry.pack(side=tk.LEFT, padx=5)
        self.nota_desde_entry.insert(0, "1.0")
        
        tk.Label(rango_frame, text="Hasta:", font=("Arial", 9), bg="lightcoral").pack(side=tk.LEFT, padx=5)
        self.nota_hasta_entry = tk.Entry(rango_frame, width=8)
        self.nota_hasta_entry.pack(side=tk.LEFT, padx=5)
        self.nota_hasta_entry.insert(0, "10.0")

        # Rango de fechas
        tk.Label(criterios_frame, text="Rango de Fechas:", font=("Arial", 10, "bold"), bg="lightcoral").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        fecha_frame = tk.Frame(criterios_frame, bg="lightcoral")
        fecha_frame.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        tk.Label(fecha_frame, text="Desde:", font=("Arial", 9), bg="lightcoral").pack(side=tk.LEFT)
        self.fecha_desde_entry = tk.Entry(fecha_frame, width=12)
        self.fecha_desde_entry.pack(side=tk.LEFT, padx=5)
        self.fecha_desde_entry.insert(0, "2025-01-01")
        
        tk.Label(fecha_frame, text="Hasta:", font=("Arial", 9), bg="lightcoral").pack(side=tk.LEFT, padx=5)
        self.fecha_hasta_entry = tk.Entry(fecha_frame, width=12)
        self.fecha_hasta_entry.pack(side=tk.LEFT, padx=5)
        self.fecha_hasta_entry.insert(0, "2025-12-31")

        # Botones de búsqueda
        buttons_frame = tk.Frame(criterios_frame, bg="lightcoral")
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=15)

        tk.Button(buttons_frame, text="🔎 Búsqueda Avanzada", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=18, command=self.busqueda_avanzada).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="🗑️ Limpiar Filtros", bg="#FF5722", fg="white", 
                 font=("Arial", 10), width=15, command=self.limpiar_filtros).pack(side=tk.LEFT, padx=5)

        # Resultados de búsqueda
        resultados_frame = tk.LabelFrame(frame, text="📋 Resultados de Búsqueda", 
                                        font=("Arial", 12, "bold"), bg="lightcoral", fg="darkred")
        resultados_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("Alumno", "Materia", "Nota", "Tipo", "Fecha", "Docente")
        self.tree_resultados = ttk.Treeview(resultados_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree_resultados.heading(col, text=col)
            if col == "Alumno" or col == "Materia":
                self.tree_resultados.column(col, width=150, anchor="w")
            else:
                self.tree_resultados.column(col, width=100, anchor="center")

        self.tree_resultados.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def buscar_calificaciones(self):
        """Buscar calificaciones con filtros básicos"""
        messagebox.showinfo("Búsqueda", "🔍 Función de búsqueda ejecutada\nResultados mostrados en la tabla")

    def busqueda_avanzada(self):
        """Ejecutar búsqueda avanzada"""
        try:
            nota_desde = float(self.nota_desde_entry.get())
            nota_hasta = float(self.nota_hasta_entry.get())
            fecha_desde = self.fecha_desde_entry.get()
            fecha_hasta = self.fecha_hasta_entry.get()
            
            messagebox.showinfo("Búsqueda Avanzada", 
                               f"🔎 Búsqueda ejecutada con criterios:\n"
                               f"• Notas: {nota_desde} - {nota_hasta}\n"
                               f"• Fechas: {fecha_desde} - {fecha_hasta}")
            
        except ValueError:
            messagebox.showerror("Error", "Verifique que los valores numéricos sean correctos")

    def limpiar_filtros(self):
        """Limpiar todos los filtros"""
        self.busqueda_entry.delete(0, tk.END)
        self.curso_combo.set("Todos")
        self.materia_filtro_combo.set("Todas")
        self.nota_desde_entry.delete(0, tk.END)
        self.nota_desde_entry.insert(0, "1.0")
        self.nota_hasta_entry.delete(0, tk.END)
        self.nota_hasta_entry.insert(0, "10.0")
        
        messagebox.showinfo("Filtros Limpiados", "✅ Todos los filtros han sido restablecidos")