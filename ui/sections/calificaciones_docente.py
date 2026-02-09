"""
Interfaz para gestión de calificaciones por parte de los docentes
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
    from server.excel_exporter import ExcelExporter
    from server.pdf_exporter import PDFExporter
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("Módulo de base de datos no disponible. Usando datos de ejemplo.")

class CalificacionesDocenteWindow:
    """Ventana para gestión de calificaciones por docentes"""
    
    def __init__(self, parent, docente_id=2):  # ID por defecto para testing
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
        self.window.title("Gestión de Calificaciones - Docente")
        self.window.geometry("1400x800")
        self.window.configure(bg="azure4")
        
        # Frame principal
        main_frame = tk.Frame(self.window, bg="azure4")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = tk.Label(main_frame, text="Sistema de Calificaciones", 
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
        tk.Button(parent, text="Actualizar Lista", command=self.actualizar_lista, 
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
        tk.Button(parent, text="Guardar Calificaciones", command=self.guardar_calificaciones,
                 bg="#2196F3", fg="white", font=("Arial", 12), width=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(parent, text="Ver Promedios", command=self.ver_promedios,
                 bg="#FF9800", fg="white", font=("Arial", 12), width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(parent, text="Exportar a Excel", command=self.exportar_notas,
                 bg="#9C27B0", fg="white", font=("Arial", 12), width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(parent, text="Exportar a PDF", command=self.exportar_notas_pdf,
                 bg="#E91E63", fg="white", font=("Arial", 12), width=15).pack(side=tk.LEFT, padx=5)
        
        tk.Button(parent, text="Alumnos en Riesgo", command=self.ver_alumnos_riesgo,
                 bg="#F44336", fg="white", font=("Arial", 12), width=18).pack(side=tk.LEFT, padx=5)
    
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
        if not self.materia_var.get():
            return
        
        if not self.periodo_var.get():
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
        
        # Cargar calificaciones existentes después de crear la tabla
        self.cargar_calificaciones_existentes(materia_seleccionada['id'])
    
    def cargar_calificaciones_existentes(self, materia_id):
        """Cargar todas las calificaciones existentes para la materia y configuración actual"""
        if not self.periodo_var.get():
            return
            
        periodo_index = self.periodo_combo.current()
        if periodo_index < 0:
            return
            
        # Cargar calificaciones para cada alumno
        for alumno_id in self.entries_notas.keys():
            self.cargar_calificacion_existente(alumno_id, materia_id)
    
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
            
            # Cargar calificación existente si existe
            self.cargar_calificacion_existente(alumno_id, materia['id'])
    
    def cargar_calificacion_existente(self, alumno_id, materia_id):
        """Cargar calificación existente si ya fue registrada"""
        if not DATABASE_AVAILABLE or not self.cal_manager:
            return
        
        # Obtener período y tipo de evaluación seleccionados
        periodo_index = self.periodo_combo.current()
        tipo_eval_index = self.tipo_eval_combo.current()
        if periodo_index < 0:
            return
        
        periodo_id = self.periodos_data[periodo_index]['id']
        
        # Si hay tipo de evaluación seleccionado, buscar calificación específica
        if tipo_eval_index >= 0:
            tipo_eval_id = self.tipos_eval_data[tipo_eval_index]['id']
            fecha_eval = self.fecha_entry.get()
            
            # Buscar calificación específica para este tipo de evaluación y fecha
            calificaciones = self.cal_manager.obtener_calificaciones_materia(materia_id, periodo_id)
            
            for cal in calificaciones:
                if (cal.get('alumno_id') == alumno_id and 
                    cal.get('tipo_evaluacion_id') == tipo_eval_id):
                    # Cargar la calificación encontrada
                    if alumno_id in self.entries_notas:
                        self.entries_notas[alumno_id].delete(0, tk.END)
                        self.entries_notas[alumno_id].insert(0, str(cal['nota']))
                    if alumno_id in self.entries_observaciones:
                        self.entries_observaciones[alumno_id].delete(0, tk.END)
                        self.entries_observaciones[alumno_id].insert(0, cal.get('observaciones', ''))
                    return
        
        # Si no hay tipo específico, cargar la última calificación de la materia
        else:
            calificaciones = self.cal_manager.obtener_calificaciones_alumno(alumno_id, periodo_id)
            
            # Buscar calificación para esta materia
            for cal in calificaciones:
                if cal.get('materia_id') == materia_id:
                    # Cargar la primera calificación encontrada
                    if alumno_id in self.entries_notas:
                        self.entries_notas[alumno_id].delete(0, tk.END)
                        self.entries_notas[alumno_id].insert(0, str(cal['nota']))
                    if alumno_id in self.entries_observaciones:
                        self.entries_observaciones[alumno_id].delete(0, tk.END)
                        self.entries_observaciones[alumno_id].insert(0, cal.get('observaciones', ''))
                    break
    
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
        calificaciones_guardadas_exitosamente = []
        
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
                        calificaciones_guardadas_exitosamente.append({
                            'alumno_id': alumno_id,
                            'nota': nota,
                            'observaciones': observaciones
                        })
                    else:
                        errores += 1
                else:
                    # Simulación para testing
                    print(f"Guardando: Alumno {alumno_id}, Nota {nota}, Obs: {observaciones}")
                    calificaciones_guardadas += 1
                    calificaciones_guardadas_exitosamente.append({
                        'alumno_id': alumno_id,
                        'nota': nota,
                        'observaciones': observaciones
                    })
                
            except ValueError:
                messagebox.showerror("Error", f"Nota inválida para alumno ID {alumno_id}")
                errores += 1
        
        # Mostrar resultado
        if calificaciones_guardadas > 0:
            mensaje = f"Se guardaron {calificaciones_guardadas} calificaciones"
            if errores > 0:
                mensaje += f" ({errores} errores)"
            messagebox.showinfo("Éxito", mensaje)
            
            # Actualizar la interfaz para mostrar las calificaciones guardadas
            self.actualizar_interfaz_despues_guardar(calificaciones_guardadas_exitosamente)
        else:
            messagebox.showwarning("Advertencia", "No se guardaron calificaciones")
    
    def actualizar_interfaz_despues_guardar(self, calificaciones_guardadas):
        """Actualizar la interfaz después de guardar para mostrar las calificaciones"""
        # Crear un diccionario para acceso rápido a las calificaciones guardadas
        calificaciones_dict = {cal['alumno_id']: cal for cal in calificaciones_guardadas}
        
        # Actualizar los campos de entrada para mostrar las notas guardadas
        for alumno_id, cal_data in calificaciones_dict.items():
            if alumno_id in self.entries_notas:
                # Limpiar y actualizar el campo de nota
                nota_entry = self.entries_notas[alumno_id]
                nota_entry.delete(0, tk.END)
                nota_entry.insert(0, str(cal_data['nota']))
                
                # Cambiar el color de fondo para indicar que fue guardado
                nota_entry.configure(bg="#E8F5E8")  # Verde claro
                
                # Actualizar observaciones
                if alumno_id in self.entries_observaciones:
                    obs_entry = self.entries_observaciones[alumno_id]
                    obs_entry.delete(0, tk.END)
                    obs_entry.insert(0, cal_data['observaciones'])
                    obs_entry.configure(bg="#E8F5E8")  # Verde claro
        
        # Programar que el color vuelva a normal después de 3 segundos
        self.window.after(3000, self.restaurar_colores_normales)
    
    def restaurar_colores_normales(self):
        """Restaurar los colores normales de los campos de entrada"""
        for nota_entry in self.entries_notas.values():
            nota_entry.configure(bg="white")
        
        for obs_entry in self.entries_observaciones.values():
            obs_entry.configure(bg="white")
    
    def ver_promedios(self):
        """Mostrar ventana con promedios de los alumnos"""
        if not self.materia_var.get() or not self.periodo_var.get():
            messagebox.showerror("Error", "Debe seleccionar materia y período")
            return
        
        PromediosWindow(self.window, self.cal_manager, 
                       self.materias_data[self.materia_combo.current()],
                       self.periodos_data[self.periodo_combo.current()])
    
    def exportar_notas(self):
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
            progress_window.configure(bg="lightblue")
            
            tk.Label(progress_window, text="Generando archivo Excel...", 
                    font=("Arial", 12), bg="lightblue").pack(pady=20)
            
            progress_window.update()
            
            # Exportar a Excel
            archivo_generado = self.excel_exporter.exportar_calificaciones_materia(
                materia_id, periodo_id, self.docente_id
            )
            
            progress_window.destroy()
            
            # Mostrar resultado
            resultado = messagebox.askyesno(
                "Exportación Exitosa", 
                f"Archivo generado exitosamente:\n{archivo_generado}\n\n¿Desea abrir la carpeta donde se guardó?"
            )
            
            if resultado:
                import subprocess
                import platform
                
                # Abrir carpeta según el sistema operativo
                if platform.system() == "Windows":
                    subprocess.run(f'explorer /select,"{archivo_generado}"', shell=True)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", "-R", archivo_generado])
                else:  # Linux
                    subprocess.run(["xdg-open", os.path.dirname(archivo_generado)])
        
        except ImportError:
            messagebox.showerror("Error", "La librería openpyxl no está instalada.\nInstale con: pip install openpyxl")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
            print(f"Error detallado: {e}")
    
    def exportar_notas_pdf(self):
        """Exportar notas a archivo PDF"""
        if not self.materia_var.get() or not self.periodo_var.get():
            messagebox.showerror("Error", "Debe seleccionar materia y período para exportar")
            return
        
        # Verificar si ReportLab está disponible
        try:
            from reportlab.lib.pagesizes import letter
            pdf_disponible = True
        except ImportError:
            pdf_disponible = False
        
        if not pdf_disponible:
            self.mostrar_ventana_pdf_no_disponible()
            return
        
        # Verificar que el PDF exporter esté disponible
        if not self.pdf_exporter:
            messagebox.showerror("Error", "PDF Exporter no está disponible")
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
            progress_window.configure(bg="lightcoral")
            
            tk.Label(progress_window, text="Generando archivo PDF...", font=("Arial", 12), bg="lightcoral", fg="white").pack(pady=20)
            
            progress_window.update()
            
            # Exportar a PDF
            archivo_generado = self.pdf_exporter.exportar_calificaciones_materia_pdf(
                materia_id, periodo_id, self.docente_id
            )
            
            progress_window.destroy()
            
            # Mostrar resultado
            resultado = messagebox.askyesno(
                "Exportación Exitosa", 
                f"Archivo PDF generado exitosamente:\n{archivo_generado}\n\n¿Desea abrir la carpeta donde se guardó?"
            )
            
            if resultado:
                import subprocess
                import platform
                
                # Abrir carpeta según el sistema operativo
                if platform.system() == "Windows":
                    subprocess.run(f'explorer /select,"{archivo_generado}"', shell=True)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", "-R", archivo_generado])
                else:  # Linux
                    subprocess.run(["xdg-open", os.path.dirname(archivo_generado)])
        
        except ImportError as e:
            messagebox.showerror("Error", f"La librería reportlab no está instalada.\nInstale con: pip install reportlab\nError: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar PDF: {e}")
            print(f"Error detallado: {e}")
    
    def mostrar_ventana_pdf_no_disponible(self):
        """Mostrar ventana informativa cuando PDF no está disponible"""
        info_window = tk.Toplevel(self.window)
        info_window.title("📄 Exportación PDF")
        info_window.geometry("600x500")
        info_window.configure(bg="#FFF3E0")
        info_window.transient(self.window)
        info_window.grab_set()
        
        # Centrar ventana
        info_window.geometry("+%d+%d" % (
            self.window.winfo_rootx() + 150,
            self.window.winfo_rooty() + 100
        ))
        
        # Título
        tk.Label(info_window, text="📄 Exportación a PDF", 
                font=("Arial", 18, "bold"), bg="#FFF3E0", fg="#E65100").pack(pady=20)
        
        # Mensaje principal
        tk.Label(info_window, text="La librería ReportLab no está instalada", 
                font=("Arial", 14), bg="#FFF3E0", fg="#666").pack(pady=10)
        
        # Frame de opciones
        opciones_frame = tk.LabelFrame(info_window, text="💡 Opciones Disponibles", 
                                      font=("Arial", 14, "bold"), bg="#FFF3E0", fg="#FF9800")
        opciones_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Opción 1: Excel
        excel_frame = tk.Frame(opciones_frame, bg="white", relief=tk.RAISED, bd=2)
        excel_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(excel_frame, text="✅ OPCIÓN RECOMENDADA: Exportar a Excel", 
                 font=("Arial", 12, "bold"), bg="white", fg="#4CAF50").pack(pady=5)
        
        tk.Label(excel_frame, text="Excel funciona perfectamente y es compatible con todos los sistemas", 
                 font=("Arial", 10), bg="white", fg="#666").pack(pady=2)
        
        tk.Button(excel_frame, text="📊 Exportar a Excel Ahora", 
                 font=("Arial", 11, "bold"), bg="#4CAF50", fg="white",
                 command=lambda: [info_window.destroy(), self.exportar_notas()]).pack(pady=10)
        
        # Opción 2: Instalar ReportLab
        install_frame = tk.Frame(opciones_frame, bg="#FFF8E1", relief=tk.RAISED, bd=2)
        install_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(install_frame, text="🔧 OPCIÓN AVANZADA: Instalar ReportLab para PDF", 
                 font=("Arial", 12, "bold"), bg="#FFF8E1", fg="#F57C00").pack(pady=5)
        
        tk.Label(install_frame, text="Ejecuta en tu terminal: pip install reportlab", 
                 font=("Courier", 10), bg="#FFF8E1", fg="#333").pack(pady=2)
        
        # Botón cerrar
        tk.Button(info_window, text="Cerrar", font=("Arial", 12), bg="#666", fg="white",
                 command=info_window.destroy).pack(pady=20)
    
    def ver_alumnos_riesgo(self):
        """Ver alumnos en riesgo académico"""
        if not self.periodo_var.get():
            messagebox.showerror("Error", "Debe seleccionar un período")
            return
        
        periodo_id = self.periodos_data[self.periodo_combo.current()]['id']
        AlumnosRiesgoWindow(self.window, self.cal_manager, periodo_id)

class PromediosWindow:
    """Ventana para mostrar promedios de alumnos"""
    
    def __init__(self, parent, cal_manager, materia, periodo):
        self.parent = parent
        self.cal_manager = cal_manager
        self.materia = materia
        self.periodo = periodo
        self.create_window()
    
    def create_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Promedios - {self.materia['nombre']} - {self.periodo['nombre']}")
        self.window.geometry("800x600")
        self.window.configure(bg="azure4")
        
        # Título
        title = tk.Label(self.window, 
                        text=f"Promedios - {self.materia['nombre']}\n{self.periodo['nombre']}", 
                        font=("Arial", 16, "bold"), bg="azure4", fg="white")
        title.pack(pady=10)
        
        # Tabla de promedios
        tree_frame = tk.Frame(self.window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("Alumno", "Promedio", "Cantidad Notas", "Nota Mínima", "Nota Máxima")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.cargar_promedios()
    
    def cargar_promedios(self):
        """Cargar promedios en la tabla"""
        if DATABASE_AVAILABLE and self.cal_manager:
            # Obtener alumnos del curso
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
                    self.tree.insert("", tk.END, values=(
                        f"{alumno['apellido']}, {alumno['nombre']}",
                        promedio_materia['promedio'],
                        promedio_materia['cantidad_notas'],
                        promedio_materia.get('nota_min', '--'),
                        promedio_materia.get('nota_max', '--')
                    ))
                else:
                    self.tree.insert("", tk.END, values=(
                        f"{alumno['apellido']}, {alumno['nombre']}",
                        "Sin notas", "0", "--", "--"
                    ))
        else:
            # Datos de ejemplo
            ejemplos = [
                ("Pérez, Juan", "8.5", "3", "7.0", "9.0"),
                ("Gómez, Ana", "7.2", "3", "6.5", "8.0"),
                ("Martínez, Carlos", "6.8", "2", "6.0", "7.5")
            ]
            for ejemplo in ejemplos:
                self.tree.insert("", tk.END, values=ejemplo)

class AlumnosRiesgoWindow:
    """Ventana para mostrar alumnos en riesgo académico"""
    
    def __init__(self, parent, cal_manager, periodo_id):
        self.parent = parent
        self.cal_manager = cal_manager
        self.periodo_id = periodo_id
        self.create_window()
    
    def create_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Alumnos en Riesgo Académico")
        self.window.geometry("900x600")
        self.window.configure(bg="#FFEBEE")
        
        # Título
        title = tk.Label(self.window, text="Alumnos en Riesgo Académico", 
                        font=("Arial", 18, "bold"), bg="#FFEBEE", fg="#D32F2F")
        title.pack(pady=10)
        
        # Subtítulo
        subtitle = tk.Label(self.window, text="Alumnos con promedio menor a 6.0", 
                           font=("Arial", 12), bg="#FFEBEE", fg="#666")
        subtitle.pack(pady=5)
        
        # Tabla
        tree_frame = tk.Frame(self.window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        columns = ("Alumno", "Curso", "División", "Promedio General", "Materias Cursadas")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones
        buttons_frame = tk.Frame(self.window, bg="#FFEBEE")
        buttons_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(buttons_frame, text="Enviar Alerta a Preceptores", 
                 bg="#FF5722", fg="white", font=("Arial", 12),
                 command=self.enviar_alerta_preceptores).pack(side=tk.LEFT, padx=10)
        
        tk.Button(buttons_frame, text="Notificar a Padres", 
                 bg="#FF9800", fg="white", font=("Arial", 12),
                 command=self.notificar_padres).pack(side=tk.LEFT, padx=10)
        
        tk.Button(buttons_frame, text="Exportar Reporte", 
                 bg="#9C27B0", fg="white", font=("Arial", 12),
                 command=self.exportar_reporte_riesgo).pack(side=tk.LEFT, padx=10)
        
        self.cargar_alumnos_riesgo()
    
    def cargar_alumnos_riesgo(self):
        """Cargar alumnos en riesgo"""
        if DATABASE_AVAILABLE and self.cal_manager:
            alumnos_riesgo = self.cal_manager.obtener_alumnos_en_riesgo(self.periodo_id)
            
            for alumno in alumnos_riesgo:
                self.tree.insert("", tk.END, values=(
                    alumno['alumno'],
                    alumno['curso'],
                    alumno['division'],
                    alumno['promedio_general'],
                    alumno['materias_cursadas']
                ))
        else:
            # Datos de ejemplo
            ejemplos = [
                ("Martínez, Carlos", "1º Año", "A", "5.8", "5"),
                ("González, Mario", "2º Año", "A", "5.5", "6")
            ]
            for ejemplo in ejemplos:
                self.tree.insert("", tk.END, values=ejemplo)
    
    def enviar_alerta_preceptores(self):
        """Enviar alerta a preceptores"""
        messagebox.showinfo("Alerta Enviada", "Se ha enviado la alerta a los preceptores correspondientes")
    
    def notificar_padres(self):
        """Notificar a padres"""
        messagebox.showinfo("Notificación Enviada", "Se ha notificado a los padres de los alumnos en riesgo")
    
    def exportar_reporte_riesgo(self):
        """Exportar reporte de alumnos en riesgo"""
        messagebox.showinfo("Exportar Reporte", "Funcionalidad de exportación de reporte en desarrollo")

# Función para abrir la ventana desde el módulo de docentes
def abrir_calificaciones_docente(parent, docente_id=2):
    """Función para abrir la ventana de calificaciones desde otros módulos"""
    CalificacionesDocenteWindow(parent, docente_id)

if __name__ == "__main__":
    # Para testing independiente
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    app = CalificacionesDocenteWindow(root)
    root.mainloop()