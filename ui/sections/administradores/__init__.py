# Módulo de Administradores - GESJ
# Plataforma de Gestión Educativa
# Provincia de San Juan, República Argentina

from .main import AdministradoresSection
from .dashboard import DashboardEjecutivoWindow
from .institucional import GestionInstitucionalWindow
from .analytics import AnalyticsWindow
from .recursos_humanos import RecursosHumanosWindow
from .finanzas import FinanzasWindow
from .sistema import SistemaWindow

__all__ = [
    'AdministradoresSection',
    'DashboardEjecutivoWindow',
    'GestionInstitucionalWindow',
    'AnalyticsWindow',
    'RecursosHumanosWindow',
    'FinanzasWindow',
    'SistemaWindow'
]