"""
Gestor de Exportación PDF
GESJ - Plataforma de Gestión Educativa
"""

import os
from datetime import datetime
from typing import List, Dict, Optional

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class PDFManager:
    """Gestor especializado para exportación a PDF"""
    
    def __init__(self):
        if not REPORTLAB_AVAILABLE:
            print("⚠️ ReportLab no está disponible. Instale con: pip install reportlab")
    
    def crear_boletin_individual(self, datos_alumno: Dict, calificaciones: List[Dict]) -> str:
        """Crear boletín individual en PDF"""
        if not REPORTLAB_AVAILABLE:
            raise ImportError("ReportLab no está instalado")
        
        try:
            export_dir = "exportaciones_pdf"
            os.makedirs(export_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            alumno_nombre = datos_alumno.get('alumno', 'Alumno').replace(' ', '_').replace(',', '')
            
            filename = f"Boletin_{alumno_nombre}_{timestamp}.pdf"
            filepath = os.path.join(export_dir, filename)
            
            # Crear documento
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            story = []
            
            # Estilos
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1
            )
            
            # Título
            title = Paragraph("🏛️ GESJ - Boletín de Calificaciones", title_style)
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Información del alumno
            info_data = [
                ['Alumno:', datos_alumno.get('alumno', 'N/A')],
                ['Curso:', f"{datos_alumno.get('curso', 'N/A')} - División {datos_alumno.get('division', 'A')}"],
                ['DNI:', datos_alumno.get('dni', 'N/A')],
                ['Período:', datos_alumno.get('periodo', 'N/A')],
                ['Fecha:', datetime.now().strftime("%d/%m/%Y")]
            ]
            
            info_table = Table(info_data, colWidths=[2*inch, 4*inch])
            info_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            
            story.append(info_table)
            story.append(Spacer(1, 20))
            
            # Tabla de calificaciones
            if calificaciones:
                cal_data = [['Materia', 'Promedio', 'Evaluaciones', 'Estado']]
                
                for cal in calificaciones:
                    promedio = float(cal.get('promedio', 0))
                    if promedio >= 9.0:
                        estado = "Excelente"
                    elif promedio >= 8.0:
                        estado = "Muy Bueno"
                    elif promedio >= 7.0:
                        estado = "Bueno"
                    elif promedio >= 6.0:
                        estado = "Regular"
                    else:
                        estado = "En Riesgo"
                    
                    cal_data.append([
                        cal.get('materia', ''),
                        str(promedio),
                        str(cal.get('evaluaciones', 0)),
                        estado
                    ])
                
                cal_table = Table(cal_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1.5*inch])
                cal_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                
                story.append(cal_table)
            
            # Generar PDF
            doc.build(story)
            return os.path.abspath(filepath)
            
        except Exception as e:
            print(f"Error al crear boletín PDF: {e}")
            raise e
    
    def crear_reporte_curso(self, datos_curso: Dict, estadisticas: Dict) -> str:
        """Crear reporte de curso en PDF"""
        if not REPORTLAB_AVAILABLE:
            raise ImportError("ReportLab no está instalado")
        
        try:
            export_dir = "exportaciones_pdf"
            os.makedirs(export_dir, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            curso = datos_curso.get('curso', 'Curso').replace(' ', '')
            division = datos_curso.get('division', 'A')
            
            filename = f"Reporte_Curso_{curso}_{division}_{timestamp}.pdf"
            filepath = os.path.join(export_dir, filename)
            
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            story = []
            
            # Título
            styles = getSampleStyleSheet()
            title = Paragraph(f"📊 Reporte de Curso - {curso} {division}", styles['Title'])
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Estadísticas generales
            if estadisticas:
                stats_data = [
                    ['Total Alumnos:', str(estadisticas.get('total_alumnos', 0))],
                    ['Promedio General:', str(estadisticas.get('promedio_curso', 0))],
                    ['Total Evaluaciones:', str(estadisticas.get('total_calificaciones', 0))],
                    ['Materias Activas:', str(estadisticas.get('total_materias', 0))]
                ]
                
                stats_table = Table(stats_data, colWidths=[2*inch, 2*inch])
                stats_table.setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                
                story.append(stats_table)
            
            doc.build(story)
            return os.path.abspath(filepath)
            
        except Exception as e:
            print(f"Error al crear reporte de curso PDF: {e}")
            raise e