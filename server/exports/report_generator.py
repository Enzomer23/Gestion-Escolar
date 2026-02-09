"""
Generador de Reportes Unificado
GESJ - Plataforma de Gestión Educativa
"""

from typing import List, Dict, Optional
from .excel_manager import ExcelManager
from .pdf_manager import PDFManager
from ..calificaciones.manager import CalificacionesManager

class ReportGenerator:
    """Generador unificado de reportes en múltiples formatos"""
    
    def __init__(self):
        self.excel_manager = ExcelManager()
        self.pdf_manager = PDFManager()
        self.cal_manager = CalificacionesManager()
    
    def generar_reporte_completo(self, tipo_reporte: str, parametros: Dict, 
                               formato: str = "excel") -> str:
        """Generar reporte completo según tipo y parámetros"""
        try:
            if tipo_reporte == "calificaciones_materia":
                return self._generar_reporte_materia(parametros, formato)
            elif tipo_reporte == "promedios_curso":
                return self._generar_reporte_curso(parametros, formato)
            elif tipo_reporte == "boletin_individual":
                return self._generar_boletin_individual(parametros, formato)
            elif tipo_reporte == "estadisticas_generales":
                return self._generar_estadisticas_generales(parametros, formato)
            else:
                raise ValueError(f"Tipo de reporte no soportado: {tipo_reporte}")
                
        except Exception as e:
            print(f"Error generando reporte: {e}")
            raise e
    
    def _generar_reporte_materia(self, parametros: Dict, formato: str) -> str:
        """Generar reporte específico de materia"""
        materia_id = parametros['materia_id']
        periodo_id = parametros['periodo_id']
        
        # Obtener datos
        calificaciones = self.cal_manager.obtener_calificaciones_materia(materia_id, periodo_id)
        info_materia = parametros.get('info_materia', {})
        
        if formato.lower() == "excel":
            return self.excel_manager.crear_workbook_calificaciones(calificaciones, info_materia)
        elif formato.lower() == "pdf":
            return self.pdf_manager.crear_boletin_individual(info_materia, calificaciones)
        else:
            raise ValueError(f"Formato no soportado: {formato}")
    
    def _generar_reporte_curso(self, parametros: Dict, formato: str) -> str:
        """Generar reporte de curso completo"""
        curso = parametros['curso']
        division = parametros['division']
        periodo_id = parametros['periodo_id']
        
        # Obtener estadísticas del curso
        estadisticas = self.cal_manager.obtener_estadisticas_curso(curso, division, periodo_id)
        info_curso = {'curso': curso, 'division': division}
        
        if formato.lower() == "excel":
            # Obtener promedios para Excel
            alumnos = self.cal_manager.obtener_alumnos_por_curso(curso, division)
            promedios_data = []
            
            for alumno in alumnos:
                promedios = self.cal_manager.obtener_promedios_alumno(alumno['id'], periodo_id)
                for promedio in promedios:
                    promedios_data.append(promedio)
            
            return self.excel_manager.crear_workbook_promedios(promedios_data, info_curso)
        elif formato.lower() == "pdf":
            return self.pdf_manager.crear_reporte_curso(info_curso, estadisticas)
        else:
            raise ValueError(f"Formato no soportado: {formato}")
    
    def _generar_boletin_individual(self, parametros: Dict, formato: str) -> str:
        """Generar boletín individual de alumno"""
        alumno_id = parametros['alumno_id']
        periodo_id = parametros['periodo_id']
        
        # Obtener datos del alumno
        alumno_info = self.cal_manager.obtener_alumno_por_id(alumno_id)
        promedios = self.cal_manager.obtener_promedios_alumno(alumno_id, periodo_id)
        
        if formato.lower() == "pdf":
            return self.pdf_manager.crear_boletin_individual(alumno_info, promedios)
        else:
            raise ValueError("Boletín individual solo disponible en PDF")
    
    def _generar_estadisticas_generales(self, parametros: Dict, formato: str) -> str:
        """Generar reporte de estadísticas generales"""
        periodo_id = parametros['periodo_id']
        
        # Obtener estadísticas generales
        alumnos_riesgo = self.cal_manager.obtener_alumnos_en_riesgo(periodo_id)
        
        # Crear datos estructurados
        datos_estadisticas = {
            'alumnos_riesgo': alumnos_riesgo,
            'total_alumnos': len(alumnos_riesgo),
            'fecha_generacion': datetime.now()
        }
        
        if formato.lower() == "excel":
            return self.excel_manager.crear_workbook_calificaciones(alumnos_riesgo, datos_estadisticas)
        elif formato.lower() == "pdf":
            return self.pdf_manager.crear_reporte_curso(datos_estadisticas, {})
        else:
            raise ValueError(f"Formato no soportado: {formato}")