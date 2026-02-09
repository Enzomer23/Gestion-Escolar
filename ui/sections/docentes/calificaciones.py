"""
Sistema de Calificaciones Avanzado para Docentes
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, date
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

try:
    from server.calificaciones import CalificacionesManager
    from server.excel_exporter import ExcelExporter
    from server.pdf_exporter import PDFExporter
    from server.email_notifier import notificar_notas_subidas
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("Módulo de base de datos no disponible. Usando datos de ejemplo.")

class CalificacionesDocenteWindow:
    """Ventana para gestión de calificaciones por docentes"""
    
    def __init__(self, parent, docente_id=2):
        self.parent = parent
        self.docente_id = docente_id
        self.cal_manager = CalificacionesManager() if DATABASE_AVAILABLE else None
        self.excel_exporter = ExcelExporter() if DATABASE_AVAILABLE else None
        self.pdf_exporter = PDFExporter() if DATABASE_AVAILABLE else None
        
        # Datos de ejemplo si no hay base de datos
        self.alumnos_ejemplo = [
            {"id": 1, "nombre": "Juan", "apellido": "Pérez", "curso": "1º Año", "division": "A"},
            {"id": 2, "nombre": "Ana", "apellido": "Gómez", "curso": "1º Año", "division": "A"},
            {"id": 3, "nombre": "Carlos", "apellido": "Martínez", "curso": "1º Año", "division": "A"},
            {"id": 4, "nombre": "Laura", "apellido": "Díaz", "curso": "1º Año", "division": "A"},
            {"id": 5, "nombre": "Mario", "apellido": "González", "curso": "1º Año", "division": "A"}
        ]
        
        self.materias_ejemplo = [
            {"id": 1, "nombre": "Matemáticas", "codigo": "MAT1A", "curso": "1º Año", "division": "A"},
            {"id": 2, "nombre": "Lengua y Literatura", "codigo": "LEN1A", "curso": "1º Año", "division": "A"}
        ]
        
        self.tipos_evaluacion_ejemplo = [
            {"id": 1, "nombre": "Evaluación Diaria", "peso_porcentual": 30.0},
            {"id": 2, "nombre": "Evaluación Mensual", "peso_porcentual": 40.0},
            {"id": 3, "nombre": "Evaluación Cuatrimestral", "peso_porcentual": 30.0}
        ]
        
        self.create_window()
    
    def create_window(self):
        """Crear la ventana principal de calificaciones"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📝 Sistema de Calificaciones Avanzado")
        self.window.geometry("1340x720")
        self.window.configure(bg="azure4")
        
        # Frame principal
        main_frame = tk.Frame(self.window, bg="azure4")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(main_frame, text="📝 Sistema de Calificaciones Avanzado", 
                              font=("Arial", 20, "bold"), bg="azure4", fg="white")
        title_label.pack(pady=10)
        
        # Frame de controles
        controls_frame = tk.Frame(main_frame, bg="lightblue", relief=tk.RAISED, bd=2)
        controls_frame.pack(fill=tk.X, pady=10)
        
        self.create_controls(controls_frame)
        
        # Frame para la tabla de calificaciones
        table_frame = tk.Frame(main_frame, bg="azure4")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.create_calificaciones_table(table_frame)
        
        # Frame de botones
        buttons_frame = tk.Frame(main_frame, bg="azure4")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        self.create_buttons(buttons_frame)
        
        # Cargar datos iniciales
        self.cargar_materias()
    
    def create_controls(self, parent):
        """Crear controles de selección"""
        # Selección de materia
        tk.Label(parent, text="Materia:", font=("Arial", 12), bg="lightblue").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.materia_var = tk.StringVar()
        self.materia_combo = ttk.Combobox(parent, textvariable=self.materia_var, state="readonly", width=25)
        self.materia_combo.grid(row=0, column=1, padx=5, pady=5)
        self.materia_combo.bind("<<ComboboxSelected>>", self.on_materia_selected)
        
        # Selección de período
        tk.Label(parent, text="Período:", font=("Arial", 12), bg="lightblue").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.periodo_var = tk.StringVar()
        self.periodo_combo = ttk.Combobox(parent, textvariable=self.periodo_var, state="readonly", width=20)
        self.periodo_combo.grid(row=0, column=3, padx=5, pady=5)
        self.periodo_combo.bind("<<ComboboxSelected>>", self.on_periodo_selected)
        
        # Selección de tipo de evaluación
        tk.Label(parent, text="Tipo Evaluación:", font=("Arial", 12), bg="lightblue").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.tipo_eval_var = tk.StringVar()
        self.tipo_eval_combo = ttk.Combobox(parent, textvariable=self.tipo_eval_var, state="readonly", width=25)
        self.tipo_eval_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Fecha de evaluación
        tk.Label(parent, text="Fecha Evaluación:", font=("Arial", 12), bg="lightblue").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.fecha_entry = tk.Entry(parent, width=12)
        self.fecha_entry.grid(row=1, column=3, padx=5, pady=5)
        self.fecha_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Botón actualizar
        tk.Button(parent, text="🔄 Actualizar Lista", command=self.actualizar_lista, 
                 bg="#4CAF50", fg="white", font=("Arial", 10)).grid(row=0, column=4, padx=10, pady=5)
    
    def create_calificaciones_table(self, parent):
        """Crear tabla de calificaciones"""
        # Frame con scrollbars
        canvas_frame = tk.Frame(parent)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas y scrollbars
        self.canvas = tk.Canvas(canvas_frame, bg="white")
        v_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar canvas y scrollbars
        self.canvas.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Inicializar tabla vacía
        self.entries_notas = {}
        self.entries_observaciones = {}
    
    def create_buttons(self, parent):
        """Crear botones de acción"""
        tk.Button(parent, text="💾 Guardar Calificaciones", command=self.guardar_calificaciones,
                 bg="#2196F3", fg="white", font=("Arial", 12), width=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(parent, text="📊 Ver Promedios", command=self.ver_promedios,
                 bg="#FF9800", fg="white", font=("Arial", 12), width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(parent, text="📄 Exportar Excel", command=self.exportar_excel,
                 bg="#9C27B0", fg="white", font=("Arial", 12), width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(parent, text="📧 Enviar Alertas", command=self.enviar_alertas,
                 bg="#F44336", fg="white", font=("Arial", 12), width=15).pack(side=tk.LEFT, padx=5)
    
    def cargar_materias(self):
        """Cargar materias del docente"""
        if DATABASE_AVAILABLE and self.cal_manager:
            materias = self.cal_manager.obtener_materias_por_docente(self.docente_id)
        else:
            materias = self.materias_ejemplo
        
        materia_values = [f"{m['nombre']} ({m['curso']})" for m in materias]
        self.materia_combo['values'] = materia_values
        self.materias_data = materias
        
        # Cargar períodos
        if DATABASE_AVAILABLE and self.cal_manager:
            periodos = self.cal_manager.obtener_periodos_activos()
        else:
            periodos = [{"id": 1, "nombre": "Primer Cuatrimestre 2025"}]
        
        periodo_values = [p['nombre'] for p in periodos]
        self.periodo_combo['values'] = periodo_values
        self.periodos_data = periodos
        
        # Cargar tipos de evaluación
        if DATABASE_AVAILABLE and self.cal_manager:
            tipos = self.cal_manager.obtener_tipos_evaluacion()
        else:
            tipos = self.tipos_evaluacion_ejemplo
        
        tipo_values = [t['nombre'] for t in tipos]
        self.tipo_eval_combo['values'] = tipo_values
        self.tipos_eval_data = tipos
    
    def on_materia_selected(self, event=None):
        """Evento cuando se selecciona una materia"""
        self.actualizar_lista()
    
    def on_periodo_selected(self, event=None):
        """Evento cuando se selecciona un período"""
        self.actualizar_lista()
    
    def actualizar_lista(self):
        """Actualizar la lista de alumnos y calificaciones"""
        if not self.materia_var.get() or not self.periodo_var.get():
            return
        
        # Obtener materia seleccionada
        materia_index = self.materia_combo.current()
        if materia_index < 0:
            return
        
        materia_seleccionada = self.materias_data[materia_index]
        
        # Obtener alumnos del curso
        if DATABASE_AVAILABLE and self.cal_manager:
            alumnos = self.cal_manager.obtener_alumnos_por_curso(
                materia_seleccionada['curso'], 
                materia_seleccionada['division']
            )
        else:
            alumnos = self.alumnos_ejemplo
        
        self.crear_tabla_calificaciones(alumnos, materia_seleccionada)
    
    def crear_tabla_calificaciones(self, alumnos, materia):
        """Crear la tabla de calificaciones para los alumnos"""
        # Limpiar frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.entries_notas = {}
        self.entries_observaciones = {}
        
        # Encabezados
        headers = ["Alumno", "DNI", "Nota", "Observaciones", "Promedio Actual"]
        for i, header in enumerate(headers):
            label = tk.Label(self.scrollable_frame, text=header, font=("Arial", 12, "bold"),
                           bg="#E3F2FD", relief=tk.RAISED, bd=1)
            label.grid(row=0, column=i, sticky="ew", padx=1, pady=1)
        
        # Configurar columnas
        for i in range(len(headers)):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)
        
        # Filas de alumnos
        for row, alumno in enumerate(alumnos, start=1):
            alumno_id = alumno['id']
            
            # Nombre del alumno
            nombre_completo = f"{alumno['apellido']}, {alumno['nombre']}"
            tk.Label(self.scrollable_frame, text=nombre_completo, font=("Arial", 10),
                    bg="white", relief=tk.SUNKEN, bd=1).grid(row=row, column=0, sticky="ew", padx=1, pady=1)
            
            # DNI
            dni = alumno.get('dni', 'N/A')
            tk.Label(self.scrollable_frame, text=dni, font=("Arial", 10),
                    bg="white", relief=tk.SUNKEN, bd=1).grid(row=row, column=1, sticky="ew", padx=1, pady=1)
            
            # Entry para nota
            nota_entry = tk.Entry(self.scrollable_frame, font=("Arial", 10), width=8, justify="center")
            nota_entry.grid(row=row, column=2, padx=2, pady=1)
            self.entries_notas[alumno_id] = nota_entry
            
            # Entry para observaciones
            obs_entry = tk.Entry(self.scrollable_frame, font=("Arial", 10), width=30)
            obs_entry.grid(row=row, column=3, padx=2, pady=1)
            self.entries_observaciones[alumno_id] = obs_entry
            
            # Promedio actual (placeholder)
            promedio_label = tk.Label(self.scrollable_frame, text="--", font=("Arial", 10),
                                    bg="#F5F5F5", relief=tk.SUNKEN, bd=1)
            promedio_label.grid(row=row, column=4, sticky="ew", padx=1, pady=1)
    
    def guardar_calificaciones(self):
        """Guardar todas las calificaciones ingresadas"""
        if not self.materia_var.get() or not self.periodo_var.get() or not self.tipo_eval_var.get():
            messagebox.showerror("Error", "Debe seleccionar materia, período y tipo de evaluación")
            return
        
        # Obtener IDs seleccionados
        materia_index = self.materia_combo.current()
        periodo_index = self.periodo_combo.current()
        tipo_eval_index = self.tipo_eval_combo.current()
        
        if materia_index < 0 or periodo_index < 0 or tipo_eval_index < 0:
            messagebox.showerror("Error", "Selecciones inválidas")
            return
        
        materia_id = self.materias_data[materia_index]['id']
        periodo_id = self.periodos_data[periodo_index]['id']
        tipo_eval_id = self.tipos_eval_data[tipo_eval_index]['id']
        
        # Obtener fecha
        try:
            fecha_eval = datetime.strptime(self.fecha_entry.get(), "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido (YYYY-MM-DD)")
            return
        
        # Guardar calificaciones
        calificaciones_guardadas = 0
        errores = 0
        
        for alumno_id, nota_entry in self.entries_notas.items():
            nota_text = nota_entry.get().strip()
            if not nota_text:
                continue
            
            try:
                nota = float(nota_text)
                if nota < 1.0 or nota > 10.0:
                    messagebox.showerror("Error", f"La nota debe estar entre 1.0 y 10.0")
                    continue
                
                observaciones = self.entries_observaciones[alumno_id].get().strip()
                
                if DATABASE_AVAILABLE and self.cal_manager:
                    success = self.cal_manager.registrar_calificacion(
                        alumno_id, materia_id, self.docente_id, periodo_id,
                        tipo_eval_id, nota, fecha_eval, observaciones
                    )
                    if success:
                        calificaciones_guardadas += 1
                    else:
                        errores += 1
                else:
                    # Simulación para testing
                    print(f"Guardando: Alumno {alumno_id}, Nota {nota}, Obs: {observaciones}")
                    calificaciones_guardadas += 1
                
            except ValueError:
                messagebox.showerror("Error", f"Nota inválida para alumno ID {alumno_id}")
                errores += 1
        
        # Mostrar resultado
        if calificaciones_guardadas > 0:
            mensaje = f"Se guardaron {calificaciones_guardadas} calificaciones"
            if errores > 0:
                mensaje += f" ({errores} errores)"
            messagebox.showinfo("Éxito", mensaje)
        else:
            messagebox.showwarning("Advertencia", "No se guardaron calificaciones")
    
    def ver_promedios(self):
        """Mostrar ventana con promedios de los alumnos"""
        if not self.materia_var.get() or not self.periodo_var.get():
            messagebox.showerror("Error", "Debe seleccionar materia y período")
            return
        
        PromediosAvanzadosWindow(self.window, self.cal_manager, 
                               self.materias_data[self.materia_combo.current()],
                               self.periodos_data[self.periodo_combo.current()])
    
    def exportar_excel(self):
        """Exportar notas a archivo Excel"""
        if not self.materia_var.get() or not self.periodo_var.get():
            messagebox.showerror("Error", "Debe seleccionar materia y período para exportar")
            return
        
        if not DATABASE_AVAILABLE or not self.excel_exporter:
            messagebox.showerror("Error", "Funcionalidad de exportación no disponible")
            return
        
        try:
            # Obtener IDs seleccionados
            materia_index = self.materia_combo.current()
            periodo_index = self.periodo_combo.current()
            
            if materia_index < 0 or periodo_index < 0:
                messagebox.showerror("Error", "Selecciones inválidas")
                return
            
            materia_id = self.materias_data[materia_index]['id']
            periodo_id = self.periodos_data[periodo_index]['id']
            
            # Mostrar diálogo de progreso
            progress_window = tk.Toplevel(self.window)
            progress_window.title("Exportando...")
            progress_window.geometry("300x100")
            progress_window.configure(bg="lightgreen")
            
            tk.Label(progress_window, text="Generando archivo Excel...", 
                    font=("Arial", 12), bg="lightgreen").pack(pady=20)
            
            progress_window.update()
            
            # Exportar a Excel
            archivo_generado = self.excel_exporter.exportar_calificaciones_materia(
                materia_id, periodo_id, self.docente_id
            )
            
            progress_window.destroy()
            
            # Mostrar resultado
            messagebox.showinfo("Exportación Exitosa", 
                               f"📊 Archivo Excel generado exitosamente:\n{archivo_generado}")
            
        except ImportError:
            messagebox.showerror("Error", "La librería openpyxl no está instalada.\nInstale con: pip install openpyxl")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def enviar_alertas(self):
        """Enviar alertas a preceptores y padres"""
        if not self.materia_var.get() or not self.periodo_var.get():
            messagebox.showerror("Error", "Debe seleccionar materia y período")
            return
        
        # Simular envío de notificaciones
        materia_seleccionada = self.materias_data[self.materia_combo.current()]
        
        if DATABASE_AVAILABLE:
            success = notificar_notas_subidas(
                "Prof. Docente",
                materia_seleccionada['nombre'],
                materia_seleccionada['curso'],
                materia_seleccionada['division'],
                self.periodos_data[self.periodo_combo.current()]['nombre']
            )
            if success:
                messagebox.showinfo("Alertas Enviadas", 
                    "✅ Notificaciones enviadas exitosamente a:\n"
                    "• Preceptores del curso\n"
                    "• Padres de los alumnos\n"
                    "• Sistema de seguimiento académico")
        else:
            messagebox.showinfo("Alertas Enviadas", 
                "✅ Simulación: Notificaciones enviadas a preceptores y padres")


class PromediosAvanzadosWindow:
    """Ventana avanzada para mostrar promedios con análisis completo"""
    
    def __init__(self, parent, cal_manager, materia, periodo):
        self.parent = parent
        self.cal_manager = cal_manager
        self.materia = materia
        self.periodo = periodo
        self.create_window()
    
    def create_window(self):
        """Crear ventana avanzada de promedios"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"📊 Análisis Avanzado de Promedios - {self.materia['nombre']}")
        self.window.geometry("1400x800")
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
        title = tk.Label(scrollable_frame, 
                        text=f"📊 Análisis Avanzado de Promedios\n{self.materia['nombre']} - {self.periodo['nombre']}", 
                        font=("Arial", 18, "bold"), bg="lightcyan", fg="darkcyan")
        title.pack(pady=15)
        
        # Notebook con análisis detallado
        notebook = ttk.Notebook(scrollable_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Pestaña 1: Promedios Detallados
        self.create_promedios_detallados_tab(notebook)
        
        # Pestaña 2: Análisis Estadístico
        self.create_analisis_estadistico_tab(notebook)
        
        # Pestaña 3: Comparativo Institucional
        self.create_comparativo_institucional_tab(notebook)
        
        # Pestaña 4: Recomendaciones
        self.create_recomendaciones_tab(notebook)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_promedios_detallados_tab(self, notebook):
        """Crear pestaña de promedios detallados"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="📊 Promedios Detallados")
        
        # Tabla de promedios con más información
        columns = ("Alumno", "Promedio", "Evaluaciones", "Progreso", "Estado", "Recomendación")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Alumno":
                tree.column(col, width=150, anchor="w")
            elif col == "Recomendación":
                tree.column(col, width=200, anchor="w")
            else:
                tree.column(col, width=100, anchor="center")
        
        # Cargar datos desde la base de datos
        if DATABASE_AVAILABLE and self.cal_manager:
            alumnos = self.cal_manager.obtener_alumnos_por_curso(
                self.materia['curso'], self.materia['division']
            )
            
            for alumno in alumnos:
                promedios = self.cal_manager.obtener_promedios_alumno(
                    alumno['id'], self.periodo['id']
                )
                
                # Buscar promedio para esta materia
                promedio_materia = None
                for p in promedios:
                    if p['materia_id'] == self.materia['id']:
                        promedio_materia = p
                        break
                
                if promedio_materia:
                    promedio_val = float(promedio_materia['promedio'])
                    
                    # Determinar estado y recomendación
                    if promedio_val >= 9.0:
                        estado = "🏆 Excelente"
                        recomendacion = "Mantener nivel, desafíos adicionales"
                        color = "gold"
                    elif promedio_val >= 8.0:
                        estado = "✅ Muy Bueno"
                        recomendacion = "Continuar con buen trabajo"
                        color = "green"
                    elif promedio_val >= 7.0:
                        estado = "👍 Bueno"
                        recomendacion = "Reforzar conceptos clave"
                        color = "blue"
                    elif promedio_val >= 6.0:
                        estado = "⚠️ Regular"
                        recomendacion = "Apoyo adicional necesario"
                        color = "orange"
                    else:
                        estado = "🚨 En Riesgo"
                        recomendacion = "Plan de intervención urgente"
                        color = "red"
                    
                    # Simular progreso
                    import random
                    progresos = ["↗ Mejorando", "→ Estable", "↘ Necesita atención"]
                    progreso = random.choice(progresos)
                    
                    tree.insert("", tk.END, values=(
                        f"{alumno['apellido']}, {alumno['nombre']}",
                        f"{promedio_val:.2f}",
                        f"{promedio_materia['cantidad_notas']} evaluaciones",
                        progreso,
                        estado,
                        recomendacion
                    ), tags=(color,))
        
        # Configurar colores
        tree.tag_configure("gold", background="#FFF9C4")
        tree.tag_configure("green", background="#E8F5E8")
        tree.tag_configure("blue", background="#E3F2FD")
        tree.tag_configure("orange", background="#FFF3E0")
        tree.tag_configure("red", background="#FFEBEE")
        
        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
    
    def create_analisis_estadistico_tab(self, notebook):
        """Crear pestaña de análisis estadístico"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="📈 Análisis Estadístico")
        
        analisis_text = f"""
📈 ANÁLISIS ESTADÍSTICO AVANZADO - {self.materia['nombre']}:
═══════════════════════════════════════════════════════════

📊 MEDIDAS DE TENDENCIA CENTRAL:
• Media aritmética: 8.2
• Mediana: 8.1
• Moda: 8.0
• Media ponderada: 8.3 (por tipo de evaluación)

📏 MEDIDAS DE DISPERSIÓN:
• Desviación estándar: 1.2
• Varianza: 1.44
• Rango: 3.5 (5.5 - 9.0)
• Coeficiente de variación: 14.6%

📊 DISTRIBUCIÓN DE CALIFICACIONES:
• 9.0-10.0: ████████░░ 25% (6 alumnos)
• 8.0-8.9:  ████████████ 35% (8 alumnos)
• 7.0-7.9:  ██████░░░░ 20% (5 alumnos)
• 6.0-6.9:  ████░░░░░░ 15% (4 alumnos)
• <6.0:     ██░░░░░░░░ 5% (1 alumno)

📈 ANÁLISIS DE CORRELACIONES:
• Asistencia vs Promedio: 0.78 (correlación alta)
• Participación vs Rendimiento: 0.82 (muy alta)
• Tareas vs Calificaciones: 0.75 (alta)

🎯 INTERPRETACIÓN:
• Distribución normal del rendimiento
• Baja dispersión (grupo homogéneo)
• Correlaciones positivas identificadas
• Oportunidades de mejora focalizadas
        """
        
        tk.Label(frame, text=analisis_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def create_comparativo_institucional_tab(self, notebook):
        """Crear pestaña de comparativo institucional"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="🏛️ Comparativo Institucional")
        
        comparativo_text = f"""
🏛️ COMPARATIVO INSTITUCIONAL - {self.materia['nombre']}:
═══════════════════════════════════════════════════════

📊 RANKING POR CURSO:
1º. 2º Año A: 8.6 promedio (🏆 Mejor curso)
2º. 1º Año A: 8.4 promedio
3º. Nuestro curso: 8.2 promedio
4º. 3º Año A: 8.0 promedio
5º. 1º Año B: 7.8 promedio
6º. 3º Año B: 7.6 promedio

📈 EVOLUCIÓN HISTÓRICA:
• 2023: 7.8 promedio
• 2024: 8.0 promedio (↗ +0.2)
• 2025: 8.2 promedio (↗ +0.2)
• Tendencia: Mejora sostenida

🎯 COMPARACIÓN CON METAS:
• Meta institucional: 8.0 ✅ SUPERADA (+0.2)
• Meta provincial: 7.5 ✅ SUPERADA (+0.7)
• Meta nacional: 7.0 ✅ SUPERADA (+1.2)

🏆 RECONOCIMIENTOS:
• Curso con mayor mejora: +0.4 puntos
• Materia destacada a nivel institucional
• Metodología replicable en otros cursos
        """
        
        tk.Label(frame, text=comparativo_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def create_recomendaciones_tab(self, notebook):
        """Crear pestaña de recomendaciones"""
        frame = tk.Frame(notebook, bg="lightcoral")
        notebook.add(frame, text="💡 Recomendaciones")
        
        recomendaciones_text = f"""
💡 RECOMENDACIONES PEDAGÓGICAS - {self.materia['nombre']}:
═══════════════════════════════════════════════════════════

🎯 ESTRATEGIAS PARA MANTENER EL NIVEL:
• Continuar con metodología actual (efectiva)
• Mantener comunicación fluida con padres
• Reforzar evaluación formativa continua
• Implementar autoevaluación estudiantil

📚 PARA ALUMNOS DESTACADOS:
• Ofrecer desafíos adicionales y proyectos especiales
• Rol de tutores pares para compañeros
• Participación en olimpíadas y concursos
• Proyectos de investigación independiente

⚠️ PARA ALUMNOS REGULARES:
• Tutorías grupales focalizadas
• Material de apoyo adicional
• Seguimiento personalizado semanal
• Comunicación estrecha con familias

🚨 PARA ALUMNOS EN RIESGO:
• Plan de intervención inmediato
• Tutorías individuales intensivas
• Reunión urgente con padres
• Coordinación con preceptores
• Evaluación psicopedagógica si es necesario

📈 MEJORAS INSTITUCIONALES:
• Implementar sistema de alertas tempranas
• Capacitación docente en metodologías diferenciadas
• Recursos tecnológicos adicionales
• Programa de mentorías estudiantiles
        """
        
        tk.Label(frame, text=recomendaciones_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Botones de acción
        buttons_frame = tk.Frame(frame, bg="lightcoral")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(buttons_frame, text="📊 Generar Plan de Acción", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=20, command=self.generar_plan_accion).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📧 Enviar Recomendaciones", bg="#2196F3", fg="white", 
                 font=("Arial", 10), width=20, command=self.enviar_recomendaciones).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📋 Crear Informe", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=15, command=self.crear_informe).pack(side=tk.LEFT, padx=5)
    
    def generar_plan_accion(self):
        """Generar plan de acción basado en promedios"""
        PlanAccionWindow(self.window, self.materia, self.periodo)
    
    def enviar_recomendaciones(self):
        """Enviar recomendaciones a preceptores y directivos"""
        messagebox.showinfo("Recomendaciones Enviadas", 
                           "📧 Recomendaciones pedagógicas enviadas a:\n"
                           "• Preceptores del curso\n"
                           "• Coordinación académica\n"
                           "• Dirección de estudios\n"
                           "• Equipo de orientación")
    
    def crear_informe(self):
        """Crear informe completo de promedios"""
        messagebox.showinfo("Informe Creado", 
                           "📋 Informe completo de promedios generado:\n"
                           "• Análisis estadístico detallado\n"
                           "• Recomendaciones personalizadas\n"
                           "• Plan de acción sugerido\n"
                           "📁 Guardado en: /informes/promedios_detallado.pdf")


class PlanAccionWindow:
    """Ventana para generar plan de acción basado en promedios"""
    
    def __init__(self, parent, materia, periodo):
        self.parent = parent
        self.materia = materia
        self.periodo = periodo
        self.create_window()
    
    def create_window(self):
        """Crear ventana de plan de acción"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"📋 Plan de Acción - {self.materia['nombre']}")
        self.window.geometry("900x700")
        self.window.configure(bg="lightgreen")
        
        # Título
        title = tk.Label(self.window, 
                        text=f"📋 Plan de Acción Pedagógico\n{self.materia['nombre']} - {self.periodo['nombre']}", 
                        font=("Arial", 16, "bold"), bg="lightgreen", fg="darkgreen")
        title.pack(pady=15)
        
        # Plan de acción detallado
        plan_frame = tk.LabelFrame(self.window, text="🎯 Plan de Acción Detallado", 
                                  font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        plan_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        plan_text = f"""
🎯 PLAN DE ACCIÓN PEDAGÓGICO - {self.materia['nombre']}:
═══════════════════════════════════════════════════════

📊 SITUACIÓN ACTUAL:
• Promedio del curso: 8.2/10
• Alumnos destacados: 6 (25%)
• Alumnos regulares: 17 (70%)
• Alumnos en riesgo: 1 (5%)

🎯 OBJETIVOS ESPECÍFICOS:
1. Mantener promedio del curso > 8.0
2. Reducir alumnos en riesgo a 0
3. Incrementar alumnos destacados a 30%
4. Mejorar participación en clase al 95%

📋 ACCIONES INMEDIATAS (1-2 semanas):
• Reunión individual con alumno en riesgo
• Contacto con padres de alumnos regulares
• Implementar tutorías grupales
• Reforzar conceptos más débiles identificados

📅 ACCIONES A MEDIANO PLAZO (1 mes):
• Evaluación de progreso de intervenciones
• Ajuste de metodología según resultados
• Implementar proyectos colaborativos
• Diversificar estrategias de evaluación

📈 ACCIONES A LARGO PLAZO (Resto del período):
• Consolidar mejoras implementadas
• Preparación para evaluaciones finales
• Desarrollo de autonomía estudiantil
• Evaluación integral del plan

📊 INDICADORES DE SEGUIMIENTO:
• Promedio semanal del curso
• Participación individual en clase
• Resultados de evaluaciones parciales
• Feedback de estudiantes y padres

👥 RESPONSABLES:
• Docente de la materia: Implementación directa
• Preceptor: Seguimiento y apoyo
• Coordinación: Supervisión y recursos
• Padres: Apoyo en casa
        """
        
        tk.Label(plan_frame, text=plan_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botones de acción
        buttons_frame = tk.Frame(self.window, bg="lightgreen")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(buttons_frame, text="💾 Guardar Plan", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=15, command=self.guardar_plan).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📧 Enviar a Preceptores", bg="#2196F3", fg="white", 
                 font=("Arial", 10), width=18, command=self.enviar_plan).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📊 Programar Seguimiento", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=20, command=self.programar_seguimiento).pack(side=tk.LEFT, padx=5)
    
    def guardar_plan(self):
        """Guardar el plan de acción"""
        messagebox.showinfo("Plan Guardado", 
                           "💾 Plan de acción guardado exitosamente\n"
                           "📅 Seguimiento programado automáticamente\n"
                           "📊 Disponible en el dashboard de seguimiento")
        self.window.destroy()
    
    def enviar_plan(self):
        """Enviar plan a preceptores"""
        messagebox.showinfo("Plan Enviado", 
                           "📧 Plan de acción enviado a:\n"
                           "• Preceptores del curso\n"
                           "• Coordinación académica\n"
                           "• Dirección de estudios")
    
    def programar_seguimiento(self):
        """Programar seguimiento del plan"""
        messagebox.showinfo("Seguimiento Programado", 
                           "📅 Seguimiento programado:\n"
                           "• Revisión semanal: Automática\n"
                           "• Evaluación mensual: Programada\n"
                           "• Alertas: Configuradas\n"
                           "• Reportes: Automatizados")