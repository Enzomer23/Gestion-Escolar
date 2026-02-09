"""
Sistema de notificaciones por email para GESJ
Provincia de San Juan, República Argentina
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
from typing import List, Dict, Optional
import mysql.connector
from .database import crear_conexion

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