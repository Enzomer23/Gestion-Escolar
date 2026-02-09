"""
Panel de Filtros Reutilizable
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Callable, Optional

class FilterPanel:
    """Panel reutilizable para filtros de búsqueda"""
    
    def __init__(self, parent, title: str = "🔍 Filtros", bg_color: str = "lightcyan"):
        self.parent = parent
        self.title = title
        self.bg_color = bg_color
        self.filters = {}
        self.filter_frame = None
        self.callback = None
        self.create_panel()
    
    def create_panel(self):
        """Crear el panel de filtros"""
        self.filter_frame = tk.LabelFrame(
            self.parent, 
            text=self.title, 
            font=("Arial", 12, "bold"), 
            bg=self.bg_color, 
            fg="darkcyan", 
            padx=10, 
            pady=8
        )
        self.filter_frame.pack(fill=tk.X, pady=(0, 15))
    
    def add_text_filter(self, label: str, key: str, row: int = 0, column: int = 0, 
                       width: int = 20, default: str = ""):
        """Agregar filtro de texto"""
        tk.Label(self.filter_frame, text=f"{label}:", font=("Arial", 10), 
                bg=self.bg_color).grid(row=row, column=column*2, padx=5, pady=5, sticky="w")
        
        entry = tk.Entry(self.filter_frame, width=width)
        entry.insert(0, default)
        entry.grid(row=row, column=column*2+1, padx=5, pady=5)
        
        self.filters[key] = entry
        return entry
    
    def add_combo_filter(self, label: str, key: str, values: List[str], 
                        row: int = 0, column: int = 0, width: int = 15, default: str = ""):
        """Agregar filtro de combobox"""
        tk.Label(self.filter_frame, text=f"{label}:", font=("Arial", 10), 
                bg=self.bg_color).grid(row=row, column=column*2, padx=5, pady=5, sticky="w")
        
        combo = ttk.Combobox(self.filter_frame, values=values, state="readonly", width=width)
        if default and default in values:
            combo.set(default)
        elif values:
            combo.set(values[0])
        combo.grid(row=row, column=column*2+1, padx=5, pady=5)
        
        self.filters[key] = combo
        return combo
    
    def add_search_button(self, row: int = 0, column: int = 3, text: str = "🔍 Buscar"):
        """Agregar botón de búsqueda"""
        search_btn = tk.Button(
            self.filter_frame, 
            text=text, 
            bg="#2196F3", 
            fg="white", 
            font=("Arial", 10), 
            width=12,
            command=self._execute_search
        )
        search_btn.grid(row=row, column=column*2, padx=10, pady=5)
        return search_btn
    
    def add_clear_button(self, row: int = 0, column: int = 4, text: str = "🗑️ Limpiar"):
        """Agregar botón de limpiar filtros"""
        clear_btn = tk.Button(
            self.filter_frame, 
            text=text, 
            bg="#FF5722", 
            fg="white", 
            font=("Arial", 10), 
            width=12,
            command=self.clear_filters
        )
        clear_btn.grid(row=row, column=column*2, padx=5, pady=5)
        return clear_btn
    
    def get_filter_values(self) -> Dict:
        """Obtener valores actuales de todos los filtros"""
        values = {}
        for key, widget in self.filters.items():
            if isinstance(widget, tk.Entry):
                values[key] = widget.get()
            elif isinstance(widget, ttk.Combobox):
                values[key] = widget.get()
        return values
    
    def clear_filters(self):
        """Limpiar todos los filtros"""
        for widget in self.filters.values():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                if widget['values']:
                    widget.set(widget['values'][0])
    
    def set_search_callback(self, callback: Callable):
        """Establecer callback para búsqueda"""
        self.callback = callback
    
    def _execute_search(self):
        """Ejecutar búsqueda si hay callback"""
        if self.callback:
            filter_values = self.get_filter_values()
            self.callback(filter_values)