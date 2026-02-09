"""
Finanzas y Presupuesto para Administradores
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

class FinanzasWindow:
    """Ventana para gestión financiera y presupuestaria"""
    
    def __init__(self, parent, estadisticas_data):
        self.parent = parent
        self.estadisticas_data = estadisticas_data
        self.create_window()

    def create_window(self):
        """Crear ventana principal de finanzas"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("💰 Finanzas y Presupuesto")
        self.window.geometry("1340x720")
        self.window.configure(bg="lightsteelblue")

        # Frame principal con scroll
        main_frame = tk.Frame(self.window, bg="lightsteelblue")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg="lightsteelblue")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="lightsteelblue")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Título
        title = tk.Label(scrollable_frame, text="💰 Gestión Financiera y Presupuestaria", 
                        font=("Arial", 18, "bold"), bg="lightsteelblue", fg="darkblue")
        title.pack(pady=15)

        # Panel de métricas financieras
        self.create_financial_metrics(scrollable_frame)
        
        # Notebook con pestañas
        self.create_notebook(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_financial_metrics(self, parent):
        """Crear métricas financieras"""
        metrics_frame = tk.LabelFrame(parent, text="💰 Métricas Financieras", 
                                     font=("Arial", 12, "bold"), bg="lightsteelblue", 
                                     fg="darkblue", padx=10, pady=8)
        metrics_frame.pack(fill=tk.X, pady=(0, 15))

        metrics_data = [
            ("💰 Presupuesto Anual", "$2.5M", "green", "Aprobado"),
            ("📊 Ejecutado", "67%", "green", "En tiempo"),
            ("💳 Gastos Mes", "$180K", "orange", "↗ +5%"),
            ("🏦 Reservas", "$350K", "blue", "Saludable")
        ]

        for i, (label, value, color, info) in enumerate(metrics_data):
            metric_frame = tk.Frame(metrics_frame, bg="white", relief=tk.RAISED, bd=2)
            metric_frame.grid(row=0, column=i, padx=8, pady=5, sticky="ew")
            
            tk.Label(metric_frame, text=label, font=("Arial", 9, "bold"), bg="white").pack()
            tk.Label(metric_frame, text=value, font=("Arial", 16, "bold"), 
                    bg="white", fg=color).pack()
            tk.Label(metric_frame, text=info, font=("Arial", 8), 
                    bg="white", fg="gray").pack()

        for i in range(4):
            metrics_frame.grid_columnconfigure(i, weight=1)

    def create_notebook(self, parent):
        """Crear notebook con pestañas"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Pestaña 1: Presupuesto
        self.create_presupuesto_tab(notebook)
        
        # Pestaña 2: Control de Gastos
        self.create_gastos_tab(notebook)
        
        # Pestaña 3: Proyecciones
        self.create_proyecciones_tab(notebook)

    def create_presupuesto_tab(self, notebook):
        """Crear pestaña de presupuesto"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="💰 Presupuesto")

        tk.Label(frame, text="💰 Gestión Presupuestaria 2025", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Distribución presupuestaria
        presupuesto_text = """
        💰 PRESUPUESTO INSTITUCIONAL 2025:
        ═══════════════════════════════════════
        
        📊 DISTRIBUCIÓN POR CATEGORÍA:
        • Salarios y Beneficios:    $1,625,000 (65%)
        • Infraestructura:          $375,000  (15%)
        • Tecnología Educativa:     $250,000  (10%)
        • Materiales Didácticos:    $125,000  (5%)
        • Capacitación Docente:     $75,000   (3%)
        • Reserva de Emergencia:    $50,000   (2%)
        
        📈 EJECUCIÓN PRESUPUESTARIA:
        ═══════════════════════════════
        • Enero: $180,000 ejecutados (7.2%)
        • Proyección Trimestre 1: $625,000 (25%)
        • Variación vs presupuesto: -2.1% (favorable)
        
        🎯 INDICADORES CLAVE:
        ═══════════════════════
        • Eficiencia presupuestaria: 97.8%
        • Cumplimiento de metas: 94.2%
        • Ahorro vs año anterior: $45,000
        """

        tk.Label(frame, text=presupuesto_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def create_gastos_tab(self, notebook):
        """Crear pestaña de control de gastos"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="💳 Control de Gastos")

        tk.Label(frame, text="💳 Control y Seguimiento de Gastos", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Tabla de gastos recientes
        columns = ("Fecha", "Concepto", "Categoría", "Monto", "Estado")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Concepto":
                tree.column(col, width=200, anchor="w")
            else:
                tree.column(col, width=120, anchor="center")

        # Datos de gastos
        gastos_data = [
            ("15/01/2025", "Materiales de oficina", "Administrativo", "$2,500", "Aprobado"),
            ("14/01/2025", "Mantenimiento equipos", "Infraestructura", "$8,000", "Pagado"),
            ("13/01/2025", "Capacitación docente", "Desarrollo", "$5,500", "Aprobado"),
            ("12/01/2025", "Software educativo", "Tecnología", "$12,000", "Pendiente")
        ]

        for gasto in gastos_data:
            tree.insert("", tk.END, values=gasto)

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def create_proyecciones_tab(self, notebook):
        """Crear pestaña de proyecciones financieras"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="📈 Proyecciones")

        tk.Label(frame, text="📈 Proyecciones Financieras", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Proyecciones
        proyecciones_text = """
        📈 PROYECCIONES FINANCIERAS 2025-2027:
        ═══════════════════════════════════════
        
        💰 INGRESOS PROYECTADOS:
        • 2025: $2,650,000 (+6% vs 2024)
        • 2026: $2,809,000 (+6% vs 2025)
        • 2027: $2,978,000 (+6% vs 2026)
        
        📊 PRINCIPALES FUENTES:
        • Subsidios provinciales: 70%
        • Aportes cooperadora: 20%
        • Proyectos especiales: 10%
        
        🎯 INVERSIONES PLANIFICADAS:
        • Infraestructura tecnológica: $400,000
        • Mejoras edilicias: $300,000
        • Equipamiento didáctico: $200,000
        • Capacitación personal: $100,000
        
        📈 INDICADORES DE SOSTENIBILIDAD:
        • Ratio ingresos/gastos: 1.08 (saludable)
        • Reservas mínimas: 3 meses operación
        • Capacidad de inversión: 15% ingresos
        """

        tk.Label(frame, text=proyecciones_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

    def crear_presupuesto(self):
        """Crear nuevo presupuesto"""
        CrearPresupuestoWindow(self.window)

    def aprobar_gasto(self):
        """Aprobar gastos pendientes"""
        AprobarGastosWindow(self.window)

    def generar_reporte_financiero(self):
        """Generar reporte financiero completo"""
        messagebox.showinfo("Reporte Financiero", 
                           "📊 Reporte financiero generado exitosamente\n"
                           "📁 Ubicación: /reportes/financiero_enero_2025.pdf")


class CrearPresupuestoWindow:
    """Ventana para crear nuevo presupuesto"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_window()

    def create_window(self):
        """Crear ventana de nuevo presupuesto"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("💰 Crear Nuevo Presupuesto")
        self.window.geometry("700x600")
        self.window.configure(bg="lightblue")

        # Título
        title = tk.Label(self.window, text="💰 Planificación Presupuestaria", 
                        font=("Arial", 16, "bold"), bg="lightblue", fg="darkblue")
        title.pack(pady=15)

        # Formulario de presupuesto
        form_frame = tk.LabelFrame(self.window, text="📝 Datos del Presupuesto", 
                                  font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Campos principales
        tk.Label(form_frame, text="Año Fiscal:", font=("Arial", 10, "bold"), bg="lightblue").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        año_combo = ttk.Combobox(form_frame, values=["2025", "2026", "2027"], state="readonly", width=20)
        año_combo.set("2025")
        año_combo.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # Categorías presupuestarias
        categorias_frame = tk.LabelFrame(form_frame, text="💰 Distribución por Categorías", 
                                        font=("Arial", 11, "bold"), bg="lightblue", fg="darkblue")
        categorias_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        categorias = [
            ("Salarios y Beneficios", "65%", "$1,625,000"),
            ("Infraestructura", "15%", "$375,000"),
            ("Tecnología Educativa", "10%", "$250,000"),
            ("Materiales Didácticos", "5%", "$125,000"),
            ("Capacitación", "3%", "$75,000"),
            ("Reserva de Emergencia", "2%", "$50,000")
        ]

        for i, (categoria, porcentaje, monto) in enumerate(categorias):
            cat_frame = tk.Frame(categorias_frame, bg="white", relief=tk.RAISED, bd=1)
            cat_frame.pack(fill=tk.X, padx=5, pady=2)
            
            tk.Label(cat_frame, text=categoria, font=("Arial", 9), bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            tk.Label(cat_frame, text=porcentaje, font=("Arial", 9, "bold"), bg="white", fg="blue").pack(side=tk.RIGHT, padx=5)
            tk.Label(cat_frame, text=monto, font=("Arial", 9, "bold"), bg="white", fg="green").pack(side=tk.RIGHT, padx=10)

        # Botones
        buttons_frame = tk.Frame(self.window, bg="lightblue")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="💾 Guardar Presupuesto", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=20, command=self.guardar_presupuesto).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📊 Simular Escenarios", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=18).pack(side=tk.LEFT, padx=5)

    def guardar_presupuesto(self):
        """Guardar el presupuesto"""
        messagebox.showinfo("Presupuesto Guardado", 
                           "💰 Presupuesto guardado exitosamente\n"
                           "📊 Disponible para seguimiento y control")
        self.window.destroy()


class AprobarGastosWindow:
    """Ventana para aprobar gastos pendientes"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_window()

    def create_window(self):
        """Crear ventana de aprobación de gastos"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("✅ Aprobar Gastos Pendientes")
        self.window.geometry("900x600")
        self.window.configure(bg="lightyellow")

        # Título
        title = tk.Label(self.window, text="✅ Aprobación de Gastos Pendientes", 
                        font=("Arial", 16, "bold"), bg="lightyellow", fg="darkorange")
        title.pack(pady=15)

        # Tabla de gastos pendientes
        columns = ("Fecha", "Solicitante", "Concepto", "Monto", "Categoría", "Acción")
        tree = ttk.Treeview(self.window, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Concepto":
                tree.column(col, width=200, anchor="w")
            else:
                tree.column(col, width=120, anchor="center")

        # Datos de gastos pendientes
        gastos_pendientes = [
            ("16/01/2025", "Prof. González", "Material didáctico", "$3,500", "Educativo", "Pendiente"),
            ("15/01/2025", "Mantenimiento", "Reparación proyector", "$8,000", "Infraestructura", "Pendiente"),
            ("14/01/2025", "Secretaría", "Papelería y útiles", "$1,200", "Administrativo", "Pendiente")
        ]

        for gasto in gastos_pendientes:
            tree.insert("", tk.END, values=gasto)

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Botones de aprobación
        buttons_frame = tk.Frame(self.window, bg="lightyellow")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="✅ Aprobar Seleccionado", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="❌ Rechazar", bg="#F44336", fg="white", 
                 font=("Arial", 10), width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="📝 Solicitar Información", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=20).pack(side=tk.LEFT, padx=5)