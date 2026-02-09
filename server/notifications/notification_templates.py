"""
Plantillas de Notificaciones
GESJ - Plataforma de Gestión Educativa
"""

class NotificationTemplates:
    """Plantillas HTML para diferentes tipos de notificaciones"""
    
    def get_template_base(self) -> str:
        """Plantilla base HTML para emails"""
        return """
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
                {contenido}
            </div>
            
            <div class="footer">
                <p>Este es un mensaje automático del Sistema GESJ</p>
                <p>📧 No responder a este email | 📞 Consultas: gesj.sanjuan@edu.ar</p>
            </div>
        </body>
        </html>
        """
    
    def get_template_calificaciones_preceptor(self) -> str:
        """Plantilla para notificar calificaciones a preceptores"""
        contenido = """
        <h2>📊 Notificación de Calificaciones Actualizadas</h2>
        
        <div class="info-box">
            <h3>📋 Información de la Actualización:</h3>
            <p><strong>Docente:</strong> <span class="highlight">{docente}</span></p>
            <p><strong>Materia:</strong> <span class="highlight">{materia}</span></p>
            <p><strong>Curso:</strong> <span class="highlight">{curso} - División {division}</span></p>
            <p><strong>Período:</strong> <span class="highlight">{periodo}</span></p>
            <p><strong>Fecha de actualización:</strong> <span class="highlight">{fecha}</span></p>
        </div>
        
        <div class="info-box">
            <h3>📝 Acciones Recomendadas:</h3>
            <ul>
                <li>✅ Revisar las calificaciones en el sistema</li>
                <li>📞 Contactar a padres de alumnos con bajo rendimiento</li>
                <li>📋 Actualizar registros de seguimiento académico</li>
                <li>🚨 Identificar alumnos que requieren intervención</li>
            </ul>
        </div>
        """
        return self.get_template_base().format(contenido=contenido)
    
    def get_template_calificaciones_padre(self) -> str:
        """Plantilla para notificar calificaciones a padres"""
        contenido = """
        <h2>📚 Nuevas Calificaciones Disponibles</h2>
        
        <p>Estimado/a Padre/Madre de Familia,</p>
        
        <div class="info-box">
            <h3>📋 Información de las Calificaciones:</h3>
            <p><strong>Docente:</strong> <span class="highlight">{docente}</span></p>
            <p><strong>Materia:</strong> <span class="highlight">{materia}</span></p>
            <p><strong>Curso:</strong> <span class="highlight">{curso} - División {division}</span></p>
            <p><strong>Período:</strong> <span class="highlight">{periodo}</span></p>
            <p><strong>Fecha de actualización:</strong> <span class="highlight">{fecha}</span></p>
        </div>
        
        <div class="info-box">
            <h3>👨‍👩‍👧‍👦 Información para Padres:</h3>
            <p>Las calificaciones de su hijo/a en la materia <strong>{materia}</strong> han sido actualizadas.</p>
            
            <h4>📱 Cómo acceder:</h4>
            <ol>
                <li>Ingrese al sistema GESJ con sus credenciales</li>
                <li>Vaya a la sección "Padres"</li>
                <li>Seleccione "Ver Rendimiento y Asistencia"</li>
                <li>Consulte las calificaciones actualizadas</li>
            </ol>
        </div>
        """
        return self.get_template_base().format(contenido=contenido)
    
    def get_template_riesgo_critico(self) -> str:
        """Plantilla para alerta de riesgo crítico"""
        contenido = """
        <h2>🚨 ALERTA DE RIESGO ACADÉMICO CRÍTICO</h2>
        
        <div class="info-box" style="border-left-color: #F44336;">
            <h3>⚠️ Información del Estudiante:</h3>
            <p><strong>Alumno:</strong> <span class="highlight">{alumno}</span></p>
            <p><strong>Curso:</strong> <span class="highlight">{curso} - División {division}</span></p>
            <p><strong>Promedio Actual:</strong> <span style="color: #F44336; font-weight: bold;">{promedio}</span></p>
            <p><strong>Nivel de Riesgo:</strong> <span style="color: #F44336; font-weight: bold;">{nivel}</span></p>
        </div>
        
        <div class="info-box">
            <h3>🎯 Acciones Inmediatas Requeridas:</h3>
            <ul>
                <li>🔴 Evaluación psicopedagógica inmediata</li>
                <li>🔴 Plan de recuperación intensiva</li>
                <li>🔴 Reunión urgente con padres</li>
                <li>🔴 Seguimiento semanal personalizado</li>
            </ul>
        </div>
        """
        return self.get_template_base().format(contenido=contenido)
    
    def get_template_riesgo_alto(self) -> str:
        """Plantilla para alerta de riesgo alto"""
        contenido = """
        <h2>🟡 ALERTA DE RIESGO ACADÉMICO ALTO</h2>
        
        <div class="info-box" style="border-left-color: #FF9800;">
            <h3>⚠️ Información del Estudiante:</h3>
            <p><strong>Alumno:</strong> <span class="highlight">{alumno}</span></p>
            <p><strong>Curso:</strong> <span class="highlight">{curso} - División {division}</span></p>
            <p><strong>Promedio Actual:</strong> <span style="color: #FF9800; font-weight: bold;">{promedio}</span></p>
            <p><strong>Nivel de Riesgo:</strong> <span style="color: #FF9800; font-weight: bold;">{nivel}</span></p>
        </div>
        
        <div class="info-box">
            <h3>🎯 Acciones Recomendadas:</h3>
            <ul>
                <li>🟡 Tutoría académica adicional</li>
                <li>🟡 Plan de reforzamiento</li>
                <li>🟡 Comunicación con padres</li>
                <li>🟡 Seguimiento quincenal</li>
            </ul>
        </div>
        """
        return self.get_template_base().format(contenido=contenido)
    
    def get_template_riesgo_moderado(self) -> str:
        """Plantilla para alerta de riesgo moderado"""
        contenido = """
        <h2>🟢 SEGUIMIENTO ACADÉMICO</h2>
        
        <div class="info-box" style="border-left-color: #4CAF50;">
            <h3>📊 Información del Estudiante:</h3>
            <p><strong>Alumno:</strong> <span class="highlight">{alumno}</span></p>
            <p><strong>Curso:</strong> <span class="highlight">{curso} - División {division}</span></p>
            <p><strong>Promedio Actual:</strong> <span style="color: #4CAF50; font-weight: bold;">{promedio}</span></p>
            <p><strong>Estado:</strong> <span style="color: #4CAF50; font-weight: bold;">Seguimiento Preventivo</span></p>
        </div>
        
        <div class="info-box">
            <h3>🎯 Acciones de Apoyo:</h3>
            <ul>
                <li>🟢 Reforzamiento en materias específicas</li>
                <li>🟢 Seguimiento mensual</li>
                <li>🟢 Apoyo motivacional</li>
                <li>🟢 Comunicación regular con familia</li>
            </ul>
        </div>
        """
        return self.get_template_base().format(contenido=contenido)
    
    def get_template_padre_riesgo(self) -> str:
        """Plantilla específica para padres sobre riesgo académico"""
        contenido = """
        <h2>📚 Información sobre el Rendimiento Académico</h2>
        
        <p>Estimado/a Padre/Madre de Familia,</p>
        
        <div class="info-box">
            <h3>📊 Información Académica:</h3>
            <p>Nos dirigimos a usted para informarle sobre el rendimiento académico de <strong>{alumno}</strong>.</p>
            <p><strong>Promedio Actual:</strong> <span class="highlight">{promedio}</span></p>
        </div>
        
        <div class="info-box">
            <h3>🤝 Trabajo en Conjunto:</h3>
            <p>Para apoyar el progreso académico de su hijo/a, sugerimos:</p>
            <ul>
                <li>📚 Establecer rutina de estudio en casa</li>
                <li>📞 Mantener comunicación con docentes</li>
                <li>🎯 Participar en reuniones de seguimiento</li>
                <li>💪 Brindar apoyo emocional y motivacional</li>
            </ul>
        </div>
        
        <div class="info-box">
            <p><strong>💡 Próximos Pasos:</strong> Nos pondremos en contacto para coordinar una reunión y establecer un plan de apoyo personalizado.</p>
        </div>
        """
        return self.get_template_base().format(contenido=contenido)