"""
Widget Selector de Estudiantes
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Callable, Optional

class StudentSelectorWidget:
    """Widget especializado para selección de estudiantes"""
    
    def __init__(self, parent, title: str = "👤 Seleccionar Estudiante"):
        self.parent = parent
        self.title = title
        self.alumnos_data = []
        self.selection_callback = None
        self.create_widget()
    
    def create_widget(self):
        """Crear el widget selector"""
        self.selector_frame = tk.LabelFrame(
            self.parent, 
            text=self.title, 
            font=("Arial", 12, "bold"), 
            bg="white", 
            fg="darkblue"
        )
        self.selector_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Búsqueda rápida
        search_frame = tk.Frame(self.selector_frame, bg="white")
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(search_frame, text="🔍 Buscar:", font=("Arial", 10), bg="white").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search_change)
        
        # Combobox de selección
        tk.Label(self.selector_frame, text="Estudiante:", font=("Arial", 10, "bold"), bg="white").pack(pady=5)
        self.alumno_combo = ttk.Combobox(self.selector_frame, state="readonly", width=50)
        self.alumno_combo.pack(pady=5)
        self.alumno_combo.bind("<<ComboboxSelected>>", self.on_selection_change)
        
        # Información del estudiante seleccionado
        self.info_frame = tk.Frame(self.selector_frame, bg="#F5F5F5", relief=tk.SUNKEN, bd=2)
        self.info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.info_label = tk.Label(
            self.info_frame, 
            text="Seleccione un estudiante para ver su información", 
            font=("Arial", 10), 
            bg="#F5F5F5", 
            fg="gray"
        )
        self.info_label.pack(pady=10)
    
    def load_students(self, alumnos: List[Dict]):
        """Cargar lista de estudiantes"""
        self.alumnos_data = alumnos
        self.update_combo_values()
    
    def update_combo_values(self, filter_text: str = ""):
        """Actualizar valores del combobox con filtro opcional"""
        if filter_text:
            filtered_alumnos = [
                alumno for alumno in self.alumnos_data
                if filter_text.lower() in f"{alumno['apellido']}, {alumno['nombre']}".lower()
                or filter_text.lower() in alumno.get('dni', '').lower()
                or filter_text.lower() in alumno.get('curso', '').lower()
            ]
        else:
            filtered_alumnos = self.alumnos_data
        
        alumno_values = [
            f"{a['apellido']}, {a['nombre']} ({a['curso']} {a['division']}) - DNI: {a.get('dni', 'N/A')}"
            for a in filtered_alumnos
        ]
        
        self.alumno_combo['values'] = alumno_values
        self.filtered_alumnos = filtered_alumnos
    
    def on_search_change(self, event=None):
        """Evento cuando cambia el texto de búsqueda"""
        search_text = self.search_entry.get()
        self.update_combo_values(search_text)
    
    def on_selection_change(self, event=None):
        """Evento cuando cambia la selección"""
        index = self.alumno_combo.current()
        if index >= 0 and hasattr(self, 'filtered_alumnos'):
            alumno_seleccionado = self.filtered_alumnos[index]
            self.update_student_info(alumno_seleccionado)
            
            if self.selection_callback:
                self.selection_callback(alumno_seleccionado)
    
    def update_student_info(self, alumno: Dict):
        """Actualizar información del estudiante seleccionado"""
        info_text = f"""
👤 {alumno['apellido']}, {alumno['nombre']}
🎓 Curso: {alumno['curso']} - División {alumno['division']}
🆔 DNI: {alumno.get('dni', 'No especificado')}
📅 Fecha de Nacimiento: {alumno.get('fecha_nacimiento', 'No especificada')}
        """.strip()
        
        self.info_label.config(text=info_text, fg="darkblue", justify=tk.LEFT)
    
    def get_selected_student(self) -> Optional[Dict]:
        """Obtener estudiante seleccionado"""
        index = self.alumno_combo.current()
        if index >= 0 and hasattr(self, 'filtered_alumnos'):
            return self.filtered_alumnos[index]
        return None
    
    def set_selection_callback(self, callback: Callable):
        """Establecer callback para cuando cambia la selección"""
        self.selection_callback = callback
    
    def clear_selection(self):
        """Limpiar selección"""
        self.alumno_combo.set("")
        self.search_entry.delete(0, tk.END)
        self.info_label.config(
            text="Seleccione un estudiante para ver su información", 
            fg="gray"
        )