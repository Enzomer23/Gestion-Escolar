# Módulo de Calificaciones - Backend
# GESJ - Plataforma de Gestión Educativa
# Provincia de San Juan, República Argentina

from .manager import CalificacionesManager
from .alumnos import AlumnosOperations
from .materias import MateriasOperations
from .evaluaciones import EvaluacionesOperations
from .promedios import PromediosOperations
from .estadisticas import EstadisticasOperations
from .reportes import ReportesOperations

__all__ = [
    'CalificacionesManager',
    'AlumnosOperations',
    'MateriasOperations', 
    'EvaluacionesOperations',
    'PromediosOperations',
    'EstadisticasOperations',
    'ReportesOperations'
]