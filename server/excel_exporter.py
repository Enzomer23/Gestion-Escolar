"""
ARCHIVO DE COMPATIBILIDAD - Exportador Excel
GESJ - Plataforma de Gestión Educativa

Redirige al nuevo sistema modular de exportaciones.
"""

from .exports.excel_manager import ExcelManager

class ExcelExporter:
    """Clase de compatibilidad para ExcelExporter"""
    
    def __init__(self):
        self.excel_manager = ExcelManager()
        print("✅ Usando sistema modular de exportación Excel")
    
    def exportar_calificaciones_materia(self, materia_id: int, periodo_id: int, docente_id: int) -> str:
        """Método de compatibilidad"""
        # Obtener datos necesarios
        from .calificaciones.manager import CalificacionesManager
        cal_manager = CalificacionesManager()
        
        calificaciones = cal_manager.obtener_calificaciones_materia(materia_id, periodo_id)
        info_materia = cal_manager.materias.obtener_por_id(materia_id)
        
        return self.excel_manager.crear_workbook_calificaciones(calificaciones, info_materia or {})