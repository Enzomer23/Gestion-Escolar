"""
Panel de Métricas Reutilizable
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from typing import List, Tuple

class MetricsPanel:
    """Panel reutilizable para mostrar métricas"""
    
    def __init__(self, parent, title: str, bg_color: str = "lightcyan"):
        self.parent = parent
        self.title = title
        self.bg_color = bg_color
        self.metrics_frame = None
        self.create_panel()
    
    def create_panel(self):
        """Crear el panel de métricas"""
        self.metrics_frame = tk.LabelFrame(
            self.parent, 
            text=self.title, 
            font=("Arial", 12, "bold"), 
            bg=self.bg_color, 
            fg="darkcyan", 
            padx=10, 
            pady=8
        )
        self.metrics_frame.pack(fill=tk.X, pady=(0, 15))
    
    def add_metrics(self, metrics_data: List[Tuple[str, str, str, str]]):
        """Agregar métricas al panel"""
        for i, (label, value, color, info) in enumerate(metrics_data):
            metric_frame = tk.Frame(self.metrics_frame, bg="white", relief=tk.RAISED, bd=2)
            metric_frame.grid(row=0, column=i, padx=8, pady=5, sticky="ew")
            
            tk.Label(metric_frame, text=label, font=("Arial", 9, "bold"), bg="white").pack()
            tk.Label(metric_frame, text=value, font=("Arial", 16, "bold"), 
                    bg="white", fg=color).pack()
            tk.Label(metric_frame, text=info, font=("Arial", 8), 
                    bg="white", fg="gray").pack()
        
        # Configurar columnas
        for i in range(len(metrics_data)):
            self.metrics_frame.grid_columnconfigure(i, weight=1)
    
    def update_metric(self, index: int, new_value: str, new_color: str = None):
        """Actualizar una métrica específica"""
        # Implementar actualización dinámica si es necesario
        pass