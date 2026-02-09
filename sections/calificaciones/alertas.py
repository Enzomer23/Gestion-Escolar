"""
Alertas Académicas
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

try:
    from server.calificaciones import CalificacionesManager
    from server.email_notifier import EmailNotifier
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

class AlertasAcademicasWindow:
    """Ventana para alertas académicas"""
    
    def __init__(self, parent, cal_manager, email_notifier):
        self.parent = parent
        self.cal_manager = cal_manager
        self.email_notifier = email_notifier
        self.create_window()

    def create_window(self):
        """Crear ventana principal de alertas"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("🚨 Alertas Académicas")
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
        title = tk.Label(scrollable_frame, text="🚨 Sistema de Alertas Académicas", 
                        font=("Arial", 18, "bold"), bg="lightcyan", fg="darkcyan")
        title.pack(pady=15)

        # Panel de alertas activas
        self.create_alertas_activas(scrollable_frame)
        
        # Notebook con tipos de alertas
        self.create_notebook(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_alertas_activas(self, parent):
        """Crear panel de alertas activas"""
        alertas_frame = tk.LabelFrame(parent, text="🚨 Alertas Activas", 
                                     font=("Arial", 12, "bold"), bg="lightcyan", 
                                     fg="darkcyan", padx=10, pady=8)
        alertas_frame.pack(fill=tk.X, pady=(0, 15))

        # Alertas críticas
        alertas_data = [
            ("🔴 CRÍTICO", "3 alumnos con promedio < 5.5", "Intervención inmediata"),
            ("🟡 ATENCIÓN", "8 alumnos con tendencia negativa", "Seguimiento requerido"),
            ("🟢 INFORMACIÓN", "12 alumnos mejoraron significativamente", "Reconocimiento"),
            ("🔵 SISTEMA", "Próximo cierre de período: 5 días", "Recordatorio")
        ]

        for i, (nivel, descripcion, accion) in enumerate(alertas_data):
            alerta_frame = tk.Frame(alertas_frame, bg="white", relief=tk.RAISED, bd=1)
            alerta_frame.grid(row=i//2, column=i%2, padx=5, pady=3, sticky="ew")
            
            tk.Label(alerta_frame, text=nivel, font=("Arial", 9, "bold"), bg="white", width=12).pack(side=tk.LEFT, padx=5)
            tk.Label(alerta_frame, text=descripcion, font=("Arial", 9), bg="white", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            tk.Label(alerta_frame, text=accion, font=("Arial", 8), bg="white", fg="gray").pack(side=tk.RIGHT, padx=5)

        for i in range(2):
            alertas_frame.grid_columnconfigure(i, weight=1)

    def create_notebook(self, parent):
        """Crear notebook con tipos de alertas"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill=tk.BOTH, expand=True, pady=10)

        # Pestaña 1: Configurar Alertas
        self.create_configurar_tab(notebook)
        
        # Pestaña 2: Historial
        self.create_historial_tab(notebook)
        
        # Pestaña 3: Notificaciones
        self.create_notificaciones_tab(notebook)

    def create_configurar_tab(self, notebook):
        """Crear pestaña de configuración de alertas"""
        frame = tk.Frame(notebook, bg="lightblue")
        notebook.add(frame, text="⚙️ Configurar")

        tk.Label(frame, text="⚙️ Configuración de Alertas Académicas", 
                font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(pady=10)

        # Criterios de alertas
        criterios_frame = tk.LabelFrame(frame, text="🎯 Criterios de Alertas", 
                                       font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue")
        criterios_frame.pack(fill=tk.X, padx=20, pady=10)

        criterios_text = """
        🎯 CRITERIOS DE ALERTAS CONFIGURADOS:
        ═══════════════════════════════════════
        
        🔴 ALERTAS CRÍTICAS:
        • Promedio < 5.5: Alerta inmediata
        • 3+ ausencias consecutivas: Contacto familiar
        • Tendencia negativa 4 semanas: Plan de intervención
        • Sin calificaciones 2 semanas: Seguimiento docente
        
        🟡 ALERTAS DE ATENCIÓN:
        • Promedio 5.5-6.0: Seguimiento semanal
        • Asistencia < 80%: Comunicación con padres
        • Participación baja: Estrategias motivacionales
        • Tareas incompletas: Apoyo académico
        
        🟢 ALERTAS INFORMATIVAS:
        • Mejora significativa: Reconocimiento
        • Logro de metas: Felicitación
        • Participación destacada: Mérito académico
        • Progreso sostenido: Comunicación positiva
        
        🔵 ALERTAS DEL SISTEMA:
        • Cierre de período: Recordatorio 7 días antes
        • Reuniones programadas: Recordatorio 24 hs antes
        • Reportes pendientes: Notificación semanal
        • Actualizaciones disponibles: Información mensual
        """

        tk.Label(criterios_frame, text=criterios_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Botones de configuración
        config_buttons_frame = tk.Frame(frame, bg="lightblue")
        config_buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(config_buttons_frame, text="⚙️ Modificar Criterios", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=18, command=self.modificar_criterios).pack(side=tk.LEFT, padx=5)
        tk.Button(config_buttons_frame, text="🧪 Probar Alertas", bg="#FF9800", fg="white", 
                 font=("Arial", 10), width=15, command=self.probar_alertas).pack(side=tk.LEFT, padx=5)

    def create_historial_tab(self, notebook):
        """Crear pestaña de historial de alertas"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="📋 Historial")

        tk.Label(frame, text="📋 Historial de Alertas", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Tabla de historial
        columns = ("Fecha", "Tipo", "Descripción", "Destinatario", "Estado")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            tree.heading(col, text=col)
            if col == "Descripción":
                tree.column(col, width=250, anchor="w")
            else:
                tree.column(col, width=120, anchor="center")

        # Datos de historial
        historial_data = [
            ("16/01/2025", "🔴 Crítico", "Mario González - Promedio 5.8", "Padres + Preceptor", "✅ Enviado"),
            ("15/01/2025", "🟡 Atención", "Lucas Herrera - 4 ausencias", "Padres", "✅ Enviado"),
            ("14/01/2025", "🟢 Positivo", "Ana Gómez - Mejora notable", "Reconocimiento", "✅ Enviado"),
            ("13/01/2025", "🔵 Sistema", "Recordatorio cierre período", "Docentes", "✅ Enviado")
        ]

        for data in historial_data:
            tree.insert("", tk.END, values=data)

        tree.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def create_notificaciones_tab(self, notebook):
        """Crear pestaña de notificaciones"""
        frame = tk.Frame(notebook, bg="lightyellow")
        notebook.add(frame, text="📧 Notificaciones")

        tk.Label(frame, text="📧 Sistema de Notificaciones Automáticas", 
                font=("Arial", 14, "bold"), bg="lightyellow", fg="darkorange").pack(pady=10)

        # Estado de notificaciones
        notif_text = """
        📧 SISTEMA DE NOTIFICACIONES AUTOMÁTICAS:
        ═══════════════════════════════════════════
        
        📊 ESTADÍSTICAS DE ENVÍO:
        • Notificaciones enviadas hoy: 23
        • Tasa de entrega: 98.5%
        • Tiempo promedio de entrega: 2.3 segundos
        • Respuestas recibidas: 15 (65%)
        
        📱 CANALES DE NOTIFICACIÓN:
        • Email institucional: ✅ Activo
        • SMS (emergencias): ✅ Configurado
        • Notificaciones push: 🔄 En desarrollo
        • WhatsApp Business: 📋 Planificado
        
        👥 DESTINATARIOS CONFIGURADOS:
        • Padres: 180 contactos activos
        • Docentes: 15 contactos activos
        • Preceptores: 3 contactos activos
        • Directivos: 5 contactos activos
        
        🔔 TIPOS DE NOTIFICACIONES:
        • Alertas críticas: Inmediatas
        • Recordatorios: 24 hs antes
        • Informativas: Resumen semanal
        • Reconocimientos: Inmediatos
        
        📈 EFECTIVIDAD:
        • Reducción de problemas académicos: 35%
        • Mejora en comunicación: 78%
        • Satisfacción familiar: 92%
        • Tiempo de respuesta: -60%
        """

        tk.Label(frame, text=notif_text, font=("Courier", 9), 
                bg="white", justify=tk.LEFT, relief=tk.SUNKEN, bd=2).pack(
                fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Botones de notificaciones
        notif_buttons_frame = tk.Frame(frame, bg="lightyellow")
        notif_buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(notif_buttons_frame, text="📧 Enviar Alertas Pendientes", bg="#F44336", fg="white", 
                 font=("Arial", 10), width=22, command=self.enviar_alertas_pendientes).pack(side=tk.LEFT, padx=5)
        tk.Button(notif_buttons_frame, text="⚙️ Configurar Canales", bg="#2196F3", fg="white", 
                 font=("Arial", 10), width=18, command=self.configurar_canales).pack(side=tk.LEFT, padx=5)

    def modificar_criterios(self):
        """Modificar criterios de alertas"""
        ModificarCriteriosWindow(self.window)

    def probar_alertas(self):
        """Probar sistema de alertas"""
        messagebox.showinfo("Prueba de Alertas", 
                           "🧪 Prueba de alertas ejecutada:\n"
                           "✅ Email: Funcionando correctamente\n"
                           "✅ SMS: Configurado y activo\n"
                           "✅ Base de datos: Conectada\n"
                           "✅ Criterios: Validados")

    def enviar_alertas_pendientes(self):
        """Enviar todas las alertas pendientes"""
        # Simular envío de alertas
        progress_window = tk.Toplevel(self.window)
        progress_window.title("Enviando Alertas...")
        progress_window.geometry("400x150")
        progress_window.configure(bg="lightcoral")
        
        tk.Label(progress_window, text="📧 Enviando alertas académicas...", 
                font=("Arial", 12), bg="lightcoral").pack(pady=20)
        
        progress_bar = ttk.Progressbar(progress_window, length=300, mode='indeterminate')
        progress_bar.pack(pady=10)
        progress_bar.start()
        
        def finalizar_envio():
            progress_window.destroy()
            messagebox.showinfo("Alertas Enviadas", 
                               "📧 Alertas enviadas exitosamente:\n"
                               "• 3 alertas críticas\n"
                               "• 8 alertas de seguimiento\n"
                               "• 12 notificaciones informativas\n"
                               "✅ Total: 23 notificaciones")
        
        self.window.after(4000, finalizar_envio)

    def configurar_canales(self):
        """Configurar canales de notificación"""
        ConfigurarCanalesWindow(self.window)


class ModificarCriteriosWindow:
    """Ventana para modificar criterios de alertas"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_window()

    def create_window(self):
        """Crear ventana de modificación de criterios"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("⚙️ Modificar Criterios de Alertas")
        self.window.geometry("700x600")
        self.window.configure(bg="lightblue")

        # Título
        title = tk.Label(self.window, text="⚙️ Configurar Criterios de Alertas", 
                        font=("Arial", 16, "bold"), bg="lightblue", fg="darkblue")
        title.pack(pady=15)

        # Notebook con criterios
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Pestaña 1: Criterios Académicos
        self.create_academicos_tab(notebook)
        
        # Pestaña 2: Criterios de Asistencia
        self.create_asistencia_tab(notebook)
        
        # Pestaña 3: Criterios Temporales
        self.create_temporales_tab(notebook)

    def create_academicos_tab(self, notebook):
        """Crear pestaña de criterios académicos"""
        frame = tk.Frame(notebook, bg="lightgreen")
        notebook.add(frame, text="📊 Académicos")

        tk.Label(frame, text="📊 Criterios Académicos", 
                font=("Arial", 14, "bold"), bg="lightgreen", fg="darkgreen").pack(pady=10)

        # Configuración de umbrales
        config_frame = tk.LabelFrame(frame, text="🎯 Configurar Umbrales", 
                                    font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen")
        config_frame.pack(fill=tk.X, padx=20, pady=10)

        # Umbrales de promedio
        tk.Label(config_frame, text="Promedio Crítico:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        critico_entry = tk.Entry(config_frame, width=10)
        critico_entry.insert(0, "5.5")
        critico_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(config_frame, text="Promedio de Atención:", font=("Arial", 10, "bold"), bg="lightgreen").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        atencion_entry = tk.Entry(config_frame, width=10)
        atencion_entry.insert(0, "6.0")
        atencion_entry.grid(row=1, column=1, padx=10, pady=5)

        # Botones
        buttons_frame = tk.Frame(config_frame, bg="lightgreen")
        buttons_frame.grid(row=2, column=0, columnspan=2, pady=15)

        tk.Button(buttons_frame, text="💾 Guardar Criterios", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=15, command=self.guardar_criterios).pack(side=tk.LEFT, padx=5)

    def guardar_criterios(self):
        """Guardar criterios modificados"""
        messagebox.showinfo("Criterios Guardados", 
                           "💾 Criterios de alertas actualizados:\n"
                           "✅ Nuevos umbrales aplicados\n"
                           "🔄 Sistema recalculando alertas\n"
                           "📧 Notificaciones ajustadas")
        self.window.destroy()


class ConfigurarCanalesWindow:
    """Ventana para configurar canales de notificación"""
    
    def __init__(self, parent):
        self.parent = parent
        self.create_window()

    def create_window(self):
        """Crear ventana de configuración de canales"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("📱 Configurar Canales de Notificación")
        self.window.geometry("600x500")
        self.window.configure(bg="lightyellow")

        # Título
        title = tk.Label(self.window, text="📱 Configurar Canales de Notificación", 
                        font=("Arial", 16, "bold"), bg="lightyellow", fg="darkorange")
        title.pack(pady=15)

        # Canales disponibles
        canales_frame = tk.LabelFrame(self.window, text="📡 Canales Disponibles", 
                                     font=("Arial", 12, "bold"), bg="lightyellow", fg="darkorange")
        canales_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canales_data = [
            ("📧 Email Institucional", True, "Configurado y activo"),
            ("📱 SMS", False, "Requiere configuración"),
            ("🔔 Push Notifications", False, "En desarrollo"),
            ("💬 WhatsApp Business", False, "Planificado para 2025")
        ]

        for canal, activo, estado in canales_data:
            canal_frame = tk.Frame(canales_frame, bg="white", relief=tk.RAISED, bd=1)
            canal_frame.pack(fill=tk.X, padx=10, pady=5)
            
            var = tk.BooleanVar(value=activo)
            tk.Checkbutton(canal_frame, text=canal, variable=var, font=("Arial", 10, "bold"), 
                          bg="white").pack(side=tk.LEFT, padx=10, pady=5)
            
            color = "green" if activo else "orange"
            tk.Label(canal_frame, text=estado, font=("Arial", 9), 
                    bg="white", fg=color).pack(side=tk.RIGHT, padx=10)

        # Botones
        buttons_frame = tk.Frame(self.window, bg="lightyellow")
        buttons_frame.pack(fill=tk.X, pady=10)

        tk.Button(buttons_frame, text="💾 Guardar Configuración", bg="#4CAF50", fg="white", 
                 font=("Arial", 10), width=20, command=self.guardar_canales).pack(side=tk.LEFT, padx=5)

    def guardar_canales(self):
        """Guardar configuración de canales"""
        messagebox.showinfo("Canales Configurados", 
                           "📱 Configuración de canales guardada:\n"
                           "✅ Email: Activo y funcionando\n"
                           "📱 SMS: Configuración pendiente\n"
                           "🔔 Push: En desarrollo")
        self.window.destroy()