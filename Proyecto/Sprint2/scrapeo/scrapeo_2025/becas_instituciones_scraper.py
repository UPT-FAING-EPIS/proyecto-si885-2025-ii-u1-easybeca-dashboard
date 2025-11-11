#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper de Instituciones por Beca
Extrae información detallada de las instituciones educativas donde se ofrecen las becas
Similar al formato de Beca 18 con universidades y modalidades
Autor: Sistema de Scraping Integral
Fecha: 2025
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import logging
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import re
from datetime import datetime

class BecasInstitucionesScraper:
    """
    Scraper para extraer instituciones educativas por cada beca
    """
    
    def __init__(self):
        self.setup_logging()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Datos de instituciones por beca
        self.instituciones_por_beca = self._inicializar_instituciones_data()
    
    def setup_logging(self):
        """Configura el sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('becas_instituciones_scraper.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _inicializar_instituciones_data(self) -> Dict:
        """Inicializa la estructura de datos de instituciones por beca"""
        return {
            'beca_18': {
                'nombre_beca': 'Beca 18',
                'tipo_instituciones': 'Universidades',
                'total_instituciones': 95,
                'instituciones': [
                    # Se cargarían las 95 universidades de Beca 18
                    # Por ahora incluimos algunas de ejemplo
                    {
                        'nombre': 'Universidad Nacional de Barranca',
                        'tipo': 'Pública',
                        'ubicacion': 'Lima',
                        'estado': 'Licenciada',
                        'modalidades_disponibles': ['Ordinaria', 'EIB', 'Protección']
                    },
                    {
                        'nombre': 'Universidad Nacional Hermilio Valdizán',
                        'tipo': 'Pública', 
                        'ubicacion': 'Huánuco',
                        'estado': 'Licenciada',
                        'modalidades_disponibles': ['Ordinaria', 'Vraem']
                    }
                    # ... resto de universidades
                ]
            },
            
            'beca_tec': {
                'nombre_beca': 'Beca Tec',
                'tipo_instituciones': 'Institutos Técnicos',
                'total_instituciones': 28,
                'instituciones': [
                    # LIMA
                    {
                        'nombre': 'EEST Privada ADEX',
                        'tipo': 'Privada',
                        'ubicacion': 'San Borja, Lima',
                        'region': 'Lima',
                        'programas': [
                            {'nombre': 'Administración de Negocios Internacionales', 'modalidad': 'Presencial/Semipresencial'},
                            {'nombre': 'Gestión Administrativa', 'modalidad': 'Presencial/Semipresencial'},
                            {'nombre': 'Gestión Logística', 'modalidad': 'Presencial/Semipresencial'},
                            {'nombre': 'Marketing', 'modalidad': 'Presencial/Semipresencial'}
                        ]
                    },
                    {
                        'nombre': 'EEST Privada Corriente Alterna',
                        'tipo': 'Privada',
                        'ubicacion': 'La Victoria, Lima',
                        'region': 'Lima',
                        'programas': [
                            {'nombre': 'Diseño de Interiores', 'modalidad': 'Semipresencial'},
                            {'nombre': 'Diseño Gráfico', 'modalidad': 'Semipresencial'},
                            {'nombre': 'Marketing', 'modalidad': 'Semipresencial'}
                        ]
                    },
                    {
                        'nombre': 'EEST Privada IDAT',
                        'tipo': 'Privada',
                        'ubicacion': 'San Juan de Miraflores, Lima',
                        'region': 'Lima',
                        'sedes': 'Múltiples sedes',
                        'programas': [
                            {'nombre': 'Administración de Negocios Bancarios y Financieros', 'modalidad': 'Presencial'},
                            {'nombre': 'Administración de Negocios Internacionales', 'modalidad': 'Presencial'},
                            {'nombre': 'Contabilidad', 'modalidad': 'Presencial'},
                            {'nombre': 'Desarrollo de Sistemas de Información', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño de Interiores', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño Gráfico Visual', 'modalidad': 'Presencial'},
                            {'nombre': 'Gestión Administrativa', 'modalidad': 'Presencial'},
                            {'nombre': 'Gestión de Recursos Humanos', 'modalidad': 'Presencial'},
                            {'nombre': 'Marketing', 'modalidad': 'Presencial'}
                        ]
                    },
                    {
                        'nombre': 'EEST Privada Toulouse Lautrec',
                        'tipo': 'Privada',
                        'ubicacion': 'Magdalena del Mar y Santiago de Surco, Lima',
                        'region': 'Lima',
                        'sedes': 'Múltiples sedes',
                        'programas': [
                            {'nombre': 'Animación Digital', 'modalidad': 'Presencial'},
                            {'nombre': 'Cinematografía', 'modalidad': 'Presencial'},
                            {'nombre': 'Comunicación Audiovisual', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño de Interiores', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño de Videojuegos y Entretenimiento Digital', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño Gráfico', 'modalidad': 'Presencial'},
                            {'nombre': 'Fotografía e Imagen Digital', 'modalidad': 'Presencial'},
                            {'nombre': 'Marketing', 'modalidad': 'Presencial'},
                            {'nombre': 'Publicidad y Medios Digitales', 'modalidad': 'Presencial'}
                        ]
                    },
                    
                    # AREQUIPA
                    {
                        'nombre': 'EEST Privada Toulouse Lautrec',
                        'tipo': 'Privada',
                        'ubicacion': 'Arequipa',
                        'region': 'Arequipa',
                        'programas': [
                            {'nombre': 'Animación Digital', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño de Interiores', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño Gráfico', 'modalidad': 'Presencial'},
                            {'nombre': 'Marketing', 'modalidad': 'Presencial'},
                            {'nombre': 'Publicidad y Medios Digitales', 'modalidad': 'Presencial'}
                        ]
                    },
                    {
                        'nombre': 'IES Privado del Sur',
                        'tipo': 'Privada',
                        'ubicacion': 'Arequipa',
                        'region': 'Arequipa',
                        'programas': [
                            {'nombre': 'Administración de Negocios Bancarios y Financieros', 'modalidad': 'Presencial'},
                            {'nombre': 'Administración de Negocios Internacionales', 'modalidad': 'Presencial'},
                            {'nombre': 'Administración de Servicios de Hostelería y Restaurantes', 'modalidad': 'Presencial'},
                            {'nombre': 'Desarrollo de Sistemas de Información', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño de Modas', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño Gráfico y Multimedia', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño y Decoración de Interiores', 'modalidad': 'Presencial'},
                            {'nombre': 'Gastronomía', 'modalidad': 'Presencial'},
                            {'nombre': 'Gestión Administrativa', 'modalidad': 'Presencial'},
                            {'nombre': 'Guía Oficial de Turismo', 'modalidad': 'Presencial'},
                            {'nombre': 'Marketing', 'modalidad': 'Presencial'}
                        ]
                    },
                    {
                        'nombre': 'IES Privado Instituto Politécnico',
                        'tipo': 'Privada',
                        'ubicacion': 'Arequipa',
                        'region': 'Arequipa',
                        'programas': [
                            {'nombre': 'Administración de Empresas', 'modalidad': 'Presencial'},
                            {'nombre': 'Contabilidad con Mención en Procesos de Tributación', 'modalidad': 'Presencial'},
                            {'nombre': 'Enfermería Técnica', 'modalidad': 'Presencial'},
                            {'nombre': 'Farmacia Técnica', 'modalidad': 'Presencial'}
                        ]
                    },
                    
                    # CUSCO
                    {
                        'nombre': 'EEST Privada Khipu',
                        'tipo': 'Privada',
                        'ubicacion': 'Cusco',
                        'region': 'Cusco',
                        'programas': [
                            {'nombre': 'Administración de Empresas', 'modalidad': 'Presencial'},
                            {'nombre': 'Administración de Hoteles y Restaurantes', 'modalidad': 'Presencial'}
                        ]
                    },
                    {
                        'nombre': 'IES Privado Khipu',
                        'tipo': 'Privada',
                        'ubicacion': 'Cusco y San Sebastián',
                        'region': 'Cusco',
                        'sedes': 'Múltiples sedes',
                        'programas': [
                            # Cusco
                            {'nombre': 'Desarrollo de Sistemas de Información', 'modalidad': 'Presencial', 'sede': 'Cusco'},
                            {'nombre': 'Gastronomía', 'modalidad': 'Presencial', 'sede': 'Cusco'},
                            {'nombre': 'Guía Oficial de Turismo', 'modalidad': 'Presencial', 'sede': 'Cusco'},
                            # San Sebastián
                            {'nombre': 'Administración de Negocios Bancarios y Financieros', 'modalidad': 'Presencial', 'sede': 'San Sebastián'},
                            {'nombre': 'Administración de Negocios Internacionales', 'modalidad': 'Presencial', 'sede': 'San Sebastián'},
                            {'nombre': 'Contabilidad', 'modalidad': 'Presencial', 'sede': 'San Sebastián'},
                            {'nombre': 'Marketing', 'modalidad': 'Presencial', 'sede': 'San Sebastián'}
                        ]
                    },
                    {
                        'nombre': 'IES Privado Antonio Lorena',
                        'tipo': 'Privada',
                        'ubicacion': 'San Sebastián, Cusco',
                        'region': 'Cusco',
                        'programas': [
                            {'nombre': 'Enfermería Técnica', 'modalidad': 'Presencial'},
                            {'nombre': 'Farmacia Técnica', 'modalidad': 'Presencial'}
                        ]
                    },
                    
                    # LAMBAYEQUE
                    {
                        'nombre': 'IES Privado Cumbre',
                        'tipo': 'Privada',
                        'ubicacion': 'Chiclayo',
                        'region': 'Lambayeque',
                        'programas': [
                            {'nombre': 'Gastronomía', 'modalidad': 'Presencial'}
                        ]
                    },
                    {
                        'nombre': 'IES Privado de Emprendedores ISAG',
                        'tipo': 'Privada',
                        'ubicacion': 'Chiclayo y La Victoria',
                        'region': 'Lambayeque',
                        'sedes': 'Múltiples sedes',
                        'programas': [
                            # Chiclayo
                            {'nombre': 'Administración de Empresas', 'modalidad': 'Presencial', 'sede': 'Chiclayo'},
                            {'nombre': 'Administración de Servicios de Hostelería y Restaurantes', 'modalidad': 'Presencial', 'sede': 'Chiclayo'},
                            {'nombre': 'Contabilidad', 'modalidad': 'Presencial', 'sede': 'Chiclayo'},
                            {'nombre': 'Enfermería Técnica', 'modalidad': 'Presencial', 'sede': 'Chiclayo'},
                            {'nombre': 'Farmacia Técnica', 'modalidad': 'Presencial', 'sede': 'Chiclayo'},
                            {'nombre': 'Fisioterapia y Rehabilitación', 'modalidad': 'Presencial', 'sede': 'Chiclayo'},
                            {'nombre': 'Gastronomía', 'modalidad': 'Presencial', 'sede': 'Chiclayo'},
                            # La Victoria
                            {'nombre': 'Desarrollo de Sistemas de la Información', 'modalidad': 'Presencial', 'sede': 'La Victoria'},
                            {'nombre': 'Diseño Publicitario', 'modalidad': 'Presencial', 'sede': 'La Victoria'},
                            {'nombre': 'Traducción e Interpretación de Idiomas', 'modalidad': 'Presencial', 'sede': 'La Victoria'}
                        ]
                    }
                    # LAMBAYEQUE (continuación)
                    {
                        'nombre': 'IES Privado IDAT',
                        'tipo': 'Privada',
                        'ubicacion': 'Chiclayo',
                        'region': 'Lambayeque',
                        'programas': [
                            {'nombre': 'Administración de Negocios Bancarios y Financieros', 'modalidad': 'Presencial'},
                            {'nombre': 'Administración de Negocios Internacionales', 'modalidad': 'Presencial'},
                            {'nombre': 'Contabilidad', 'modalidad': 'Presencial'},
                            {'nombre': 'Desarrollo de Sistemas de Información', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño de Interiores', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño Gráfico', 'modalidad': 'Presencial'},
                            {'nombre': 'Gestión Administrativa', 'modalidad': 'Presencial'},
                            {'nombre': 'Marketing', 'modalidad': 'Presencial'}
                        ]
                    },
                    {
                        'nombre': 'IES Privado Instituto Politécnico',
                        'tipo': 'Privada',
                        'ubicacion': 'Pimentel',
                        'region': 'Lambayeque',
                        'programas': [
                            {'nombre': 'Administración de Negocios Internacionales', 'modalidad': 'Presencial'},
                            {'nombre': 'Enfermería Técnica', 'modalidad': 'Presencial'},
                            {'nombre': 'Farmacia Técnica', 'modalidad': 'Presencial'},
                            {'nombre': 'Fisioterapia y Rehabilitación', 'modalidad': 'Presencial'}
                        ]
                    },
                    {
                        'nombre': 'IES Privado Manuel Mesones Muro-Master System',
                        'tipo': 'Privada',
                        'ubicacion': 'Chiclayo',
                        'region': 'Lambayeque',
                        'programas': [
                            {'nombre': 'Enfermería Técnica', 'modalidad': 'Presencial'},
                            {'nombre': 'Farmacia Técnica', 'modalidad': 'Presencial'}
                        ]
                    },
                    {
                        'nombre': 'IES Privado Pedro Cieza de León',
                        'tipo': 'Privada',
                        'ubicacion': 'Chiclayo',
                        'region': 'Lambayeque',
                        'programas': [
                            {'nombre': 'Enfermería Técnica', 'modalidad': 'Presencial'},
                            {'nombre': 'Farmacia Técnica', 'modalidad': 'Presencial'},
                            {'nombre': 'Gestión Administrativa', 'modalidad': 'Presencial'}
                        ]
                    },
                    
                    # PIURA
                    {
                        'nombre': 'IES Privado Ceturgh Perú',
                        'tipo': 'Privada',
                        'ubicacion': 'Piura y Sullana',
                        'region': 'Piura',
                        'sedes': 'Múltiples sedes',
                        'programas': [
                            # Piura
                            {'nombre': 'Administración de Servicios de Hostelería y Restaurantes', 'modalidad': 'Presencial', 'sede': 'Piura'},
                            {'nombre': 'Gastronomía', 'modalidad': 'Presencial', 'sede': 'Piura'},
                            {'nombre': 'Aviación Comercial (Técnico)', 'modalidad': 'Presencial', 'sede': 'Piura'},
                            {'nombre': 'Bar y Coctelería (Técnico)', 'modalidad': 'Presencial', 'sede': 'Piura'},
                            {'nombre': 'Cocina (Técnico)', 'modalidad': 'Presencial', 'sede': 'Piura'},
                            {'nombre': 'Panadería y Pastelería (Técnico)', 'modalidad': 'Presencial', 'sede': 'Piura'},
                            # Sullana
                            {'nombre': 'Bar y Coctelería (Técnico)', 'modalidad': 'Presencial', 'sede': 'Sullana'},
                            {'nombre': 'Cocina (Técnico)', 'modalidad': 'Presencial', 'sede': 'Sullana'},
                            {'nombre': 'Panadería y Pastelería (Técnico)', 'modalidad': 'Presencial', 'sede': 'Sullana'}
                        ]
                    },
                    {
                        'nombre': 'IES Privado IDAT',
                        'tipo': 'Privada',
                        'ubicacion': 'Piura',
                        'region': 'Piura',
                        'programas': [
                            {'nombre': 'Administración de Negocios Bancarios y Financieros', 'modalidad': 'Presencial'},
                            {'nombre': 'Administración de Negocios Internacionales', 'modalidad': 'Presencial'},
                            {'nombre': 'Contabilidad', 'modalidad': 'Presencial'},
                            {'nombre': 'Desarrollo de Sistemas de Información', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño Gráfico', 'modalidad': 'Presencial'},
                            {'nombre': 'Gestión Administrativa', 'modalidad': 'Presencial'},
                            {'nombre': 'Marketing', 'modalidad': 'Presencial'}
                        ]
                    },
                    {
                        'nombre': 'IES Privado Instituto Politécnico',
                        'tipo': 'Privada',
                        'ubicacion': 'Piura',
                        'region': 'Piura',
                        'programas': [
                            {'nombre': 'Administración de Empresas', 'modalidad': 'Presencial'},
                            {'nombre': 'Arquitectura de Plataformas y Servicios de TI con Mención en Programación Multimedia', 'modalidad': 'Presencial'},
                            {'nombre': 'Contabilidad con Mención en Procesos de Tributación', 'modalidad': 'Presencial'},
                            {'nombre': 'Enfermería Técnica', 'modalidad': 'Presencial'}
                        ]
                    },
                    
                    # LA LIBERTAD
                    {
                        'nombre': 'IES Privado Cibertec',
                        'tipo': 'Privada',
                        'ubicacion': 'Trujillo',
                        'region': 'La Libertad',
                        'programas': [
                            {'nombre': 'Administración de Negocios Internacionales', 'modalidad': 'Presencial'},
                            {'nombre': 'Computación e Informática', 'modalidad': 'Presencial'},
                            {'nombre': 'Contabilidad', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño de Interiores', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño Gráfico', 'modalidad': 'Presencial'},
                            {'nombre': 'Gestión de Recursos Humanos', 'modalidad': 'Presencial'},
                            {'nombre': 'Marketing', 'modalidad': 'Presencial'},
                            {'nombre': 'Publicidad y Branding', 'modalidad': 'Presencial'},
                            {'nombre': 'Seguridad y Prevención de Riesgos', 'modalidad': 'Presencial'}
                        ]
                    },
                    
                    # JUNÍN
                    {
                        'nombre': 'IES Privado Centro Peruano de Estudios Bancarios - CEPEBAN',
                        'tipo': 'Privada',
                        'ubicacion': 'Huancayo',
                        'region': 'Junín',
                        'programas': [
                            {'nombre': 'Administración de Negocios Bancarios y Financieros', 'modalidad': 'Presencial'}
                        ]
                    },
                    {
                        'nombre': 'IES Privado Continental',
                        'tipo': 'Privada',
                        'ubicacion': 'Huancayo',
                        'region': 'Junín',
                        'programas': [
                            {'nombre': 'Administración de Empresas', 'modalidad': 'Presencial'},
                            {'nombre': 'Administración de Negocios Bancarios y Financieros', 'modalidad': 'Presencial'},
                            {'nombre': 'Contabilidad', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño de Interiores', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño de Modas', 'modalidad': 'Presencial'},
                            {'nombre': 'Diseño Gráfico Publicitario', 'modalidad': 'Presencial'},
                            {'nombre': 'Gastronomía', 'modalidad': 'Presencial'},
                            {'nombre': 'Gestión de la Construcción', 'modalidad': 'Presencial'}
                        ]
                    },
                    {
                        'nombre': 'IES Privado Interamericano',
                        'tipo': 'Privada',
                        'ubicacion': 'Huancayo',
                        'region': 'Junín',
                        'programas': [
                            {'nombre': 'Construcción Civil', 'modalidad': 'Presencial'},
                            {'nombre': 'Electricidad Industrial', 'modalidad': 'Presencial'},
                            {'nombre': 'Gestión Logística', 'modalidad': 'Presencial'},
                            {'nombre': 'Mantenimiento de Maquinaria Pesada', 'modalidad': 'Presencial'}
                        ]
                    },
                    
                    # TACNA
                    {
                        'nombre': 'IES Privado John Von Neumann',
                        'tipo': 'Privada',
                        'ubicacion': 'Tacna',
                        'region': 'Tacna',
                        'programas': [
                            {'nombre': 'Administración de Negocios Internacionales', 'modalidad': 'Presencial'},
                            {'nombre': 'Contabilidad', 'modalidad': 'Presencial'}
                        ]
                    },
                    
                    # AYACUCHO
                    {
                        'nombre': 'IES Privado CESDE',
                        'tipo': 'Privada',
                        'ubicacion': 'Carmen Alto',
                        'region': 'Ayacucho',
                        'programas': [
                            {'nombre': 'Administración de Centros de Cómputo', 'modalidad': 'Presencial'},
                            {'nombre': 'Administración de Negocios Bancarios y Financieros', 'modalidad': 'Presencial'},
                            {'nombre': 'Asistencia Administrativa', 'modalidad': 'Presencial'},
                            {'nombre': 'Contabilidad', 'modalidad': 'Presencial'},
                            {'nombre': 'Enfermería Técnica', 'modalidad': 'Presencial'},
                            {'nombre': 'Entrenamiento Deportivo', 'modalidad': 'Presencial'},
                            {'nombre': 'Gestión Administrativa', 'modalidad': 'Presencial'},
                            {'nombre': 'Gestión de Recursos Humanos', 'modalidad': 'Presencial'},
                            {'nombre': 'Marketing', 'modalidad': 'Presencial'}
                        ]
                    },
                    {
                        'nombre': 'IES Privado La Pontificia',
                        'tipo': 'Privada',
                        'ubicacion': 'Carmen Alto y Andrés Avelino Cáceres',
                        'region': 'Ayacucho',
                        'sedes': 'Múltiples sedes',
                        'programas': [
                            {'nombre': 'Administración de Empresas', 'modalidad': 'Presencial'},
                            {'nombre': 'Contabilidad', 'modalidad': 'Presencial'},
                            {'nombre': 'Enfermería Técnica', 'modalidad': 'Presencial'}
                        ]
                    },
                    
                    # SAN MARTÍN
                    {
                        'nombre': 'IES Privado Amazónico',
                        'tipo': 'Privada',
                        'ubicacion': 'Tarapoto',
                        'region': 'San Martín',
                        'programas': [
                            {'nombre': 'Contabilidad', 'modalidad': 'Presencial'},
                            {'nombre': 'Enfermería Técnica', 'modalidad': 'Presencial'},
                            {'nombre': 'Gestión Administrativa', 'modalidad': 'Presencial'}
                        ]
                    },
                    {
                        'nombre': 'IES Privado Ciro Alegría',
                        'tipo': 'Privada',
                        'ubicacion': 'Morales',
                        'region': 'San Martín',
                        'programas': [
                            {'nombre': 'Contabilidad', 'modalidad': 'Presencial'},
                            {'nombre': 'Enfermería Técnica', 'modalidad': 'Presencial'},
                            {'nombre': 'Farmacia Técnica', 'modalidad': 'Presencial'},
                            {'nombre': 'Gestión Administrativa', 'modalidad': 'Presencial'},
                            {'nombre': 'Mecatrónica Automotriz', 'modalidad': 'Presencial'}
                        ]
                    }
                ]
            },
            
            'beca_peru': {
                'nombre_beca': 'Beca Perú',
                'tipo_instituciones': 'Universidades Privadas Participantes',
                'total_instituciones': 'Variable',
                'instituciones': [
                    # Se cargarían las universidades privadas participantes
                    {
                        'nombre': 'Universidad Privada del Norte',
                        'tipo': 'Privada',
                        'ubicacion': 'Lima y provincias',
                        'estado': 'Licenciada',
                        'programas_disponibles': 'Pregrado'
                    },
                    {
                        'nombre': 'Universidad César Vallejo',
                        'tipo': 'Privada',
                        'ubicacion': 'Lima y provincias',
                        'estado': 'Licenciada',
                        'programas_disponibles': 'Pregrado'
                    }
                    # ... resto de universidades participantes
                ]
            },
            
            'beca_generacion_bicentenario': {
                'nombre_beca': 'Beca Generación Bicentenario',
                'tipo_instituciones': 'Universidades Top 400 Mundial',
                'total_instituciones': 'Top 400',
                'criterio_seleccion': 'Rankings internacionales (QS, THE, ARWU)',
                'instituciones': [
                    # Ejemplos de universidades elegibles
                    {
                        'nombre': 'Harvard University',
                        'pais': 'Estados Unidos',
                        'ranking_qs': 1,
                        'programas_disponibles': 'Maestrías y Doctorados'
                    },
                    {
                        'nombre': 'Stanford University',
                        'pais': 'Estados Unidos',
                        'ranking_qs': 3,
                        'programas_disponibles': 'Maestrías y Doctorados'
                    },
                    {
                        'nombre': 'University of Cambridge',
                        'pais': 'Reino Unido',
                        'ranking_qs': 2,
                        'programas_disponibles': 'Maestrías y Doctorados'
                    }
                    # ... resto de universidades top 400
                ]
            },
            
            'chevening': {
                'nombre_beca': 'Becas Chevening',
                'tipo_instituciones': 'Universidades del Reino Unido',
                'total_instituciones': 'Todas las universidades elegibles del Reino Unido',
                'instituciones': [
                    {
                        'nombre': 'University of Oxford',
                        'pais': 'Reino Unido',
                        'ubicacion': 'Oxford',
                        'programas_disponibles': 'Maestrías de un año'
                    },
                    {
                        'nombre': 'University of Cambridge',
                        'pais': 'Reino Unido',
                        'ubicacion': 'Cambridge',
                        'programas_disponibles': 'Maestrías de un año'
                    },
                    {
                        'nombre': 'Imperial College London',
                        'pais': 'Reino Unido',
                        'ubicacion': 'Londres',
                        'programas_disponibles': 'Maestrías de un año'
                    }
                    # ... resto de universidades del Reino Unido
                ]
            },
            
            'fulbright': {
                'nombre_beca': 'Becas Fulbright',
                'tipo_instituciones': 'Universidades de Estados Unidos',
                'total_instituciones': 'Universidades acreditadas de EE.UU.',
                'instituciones': [
                    {
                        'nombre': 'Massachusetts Institute of Technology (MIT)',
                        'pais': 'Estados Unidos',
                        'ubicacion': 'Cambridge, Massachusetts',
                        'programas_disponibles': 'Maestrías y Doctorados'
                    },
                    {
                        'nombre': 'University of California, Berkeley',
                        'pais': 'Estados Unidos',
                        'ubicacion': 'Berkeley, California',
                        'programas_disponibles': 'Maestrías y Doctorados'
                    }
                    # ... resto de universidades de EE.UU.
                ]
            }
        }
    
    def expandir_datos_instituciones(self) -> List[Dict]:
        """Expande los datos para crear registros beca-institución-programa"""
        datos_expandidos = []
        
        for codigo_beca, info_beca in self.instituciones_por_beca.items():
            nombre_beca = info_beca['nombre_beca']
            tipo_instituciones = info_beca['tipo_instituciones']
            
            for institucion in info_beca['instituciones']:
                nombre_institucion = institucion['nombre']
                tipo_institucion = institucion.get('tipo', 'No especificado')
                ubicacion = institucion.get('ubicacion', 'No especificado')
                region = institucion.get('region', 'No especificado')
                
                # Si la institución tiene programas
                if 'programas' in institucion:
                    for programa in institucion['programas']:
                        registro = {
                            'codigo_beca': codigo_beca,
                            'nombre_beca': nombre_beca,
                            'tipo_instituciones': tipo_instituciones,
                            'nombre_institucion': nombre_institucion,
                            'tipo_institucion': tipo_institucion,
                            'ubicacion': ubicacion,
                            'region': region,
                            'sedes': institucion.get('sedes', 'Sede única'),
                            'programa': programa['nombre'],
                            'modalidad_programa': programa['modalidad'],
                            'sede_programa': programa.get('sede', ubicacion)
                        }
                        datos_expandidos.append(registro)
                else:
                    # Para becas sin programas específicos (como becas internacionales)
                    registro = {
                        'codigo_beca': codigo_beca,
                        'nombre_beca': nombre_beca,
                        'tipo_instituciones': tipo_instituciones,
                        'nombre_institucion': nombre_institucion,
                        'tipo_institucion': tipo_institucion,
                        'ubicacion': ubicacion,
                        'region': region,
                        'sedes': 'No aplica',
                        'programa': institucion.get('programas_disponibles', 'Todos los programas elegibles'),
                        'modalidad_programa': 'Variable',
                        'sede_programa': ubicacion
                    }
                    datos_expandidos.append(registro)
        
        return datos_expandidos
    
    def generar_estadisticas_instituciones(self, datos_expandidos: List[Dict]) -> Dict:
        """Genera estadísticas de las instituciones por beca"""
        estadisticas = {
            'fecha_generacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_registros': len(datos_expandidos),
            'total_becas': len(self.instituciones_por_beca),
            'resumen_por_beca': {},
            'resumen_por_region': {},
            'resumen_por_tipo_institucion': {},
            'programas_mas_comunes': {}
        }
        
        # Estadísticas por beca
        for codigo_beca, info_beca in self.instituciones_por_beca.items():
            registros_beca = [r for r in datos_expandidos if r['codigo_beca'] == codigo_beca]
            instituciones_unicas = len(set(r['nombre_institucion'] for r in registros_beca))
            programas_unicos = len(set(r['programa'] for r in registros_beca))
            
            estadisticas['resumen_por_beca'][codigo_beca] = {
                'nombre_beca': info_beca['nombre_beca'],
                'total_registros': len(registros_beca),
                'instituciones_unicas': instituciones_unicas,
                'programas_unicos': programas_unicos,
                'tipo_instituciones': info_beca['tipo_instituciones']
            }
        
        # Estadísticas por región
        regiones = {}
        for registro in datos_expandidos:
            region = registro['region']
            if region not in regiones:
                regiones[region] = {'total_registros': 0, 'instituciones': set(), 'becas': set()}
            regiones[region]['total_registros'] += 1
            regiones[region]['instituciones'].add(registro['nombre_institucion'])
            regiones[region]['becas'].add(registro['nombre_beca'])
        
        for region, datos in regiones.items():
            estadisticas['resumen_por_region'][region] = {
                'total_registros': datos['total_registros'],
                'instituciones_unicas': len(datos['instituciones']),
                'becas_disponibles': len(datos['becas'])
            }
        
        # Estadísticas por tipo de institución
        tipos = {}
        for registro in datos_expandidos:
            tipo = registro['tipo_institucion']
            if tipo not in tipos:
                tipos[tipo] = {'total_registros': 0, 'instituciones': set()}
            tipos[tipo]['total_registros'] += 1
            tipos[tipo]['instituciones'].add(registro['nombre_institucion'])
        
        for tipo, datos in tipos.items():
            estadisticas['resumen_por_tipo_institucion'][tipo] = {
                'total_registros': datos['total_registros'],
                'instituciones_unicas': len(datos['instituciones'])
            }
        
        # Programas más comunes
        programas = {}
        for registro in datos_expandidos:
            programa = registro['programa']
            if programa not in programas:
                programas[programa] = {'frecuencia': 0, 'becas': set(), 'instituciones': set()}
            programas[programa]['frecuencia'] += 1
            programas[programa]['becas'].add(registro['nombre_beca'])
            programas[programa]['instituciones'].add(registro['nombre_institucion'])
        
        # Top 10 programas más comunes
        programas_ordenados = sorted(programas.items(), key=lambda x: x[1]['frecuencia'], reverse=True)[:10]
        for programa, datos in programas_ordenados:
            estadisticas['programas_mas_comunes'][programa] = {
                'frecuencia': datos['frecuencia'],
                'becas_que_lo_ofrecen': len(datos['becas']),
                'instituciones_que_lo_ofrecen': len(datos['instituciones'])
            }
        
        return estadisticas
    
    def guardar_csv_instituciones(self, datos_expandidos: List[Dict], nombre_archivo: str):
        """Guarda los datos expandidos en formato CSV"""
        try:
            df = pd.DataFrame(datos_expandidos)
            df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
            self.logger.info(f"Archivo CSV guardado: {nombre_archivo}")
            self.logger.info(f"Total de registros: {len(datos_expandidos)}")
        except Exception as e:
            self.logger.error(f"Error al guardar CSV {nombre_archivo}: {str(e)}")
    
    def guardar_json_instituciones(self, datos: Dict, nombre_archivo: str):
        """Guarda los datos en formato JSON"""
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            self.logger.info(f"Archivo JSON guardado: {nombre_archivo}")
        except Exception as e:
            self.logger.error(f"Error al guardar JSON {nombre_archivo}: {str(e)}")
    
    def generar_reporte_por_beca(self, datos_expandidos: List[Dict]):
        """Genera reportes individuales por cada beca"""
        for codigo_beca, info_beca in self.instituciones_por_beca.items():
            registros_beca = [r for r in datos_expandidos if r['codigo_beca'] == codigo_beca]
            
            if registros_beca:
                # CSV por beca
                nombre_csv = f"instituciones_{codigo_beca}.csv"
                df_beca = pd.DataFrame(registros_beca)
                df_beca.to_csv(nombre_csv, index=False, encoding='utf-8-sig')
                
                # Estadísticas por beca
                instituciones_unicas = len(set(r['nombre_institucion'] for r in registros_beca))
                programas_unicos = len(set(r['programa'] for r in registros_beca))
                regiones_unicas = len(set(r['region'] for r in registros_beca))
                
                self.logger.info(f"\n=== {info_beca['nombre_beca']} ===")
                self.logger.info(f"Total registros: {len(registros_beca)}")
                self.logger.info(f"Instituciones únicas: {instituciones_unicas}")
                self.logger.info(f"Programas únicos: {programas_unicos}")
                self.logger.info(f"Regiones con presencia: {regiones_unicas}")
                self.logger.info(f"Archivo generado: {nombre_csv}")
    
    def ejecutar_procesamiento_completo(self):
        """Ejecuta el procesamiento completo de instituciones por beca"""
        self.logger.info("=== INICIANDO PROCESAMIENTO DE INSTITUCIONES POR BECA ===")
        
        # Expandir datos
        self.logger.info("Expandiendo datos de instituciones...")
        datos_expandidos = self.expandir_datos_instituciones()
        
        # Generar estadísticas
        self.logger.info("Generando estadísticas...")
        estadisticas = self.generar_estadisticas_instituciones(datos_expandidos)
        
        # Guardar archivo principal CSV
        self.logger.info("Guardando archivo CSV principal...")
        self.guardar_csv_instituciones(datos_expandidos, "becas_instituciones_completo.csv")
        
        # Guardar archivo principal JSON
        datos_completos = {
            'metadatos': {
                'descripcion': 'Instituciones educativas por beca - Formato expandido',
                'fecha_generacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'version': '1.0',
                'total_registros': len(datos_expandidos)
            },
            'estadisticas': estadisticas,
            'datos': datos_expandidos
        }
        
        self.logger.info("Guardando archivo JSON principal...")
        self.guardar_json_instituciones(datos_completos, "becas_instituciones_completo.json")
        
        # Generar reportes individuales por beca
        self.logger.info("Generando reportes individuales por beca...")
        self.generar_reporte_por_beca(datos_expandidos)
        
        # Guardar solo estadísticas
        self.logger.info("Guardando estadísticas...")
        self.guardar_json_instituciones(estadisticas, "estadisticas_instituciones.json")
        
        self.logger.info("\n=== PROCESAMIENTO COMPLETADO ===")
        self.logger.info(f"Total de registros procesados: {len(datos_expandidos)}")
        self.logger.info(f"Total de becas procesadas: {len(self.instituciones_por_beca)}")
        
        return datos_expandidos, estadisticas


def main():
    """Función principal"""
    scraper = BecasInstitucionesScraper()
    datos_expandidos, estadisticas = scraper.ejecutar_procesamiento_completo()
    
    print("\n=== RESUMEN FINAL ===")
    print(f"Total de registros generados: {len(datos_expandidos)}")
    print(f"Total de becas procesadas: {estadisticas['total_becas']}")
    print("\nArchivos generados:")
    print("- becas_instituciones_completo.csv")
    print("- becas_instituciones_completo.json")
    print("- estadisticas_instituciones.json")
    print("- instituciones_[codigo_beca].csv (por cada beca)")
    
    print("\n=== ESTADÍSTICAS POR BECA ===")
    for codigo_beca, stats in estadisticas['resumen_por_beca'].items():
        print(f"{stats['nombre_beca']}: {stats['total_registros']} registros, {stats['instituciones_unicas']} instituciones")


if __name__ == "__main__":
    main()