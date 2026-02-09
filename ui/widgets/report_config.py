"""
Widget de Configuración de Reportes
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Callable, Optional

class ReportConfigWidget:
    """Widget especializado para configuración de reportes"""
    
    def __init__(self, parent, title: str = "⚙️ Configuración de Reporte"):
        self.parent = parent
        self.title = title
        self.config_vars = {}
        self.generate_callback = None
        self.create_widget()
    
    def create_widget(self):
        """Crear el widget de configuración"""
        self.config_frame = tk.LabelFrame(
            self.parent, 
            text=self.title, 
            font=("Arial", 12, "bold"), 
            bg="lightblue", 
            fg="darkblue"
        )
        self.config_frame.pack(fill=tk.X, padx=20, pady=10)
    
    def add_combo_option(self, label: str, key: str, values: List[str], 
                        default: str = "", row: int = 0, column: int = 0):
        """Agregar opción de combobox"""
        tk.Label(
            self.config_frame, 
            text=f"{label}:", 
            font=("Arial", 10, "bold"), 
            bg="lightblue"
        ).grid(row=row, column=column*2, padx=10, pady=5, sticky="w")
        
        combo = ttk.Combobox(
            self.config_frame, 
            values=values, 
            state="readonly", 
            width=25
        )
        if default and default in values:
            combo.set(default)
        elif values:
            combo.set(values[0])
        
        combo.grid(row=row, column=column*2+1, padx=10, pady=5)
        self.config_vars[key] = combo
        return combo
    
    def add_checkbox_group(self, label: str, key: str, options: List[tuple], 
                          row: int = 0, column: int = 0):
        """Agregar grupo de checkboxes"""
        tk.Label(
            self.config_frame, 
            text=f"{label}:", 
            font=("Arial", 10, "bold"), 
            bg="lightblue"
        ).grid(row=row, column=column*2, padx=10, pady=5, sticky="nw")
        
        checkbox_frame = tk.Frame(self.config_frame, bg="lightblue")
        checkbox_frame.grid(row=row, column=column*2+1, padx=10, pady=5, sticky="w")
        
        checkbox_vars = {}
        for i, (option_text, default_value) in enumerate(options):
            var = tk.BooleanVar(value=default_value)
            checkbox = tk.Checkbutton(
                checkbox_frame, 
                text=option_text, 
                variable=var, 
                bg="lightblue"
            )
            checkbox.grid(row=i//2, column=i%2, sticky="w", padx=5, pady=2)
            checkbox_vars[option_text] = var
        
        self.config_vars[key] = checkbox_vars
        return checkbox_vars
    
    def add_text_option(self, label: str, key: str, default: str = "", 
                       row: int = 0, column: int = 0, width: int = 25):
        """Agregar opción de texto"""
        tk.Label(
            self.config_frame, 
            text=f"{label}:", 
            font=("Arial", 10, "bold"), 
            bg="lightblue"
        ).grid(row=row, column=column*2, padx=10, pady=5, sticky="w")
        
        entry = tk.Entry(self.config_frame, width=width)
        entry.insert(0, default)
        entry.grid(row=row, column=column*2+1, padx=10, pady=5)
        
        self.config_vars[key] = entry
        return entry
    
    def add_generate_button(self, text: str = "📊 Generar Reporte", 
                           row: int = 10, column: int = 0, columnspan: int = 4):
        """Agregar botón de generar"""
        button_frame = tk.Frame(self.config_frame, bg="lightblue")
        button_frame.grid(row=row, column=column, columnspan=columnspan, pady=15)
        
        generate_btn = tk.Button(
            button_frame, 
            text=text, 
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 10), 
            width=18,
            command=self._execute_generate
        )
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        preview_btn = tk.Button(
            button_frame, 
            text="👁️ Vista Previa", 
            bg="#2196F3", 
            fg="white", 
            font=("Arial", 10), 
            width=15,
            command=self._show_preview
        )
        preview_btn.pack(side=tk.LEFT, padx=5)
        
        return generate_btn, preview_btn
    
    def get_configuration(self) -> Dict:
        """Obtener configuración actual"""
        config = {}
        for key, widget in self.config_vars.items():
            if isinstance(widget, tk.Entry):
                config[key] = widget.get()
            elif isinstance(widget, ttk.Combobox):
                config[key] = widget.get()
            elif isinstance(widget, dict):  # Grupo de checkboxes
                config[key] = {
                    option: var.get() 
                    for option, var in widget.items()
                }
        return config
    
    def set_generate_callback(self, callback: Callable):
        """Establecer callback para generar reporte"""
        self.generate_callback = callback
    
    def _execute_generate(self):
        """Ejecutar generación de reporte"""
        if self.generate_callback:
            config = self.get_configuration()
            self.generate_callback(config)
    
    def _show_preview(self):
        """Mostrar vista previa del reporte"""
        from tkinter import messagebox
        config = self.get_configuration()
        messagebox.showinfo(
            "Vista Previa", 
            f"👁️ Vista previa del reporte:\n"
            f"• Configuración: {len(config)} opciones\n"
            f"• Formato: {config.get('formato', 'No especificado')}\n"
            f"• Listo para generar"
        )