"""
Componente de Tabla de Datos Reutilizable
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Optional, Callable

class DataTable:
    """Componente reutilizable para mostrar datos en tabla"""
    
    def __init__(self, parent, columns: List[str], data: List[Dict] = None):
        self.parent = parent
        self.columns = columns
        self.data = data or []
        self.tree = None
        self.create_table()
    
    def create_table(self):
        """Crear la tabla con scrollbars"""
        # Frame contenedor
        self.table_frame = tk.Frame(self.parent)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview con scrollbars
        self.tree = ttk.Treeview(self.table_frame, columns=self.columns, show="headings")
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Configurar columnas
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        
        # Empaquetar
        self.tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Cargar datos si existen
        if self.data:
            self.load_data(self.data)
    
    def load_data(self, data: List[Dict]):
        """Cargar datos en la tabla"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insertar nuevos datos
        for row_data in data:
            values = [row_data.get(col, '') for col in self.columns]
            self.tree.insert("", tk.END, values=values)
    
    def add_row(self, row_data: Dict):
        """Agregar una fila a la tabla"""
        values = [row_data.get(col, '') for col in self.columns]
        self.tree.insert("", tk.END, values=values)
    
    def get_selected_item(self) -> Optional[Dict]:
        """Obtener el item seleccionado"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']
            return {col: values[i] for i, col in enumerate(self.columns)}
        return None
    
    def configure_column(self, column: str, width: int = None, anchor: str = None):
        """Configurar una columna específica"""
        if width:
            self.tree.column(column, width=width)
        if anchor:
            self.tree.column(column, anchor=anchor)
    
    def add_tag_config(self, tag: str, **kwargs):
        """Agregar configuración de tag para colorear filas"""
        self.tree.tag_configure(tag, **kwargs)
    
    def bind_double_click(self, callback: Callable):
        """Vincular evento de doble click"""
        self.tree.bind("<Double-1>", callback)