# Módulo de Docentes - GESJ
# Plataforma de Gestión Educativa
# Provincia de San Juan, República Argentina

from .main import DocentesSection
from .calificaciones import CalificacionesDocenteWindow
from .reportes import ReportesDocenteWindow
from .comunicacion import ComunicacionDocenteWindow
from .recursos import RecursosDocenteWindow

__all__ = [
    'DocentesSection',
    'CalificacionesDocenteWindow',
    'ReportesDocenteWindow', 
    'ComunicacionDocenteWindow',
    'RecursosDocenteWindow'
]