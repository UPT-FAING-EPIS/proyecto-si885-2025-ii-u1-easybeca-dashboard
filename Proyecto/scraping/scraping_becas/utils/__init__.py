# Paquete de utilidades para la API de Scraping de Becas Perú

from .helpers import (
    timing_decorator,
    DataValidator,
    TextCleaner,
    ExcelProcessor,
    URLValidator,
    ScrapingStatus,
    ExcelComparator
)

__all__ = [
    'timing_decorator',
    'DataValidator',
    'TextCleaner',
    'ExcelProcessor',
    'URLValidator',
    'ScrapingStatus',
    'ExcelComparator'
]

__version__ = '1.0.0'
__author__ = 'API Scraping Becas Perú'
__description__ = 'Utilidades y helpers para el sistema de scraping de becas'