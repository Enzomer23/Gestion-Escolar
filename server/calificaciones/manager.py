"""
Manager Principal del Sistema de Calificaciones
GESJ - Plataforma de Gestión Educativa
"""

from .alumnos import AlumnosOperations
from .materias import MateriasOperations
from .evaluaciones import EvaluacionesOperations
from .promedios import PromediosOperations
from .estadisticas import EstadisticasOperations
from .reportes import ReportesOperations

class CalificacionesManager:
    """Manager principal que coordina todas las operaciones de calificaciones"""
    
    def __init__(self):
        self.alumnos = AlumnosOperations()
        self.materias = MateriasOperations()
        self.evaluaciones = EvaluacionesOperations()
        self.promedios = PromediosOperations()
        self.estadisticas = EstadisticasOperations()
        self.reportes = ReportesOperations()
    
    # Delegación a módulos especializados
    def obtener_alumnos_por_curso(self, curso: str, division: str = 'A'):
        return self.alumnos.obtener_por_curso(curso, division)
    
    def obtener_alumno_por_id(self, alumno_id: int):
        return self.alumnos.obtener_por_id(alumno_id)
    
    def obtener_materias_por_docente(self, docente_id: int):
        return self.materias.obtener_por_docente(docente_id)
    
    def obtener_materias_por_curso(self, curso: str, division: str = 'A'):
        return self.materias.obtener_por_curso(curso, division)
    
    def obtener_periodos_activos(self):
        return self.evaluaciones.obtener_periodos_activos()
    
    def obtener_tipos_evaluacion(self):
        return self.evaluaciones.obtener_tipos_evaluacion()
    
    def registrar_calificacion(self, alumno_id: int, materia_id: int, docente_id: int, 
                             periodo_id: int, tipo_evaluacion_id: int, nota: float, 
                             fecha_evaluacion, observaciones: str = ""):
        return self.evaluaciones.registrar_calificacion(
            alumno_id, materia_id, docente_id, periodo_id, 
            tipo_evaluacion_id, nota, fecha_evaluacion, observaciones
        )
    
    def obtener_calificaciones_alumno(self, alumno_id: int, periodo_id: int = None):
        return self.evaluaciones.obtener_calificaciones_alumno(alumno_id, periodo_id)
    
    def obtener_calificaciones_materia(self, materia_id: int, periodo_id: int):
        return self.evaluaciones.obtener_calificaciones_materia(materia_id, periodo_id)
    
    def obtener_promedios_alumno(self, alumno_id: int, periodo_id: int = None):
        return self.promedios.obtener_promedios_alumno(alumno_id, periodo_id)
    
    def obtener_promedio_general_alumno(self, alumno_id: int, periodo_id: int):
        return self.promedios.obtener_promedio_general(alumno_id, periodo_id)
    
    def actualizar_promedios(self):
        return self.promedios.actualizar_todos()
    
    def actualizar_promedios_simple(self, alumno_id: int, materia_id: int, periodo_id: int):
        return self.promedios.actualizar_simple(alumno_id, materia_id, periodo_id)
    
    def obtener_estadisticas_curso(self, curso: str, division: str, periodo_id: int):
        return self.estadisticas.obtener_estadisticas_curso(curso, division, periodo_id)
    
    def obtener_alumnos_en_riesgo(self, periodo_id: int, promedio_minimo: float = 6.0):
        return self.estadisticas.obtener_alumnos_en_riesgo(periodo_id, promedio_minimo)
    
    def obtener_ranking_alumnos_por_promedio(self, materia_id: int, periodo_id: int):
        return self.estadisticas.obtener_ranking_alumnos(materia_id, periodo_id)
    
    def obtener_tendencias_promedios(self, materia_id: int, alumno_id: int = None):
        return self.estadisticas.obtener_tendencias_promedios(materia_id, alumno_id)
    
    def obtener_estadisticas_promedios_curso(self, curso: str, division: str, periodo_id: int):
        return self.estadisticas.obtener_estadisticas_promedios_curso(curso, division, periodo_id)