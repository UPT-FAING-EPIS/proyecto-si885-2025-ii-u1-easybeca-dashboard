# Paquete de scrapers para la API de Scraping de Becas Perú

from .pronabec_scraper import PronabecScraper
from .universities_scraper import UniversitiesScraper
from .bcp_scraper import BCPScraper

__all__ = [
    'PronabecScraper',
    'UniversitiesScraper', 
    'BCPScraper'
]

__version__ = '1.0.0'
__author__ = 'API Scraping Becas Perú'
__description__ = 'Scrapers para extraer información de becas de diferentes fuentes oficiales en Perú'