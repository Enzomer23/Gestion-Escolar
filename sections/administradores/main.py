"""
Ventana principal para la sección de Administradores
GESJ - Plataforma de Gestión Educativa
"""

import tkinter as tk
from tkinter import messagebox, ttk
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from typing import List, Dict, Optional

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

# Importar módulos específicos de administradores
from .dashboard import DashboardEjecutivoWindow
from .institucional import GestionInstitucionalWindow
from .analytics import AnalyticsWindow
from .recursos_humanos import RecursosHumanosWindow
from .finanzas import FinanzasWindow
from .sistema import SistemaWindow

try:
    from server.calificaciones import CalificacionesManager
    from server.database import crear_conexion, obtener_todos_usuarios
    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False

# Configuración del servidor de email (Gmail como ejemplo)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': '',  # Email institucional (vacío para modo simulación)
    'password': '',     # Contraseña de aplicación (vacío para modo simulación)
    'sender_name': 'GESJ - Sistema de Gestión Educativa'
}

# Modo simulación por defecto
SIMULATION_MODE = True

class EmailNotifier:
    """Clase para enviar notificaciones por email"""
    
    def __init__(self):
        self.smtp_server = EMAIL_CONFIG['smtp_server']
        self.smtp_port = EMAIL_CONFIG['smtp_port']
        self.email = EMAIL_CONFIG['email']
        self.password = EMAIL_CONFIG['password']
        self.sender_name = EMAIL_CONFIG['sender_name']
        self.simulation_mode = SIMULATION_MODE or not (self.email and self.password)
    
    def enviar_notificacion_notas_subidas(self, docente_nombre: str, materia_nombre: str, 
                                        curso: str, division: str, periodo: str,
                                        emails_preceptores: List[str], emails_padres: List[str],
                                        archivo_adjunto: str = None) -> bool:
        """
        Enviar notificación cuando un docente sube las notas
        
        Args:
            docente_nombre: Nombre del docente
            materia_nombre: Nombre de la materia
            curso: Curso (ej: "1º Año")
            division: División (ej: "A")
            periodo: Período académico
            emails_preceptores: Lista de emails de preceptores
            emails_padres: Lista de emails de padres
            archivo_adjunto: Ruta del archivo de calificaciones (opcional)
        
        Returns:
            bool: True si se enviaron correctamente, False en caso contrario
        """
        
        # Modo simulación
        if self.simulation_mode:
            print("🔄 MODO SIMULACIÓN - Sistema de Notificaciones GESJ")
            print("=" * 60)
            print(f"📧 Simulando envío de notificaciones:")
            print(f"   👨‍🏫 Docente: {docente_nombre}")
            print(f"   📚 Materia: {materia_nombre}")
            print(f"   🎓 Curso: {curso} - División {division}")
            print(f"   📅 Período: {periodo}")
            print(f"   📎 Archivo: {archivo_adjunto if archivo_adjunto else 'Sin archivo adjunto'}")
            print(f"   📧 Preceptores ({len(emails_preceptores)}): {', '.join(emails_preceptores)}")
            print(f"   👨‍👩‍👧‍👦 Padres ({len(emails_padres)}): {', '.join(emails_padres)}")
            print("✅ Simulación completada exitosamente")
            print("=" * 60)
            return True
        
        try:
            # Crear conexión SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            
            # Enviar a preceptores
            if emails_preceptores:
                self._enviar_a_preceptores(server, docente_nombre, materia_nombre, 
                                         curso, division, periodo, emails_preceptores, archivo_adjunto)
            
            # Enviar a padres
            if emails_padres:
                self._enviar_a_padres(server, docente_nombre, materia_nombre, 
                                    curso, division, periodo, emails_padres)
            
            server.quit()
            return True
            
        except Exception as e:
            print(f"Error al enviar notificaciones: {e}")
            return False
    
    def _enviar_a_preceptores(self, server, docente_nombre: str, materia_nombre: str,
                            curso: str, division: str, periodo: str, 
                            emails_preceptores: List[str], archivo_adjunto: str = None):
        """Enviar notificación específica a preceptores"""
        
        asunto = f"📊 Calificaciones Actualizadas - {materia_nombre} - {curso} {division}"
        
        # Crear mensaje HTML para preceptores
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #2E7D32; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f5f5f5; }}
                .info-box {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid #2E7D32; }}
                .footer {{ background-color: #E8F5E9; padding: 15px; text-align: center; font-size: 12px; }}
                .highlight {{ color: #2E7D32; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏛️ GESJ - Sistema de Gestión Educativa</h1>
                <h2>Provincia de San Juan, República Argentina</h2>
            </div>
            
            <div class="content">
                <h2>📊 Notificación de Calificaciones Actualizadas</h2>
                
                <div class="info-box">
                    <h3>📋 Información de la Actualización:</h3>
                    <p><strong>Docente:</strong> <span class="highlight">{docente_nombre}</span></p>
                    <p><strong>Materia:</strong> <span class="highlight">{materia_nombre}</span></p>
                    <p><strong>Curso:</strong> <span class="highlight">{curso} - División {division}</span></p>
                    <p><strong>Período:</strong> <span class="highlight">{periodo}</span></p>
                    <p><strong>Fecha de actualización:</strong> <span class="highlight">{datetime.now().strftime('%d/%m/%Y %H:%M')}</span></p>
                </div>
                
                <div class="info-box">
                    <h3>📝 Acciones Recomendadas para Preceptores:</h3>
                    <ul>
                        <li>✅ Revisar las calificaciones en el sistema</li>
                        <li>📞 Contactar a padres de alumnos con bajo rendimiento</li>
                        <li>📋 Actualizar registros de seguimiento académico</li>
                        <li>🚨 Identificar alumnos que requieren intervención</li>
                    </ul>
                </div>
                
                <div class="info-box">
                    <p><strong>💻 Acceso al Sistema:</strong> Ingrese al sistema GESJ con sus credenciales para ver el detalle completo de las calificaciones.</p>
                </div>
            </div>
            
            <div class="footer">
                <p>Este es un mensaje automático del Sistema GESJ</p>
                <p>📧 No responder a este email | 📞 Consultas: gesj.sanjuan@edu.ar</p>
            </div>
        </body>
        </html>
        """
        
        for email_preceptor in emails_preceptores:
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.sender_name} <{self.email}>"
            msg['To'] = email_preceptor
            msg['Subject'] = asunto
            
            # Agregar contenido HTML
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Adjuntar archivo si existe
            if archivo_adjunto and os.path.exists(archivo_adjunto):
                self._adjuntar_archivo(msg, archivo_adjunto)
            
            # Enviar
            server.send_message(msg)
            print(f"✅ Notificación enviada a preceptor: {email_preceptor}")
    
    def _enviar_a_padres(self, server, docente_nombre: str, materia_nombre: str,
                       curso: str, division: str, periodo: str, emails_padres: List[str]):
        """Enviar notificación específica a padres"""
        
        asunto = f"📚 Calificaciones Disponibles - {materia_nombre} - {curso} {division}"
        
        # Crear mensaje HTML para padres
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #1976D2; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f5f5f5; }}
                .info-box {{ background-color: white; padding: 15px; margin: 10px 0; border-left: 4px solid #1976D2; }}
                .footer {{ background-color: #E3F2FD; padding: 15px; text-align: center; font-size: 12px; }}
                .highlight {{ color: #1976D2; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏛️ GESJ - Sistema de Gestión Educativa</h1>
                <h2>Provincia de San Juan, República Argentina</h2>
            </div>
            
            <div class="content">
                <h2>📚 Nuevas Calificaciones Disponibles</h2>
                
                <p>Estimado/a Padre/Madre de Familia,</p>
                
                <div class="info-box">
                    <h3>📋 Información de las Calificaciones:</h3>
                    <p><strong>Docente:</strong> <span class="highlight">{docente_nombre}</span></p>
                    <p><strong>Materia:</strong> <span class="highlight">{materia_nombre}</span></p>
                    <p><strong>Curso:</strong> <span class="highlight">{curso} - División {division}</span></p>
                    <p><strong>Período:</strong> <span class="highlight">{periodo}</span></p>
                    <p><strong>Fecha de actualización:</strong> <span class="highlight">{datetime.now().strftime('%d/%m/%Y %H:%M')}</span></p>
                </div>
                
                <div class="info-box">
                    <h3>👨‍👩‍👧‍👦 Información para Padres:</h3>
                    <p>Las calificaciones de su hijo/a en la materia <strong>{materia_nombre}</strong> han sido actualizadas por el docente <strong>{docente_nombre}</strong>.</p>
                    
                    <h4>📱 Cómo acceder:</h4>
                    <ol>
                        <li>Ingrese al sistema GESJ con sus credenciales</li>
                        <li>Vaya a la sección "Padres"</li>
                        <li>Seleccione "Ver Rendimiento y Asistencia"</li>
                        <li>Consulte las calificaciones actualizadas</li>
                    </ol>
                </div>
                
                <div class="info-box">
                    <p><strong>💡 Recomendación:</strong> Le sugerimos revisar regularmente el progreso académico de su hijo/a y mantener comunicación con los docentes ante cualquier consulta.</p>
                </div>
            </div>
            
            <div class="footer">
                <p>Este es un mensaje automático del Sistema GESJ</p>
                <p>📧 No responder a este email | 📞 Consultas: gesj.sanjuan@edu.ar</p>
                <p>🏛️ Institución Educativa - Provincia de San Juan</p>
            </div>
        </body>
        </html>
        """
        
        for email_padre in emails_padres:
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.sender_name} <{self.email}>"
            msg['To'] = email_padre
            msg['Subject'] = asunto
            
            # Agregar contenido HTML
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Enviar
            server.send_message(msg)
            print(f"✅ Notificación enviada a padre: {email_padre}")
    
    def _adjuntar_archivo(self, msg, archivo_path: str):
        """Adjuntar archivo al mensaje de email"""
        try:
            with open(archivo_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            filename = os.path.basename(archivo_path)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}',
            )
            
            msg.attach(part)
        except Exception as e:
            print(f"Error al adjuntar archivo: {e}")
    
    def obtener_emails_preceptores(self, curso: str, division: str) -> List[str]:
        """Obtener emails de preceptores para un curso específico"""
        try:
            connection = crear_conexion()
            if connection:
                cursor = connection.cursor()
                
                # Por ahora, obtener todos los preceptores
                # En el futuro se puede hacer más específico por curso
                query = """
                    SELECT DISTINCT u.nombre_usuario as email
                    FROM usuarios u 
                    WHERE u.tipo_usuario = 'Preceptor'
                """
                cursor.execute(query)
                resultados = cursor.fetchall()
                
                # Convertir nombres de usuario a emails (simulado)
                emails = [f"{resultado[0]}@gesj.edu.ar" for resultado in resultados]
                
                cursor.close()
                connection.close()
                return emails
        except Exception as e:
            print(f"Error al obtener emails de preceptores: {e}")
        
        # Emails de ejemplo si no hay base de datos
        return ["preceptor1@gesj.edu.ar", "preceptor.general@gesj.edu.ar"]
    
    def obtener_emails_padres(self, curso: str, division: str) -> List[str]:
        """Obtener emails de padres para un curso específico"""
        try:
            connection = crear_conexion()
            if connection:
                cursor = connection.cursor()
                
                query = """
                    SELECT DISTINCT u.nombre_usuario as email
                    FROM usuarios u 
                    JOIN alumnos a ON u.id = a.padre_id
                    WHERE u.tipo_usuario = 'Padre' 
                    AND a.curso = %s 
                    AND a.division = %s
                    AND a.activo = TRUE
                """
                cursor.execute(query, (curso, division))
                resultados = cursor.fetchall()
                
                # Convertir nombres de usuario a emails (simulado)
                emails = [f"{resultado[0]}@gmail.com" for resultado in resultados]
                
                cursor.close()
                connection.close()
                return emails
        except Exception as e:
            print(f"Error al obtener emails de padres: {e}")
        
        # Emails de ejemplo si no hay base de datos
        return ["padre1@gmail.com", "padre2@gmail.com", "padre3@gmail.com"]

# Función de utilidad para envío rápido
def notificar_notas_subidas(docente_nombre: str, materia_nombre: str, curso: str, 
                          division: str, periodo: str, archivo_calificaciones: str = None) -> bool:
    """
    Función de utilidad para enviar notificaciones rápidamente
    
    Args:
        docente_nombre: Nombre del docente
        materia_nombre: Nombre de la materia  
        curso: Curso
        division: División
        periodo: Período académico
        archivo_calificaciones: Ruta del archivo de calificaciones (opcional)
    
    Returns:
        bool: True si se enviaron correctamente
    """
    notifier = EmailNotifier()
    
    # Obtener emails
    emails_preceptores = notifier.obtener_emails_preceptores(curso, division)
    emails_padres = notifier.obtener_emails_padres(curso, division)
    
    # Enviar notificaciones
    return notifier.enviar_notificacion_notas_subidas(
        docente_nombre, materia_nombre, curso, division, periodo,
        emails_preceptores, emails_padres, archivo_calificaciones
    )

class AdministradoresSection:
    def __init__(self, root):
        self.root = root
        self.cal_manager = CalificacionesManager() if DATABASE_AVAILABLE else None
        self.email_notifier = EmailNotifier()
        self.usuarios_data = self.obtener_usuarios_data()
        self.create_administradores_window()
    
    def obtener_usuarios_data(self):
        """Obtener datos de usuarios desde la base de datos"""
        if DATABASE_AVAILABLE:
            try:
                return obtener_todos_usuarios()
            except Exception as e:
                print(f"Error obteniendo usuarios: {e}")
                return []
        else:
            # Datos de ejemplo si no hay base de datos
            return [
                ("admin1", "Administrativo", "admin1@gesj.edu.ar"),
                ("docente1", "Docente", "docente1@gesj.edu.ar"),
                ("preceptor1", "Preceptor", "preceptor1@gesj.edu.ar"),
                ("padre1", "Padre", "padre1@gmail.com")
            ]
    
    def create_administradores_window(self):
        """Crear ventana principal de administradores"""
        self.administradores_window = tk.Toplevel(self.root)
        self.administradores_window.title("GESJ - Panel de Administradores")
        
        # Optimizado para pantallas 1366x768
        self.administradores_window.geometry("1340x720+13+24")
        self.administradores_window.configure(bg="lightsteelblue")

        self.create_header()
        self.create_main_content()
        self.create_footer()

    def create_header(self):
        """Crear encabezado"""
        header_frame = tk.Frame(self.administradores_window, bg="steelblue", padx=15, pady=8)
        header_frame.pack(fill=tk.X)

        title = tk.Label(header_frame, text="GESJ - Panel Ejecutivo de Administradores", 
                        font=("Franklin Gothic Heavy", 18, "bold"), bg="steelblue", fg="white")
        title.pack(pady=5)

        subtitle = tk.Label(header_frame, text="Sistema de Gestión Integral y Business Intelligence", 
                           font=("Arial", 11), bg="steelblue", fg="lightblue")
        subtitle.pack()

    def create_main_content(self):
        """Crear contenido principal con funcionalidades"""
        # Frame principal con scroll
        main_frame = tk.Frame(self.administradores_window, bg="lightsteelblue")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=8)

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

        # Panel de métricas ejecutivas
        self.create_executive_metrics(scrollable_frame)
        
        # Panel de funcionalidades principales
        self.create_functions_panel(scrollable_frame)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_executive_metrics(self, parent):
        """Panel de métricas ejecutivas"""
        metrics_frame = tk.LabelFrame(parent, text="📊 Métricas Ejecutivas", 
                                     font=("Arial", 12, "bold"), bg="lightsteelblue", 
                                     fg="darkblue", padx=10, pady=8)
        metrics_frame.pack(fill=tk.X, pady=(0, 15))

        # Obtener estadísticas desde la base de datos
        if DATABASE_AVAILABLE and self.cal_manager:
            try:
                # Aquí podrías obtener métricas reales
                total_alumnos = len(self.usuarios_data) * 50  # Simulado
                promedio_general = 8.3
                eficiencia = 94.2
                satisfaccion = 89.1
            except:
                total_alumnos = 247
                promedio_general = 8.3
                eficiencia = 94.2
                satisfaccion = 89.1
        else:
            total_alumnos = 247
            promedio_general = 8.3
            eficiencia = 94.2
            satisfaccion = 89.1

        metrics_data = [
            ("👥 Total Estudiantes", str(total_alumnos), "blue", "Activos"),
            ("📊 Promedio General", f"{promedio_general}", "green", "↗ +0.2"),
            ("🎯 Eficiencia", f"{eficiencia}%", "green", "Meta: 95%"),
            ("😊 Satisfacción", f"{satisfaccion}%", "orange", "Meta: 90%")
        ]

        for i, (label, value, color, info) in enumerate(metrics_data):
            metric_frame = tk.Frame(metrics_frame, bg="white", relief=tk.RAISED, bd=2)
            metric_frame.grid(row=0, column=i, padx=8, pady=5, sticky="ew")
            
            tk.Label(metric_frame, text=label, font=("Arial", 9, "bold"), bg="white").pack()
            tk.Label(metric_frame, text=value, font=("Arial", 16, "bold"), 
                    bg="white", fg=color).pack()
            tk.Label(metric_frame, text=info, font=("Arial", 8), 
                    bg="white", fg="gray").pack()

        # Configurar columnas
        for i in range(4):
            metrics_frame.grid_columnconfigure(i, weight=1)

    def create_functions_panel(self, parent):
        """Panel de funcionalidades principales"""
        functions_frame = tk.LabelFrame(parent, text="🎯 Funcionalidades Ejecutivas", 
                                       font=("Arial", 12, "bold"), bg="lightsteelblue", 
                                       fg="darkblue", padx=10, pady=8)
        functions_frame.pack(fill=tk.BOTH, expand=True)

        # Funcionalidades principales
        functions = [
            ("📊 Dashboard Ejecutivo Integral", self.abrir_dashboard_ejecutivo,
             "Métricas clave, KPIs y análisis en tiempo real", "#1976D2"),
            ("🏛️ Gestión Institucional", self.abrir_gestion_institucional,
             "Planificación estratégica y calidad educativa", "#388E3C"),
            ("📈 Analytics y Business Intelligence", self.abrir_analytics,
             "Análisis predictivo y reportes ejecutivos", "#F57C00"),
            ("👥 Recursos Humanos", self.abrir_recursos_humanos,
             "Gestión de personal y evaluación de desempeño", "#7B1FA2"),
            ("💰 Finanzas y Presupuesto", self.abrir_finanzas,
             "Control presupuestario y proyecciones financieras", "#D32F2F"),
            ("⚙️ Configuración del Sistema", self.abrir_sistema,
             "Administración de usuarios y configuración general", "#455A64")
        ]

        for i, (title, command, description, color) in enumerate(functions):
            row = i // 2
            col = i % 2
            
            # Frame para cada función
            func_frame = tk.Frame(functions_frame, bg="white", relief=tk.RAISED, bd=2)
            func_frame.grid(row=row, column=col, padx=10, pady=8, sticky="ew")
            
            # Botón principal
            btn = tk.Button(func_frame, text=title, font=("Arial", 11, "bold"),
                           bg=color, fg="white", command=command,
                           width=35, height=2)
            btn.pack(pady=8)
            
            # Descripción
            desc_label = tk.Label(func_frame, text=description, 
                                 font=("Arial", 9), bg="white", fg="gray",
                                 wraplength=280)
            desc_label.pack(pady=(0, 8))

        # Configurar columnas
        for i in range(2):
            functions_frame.grid_columnconfigure(i, weight=1)

    def create_footer(self):
        """Crear pie de página"""
        footer_frame = tk.Frame(self.administradores_window, bg="steelblue", padx=15, pady=8)
        footer_frame.pack(fill=tk.X)
        
        tk.Label(footer_frame, text="GESJ - Sistema Integral de Gestión Educativa | Panel Ejecutivo de Administradores", 
                font=("Arial", 9), bg="steelblue", fg="lightblue").pack()

    # Métodos para abrir ventanas específicas
    def abrir_dashboard_ejecutivo(self):
        """Abrir dashboard ejecutivo integral"""
        estadisticas_data = {
            'total_alumnos': len(self.usuarios_data) * 50,
            'total_docentes': sum(1 for u in self.usuarios_data if u[1] == 'Docente'),
            'promedio_general': 8.3,
            'eficiencia': 94.2
        }
        DashboardEjecutivoWindow(self.administradores_window, self.cal_manager, estadisticas_data)

    def abrir_gestion_institucional(self):
        """Abrir ventana de gestión institucional"""
        GestionInstitucionalWindow(self.administradores_window, self.cal_manager)

    def abrir_analytics(self):
        """Abrir ventana de analytics y BI"""
        AnalyticsWindow(self.administradores_window, self.cal_manager)

    def abrir_recursos_humanos(self):
        """Abrir ventana de recursos humanos"""
        RecursosHumanosWindow(self.administradores_window, self.usuarios_data)

    def abrir_finanzas(self):
        """Abrir ventana de finanzas y presupuesto"""
        estadisticas_data = {
            'presupuesto_anual': 2500000,
            'ejecutado': 67,
            'gastos_mes': 180000,
            'reservas': 350000
        }
        FinanzasWindow(self.administradores_window, estadisticas_data)

    def abrir_sistema(self):
        """Abrir ventana de configuración del sistema"""
        SistemaWindow(self.administradores_window, self.usuarios_data)