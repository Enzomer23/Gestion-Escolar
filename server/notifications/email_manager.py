"""
Gestor de Email para Notificaciones
GESJ - Plataforma de Gestión Educativa
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
from typing import List, Dict, Optional
from ..database import crear_conexion

# Configuración del servidor de email
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': '',  # Email institucional
    'password': '',  # Contraseña de aplicación
    'sender_name': 'GESJ - Sistema de Gestión Educativa'
}

# Modo simulación por defecto
SIMULATION_MODE = True

class EmailManager:
    """Gestor especializado para envío de emails"""
    
    def __init__(self):
        self.smtp_server = EMAIL_CONFIG['smtp_server']
        self.smtp_port = EMAIL_CONFIG['smtp_port']
        self.email = EMAIL_CONFIG['email']
        self.password = EMAIL_CONFIG['password']
        self.sender_name = EMAIL_CONFIG['sender_name']
        self.simulation_mode = SIMULATION_MODE or not (self.email and self.password)
    
    def enviar_email_simple(self, destinatario: str, asunto: str, mensaje: str) -> bool:
        """Enviar email simple"""
        if self.simulation_mode:
            print(f"📧 SIMULACIÓN - Email enviado a: {destinatario}")
            print(f"   Asunto: {asunto}")
            return True
        
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            
            msg = MIMEText(mensaje, 'plain', 'utf-8')
            msg['From'] = f"{self.sender_name} <{self.email}>"
            msg['To'] = destinatario
            msg['Subject'] = asunto
            
            server.send_message(msg)
            server.quit()
            return True
            
        except Exception as e:
            print(f"Error al enviar email: {e}")
            return False
    
    def enviar_email_html(self, destinatario: str, asunto: str, contenido_html: str, 
                         archivo_adjunto: str = None) -> bool:
        """Enviar email con formato HTML"""
        if self.simulation_mode:
            print(f"📧 SIMULACIÓN - Email HTML enviado a: {destinatario}")
            print(f"   Asunto: {asunto}")
            if archivo_adjunto:
                print(f"   Adjunto: {archivo_adjunto}")
            return True
        
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.sender_name} <{self.email}>"
            msg['To'] = destinatario
            msg['Subject'] = asunto
            
            html_part = MIMEText(contenido_html, 'html', 'utf-8')
            msg.attach(html_part)
            
            # Adjuntar archivo si existe
            if archivo_adjunto and os.path.exists(archivo_adjunto):
                self._adjuntar_archivo(msg, archivo_adjunto)
            
            server.send_message(msg)
            server.quit()
            return True
            
        except Exception as e:
            print(f"Error al enviar email HTML: {e}")
            return False
    
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
    
    def obtener_emails_por_rol(self, rol: str, curso: str = None, division: str = None) -> List[str]:
        """Obtener emails de usuarios por rol"""
        try:
            connection = crear_conexion()
            if connection:
                cursor = connection.cursor()
                
                if rol == "Padre" and curso and division:
                    query = """
                        SELECT DISTINCT u.nombre_usuario as email
                        FROM usuarios u 
                        JOIN alumnos a ON u.id = a.padre_id
                        WHERE u.tipo_usuario = 'Padre' 
                        AND a.curso = %s AND a.division = %s
                        AND a.activo = TRUE
                    """
                    cursor.execute(query, (curso, division))
                else:
                    query = """
                        SELECT DISTINCT u.nombre_usuario as email
                        FROM usuarios u 
                        WHERE u.tipo_usuario = %s
                    """
                    cursor.execute(query, (rol,))
                
                resultados = cursor.fetchall()
                emails = [f"{resultado[0]}@gesj.edu.ar" for resultado in resultados]
                
                cursor.close()
                connection.close()
                return emails
        except Exception as e:
            print(f"Error al obtener emails: {e}")
        
        # Emails de ejemplo si no hay base de datos
        if rol == "Preceptor":
            return ["preceptor1@gesj.edu.ar", "preceptor.general@gesj.edu.ar"]
        elif rol == "Padre":
            return ["padre1@gmail.com", "padre2@gmail.com", "padre3@gmail.com"]
        else:
            return ["admin@gesj.edu.ar"]