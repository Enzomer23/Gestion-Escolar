# Módulo de Calificaciones - GESJ
# Plataforma de Gestión Educativa
# Provincia de San Juan, República Argentina

from .main import CalificacionesSection
from .registro import RegistroCalificacionesWindow
from .consulta import ConsultaCalificacionesWindow
from .promedios import PromediosAvanzadosWindow
from .estadisticas import EstadisticasWindow
from .reportes import ReportesCalificacionesWindow
from .exportacion import ExportacionWindow
from .alertas import AlertasAcademicasWindow

__all__ = [
    'CalificacionesSection',
    'RegistroCalificacionesWindow',
    'ConsultaCalificacionesWindow',
    'PromediosAvanzadosWindow',
    'EstadisticasWindow',
    'ReportesCalificacionesWindow',
    'ExportacionWindow',
    'AlertasAcademicasWindow'
]