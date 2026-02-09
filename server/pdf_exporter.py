"""
ARCHIVO DE COMPATIBILIDAD - Exportador PDF
GESJ - Plataforma de Gestión Educativa

Redirige al nuevo sistema modular de exportaciones.
"""

from .exports.pdf_manager import PDFManager

class PDFExporter:
    """Clase de compatibilidad para PDFExporter"""
    
    def __init__(self):
        self.pdf_manager = PDFManager()
        print("✅ Usando sistema modular de exportación PDF")
    
    def exportar_calificaciones_materia_pdf(self, materia_id: int, periodo_id: int, docente_id: int) -> str:
        """Método de compatibilidad"""
        # Obtener datos necesarios
        from .calificaciones.manager import CalificacionesManager
        cal_manager = CalificacionesManager()
        
        calificaciones = cal_manager.obtener_calificaciones_materia(materia_id, periodo_id)
        info_materia = cal_manager.materias.obtener_por_id(materia_id)
        
        return self.pdf_manager.crear_boletin_individual(info_materia or {}, calificaciones)