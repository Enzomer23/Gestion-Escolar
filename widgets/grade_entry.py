"""
Widget Especializado para Entrada de Calificaciones
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import messagebox
from typing import Dict, List, Callable, Optional

class GradeEntryWidget:
    """Widget especializado para entrada de calificaciones"""
    
    def __init__(self, parent, alumnos: List[Dict]):
        self.parent = parent
        self.alumnos = alumnos
        self.entries_notas = {}
        self.entries_observaciones = {}
        self.validation_callback = None
        self.create_widget()
    
    def create_widget(self):
        """Crear el widget de entrada de calificaciones"""
        # Frame principal con scroll
        self.main_frame = tk.Frame(self.parent, bg="white")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas para scroll
        self.canvas = tk.Canvas(self.main_frame, bg="white")
        v_scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        h_scrollbar = tk.Scrollbar(self.main_frame, orient="horizontal", command=self.canvas.xview)
        
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Crear tabla de entrada
        self.create_entry_table()
        
        # Empaquetar
        self.canvas.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
    
    def create_entry_table(self):
        """Crear tabla de entrada de calificaciones"""
        # Encabezados
        headers = ["#", "Alumno", "DNI", "Nota", "Observaciones", "Estado"]
        for i, header in enumerate(headers):
            label = tk.Label(
                self.scrollable_frame, 
                text=header, 
                font=("Arial", 11, "bold"),
                bg="#1976D2", 
                fg="white", 
                relief=tk.RAISED, 
                bd=1
            )
            label.grid(row=0, column=i, sticky="ew", padx=1, pady=1)
        
        # Configurar columnas
        for i in range(len(headers)):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)
        
        # Filas de alumnos
        for row, alumno in enumerate(self.alumnos, start=1):
            self.create_student_row(row, alumno)
    
    def create_student_row(self, row: int, alumno: Dict):
        """Crear fila para un alumno"""
        alumno_id = alumno['id']
        
        # Número de fila
        tk.Label(
            self.scrollable_frame, 
            text=str(row), 
            font=("Arial", 10),
            bg="#E3F2FD", 
            relief=tk.SUNKEN, 
            bd=1
        ).grid(row=row, column=0, sticky="ew", padx=1, pady=1)
        
        # Nombre del alumno
        nombre_completo = f"{alumno['apellido']}, {alumno['nombre']}"
        tk.Label(
            self.scrollable_frame, 
            text=nombre_completo, 
            font=("Arial", 10),
            bg="white", 
            relief=tk.SUNKEN, 
            bd=1
        ).grid(row=row, column=1, sticky="ew", padx=1, pady=1)
        
        # DNI
        dni = alumno.get('dni', 'N/A')
        tk.Label(
            self.scrollable_frame, 
            text=dni, 
            font=("Arial", 10),
            bg="white", 
            relief=tk.SUNKEN, 
            bd=1
        ).grid(row=row, column=2, sticky="ew", padx=1, pady=1)
        
        # Entry para nota con validación
        nota_entry = tk.Entry(
            self.scrollable_frame, 
            font=("Arial", 10), 
            width=8, 
            justify="center"
        )
        nota_entry.bind('<FocusOut>', lambda e, aid=alumno_id: self.validate_grade(aid))
        nota_entry.bind('<KeyRelease>', lambda e, aid=alumno_id: self.on_grade_change(aid))
        nota_entry.grid(row=row, column=3, padx=2, pady=1)
        self.entries_notas[alumno_id] = nota_entry
        
        # Entry para observaciones
        obs_entry = tk.Entry(
            self.scrollable_frame, 
            font=("Arial", 10), 
            width=30
        )
        obs_entry.grid(row=row, column=4, padx=2, pady=1)
        self.entries_observaciones[alumno_id] = obs_entry
        
        # Estado actual
        estado_label = tk.Label(
            self.scrollable_frame, 
            text="--", 
            font=("Arial", 9),
            bg="#F5F5F5", 
            relief=tk.SUNKEN, 
            bd=1
        )
        estado_label.grid(row=row, column=5, sticky="ew", padx=1, pady=1)
    
    def validate_grade(self, alumno_id: int):
        """Validar nota ingresada"""
        entry = self.entries_notas[alumno_id]
        nota_text = entry.get().strip()
        
        if nota_text:
            try:
                nota = float(nota_text)
                if nota < 1.0 or nota > 10.0:
                    entry.config(bg="#FFCDD2")  # Rojo claro para error
                    messagebox.showerror("Error", "La nota debe estar entre 1.0 y 10.0")
                    entry.focus()
                    return False
                else:
                    entry.config(bg="white")  # Blanco para válido
                    return True
            except ValueError:
                entry.config(bg="#FFCDD2")  # Rojo claro para error
                messagebox.showerror("Error", "Ingrese un número válido")
                entry.focus()
                return False
        else:
            entry.config(bg="white")
            return True
    
    def on_grade_change(self, alumno_id: int):
        """Evento cuando cambia una nota"""
        if self.validation_callback:
            self.validation_callback(alumno_id)
    
    def get_all_grades(self) -> Dict[int, Dict]:
        """Obtener todas las calificaciones ingresadas"""
        grades = {}
        for alumno_id, nota_entry in self.entries_notas.items():
            nota_text = nota_entry.get().strip()
            if nota_text:
                try:
                    nota = float(nota_text)
                    if 1.0 <= nota <= 10.0:
                        observaciones = self.entries_observaciones[alumno_id].get().strip()
                        grades[alumno_id] = {
                            'nota': nota,
                            'observaciones': observaciones
                        }
                except ValueError:
                    continue
        return grades
    
    def clear_all(self):
        """Limpiar todas las entradas"""
        for entry in self.entries_notas.values():
            entry.delete(0, tk.END)
            entry.config(bg="white")
        
        for entry in self.entries_observaciones.values():
            entry.delete(0, tk.END)
    
    def set_validation_callback(self, callback: Callable):
        """Establecer callback para validación"""
        self.validation_callback = callback
    
    def highlight_student(self, alumno_id: int, color: str = "#FFF3E0"):
        """Resaltar fila de un estudiante específico"""
        # Implementar resaltado visual si es necesario
        pass