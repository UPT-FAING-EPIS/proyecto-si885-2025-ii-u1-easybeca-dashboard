#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper Integral de Becas en Perú
Extrae información de todas las becas disponibles: PRONABEC, MINEDU, CONCYTEC, internacionales, etc.
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

class BecasIntegralesScraper:
    """
    Scraper integral para todas las becas disponibles en Perú
    """
    
    def __init__(self):
        self.setup_logging()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # URLs oficiales de las diferentes instituciones
        self.urls_oficiales = {
            'pronabec': 'https://www.pronabec.gob.pe/',
            'minedu': 'https://www.gob.pe/minedu',
            'concytec': 'https://portal.concytec.gob.pe/',
            'sernanp': 'https://www.gob.pe/sernanp',
            'chevening': 'https://www.chevening.org/scholarships/who-can-apply/peru/',
            'fulbright': 'https://pe.usembassy.gov/education-culture/educational-exchanges/fulbright-program/',
            'erasmus': 'https://erasmus-plus.ec.europa.eu/',
            'daad': 'https://www.daad.de/en/',
            'campus_france': 'https://www.campusfrance.org/en',
            'mext_japan': 'https://www.studyinjapan.go.jp/en/',
            'gks_korea': 'https://www.studyinkorea.go.kr/en/',
            'csc_china': 'https://www.campuschina.org/'
        }
        
        # Estructura completa de becas
        self.becas_data = self._inicializar_becas_data()
    
    def setup_logging(self):
        """Configura el sistema de logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('becas_integrales_scraper.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _inicializar_becas_data(self) -> Dict:
        """Inicializa la estructura de datos de todas las becas"""
        return {
            # BECAS PRONABEC
            'beca_18': {
                'nombre': 'Beca 18',
                'institucion': 'PRONABEC',
                'categoria': 'Pregrado',
                'tipo_estudio': 'Universitario',
                'modalidad': 'Presencial',
                'cobertura': 'Completa',
                'cantidad_becas': 'Variable por convocatoria',
                'modalidades_especificas': [
                    'Ordinaria', 'Huallaga', 'Vraem', 'EIB', 'Protección', 
                    'CNA y PA', 'FF.AA.', 'Repared'
                ],
                'requisitos_generales': 'Tercio superior o medio superior según modalidad',
                'edad_limite': '22 años (algunas modalidades)',
                'postulacion_2025': 'Por confirmar',
                'url_oficial': 'https://www.pronabec.gob.pe/beca-18/',
                'estado': 'Activa'
            },
            
            'beca_tec': {
                'nombre': 'Beca Tec',
                'institucion': 'PRONABEC',
                'categoria': 'Técnico',
                'tipo_estudio': 'Técnico Superior y Técnico-Productivo',
                'modalidad': 'Presencial únicamente',
                'cobertura': 'Costo de estudios técnicos',
                'cantidad_becas': '300 becas (30 auxiliar técnico, 90 técnico, 180 profesionales técnicos)',
                'modalidades_especificas': ['Auxiliar Técnico', 'Técnico', 'Profesional Técnico'],
                'requisitos_generales': 'Estudios técnicos superiores',
                'edad_limite': 'Variable',
                'postulacion_2025': 'Por confirmar',
                'url_oficial': 'https://www.pronabec.gob.pe/beca-tec/',
                'estado': 'Activa'
            },
            
            'beca_peru': {
                'nombre': 'Beca Perú',
                'institucion': 'PRONABEC (coordinación)',
                'categoria': 'Pregrado',
                'tipo_estudio': 'Universitario Privado',
                'modalidad': 'Presencial',
                'cobertura': 'Variable según universidad',
                'cantidad_becas': 'Variable',
                'modalidades_especificas': ['Universidades Privadas Participantes'],
                'requisitos_generales': 'Según cada universidad participante',
                'caracteristica_especial': 'No subvencionada por PRONABEC, sino por las propias universidades',
                'oportunidades': 'Dos momentos de postulación',
                'postulacion_2025': 'Del 14/04/2025 al 14/05/2025',
                'url_oficial': 'https://www.pronabec.gob.pe/beca-peru/',
                'estado': 'Activa'
            },
            
            'beca_generacion_bicentenario': {
                'nombre': 'Beca Generación Bicentenario',
                'institucion': 'PRONABEC',
                'categoria': 'Posgrado',
                'tipo_estudio': 'Maestrías y Doctorados',
                'modalidad': 'Presencial en el extranjero',
                'cobertura': 'Completa',
                'cantidad_becas': 'Variable',
                'requisitos_generales': 'Profesionales peruanos con alto rendimiento académico',
                'edad_limite': 'Sin límite de edad',
                'universidades_elegibles': 'Top 400 mejores universidades del mundo',
                'inicio_estudios': 'Entre 06/03/2025 y 31/12/2026',
                'postulacion_2025': 'Del 14 de abril (fecha exacta por confirmar)',
                'url_oficial': 'https://www.pronabec.gob.pe/beca-generacion-bicentenario/',
                'estado': 'Activa'
            },
            
            'beca_presidente_republica': {
                'nombre': 'Beca Presidente de la República',
                'institucion': 'PRONABEC',
                'categoria': 'Posgrado',
                'tipo_estudio': 'Maestrías y Doctorados',
                'modalidad': 'Nacional e Internacional',
                'cobertura': 'Estudios de posgrado completos',
                'cantidad_becas': 'Variable',
                'requisitos_generales': 'Profesionales destacados',
                'caracteristicas': 'Para profesionales destacados',
                'url_oficial': 'https://www.pronabec.gob.pe/beca-presidente-republica/',
                'estado': 'Activa'
            },
            
            'credito_educativo': {
                'nombre': 'Crédito Educativo',
                'institucion': 'PRONABEC',
                'categoria': 'Financiamiento',
                'tipo_estudio': 'Estudios Superiores',
                'modalidad': 'Préstamo con condiciones preferenciales',
                'cobertura': 'Financiamiento de estudios superiores',
                'devolucion': 'Después de culminar los estudios',
                'url_oficial': 'https://www.pronabec.gob.pe/credito-educativo/',
                'estado': 'Activa'
            },
            
            # BECAS MINEDU
            'beca_vocacion_maestro': {
                'nombre': 'Beca Vocación de Maestro',
                'institucion': 'MINEDU',
                'categoria': 'Pregrado',
                'tipo_estudio': 'Estudios de Educación',
                'modalidad': 'Presencial',
                'cobertura': 'Completa',
                'enfoque': 'Formación docente',
                'url_oficial': 'https://www.gob.pe/minedu',
                'estado': 'Activa'
            },
            
            'beca_formacion_servicio': {
                'nombre': 'Beca de Formación en Servicio',
                'institucion': 'MINEDU',
                'categoria': 'Capacitación',
                'tipo_estudio': 'Formación Continua',
                'modalidad': 'Presencial/Virtual',
                'cobertura': 'Variable',
                'dirigido_a': 'Docentes en ejercicio',
                'url_oficial': 'https://www.gob.pe/minedu',
                'estado': 'Activa'
            },
            
            # BECAS CONCYTEC
            'becas_concytec': {
                'nombre': 'Becas CONCYTEC',
                'institucion': 'CONCYTEC',
                'categoria': 'Posgrado',
                'tipo_estudio': 'Estudios de posgrado en ciencia y tecnología',
                'modalidad': 'Nacional/Internacional',
                'cobertura': 'Variable',
                'enfoque': 'Investigación científica y desarrollo tecnológico',
                'url_oficial': 'https://portal.concytec.gob.pe/',
                'estado': 'Activa'
            },
            
            # BECAS SERNANP
            'becas_sernanp': {
                'nombre': 'Becas SERNANP',
                'institucion': 'SERNANP',
                'categoria': 'Especialización',
                'tipo_estudio': 'Estudios relacionados con áreas naturales protegidas',
                'modalidad': 'Variable',
                'cobertura': 'Variable',
                'enfoque': 'Conservación y medio ambiente',
                'url_oficial': 'https://www.gob.pe/sernanp',
                'estado': 'Activa'
            },
            
            # BECAS INTERNACIONALES
            'chevening': {
                'nombre': 'Becas Chevening',
                'institucion': 'Gobierno del Reino Unido',
                'categoria': 'Posgrado',
                'tipo_estudio': 'Maestrías de un año en Reino Unido',
                'modalidad': 'Presencial en Reino Unido',
                'cobertura': 'Completa',
                'requisitos_generales': 'Liderazgo y potencial profesional',
                'pais_destino': 'Reino Unido',
                'url_oficial': 'https://www.chevening.org/scholarships/who-can-apply/peru/',
                'estado': 'Activa'
            },
            
            'fulbright': {
                'nombre': 'Becas Fulbright',
                'institucion': 'Gobierno de Estados Unidos',
                'categoria': 'Posgrado',
                'tipo_estudio': 'Maestrías y doctorados en EE.UU.',
                'modalidad': 'Presencial en Estados Unidos',
                'cobertura': 'Completa',
                'modalidades_especificas': 'Diversas según programa',
                'pais_destino': 'Estados Unidos',
                'url_oficial': 'https://pe.usembassy.gov/education-culture/educational-exchanges/fulbright-program/',
                'estado': 'Activa'
            },
            
            'erasmus_plus': {
                'nombre': 'Becas Erasmus+',
                'institucion': 'Unión Europea',
                'categoria': 'Pregrado/Posgrado',
                'tipo_estudio': 'Estudios e intercambios en Europa',
                'modalidad': 'Presencial en Europa',
                'cobertura': 'Variable',
                'modalidades_especificas': 'Pregrado, posgrado, movilidad académica',
                'pais_destino': 'Países de la Unión Europea',
                'url_oficial': 'https://erasmus-plus.ec.europa.eu/',
                'estado': 'Activa'
            },
            
            'daad': {
                'nombre': 'Becas DAAD',
                'institucion': 'Gobierno de Alemania',
                'categoria': 'Pregrado/Posgrado',
                'tipo_estudio': 'Estudios en Alemania',
                'modalidad': 'Presencial en Alemania',
                'cobertura': 'Variable',
                'niveles': 'Pregrado, posgrado, investigación',
                'pais_destino': 'Alemania',
                'url_oficial': 'https://www.daad.de/en/',
                'estado': 'Activa'
            },
            
            'gobierno_frances': {
                'nombre': 'Becas del Gobierno Francés',
                'institucion': 'Gobierno de Francia',
                'categoria': 'Pregrado/Posgrado',
                'tipo_estudio': 'Estudios en Francia',
                'modalidad': 'Presencial en Francia',
                'cobertura': 'Variable',
                'programa': 'Campus France',
                'pais_destino': 'Francia',
                'url_oficial': 'https://www.campusfrance.org/en',
                'estado': 'Activa'
            },
            
            'mext_japon': {
                'nombre': 'Becas del Gobierno Japonés (MEXT)',
                'institucion': 'Gobierno de Japón',
                'categoria': 'Pregrado/Posgrado',
                'tipo_estudio': 'Pregrado, posgrado e investigación en Japón',
                'modalidad': 'Presencial en Japón',
                'cobertura': 'Completa',
                'pais_destino': 'Japón',
                'url_oficial': 'https://www.studyinjapan.go.jp/en/',
                'estado': 'Activa'
            },
            
            'gks_corea': {
                'nombre': 'Becas Corea del Sur (GKS)',
                'institucion': 'Gobierno de Corea del Sur',
                'categoria': 'Pregrado/Posgrado',
                'tipo_estudio': 'Pregrado y posgrado en Corea del Sur',
                'modalidad': 'Presencial en Corea del Sur',
                'cobertura': 'Completa',
                'pais_destino': 'Corea del Sur',
                'url_oficial': 'https://www.studyinkorea.go.kr/en/',
                'estado': 'Activa'
            },
            
            'csc_china': {
                'nombre': 'Becas China (CSC)',
                'institucion': 'Gobierno de China',
                'categoria': 'Pregrado/Posgrado',
                'tipo_estudio': 'Estudios en universidades chinas',
                'modalidad': 'Presencial en China',
                'cobertura': 'Variable',
                'pais_destino': 'China',
                'url_oficial': 'https://www.campuschina.org/',
                'estado': 'Activa'
            },
            
            # BECAS REGIONALES/MUNICIPALES
            'becas_regionales': {
                'nombre': 'Becas de Gobiernos Regionales',
                'institucion': 'Gobiernos Regionales',
                'categoria': 'Variable',
                'tipo_estudio': 'Variable',
                'modalidad': 'Variable',
                'cobertura': 'Variable',
                'ejemplos': 'Beca Región Lima, becas regionales del Cusco, etc.',
                'caracteristica': 'Cada región puede tener programas específicos',
                'estado': 'Variable por región'
            },
            
            'becas_municipales': {
                'nombre': 'Becas Municipales',
                'institucion': 'Municipalidades',
                'categoria': 'Variable',
                'tipo_estudio': 'Variable',
                'modalidad': 'Variable',
                'cobertura': 'Variable',
                'dirigido_a': 'Estudiantes destacados de la localidad',
                'alcance': 'Municipalidades provinciales y distritales',
                'estado': 'Variable por municipio'
            },
            
            # BECAS PRIVADAS Y FUNDACIONES
            'fundacion_romero': {
                'nombre': 'Beca Fundación Romero',
                'institucion': 'Fundación Romero',
                'categoria': 'Pregrado',
                'tipo_estudio': 'Estudios superiores',
                'modalidad': 'Variable',
                'cobertura': 'Variable',
                'enfoque': 'Estudiantes de alto rendimiento',
                'url_oficial': 'https://www.fundacionromero.org.pe/',
                'estado': 'Activa'
            },
            
            'fundacion_telefonica': {
                'nombre': 'Becas Fundación Telefónica',
                'institucion': 'Fundación Telefónica',
                'categoria': 'Capacitación',
                'tipo_estudio': 'Capacitación y estudios tecnológicos',
                'modalidad': 'Presencial/Virtual',
                'cobertura': 'Variable',
                'enfoque': 'Tecnología y capacitación',
                'url_oficial': 'https://www.fundaciontelefonica.com.pe/',
                'estado': 'Activa'
            },
            
            'universidades_privadas': {
                'nombre': 'Becas de Universidades Privadas',
                'institucion': 'Universidades Privadas',
                'categoria': 'Pregrado/Posgrado',
                'tipo_estudio': 'Variable',
                'modalidad': 'Variable',
                'cobertura': 'Variable',
                'criterios': [
                    'Excelencia académica',
                    'Situación socioeconómica',
                    'Deportes',
                    'Arte y cultura',
                    'Liderazgo'
                ],
                'caracteristica': 'Cada universidad puede ofrecer sus propias becas',
                'estado': 'Variable por universidad'
            },
            
            'becas_empresariales': {
                'nombre': 'Becas Empresariales',
                'institucion': 'Empresas Privadas',
                'categoria': 'Variable',
                'tipo_estudio': 'Variable',
                'modalidad': 'Variable',
                'cobertura': 'Variable',
                'ejemplos': [
                    'Mineras (Antamina, Southern, etc.)',
                    'Bancos (BCP, Interbank, etc.)',
                    'Empresas diversas con programas de responsabilidad social'
                ],
                'enfoque': 'Responsabilidad social empresarial',
                'estado': 'Variable por empresa'
            }
        }
    
    def obtener_informacion_pronabec(self) -> Dict:
        """Extrae información actualizada de PRONABEC"""
        try:
            self.logger.info("Extrayendo información de PRONABEC...")
            url = self.urls_oficiales['pronabec']
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar información de becas en la página principal
            becas_info = {}
            
            # Buscar enlaces a becas específicas
            enlaces_becas = soup.find_all('a', href=True)
            for enlace in enlaces_becas:
                href = enlace.get('href', '').lower()
                texto = enlace.get_text(strip=True).lower()
                
                if 'beca' in texto or 'beca' in href:
                    if 'beca-18' in href or 'beca 18' in texto:
                        becas_info['beca_18_url'] = urljoin(url, enlace['href'])
                    elif 'beca-tec' in href or 'beca tec' in texto:
                        becas_info['beca_tec_url'] = urljoin(url, enlace['href'])
                    elif 'beca-peru' in href or 'beca perú' in texto:
                        becas_info['beca_peru_url'] = urljoin(url, enlace['href'])
            
            self.logger.info(f"Información de PRONABEC extraída: {len(becas_info)} enlaces encontrados")
            return becas_info
            
        except Exception as e:
            self.logger.error(f"Error al extraer información de PRONABEC: {str(e)}")
            return {}
    
    def obtener_informacion_internacional(self) -> Dict:
        """Extrae información de becas internacionales"""
        becas_internacionales = {}
        
        for nombre_beca, url in self.urls_oficiales.items():
            if nombre_beca in ['chevening', 'fulbright', 'erasmus', 'daad', 'campus_france', 'mext_japan', 'gks_korea', 'csc_china']:
                try:
                    self.logger.info(f"Extrayendo información de {nombre_beca}...")
                    response = self.session.get(url, timeout=30)
                    response.raise_for_status()
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extraer información básica
                    titulo = soup.find('title')
                    descripcion = soup.find('meta', attrs={'name': 'description'})
                    
                    becas_internacionales[nombre_beca] = {
                        'titulo_pagina': titulo.get_text(strip=True) if titulo else '',
                        'descripcion': descripcion.get('content', '') if descripcion else '',
                        'url_verificada': url,
                        'estado_conexion': 'Activa'
                    }
                    
                    time.sleep(2)  # Pausa entre requests
                    
                except Exception as e:
                    self.logger.error(f"Error al extraer información de {nombre_beca}: {str(e)}")
                    becas_internacionales[nombre_beca] = {
                        'estado_conexion': 'Error',
                        'error': str(e)
                    }
        
        return becas_internacionales
    
    def categorizar_becas(self) -> Dict:
        """Categoriza todas las becas por nivel de estudios"""
        categorias = {
            'pregrado': [],
            'posgrado': [],
            'tecnico': [],
            'capacitacion': [],
            'financiamiento': [],
            'variable': []
        }
        
        for codigo_beca, info_beca in self.becas_data.items():
            categoria = info_beca.get('categoria', '').lower()
            
            if categoria == 'pregrado':
                categorias['pregrado'].append(codigo_beca)
            elif categoria == 'posgrado':
                categorias['posgrado'].append(codigo_beca)
            elif categoria == 'técnico' or categoria == 'tecnico':
                categorias['tecnico'].append(codigo_beca)
            elif categoria == 'capacitación' or categoria == 'capacitacion':
                categorias['capacitacion'].append(codigo_beca)
            elif categoria == 'financiamiento':
                categorias['financiamiento'].append(codigo_beca)
            else:
                categorias['variable'].append(codigo_beca)
        
        return categorias
    
    def generar_resumen_estadisticas(self) -> Dict:
        """Genera estadísticas resumidas de todas las becas"""
        estadisticas = {
            'total_becas': len(self.becas_data),
            'por_institucion': {},
            'por_categoria': {},
            'por_modalidad': {},
            'becas_activas': 0,
            'becas_internacionales': 0,
            'becas_nacionales': 0
        }
        
        for codigo_beca, info_beca in self.becas_data.items():
            # Por institución
            institucion = info_beca.get('institucion', 'No especificada')
            if institucion not in estadisticas['por_institucion']:
                estadisticas['por_institucion'][institucion] = 0
            estadisticas['por_institucion'][institucion] += 1
            
            # Por categoría
            categoria = info_beca.get('categoria', 'No especificada')
            if categoria not in estadisticas['por_categoria']:
                estadisticas['por_categoria'][categoria] = 0
            estadisticas['por_categoria'][categoria] += 1
            
            # Por modalidad
            modalidad = info_beca.get('modalidad', 'No especificada')
            if modalidad not in estadisticas['por_modalidad']:
                estadisticas['por_modalidad'][modalidad] = 0
            estadisticas['por_modalidad'][modalidad] += 1
            
            # Estado
            if info_beca.get('estado') == 'Activa':
                estadisticas['becas_activas'] += 1
            
            # Nacional vs Internacional
            if 'pais_destino' in info_beca:
                estadisticas['becas_internacionales'] += 1
            else:
                estadisticas['becas_nacionales'] += 1
        
        return estadisticas
    
    def guardar_datos_csv(self, datos_completos: Dict, categorias: Dict, estadisticas: Dict):
        """Guarda todos los datos en archivos CSV"""
        try:
            # CSV principal con todas las becas
            filas_principales = []
            for codigo_beca, info_beca in datos_completos.items():
                fila = {
                    'codigo_beca': codigo_beca,
                    'nombre': info_beca.get('nombre', ''),
                    'institucion': info_beca.get('institucion', ''),
                    'categoria': info_beca.get('categoria', ''),
                    'tipo_estudio': info_beca.get('tipo_estudio', ''),
                    'modalidad': info_beca.get('modalidad', ''),
                    'cobertura': info_beca.get('cobertura', ''),
                    'cantidad_becas': info_beca.get('cantidad_becas', ''),
                    'requisitos_generales': info_beca.get('requisitos_generales', ''),
                    'edad_limite': info_beca.get('edad_limite', ''),
                    'postulacion_2025': info_beca.get('postulacion_2025', ''),
                    'url_oficial': info_beca.get('url_oficial', ''),
                    'estado': info_beca.get('estado', ''),
                    'pais_destino': info_beca.get('pais_destino', 'Perú'),
                    'enfoque': info_beca.get('enfoque', ''),
                    'caracteristicas_especiales': str(info_beca.get('modalidades_especificas', []))
                }
                filas_principales.append(fila)
            
            df_principal = pd.DataFrame(filas_principales)
            df_principal.to_csv('becas_integrales_completo.csv', index=False, encoding='utf-8-sig')
            self.logger.info(f"Archivo CSV principal guardado: {len(filas_principales)} becas")
            
            # CSV por categorías
            filas_categorias = []
            for categoria, lista_becas in categorias.items():
                for codigo_beca in lista_becas:
                    info_beca = datos_completos.get(codigo_beca, {})
                    fila = {
                        'categoria_nivel': categoria,
                        'codigo_beca': codigo_beca,
                        'nombre': info_beca.get('nombre', ''),
                        'institucion': info_beca.get('institucion', ''),
                        'tipo_estudio': info_beca.get('tipo_estudio', ''),
                        'modalidad': info_beca.get('modalidad', ''),
                        'cobertura': info_beca.get('cobertura', ''),
                        'url_oficial': info_beca.get('url_oficial', ''),
                        'estado': info_beca.get('estado', '')
                    }
                    filas_categorias.append(fila)
            
            df_categorias = pd.DataFrame(filas_categorias)
            df_categorias.to_csv('becas_por_categorias.csv', index=False, encoding='utf-8-sig')
            self.logger.info(f"Archivo CSV por categorías guardado: {len(filas_categorias)} entradas")
            
            # CSV de estadísticas
            filas_estadisticas = []
            for tipo_stat, datos_stat in estadisticas.items():
                if isinstance(datos_stat, dict):
                    for clave, valor in datos_stat.items():
                        filas_estadisticas.append({
                            'tipo_estadistica': tipo_stat,
                            'categoria': clave,
                            'cantidad': valor
                        })
                else:
                    filas_estadisticas.append({
                        'tipo_estadistica': tipo_stat,
                        'categoria': 'Total',
                        'cantidad': datos_stat
                    })
            
            df_estadisticas = pd.DataFrame(filas_estadisticas)
            df_estadisticas.to_csv('becas_estadisticas.csv', index=False, encoding='utf-8-sig')
            self.logger.info(f"Archivo CSV de estadísticas guardado: {len(filas_estadisticas)} entradas")
            
        except Exception as e:
            self.logger.error(f"Error al guardar archivos CSV: {str(e)}")
    
    def guardar_datos_json(self, datos_completos: Dict, categorias: Dict, estadisticas: Dict, info_web: Dict):
        """Guarda todos los datos en formato JSON"""
        try:
            datos_json = {
                'fecha_extraccion': datetime.now().isoformat(),
                'version': '1.0',
                'descripcion': 'Base de datos integral de becas en Perú',
                'estadisticas': estadisticas,
                'categorias': categorias,
                'becas': datos_completos,
                'informacion_web': info_web,
                'fuentes_oficiales': self.urls_oficiales
            }
            
            with open('becas_integrales_completo.json', 'w', encoding='utf-8') as f:
                json.dump(datos_json, f, ensure_ascii=False, indent=2)
            
            self.logger.info("Archivo JSON completo guardado")
            
        except Exception as e:
            self.logger.error(f"Error al guardar archivo JSON: {str(e)}")
    
    def ejecutar_scraping_completo(self):
        """Ejecuta el scraping completo de todas las becas"""
        self.logger.info("=== INICIANDO SCRAPING INTEGRAL DE BECAS ===")
        
        # Extraer información web
        info_pronabec = self.obtener_informacion_pronabec()
        info_internacional = self.obtener_informacion_internacional()
        
        # Combinar información web con datos base
        info_web = {
            'pronabec': info_pronabec,
            'internacional': info_internacional
        }
        
        # Categorizar becas
        categorias = self.categorizar_becas()
        
        # Generar estadísticas
        estadisticas = self.generar_resumen_estadisticas()
        
        # Guardar archivos
        self.guardar_datos_csv(self.becas_data, categorias, estadisticas)
        self.guardar_datos_json(self.becas_data, categorias, estadisticas, info_web)
        
        # Resumen final
        self.logger.info("=== SCRAPING COMPLETADO ===")
        self.logger.info(f"Total de becas procesadas: {estadisticas['total_becas']}")
        self.logger.info(f"Becas activas: {estadisticas['becas_activas']}")
        self.logger.info(f"Becas nacionales: {estadisticas['becas_nacionales']}")
        self.logger.info(f"Becas internacionales: {estadisticas['becas_internacionales']}")
        
        print("\n=== RESUMEN DE BECAS POR CATEGORÍA ===")
        for categoria, cantidad in estadisticas['por_categoria'].items():
            print(f"{categoria}: {cantidad} becas")
        
        print("\n=== RESUMEN DE BECAS POR INSTITUCIÓN ===")
        for institucion, cantidad in estadisticas['por_institucion'].items():
            print(f"{institucion}: {cantidad} becas")
        
        return {
            'becas': self.becas_data,
            'categorias': categorias,
            'estadisticas': estadisticas,
            'info_web': info_web
        }

def main():
    """Función principal"""
    scraper = BecasIntegralesScraper()
    resultado = scraper.ejecutar_scraping_completo()
    return resultado

if __name__ == "__main__":
    main()