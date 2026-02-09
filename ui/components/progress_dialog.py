"""
Diálogo de Progreso Reutilizable
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import ttk

class ProgressDialog:
    """Diálogo reutilizable para mostrar progreso de operaciones"""
    
    def __init__(self, parent, title: str = "Procesando...", message: str = "Por favor espere..."):
        self.parent = parent
        self.title = title
        self.message = message
        self.window = None
        self.progress_bar = None
        self.label = None
        self.create_dialog()
    
    def create_dialog(self):
        """Crear el diálogo de progreso"""
        self.window = tk.Toplevel(self.parent)
        self.window.title(self.title)
        self.window.geometry("400x150")
        self.window.configure(bg="lightblue")
        
        # Centrar ventana
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Mensaje
        self.label = tk.Label(
            self.window, 
            text=self.message, 
            font=("Arial", 12), 
            bg="lightblue"
        )
        self.label.pack(pady=20)
        
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(
            self.window, 
            length=300, 
            mode='indeterminate'
        )
        self.progress_bar.pack(pady=10)
        self.progress_bar.start()
    
    def update_message(self, new_message: str):
        """Actualizar mensaje del diálogo"""
        if self.label:
            self.label.config(text=new_message)
            self.window.update()
    
    def set_determinate(self, maximum: int = 100):
        """Cambiar a modo determinado"""
        if self.progress_bar:
            self.progress_bar.stop()
            self.progress_bar.config(mode='determinate', maximum=maximum)
    
    def update_progress(self, value: int):
        """Actualizar progreso (solo en modo determinado)"""
        if self.progress_bar:
            self.progress_bar['value'] = value
            self.window.update()
    
    def close(self):
        """Cerrar el diálogo"""
        if self.window:
            self.window.destroy()
    
    def auto_close(self, delay_ms: int = 3000):
        """Cerrar automáticamente después de un delay"""
        if self.window:
            self.window.after(delay_ms, self.close)