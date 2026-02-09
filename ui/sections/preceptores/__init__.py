# Módulo de Preceptores - GESJ
# Plataforma de Gestión Educativa
# Provincia de San Juan, República Argentina

from .main import PreceptoresSection
from .tendencias import TendenciasAcademicasWindow
from .trayectorias import TrayectoriasEscolaresWindow
from .planes import PlanesIntervencionWindow
from .reconocimientos import ReconocimientosWindow

__all__ = [
    'PreceptoresSection',
    'TendenciasAcademicasWindow', 
    'TrayectoriasEscolaresWindow',
    'PlanesIntervencionWindow',
    'ReconocimientosWindow'
]