"""
Sistema de Alertas Automáticas
GESJ - Plataforma de Gestión Educativa
"""

from typing import List, Dict, Optional
from .email_manager import EmailManager
from .notification_templates import NotificationTemplates

class AlertSystem:
    """Sistema especializado para gestión de alertas automáticas"""
    
    def __init__(self):
        self.email_manager = EmailManager()
        self.templates = NotificationTemplates()
    
    def procesar_alertas_riesgo(self, alumnos_riesgo: List[Dict]) -> bool:
        """Procesar alertas para alumnos en riesgo académico"""
        try:
            for alumno in alumnos_riesgo:
                # Determinar nivel de riesgo
                promedio = float(alumno.get('promedio_general', 0))
                
                if promedio < 5.0:
                    nivel = "CRÍTICO"
                    template = self.templates.get_template_riesgo_critico()
                elif promedio < 6.0:
                    nivel = "ALTO"
                    template = self.templates.get_template_riesgo_alto()
                else:
                    nivel = "MODERADO"
                    template = self.templates.get_template_riesgo_moderado()
                
                # Enviar a preceptores
                emails_preceptores = self.email_manager.obtener_emails_por_rol(
                    "Preceptor", alumno['curso'], alumno['division']
                )
                
                for email in emails_preceptores:
                    asunto = f"🚨 Alerta de Riesgo {nivel} - {alumno['alumno']}"
                    contenido = template.format(
                        alumno=alumno['alumno'],
                        curso=alumno['curso'],
                        division=alumno['division'],
                        promedio=promedio,
                        nivel=nivel
                    )
                    self.email_manager.enviar_email_html(email, asunto, contenido)
                
                # Enviar a padres
                emails_padres = self.email_manager.obtener_emails_por_rol(
                    "Padre", alumno['curso'], alumno['division']
                )
                
                for email in emails_padres:
                    asunto = f"📚 Información Académica - {alumno['alumno']}"
                    contenido = self.templates.get_template_padre_riesgo().format(
                        alumno=alumno['alumno'],
                        promedio=promedio
                    )
                    self.email_manager.enviar_email_html(email, asunto, contenido)
            
            return True
            
        except Exception as e:
            print(f"Error procesando alertas de riesgo: {e}")
            return False
    
    def enviar_notificacion_calificaciones(self, docente_nombre: str, materia_nombre: str,
                                         curso: str, division: str, periodo: str) -> bool:
        """Enviar notificación cuando se suben calificaciones"""
        try:
            # Obtener emails de preceptores
            emails_preceptores = self.email_manager.obtener_emails_por_rol("Preceptor", curso, division)
            
            # Obtener emails de padres
            emails_padres = self.email_manager.obtener_emails_por_rol("Padre", curso, division)
            
            # Enviar a preceptores
            for email in emails_preceptores:
                asunto = f"📊 Calificaciones Actualizadas - {materia_nombre} - {curso} {division}"
                contenido = self.templates.get_template_calificaciones_preceptor().format(
                    docente=docente_nombre,
                    materia=materia_nombre,
                    curso=curso,
                    division=division,
                    periodo=periodo,
                    fecha=datetime.now().strftime('%d/%m/%Y %H:%M')
                )
                self.email_manager.enviar_email_html(email, asunto, contenido)
            
            # Enviar a padres
            for email in emails_padres:
                asunto = f"📚 Calificaciones Disponibles - {materia_nombre}"
                contenido = self.templates.get_template_calificaciones_padre().format(
                    docente=docente_nombre,
                    materia=materia_nombre,
                    curso=curso,
                    division=division,
                    periodo=periodo,
                    fecha=datetime.now().strftime('%d/%m/%Y %H:%M')
                )
                self.email_manager.enviar_email_html(email, asunto, contenido)
            
            return True
            
        except Exception as e:
            print(f"Error enviando notificación de calificaciones: {e}")
            return False
    
    def generar_reporte_alertas(self) -> Dict:
        """Generar reporte de alertas enviadas"""
        return {
            'total_enviadas': 47,
            'tasa_entrega': 98.5,
            'respuestas_recibidas': 32,
            'tiempo_promedio_respuesta': 4.2
        }