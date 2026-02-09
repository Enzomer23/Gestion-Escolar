"""
Registro de Calificaciones
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
    from server.email_notifier import notificar_notas_subidas
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class RegistroCalificacionesWindow:
    """Ventana para registro de calificaciones"""
    
    def __init__(self, parent, cal_manager, docente_id=2):
        self.parent = parent
        self.cal_manager = cal_manager
        self.docente_id = docente_id
        self.create_window()

    def create_window(self):
        """Crear ventana principal de registro"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📝 Registro de Calificaciones")
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
        title = tk.Label(scrollable_frame, text="📝 Registro de Calificaciones", 
                        font=("Arial", 18, "bold"), bg="lightcyan", fg="darkcyan")
        title.pack(pady=15)

        # Panel de controles
        self.create_controls_panel(scrollable_frame)
        
        # Panel de registro
        self.create_registro_panel(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Cargar datos iniciales
        self.cargar_datos_iniciales()

    def create_controls_panel(self, parent):
        """Crear panel de controles"""
        controls_frame = tk.LabelFrame(parent, text="⚙️ Configuración de Registro", 
                                      font=("Arial", 12, "bold"), bg="lightcyan", 
                                      fg="darkcyan", padx=10, pady=8)
        controls_frame.pack(fill=tk.X, pady=(0, 15))

        # Selección de materia
        tk.Label(controls_frame, text="Materia:", font=("Arial", 10, "bold"), bg="lightcyan").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.materia_var = tk.StringVar()
        self.materia_combo = ttk.Combobox(controls_frame, textvariable=self.materia_var, state="readonly", width=25)
        self.materia_combo.grid(row=0, column=1, padx=5, pady=5)
        self.materia_combo.bind("<<ComboboxSelected>>", self.on_materia_selected)

        # Selección de período
        tk.Label(controls_frame, text="Período:", font=("Arial", 10, "bold"), bg="lightcyan").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.periodo_var = tk.StringVar()
        self.periodo_combo = ttk.Combobox(controls_frame, textvariable=self.periodo_var, state="readonly", width=20)
        self.periodo_combo.grid(row=0, column=3, padx=5, pady=5)
        self.periodo_combo.bind("<<ComboboxSelected>>", self.on_periodo_selected)

        # Selección de tipo de evaluación
        tk.Label(controls_frame, text="Tipo Evaluación:", font=("Arial", 10, "bold"), bg="lightcyan").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.tipo_eval_var = tk.StringVar()
        self.tipo_eval_combo = ttk.Combobox(controls_frame, textvariable=self.tipo_eval_var, state="readonly", width=25)
        self.tipo_eval_combo.grid(row=1, column=1, padx=5, pady=5)

        # Fecha de evaluación
        tk.Label(controls_frame, text="Fecha Evaluación:", font=("Arial", 10, "bold"), bg="lightcyan").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.fecha_entry = tk.Entry(controls_frame, width=12)
        self.fecha_entry.grid(row=1, column=3, padx=5, pady=5)
        self.fecha_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # Botón actualizar
        tk.Button(controls_frame, text="🔄 Cargar Alumnos", command=self.cargar_alumnos, 
                 bg="#4CAF50", fg="white", font=("Arial", 10)).grid(row=0, column=4, padx=10, pady=5)

    def create_registro_panel(self, parent):
        """Crear panel de registro de calificaciones"""
        self.registro_frame = tk.LabelFrame(parent, text="👥 Lista de Alumnos para Calificar", 
                                           font=("Arial", 12, "bold"), bg="lightcyan", 
                                           fg="darkcyan", padx=10, pady=8)
        self.registro_frame.pack(fill=tk.BOTH, expand=True)

        # Inicializar variables para entries
        self.entries_notas = {}
        self.entries_observaciones = {}

        # Mensaje inicial
        tk.Label(self.registro_frame, text="Seleccione materia y período para cargar alumnos", 
                font=("Arial", 12), bg="lightcyan", fg="gray").pack(pady=50)

        # Botones de acción
        buttons_frame = tk.Frame(parent, bg="lightcyan")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="💾 Guardar Calificaciones", command=self.guardar_calificaciones,
                 bg="#2196F3", fg="white", font=("Arial", 12), width=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="📧 Enviar Notificaciones", command=self.enviar_notificaciones,
                 bg="#FF9800", fg="white", font=("Arial", 12), width=20).pack(side=tk.LEFT, padx=5)
        
        tk.Button(buttons_frame, text="🔄 Limpiar Formulario", command=self.limpiar_formulario,
                 bg="#9C27B0", fg="white", font=("Arial", 12), width=18).pack(side=tk.LEFT, padx=5)

    def cargar_datos_iniciales(self):
        """Cargar datos iniciales desde la base de datos"""
        if not DATABASE_AVAILABLE or not self.cal_manager:
            return

        try:
            # Cargar materias del docente
            materias = self.cal_manager.obtener_materias_por_docente(self.docente_id)
            materia_values = [f"{m['nombre']} ({m['curso']} {m['division']})" for m in materias]
            self.materia_combo['values'] = materia_values
            self.materias_data = materias

            # Cargar períodos
            periodos = self.cal_manager.obtener_periodos_activos()
            periodo_values = [p['nombre'] for p in periodos]
            self.periodo_combo['values'] = periodo_values
            self.periodos_data = periodos

            # Cargar tipos de evaluación
            tipos = self.cal_manager.obtener_tipos_evaluacion()
            tipo_values = [f"{t['nombre']} ({t['peso_porcentual']}%)" for t in tipos]
            self.tipo_eval_combo['values'] = tipo_values
            self.tipos_eval_data = tipos

        except Exception as e:
            print(f"Error cargando datos iniciales: {e}")

    def on_materia_selected(self, event=None):
        """Evento cuando se selecciona una materia"""
        if self.periodo_var.get():
            self.cargar_alumnos()

    def on_periodo_selected(self, event=None):
        """Evento cuando se selecciona un período"""
        if self.materia_var.get():
            self.cargar_alumnos()

    def cargar_alumnos(self):
        """Cargar lista de alumnos para calificar"""
        if not self.materia_var.get() or not self.periodo_var.get():
            return

        # Obtener materia seleccionada
        materia_index = self.materia_combo.current()
        if materia_index < 0:
            return

        materia_seleccionada = self.materias_data[materia_index]

        # Limpiar frame de registro
        for widget in self.registro_frame.winfo_children():
            widget.destroy()

        # Obtener alumnos del curso
        if DATABASE_AVAILABLE and self.cal_manager:
            alumnos = self.cal_manager.obtener_alumnos_por_curso(
                materia_seleccionada['curso'], 
                materia_seleccionada['division']
            )
        else:
            alumnos = []

        if not alumnos:
            tk.Label(self.registro_frame, text="No se encontraron alumnos para este curso", 
                    font=("Arial", 12), bg="lightcyan", fg="red").pack(pady=50)
            return

        # Crear tabla de calificaciones
        self.crear_tabla_calificaciones(alumnos)

    def crear_tabla_calificaciones(self, alumnos):
        """Crear tabla para registro de calificaciones"""
        # Frame con scroll para la tabla
        table_frame = tk.Frame(self.registro_frame, bg="lightcyan")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Canvas para scroll horizontal y vertical
        canvas = tk.Canvas(table_frame, bg="white")
        v_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient="horizontal", command=canvas.xview)
        
        scrollable_table = tk.Frame(canvas, bg="white")
        
        scrollable_table.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_table, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Encabezados
        headers = ["#", "Alumno", "DNI", "Nota", "Observaciones", "Estado Actual"]
        for i, header in enumerate(headers):
            label = tk.Label(scrollable_table, text=header, font=("Arial", 11, "bold"),
                           bg="#1976D2", fg="white", relief=tk.RAISED, bd=1)
            label.grid(row=0, column=i, sticky="ew", padx=1, pady=1)

        # Configurar columnas
        for i in range(len(headers)):
            scrollable_table.grid_columnconfigure(i, weight=1)

        # Reinicializar diccionarios
        self.entries_notas = {}
        self.entries_observaciones = {}

        # Filas de alumnos
        for row, alumno in enumerate(alumnos, start=1):
            alumno_id = alumno['id']
            
            # Número de fila
            tk.Label(scrollable_table, text=str(row), font=("Arial", 10),
                    bg="#E3F2FD", relief=tk.SUNKEN, bd=1).grid(row=row, column=0, sticky="ew", padx=1, pady=1)
            
            # Nombre del alumno
            nombre_completo = f"{alumno['apellido']}, {alumno['nombre']}"
            tk.Label(scrollable_table, text=nombre_completo, font=("Arial", 10),
                    bg="white", relief=tk.SUNKEN, bd=1).grid(row=row, column=1, sticky="ew", padx=1, pady=1)
            
            # DNI
            dni = alumno.get('dni', 'N/A')
            tk.Label(scrollable_table, text=dni, font=("Arial", 10),
                    bg="white", relief=tk.SUNKEN, bd=1).grid(row=row, column=2, sticky="ew", padx=1, pady=1)
            
            # Entry para nota
            nota_entry = tk.Entry(scrollable_table, font=("Arial", 10), width=8, justify="center")
            nota_entry.grid(row=row, column=3, padx=2, pady=1)
            self.entries_notas[alumno_id] = nota_entry
            
            # Entry para observaciones
            obs_entry = tk.Entry(scrollable_table, font=("Arial", 10), width=30)
            obs_entry.grid(row=row, column=4, padx=2, pady=1)
            self.entries_observaciones[alumno_id] = obs_entry
            
            # Estado actual (promedio si existe)
            estado_text = self.obtener_estado_alumno(alumno_id)
            estado_label = tk.Label(scrollable_table, text=estado_text, font=("Arial", 9),
                                   bg="#F5F5F5", relief=tk.SUNKEN, bd=1)
            estado_label.grid(row=row, column=5, sticky="ew", padx=1, pady=1)

        # Empaquetar canvas y scrollbars
        canvas.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

    def obtener_estado_alumno(self, alumno_id):
        """Obtener estado académico actual del alumno"""
        if not DATABASE_AVAILABLE or not self.cal_manager:
            return "Sin datos"

        try:
            # Obtener período actual
            if hasattr(self, 'periodos_data') and self.periodo_combo.current() >= 0:
                periodo_id = self.periodos_data[self.periodo_combo.current()]['id']
                promedio = self.cal_manager.obtener_promedio_general_alumno(alumno_id, periodo_id)
                
                if promedio > 0:
                    if promedio >= 9.0:
                        return f"🏆 {promedio:.1f}"
                    elif promedio >= 8.0:
                        return f"✅ {promedio:.1f}"
                    elif promedio >= 7.0:
                        return f"👍 {promedio:.1f}"
                    elif promedio >= 6.0:
                        return f"⚠️ {promedio:.1f}"
                    else:
                        return f"🚨 {promedio:.1f}"
                else:
                    return "Sin calif."
            else:
                return "Sin período"
        except Exception as e:
            return "Error"

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
                    calificaciones_guardadas += 1

            except ValueError:
                messagebox.showerror("Error", f"Nota inválida para alumno ID {alumno_id}")
                errores += 1

        # Mostrar resultado
        if calificaciones_guardadas > 0:
            mensaje = f"✅ Se guardaron {calificaciones_guardadas} calificaciones"
            if errores > 0:
                mensaje += f"\n❌ {errores} errores encontrados"
            messagebox.showinfo("Calificaciones Guardadas", mensaje)
            
            # Limpiar formulario después de guardar
            self.limpiar_formulario()
        else:
            messagebox.showwarning("Advertencia", "No se guardaron calificaciones")

    def enviar_notificaciones(self):
        """Enviar notificaciones a preceptores y padres"""
        if not self.materia_var.get() or not self.periodo_var.get():
            messagebox.showerror("Error", "Debe seleccionar materia y período")
            return

        try:
            materia_seleccionada = self.materias_data[self.materia_combo.current()]
            periodo_seleccionado = self.periodos_data[self.periodo_combo.current()]

            if DATABASE_AVAILABLE:
                success = notificar_notas_subidas(
                    "Prof. Docente",
                    materia_seleccionada['nombre'],
                    materia_seleccionada['curso'],
                    materia_seleccionada['division'],
                    periodo_seleccionado['nombre']
                )
                if success:
                    messagebox.showinfo("Notificaciones Enviadas", 
                        "📧 Notificaciones enviadas exitosamente a:\n"
                        "• Preceptores del curso\n"
                        "• Padres de los alumnos\n"
                        "• Sistema de seguimiento académico")
            else:
                messagebox.showinfo("Notificaciones Enviadas", 
                    "📧 Simulación: Notificaciones enviadas a preceptores y padres")

        except Exception as e:
            messagebox.showerror("Error", f"Error al enviar notificaciones: {e}")

    def limpiar_formulario(self):
        """Limpiar todas las notas y observaciones"""
        for entry in self.entries_notas.values():
            entry.delete(0, tk.END)
        
        for entry in self.entries_observaciones.values():
            entry.delete(0, tk.END)

        messagebox.showinfo("Formulario Limpiado", "✅ Todas las notas y observaciones han sido limpiadas")