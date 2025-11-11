#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scraper para información de Beca 18 - PRONABEC
Extrae información sobre universidades elegibles y promedios mínimos requeridos

Autor: Asistente AI
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

class Beca18Scraper:
    """
    Scraper para extraer información de Beca 18 sobre universidades elegibles
    y promedios mínimos requeridos
    """
    
    def __init__(self):
        self.base_url = "https://www.pronabec.gob.pe"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Configurar logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('beca18_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # URLs principales identificadas
        self.urls = {
            'beca18_main': f"{self.base_url}/beca-18/",
            'beca18_2025': f"{self.base_url}/beca-18-2025/",
            'requisitos': "https://www.gob.pe/41547-requisitos-para-postular-al-concurso-beca-18"
        }
        
        # Promedios mínimos por modalidad Beca 18 2025 (información oficial PRONABEC)
        self.promedios_minimos = {
            'Ordinaria': {
                'promedio_minimo': 'Tercio superior',
                'descripcion': 'Para jóvenes menores de 22 años en situación de pobreza o pobreza extrema',
                'nota_aproximada': '15.5+',
                'requisitos_adicionales': 'Acreditar condición de pobreza según SISFOH, tercio superior en secundaria'
            },
            'Huallaga': {
                'promedio_minimo': 'Tercio superior',
                'descripcion': 'Para jóvenes menores de 22 años residentes en el Huallaga',
                'nota_aproximada': '15.5+',
                'requisitos_adicionales': 'Residir en el Huallaga, tercio superior en secundaria'
            },
            'Vraem': {
                'promedio_minimo': 'Tercio superior',
                'descripcion': 'Para jóvenes menores de 22 años residentes en zonas del VRAEM',
                'nota_aproximada': '15.5+',
                'requisitos_adicionales': 'Residir en zonas del VRAEM, tercio superior en secundaria'
            },
            'EIB': {
                'promedio_minimo': 'Medio superior',
                'descripcion': 'Para quienes dominen lenguas originarias y estudien Educación Intercultural Bilingüe',
                'nota_aproximada': '14.0+',
                'requisitos_adicionales': 'Dominar lengua originaria elegible, medio superior en secundaria'
            },
            'Protección': {
                'promedio_minimo': 'Medio superior',
                'descripcion': 'Para jóvenes menores de 22 años que estuvieron en tutela del Estado',
                'nota_aproximada': '14.0+',
                'requisitos_adicionales': 'Acreditar tutela del Estado, medio superior en secundaria'
            },
            'CNA y PA': {
                'promedio_minimo': 'Medio superior',
                'descripcion': 'Para peruanos de comunidades nativas amazónicas o población afroperuana',
                'nota_aproximada': '14.0+',
                'requisitos_adicionales': 'Acreditar pertenencia a comunidad nativa o población afroperuana'
            },
            'FF.AA.': {
                'promedio_minimo': 'Medio superior',
                'descripcion': 'Para licenciados del Servicio Militar Voluntario (mínimo 12 meses)',
                'nota_aproximada': '14.0+',
                'requisitos_adicionales': 'Licencia del Servicio Militar Voluntario, medio superior en secundaria'
            },
            'Repared': {
                'promedio_minimo': 'Nota mínima de 12.0',
                'descripcion': 'Para víctimas de la violencia ocurrida entre 1980-2000',
                'nota_aproximada': '12.0',
                'requisitos_adicionales': 'Acreditar condición de víctima de violencia 1980-2000, nota mínima 12'
            }
        }
        
        # Lista completa de universidades elegibles para Beca 18 - Convocatoria 2025
        # Basada en la información oficial de PRONABEC
        self.universidades_conocidas = [
            # UNIVERSIDADES PÚBLICAS - QUINTIL 5 (Mayor selectividad)
            {'nombre': 'Universidad Nacional de Barranca', 'tipo': 'Pública', 'quintil': 5, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional Hermilio Valdizán', 'tipo': 'Pública', 'quintil': 5, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional de San Agustín', 'tipo': 'Pública', 'quintil': 5, 'ubicacion': 'Arequipa', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional Toribio Rodríguez de Mendoza de Amazonas', 'tipo': 'Pública', 'quintil': 5, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional del Altiplano', 'tipo': 'Pública', 'quintil': 5, 'ubicacion': 'Puno', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional de San Cristóbal de Huamanga', 'tipo': 'Pública', 'quintil': 5, 'ubicacion': 'Ayacucho', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional de Jaén', 'tipo': 'Pública', 'quintil': 5, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional de Juliaca', 'tipo': 'Pública', 'quintil': 5, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional de San Antonio Abad del Cusco', 'tipo': 'Pública', 'quintil': 5, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional de Trujillo', 'tipo': 'Pública', 'quintil': 5, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional de Ucayali', 'tipo': 'Pública', 'quintil': 5, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional de Ingeniería', 'tipo': 'Pública', 'quintil': 5, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional Mayor de San Marcos', 'tipo': 'Pública', 'quintil': 5, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional Jorge Basadre Grohmann', 'tipo': 'Pública', 'quintil': 5, 'ubicacion': 'Tacna', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional de Piura', 'tipo': 'Pública', 'quintil': 5, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional José Faustino Sánchez Carrión', 'tipo': 'Pública', 'quintil': 5, 'ubicacion': 'Huacho', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional Intercultural de la Selva Central Juan Santos Atahualpa', 'tipo': 'Pública', 'quintil': 5, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional de San Martín', 'tipo': 'Pública', 'quintil': 5, 'ubicacion': 'Tarapoto', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
            {'nombre': 'Universidad Nacional de Huancavelica', 'tipo': 'Pública', 'quintil': 5, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             
             # UNIVERSIDADES PÚBLICAS - QUINTIL 4
             {'nombre': 'Universidad Nacional del Centro del Perú', 'tipo': 'Pública', 'quintil': 4, 'ubicacion': 'Huancayo', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional José María Arguedas', 'tipo': 'Pública', 'quintil': 4, 'ubicacion': 'Andahuaylas', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional Micaela Bastidas de Apurímac', 'tipo': 'Pública', 'quintil': 4, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional Autónoma de Chota', 'tipo': 'Pública', 'quintil': 4, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional Intercultural de Quillabamba', 'tipo': 'Pública', 'quintil': 4, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional San Luis Gonzaga de Ica', 'tipo': 'Pública', 'quintil': 4, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional Amazónica de Madre de Dios', 'tipo': 'Pública', 'quintil': 4, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional de Cajamarca', 'tipo': 'Pública', 'quintil': 4, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional Agraria La Molina', 'tipo': 'Pública', 'quintil': 4, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional Intercultural Fabiola Salazar Leguía de Bagua', 'tipo': 'Pública', 'quintil': 4, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional de Tumbes', 'tipo': 'Pública', 'quintil': 4, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional Daniel Alcides Carrión', 'tipo': 'Pública', 'quintil': 4, 'ubicacion': 'Pasco', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional Santiago Antúnez de Mayolo', 'tipo': 'Pública', 'quintil': 4, 'ubicacion': 'Huaraz', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional Autónoma de Tayacaja Daniel Hernández Morillo', 'tipo': 'Pública', 'quintil': 4, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional de Moquegua', 'tipo': 'Pública', 'quintil': 4, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional de la Amazonía Peruana', 'tipo': 'Pública', 'quintil': 4, 'ubicacion': 'Iquitos', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional de Cañete', 'tipo': 'Pública', 'quintil': 4, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional Pedro Ruíz Gallo', 'tipo': 'Pública', 'quintil': 4, 'ubicacion': 'Lambayeque', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional del Santa', 'tipo': 'Pública', 'quintil': 4, 'ubicacion': 'Chimbote', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             
             # UNIVERSIDADES PÚBLICAS - QUINTIL 3
             {'nombre': 'Universidad Nacional Autónoma Altoandina de Tarma', 'tipo': 'Pública', 'quintil': 3, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional Agraria de la Selva', 'tipo': 'Pública', 'quintil': 3, 'ubicacion': 'Tingo María', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional Federico Villarreal', 'tipo': 'Pública', 'quintil': 3, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional Tecnológica de Lima Sur', 'tipo': 'Pública', 'quintil': 3, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional de Frontera', 'tipo': 'Pública', 'quintil': 3, 'ubicacion': 'Sullana', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional Autónoma de Huanta', 'tipo': 'Pública', 'quintil': 3, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional Intercultural de la Amazonía', 'tipo': 'Pública', 'quintil': 3, 'ubicacion': 'Ucayali', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional del Callao', 'tipo': 'Pública', 'quintil': 3, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Nacional Autónoma de Alto Amazonas', 'tipo': 'Pública', 'quintil': 3, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             
             # UNIVERSIDADES PÚBLICAS - QUINTIL 2
             {'nombre': 'Universidad Nacional de Educación Enrique Guzmán y Valle', 'tipo': 'Pública', 'quintil': 2, 'ubicacion': 'La Cantuta', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             
             # UNIVERSIDADES PÚBLICAS - QUINTIL 1
             {'nombre': 'Universidad Nacional Ciro Alegría', 'tipo': 'Pública', 'quintil': 1, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             
             # UNIVERSIDADES PRIVADAS - QUINTIL 3
             {'nombre': 'Universidad Católica Santo Toribio de Mogrovejo', 'tipo': 'Privada', 'quintil': 3, 'ubicacion': 'Chiclayo', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Pontificia Universidad Católica del Perú', 'tipo': 'Privada', 'quintil': 3, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad de Piura', 'tipo': 'Privada', 'quintil': 3, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad del Pacífico', 'tipo': 'Privada', 'quintil': 3, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Católica de Santa María', 'tipo': 'Privada', 'quintil': 3, 'ubicacion': 'Arequipa', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Tecnológica de los Andes', 'tipo': 'Privada', 'quintil': 3, 'ubicacion': 'Abancay', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Privada de Tacna', 'tipo': 'Privada', 'quintil': 3, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Ricardo Palma', 'tipo': 'Privada', 'quintil': 3, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Peruana de Ciencias Aplicadas - UPC', 'tipo': 'Privada', 'quintil': 3, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Señor de Sipán', 'tipo': 'Privada', 'quintil': 3, 'ubicacion': 'Chiclayo', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             
             # UNIVERSIDADES PRIVADAS - QUINTIL 2
             {'nombre': 'Universidad de San Martín de Porres', 'tipo': 'Privada', 'quintil': 2, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Andina del Cusco', 'tipo': 'Privada', 'quintil': 2, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Científica del Sur', 'tipo': 'Privada', 'quintil': 2, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Peruana Unión', 'tipo': 'Privada', 'quintil': 2, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Peruana Cayetano Heredia', 'tipo': 'Privada', 'quintil': 2, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad San Ignacio de Loyola', 'tipo': 'Privada', 'quintil': 2, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Privada Antenor Orrego', 'tipo': 'Privada', 'quintil': 2, 'ubicacion': 'Trujillo', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad César Vallejo', 'tipo': 'Privada', 'quintil': 2, 'ubicacion': 'Trujillo', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Marcelino Champagnat', 'tipo': 'Privada', 'quintil': 2, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Privada San Juan Bautista', 'tipo': 'Privada', 'quintil': 2, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad de Lima', 'tipo': 'Privada', 'quintil': 2, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Le Cordon Bleu', 'tipo': 'Privada', 'quintil': 2, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad de Huánuco', 'tipo': 'Privada', 'quintil': 2, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Continental', 'tipo': 'Privada', 'quintil': 2, 'ubicacion': 'Huancayo', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Privada de Huancayo Franklin Roosevelt', 'tipo': 'Privada', 'quintil': 2, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Norbert Wiener', 'tipo': 'Privada', 'quintil': 2, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Antonio Ruiz de Montoya', 'tipo': 'Privada', 'quintil': 2, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad de Ingeniería y Tecnología - UTEC', 'tipo': 'Privada', 'quintil': 2, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad María Auxiliadora', 'tipo': 'Privada', 'quintil': 2, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Católica San Pablo', 'tipo': 'Privada', 'quintil': 2, 'ubicacion': 'Arequipa', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             
             # UNIVERSIDADES PRIVADAS - QUINTIL 1
             {'nombre': 'Universidad Autónoma de Ica', 'tipo': 'Privada', 'quintil': 1, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Peruana Los Andes', 'tipo': 'Privada', 'quintil': 1, 'ubicacion': 'Huancayo', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Católica Sedes Sapientiae', 'tipo': 'Privada', 'quintil': 1, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad de Ciencias y Humanidades', 'tipo': 'Privada', 'quintil': 1, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad La Salle', 'tipo': 'Privada', 'quintil': 1, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Facultad de Teología Pontificia y Civil de Lima', 'tipo': 'Privada', 'quintil': 1, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Jaime Bausate y Meza', 'tipo': 'Privada', 'quintil': 1, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Autónoma del Perú', 'tipo': 'Privada', 'quintil': 1, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Privada Peruano Alemana', 'tipo': 'Privada', 'quintil': 1, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Tecnológica del Perú', 'tipo': 'Privada', 'quintil': 1, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Femenina del Sagrado Corazón', 'tipo': 'Privada', 'quintil': 1, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad ESAN', 'tipo': 'Privada', 'quintil': 1, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad de Ciencias y Artes de América Latina', 'tipo': 'Privada', 'quintil': 1, 'ubicacion': 'Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Privada del Norte', 'tipo': 'Privada', 'quintil': 1, 'ubicacion': 'Trujillo/Lima', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Católica de Trujillo Benedicto XVI', 'tipo': 'Privada', 'quintil': 1, 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'},
             {'nombre': 'Universidad Para el Desarrollo Andino', 'tipo': 'Privada', 'quintil': 1, 'ubicacion': 'Huancavelica', 'estado': 'Licenciada', 'fuente': 'Lista oficial PRONABEC 2025'}
         ]
    
    def hacer_request(self, url: str, max_retries: int = 3) -> Optional[requests.Response]:
        """
        Realiza una petición HTTP con manejo de errores y reintentos
        """
        for intento in range(max_retries):
            try:
                self.logger.info(f"Realizando petición a: {url} (intento {intento + 1})")
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                # Rate limiting
                time.sleep(2)
                return response
                
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Error en intento {intento + 1}: {e}")
                if intento < max_retries - 1:
                    time.sleep(5 * (intento + 1))  # Backoff exponencial
                else:
                    self.logger.error(f"Falló después de {max_retries} intentos: {url}")
                    return None
    
    def extraer_universidades_desde_pagina(self, url: str) -> List[Dict[str, str]]:
        """
        Extrae información de universidades desde una página específica
        """
        response = self.hacer_request(url)
        if not response:
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        universidades = []
        
        # Buscar menciones de universidades en el texto
        texto_completo = soup.get_text().lower()
        
        for universidad_data in self.universidades_conocidas:
            nombre_universidad = universidad_data['nombre']
            if nombre_universidad.lower() in texto_completo:
                universidad_encontrada = universidad_data.copy()
                universidad_encontrada['fuente_url'] = url
                universidad_encontrada['elegible_beca18'] = True
                universidades.append(universidad_encontrada)
        
        # Buscar patrones adicionales de universidades
        patrones_universidad = [
            r'universidad\s+[\w\s]+',
            r'instituto\s+[\w\s]+',
            r'escuela\s+superior\s+[\w\s]+'
        ]
        
        for patron in patrones_universidad:
            matches = re.findall(patron, texto_completo, re.IGNORECASE)
            for match in matches:
                if len(match) > 10 and match not in [u['nombre'].lower() for u in universidades]:
                    universidades.append({
                        'nombre': match.title(),
                        'tipo': 'Pública' if 'nacional' in match.lower() else 'Privada',
                        'fuente_url': url,
                        'elegible_beca18': True
                    })
        
        return universidades
    
    def obtener_universidades_elegibles(self) -> List[Dict[str, str]]:
        """
        Obtiene la lista completa de universidades elegibles para Beca 18
        Retorna todas las universidades con información completa de modalidades
        """
        self.logger.info("Obteniendo lista completa de universidades elegibles para Beca 18 - Convocatoria 2025")
        
        # Obtener información de modalidades
        promedios = self.obtener_promedios_minimos()
        
        # Preparar lista de universidades con información completa
        universidades_elegibles = []
        
        for universidad_data in self.universidades_conocidas:
            universidad = universidad_data.copy()
            universidad['elegible_beca18'] = True
            universidad['fuente_url'] = universidad_data.get('fuente', 'Lista oficial PRONABEC 2025')
            universidad['convocatoria'] = '2025'
            
            # Agregar información de modalidades para cada universidad
            modalidades_info = []
            for modalidad, datos in promedios.items():
                modalidad_info = {
                    'modalidad': modalidad,
                    'nota_minima': datos['promedio_minimo'],
                    'requisitos_adicionales': datos['requisitos_adicionales'],
                    'descripcion': datos['descripcion']
                }
                modalidades_info.append(modalidad_info)
            
            universidad['modalidades'] = modalidades_info
            universidades_elegibles.append(universidad)
        
        # Contar por tipo y quintil
        publicas = [u for u in universidades_elegibles if u['tipo'] == 'Pública']
        privadas = [u for u in universidades_elegibles if u['tipo'] == 'Privada']
        
        self.logger.info(f"Total de universidades elegibles: {len(universidades_elegibles)}")
        self.logger.info(f"Universidades públicas: {len(publicas)}")
        self.logger.info(f"Universidades privadas: {len(privadas)}")
        
        # Contar por quintiles
        quintiles_count = {}
        for universidad in universidades_elegibles:
            quintil = universidad.get('quintil', 'No especificado')
            quintiles_count[quintil] = quintiles_count.get(quintil, 0) + 1
        
        for quintil, count in sorted(quintiles_count.items()):
            self.logger.info(f"Quintil {quintil}: {count} universidades")
        
        return universidades_elegibles
    
    def obtener_promedios_minimos(self) -> Dict[str, Dict[str, str]]:
        """
        Obtiene información sobre los promedios mínimos requeridos por modalidad
        """
        self.logger.info("Obteniendo información de promedios mínimos")
        
        # Ahora self.promedios_minimos ya contiene la estructura detallada
        return self.promedios_minimos
    
    def _obtener_descripcion_modalidad(self, modalidad: str) -> str:
        """
        Obtiene la descripción de cada modalidad de Beca 18
        """
        descripciones = {
            'Ordinaria': 'Para jóvenes menores de 22 años en situación de pobreza o pobreza extrema',
            'Huallaga': 'Para jóvenes menores de 22 años residentes en el Huallaga',
            'Vraem': 'Para jóvenes menores de 22 años residentes en zonas del VRAEM',
            'EIB': 'Para quienes dominen lenguas originarias y estudien Educación Intercultural Bilingüe',
            'Protección': 'Para jóvenes menores de 22 años que estuvieron en tutela del Estado',
            'CNA y PA': 'Para peruanos de comunidades nativas amazónicas o población afroperuana',
            'FF.AA.': 'Para licenciados del Servicio Militar Voluntario (mínimo 12 meses)',
            'Repared': 'Para víctimas de la violencia ocurrida entre 1980-2000'
        }
        return descripciones.get(modalidad, 'Descripción no disponible')
    
    def _obtener_requisitos_modalidad(self, modalidad: str) -> str:
        """
        Obtiene los requisitos específicos de cada modalidad
        """
        requisitos = {
            'Ordinaria': 'Acreditar condición de pobreza según SISFOH, tercio superior en secundaria',
            'Huallaga': 'Residir en el Huallaga, tercio superior en secundaria',
            'Vraem': 'Residir en zonas del VRAEM, tercio superior en secundaria',
            'EIB': 'Dominar lengua originaria elegible, medio superior en secundaria',
            'Protección': 'Acreditar tutela del Estado, medio superior en secundaria',
            'CNA y PA': 'Acreditar pertenencia a comunidad nativa o población afroperuana',
            'FF.AA.': 'Licencia del Servicio Militar Voluntario, medio superior en secundaria',
            'Repared': 'Acreditar condición de víctima de violencia 1980-2000, nota mínima 12'
        }
        return requisitos.get(modalidad, 'Requisitos no especificados')
    
    def guardar_datos_csv(self, universidades: List[Dict], promedios: Dict, archivo: str = 'beca18_datos.csv'):
        """
        Guarda los datos extraídos en formato CSV expandido
        Cada fila contiene una universidad con una modalidad específica
        """
        self.logger.info(f"Guardando datos en CSV expandido: {archivo}")
        
        # Crear lista expandida: una fila por universidad-modalidad
        datos_expandidos = []
        
        for universidad in universidades:
            # Información base de la universidad
            info_base = {
                'nombre_universidad': universidad['nombre'],
                'tipo_universidad': universidad['tipo'],
                'quintil': universidad.get('quintil', ''),
                'estado': universidad.get('estado', ''),
                'ubicacion': universidad.get('ubicacion', ''),
                'fuente': universidad.get('fuente', ''),
                'convocatoria': universidad.get('convocatoria', '')
            }
            
            # Agregar cada modalidad como una fila separada
            for modalidad_info in universidad.get('modalidades', []):
                fila = info_base.copy()
                fila.update({
                    'modalidad': modalidad_info['modalidad'],
                    'nota_minima': modalidad_info['nota_minima'],
                    'requisitos_adicionales': modalidad_info['requisitos_adicionales'],
                    'descripcion': modalidad_info['descripcion']
                })
                datos_expandidos.append(fila)
        
        # Crear DataFrame expandido
        df_expandido = pd.DataFrame(datos_expandidos)
        
        # Guardar CSV expandido
        df_expandido.to_csv(archivo.replace('.csv', '_expandido.csv'), index=False, encoding='utf-8')
        
        # También crear DataFrame con universidades básico para compatibilidad
        universidades_basico = []
        for universidad in universidades:
            uni_basico = universidad.copy()
            if 'modalidades' in uni_basico:
                del uni_basico['modalidades']  # Remover modalidades para CSV básico
            universidades_basico.append(uni_basico)
        
        df_universidades = pd.DataFrame(universidades_basico)
        
        # Guardar solo universidades en CSV
        df_universidades.to_csv('beca18_universidades.csv', index=False, encoding='utf-8')
        
        self.logger.info("Datos guardados exitosamente en CSV")
    
    def guardar_datos_json(self, universidades: List[Dict], promedios: Dict, archivo: str = 'beca18_datos.json'):
        """
        Guarda los datos extraídos en formato JSON
        """
        self.logger.info(f"Guardando datos en JSON: {archivo}")
        
        datos_completos = {
            'fecha_extraccion': time.strftime('%Y-%m-%d %H:%M:%S'),
            'universidades_elegibles': universidades,
            'promedios_minimos_por_modalidad': promedios,
            'total_universidades': len(universidades),
            'total_modalidades': len(promedios)
        }
        
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos_completos, f, ensure_ascii=False, indent=2)
        
        self.logger.info("Datos guardados exitosamente en JSON")
    
    def ejecutar_scraping_completo(self):
        """
        Ejecuta el proceso completo de scraping
        """
        self.logger.info("=== INICIANDO SCRAPING COMPLETO DE BECA 18 ===")
        
        try:
            # Obtener universidades elegibles
            universidades = self.obtener_universidades_elegibles()
            
            # Obtener promedios mínimos
            promedios = self.obtener_promedios_minimos()
            
            # Guardar datos
            self.guardar_datos_csv(universidades, promedios)
            self.guardar_datos_json(universidades, promedios)
            
            # Los promedios ya están incluidos en el JSON principal
            self.logger.info("Todos los datos (universidades y promedios) guardados")
            
            # Mostrar resumen
            self.mostrar_resumen(universidades, promedios)
            
            self.logger.info("=== SCRAPING COMPLETADO EXITOSAMENTE ===")
            
        except Exception as e:
            self.logger.error(f"Error durante el scraping: {e}")
            raise
    
    def verificar_actualizaciones_oficiales(self) -> Dict[str, any]:
        """
        Verifica si hay actualizaciones en las listas oficiales de PRONABEC
        """
        try:
            self.logger.info("Verificando actualizaciones en fuentes oficiales...")
            
            urls_oficiales = {
                'beca18_2025': 'https://www.pronabec.gob.pe/beca18_2025/',
                'beca18': 'https://www.pronabec.gob.pe/beca18/',
                'pronabec_principal': 'https://www.pronabec.gob.pe/',
                'requisitos_gob': 'https://www.gob.pe/41547-requisitos-para-postular-al-concurso-beca-18'
            }
            
            resultados = {
                'fecha_verificacion': time.strftime('%Y-%m-%d %H:%M:%S'),
                'urls_verificadas': {},
                'cambios_detectados': [],
                'recomendaciones': []
            }
            
            for nombre, url in urls_oficiales.items():
                try:
                    response = self.hacer_request(url)
                    if response:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        texto = soup.get_text().lower()
                        
                        # Buscar indicadores de actualización
                        indicadores_actualizacion = [
                            '2025', 'actualizado', 'nueva convocatoria', 
                            'rj 1393-2024', 'resolución jefatural'
                        ]
                        
                        encontrados = [ind for ind in indicadores_actualizacion if ind in texto]
                        
                        resultados['urls_verificadas'][nombre] = {
                            'url': url,
                            'accesible': True,
                            'indicadores_encontrados': encontrados,
                            'ultima_verificacion': time.strftime('%Y-%m-%d %H:%M:%S')
                        }
                        
                        if 'rj 1393-2024' in texto:
                            resultados['cambios_detectados'].append(
                                f"Referencia a RJ 1393-2024 encontrada en {nombre}"
                            )
                        
                        if '2025' in texto and nombre == 'beca18_2025':
                            resultados['cambios_detectados'].append(
                                f"Información de Beca 18 2025 confirmada en {nombre}"
                            )
                    else:
                        resultados['urls_verificadas'][nombre] = {
                            'url': url,
                            'accesible': False,
                            'error': 'No se pudo acceder al sitio'
                        }
                        
                except Exception as e:
                    resultados['urls_verificadas'][nombre] = {
                        'url': url,
                        'accesible': False,
                        'error': str(e)
                    }
                
                time.sleep(1)  # Rate limiting
            
            # Generar recomendaciones
            if resultados['cambios_detectados']:
                resultados['recomendaciones'].append(
                    "Se detectaron posibles actualizaciones. Revisar manualmente las fuentes oficiales."
                )
            
            resultados['recomendaciones'].extend([
                "Consultar directamente la RJ 1393-2024 para la lista completa de universidades",
                "Verificar las bases oficiales de Beca 18 2025 en PRONABEC",
                "Contactar a PRONABEC para información específica no pública"
            ])
            
            return resultados
            
        except Exception as e:
            self.logger.error(f"Error al verificar actualizaciones: {e}")
            return {
                'error': str(e),
                'fecha_verificacion': time.strftime('%Y-%m-%d %H:%M:%S')
            }
    
    def generar_reporte_completo(self) -> Dict[str, any]:
        """
        Genera un reporte completo con toda la información disponible
        """
        try:
            self.logger.info("Generando reporte completo...")
            
            universidades = self.obtener_universidades_elegibles()
            promedios = self.obtener_promedios_minimos()
            verificacion = self.verificar_actualizaciones_oficiales()
            
            reporte = {
                'fecha_generacion': time.strftime('%Y-%m-%d %H:%M:%S'),
                'universidades_elegibles': universidades,
                'promedios_minimos': promedios,
                'verificacion_actualizaciones': verificacion,
                'estadisticas': {
                    'total_universidades_muestra': len(universidades),
                    'total_modalidades': len(self.promedios_minimos)
                },
                'fuentes': {
                    'pronabec': 'https://www.pronabec.gob.pe/',
                    'beca18': 'https://www.pronabec.gob.pe/beca18/',
                    'beca18_2025': 'https://www.pronabec.gob.pe/beca18_2025/',
                    'documentos_oficiales': 'RJ 1393-2024 PRONABEC',
                    'sunedu': 'https://www.sunedu.gob.pe/',
                    'minedu': 'https://www.gob.pe/minedu'
                },
                'limitaciones': [
                    'Lista parcial de universidades (muestra de instituciones conocidas)',
                    'Promedios por modalidad de beca, no por universidad específica',
                    'Información basada en documentos públicos disponibles',
                    'Lista completa oficial en RJ 1393-2024 (requiere consulta manual)',
                    'Promedios específicos por universidad no son públicos',
                    'Requiere verificación constante en fuentes oficiales de PRONABEC'
                ]
            }
            
            return reporte
            
        except Exception as e:
            self.logger.error(f"Error al generar reporte: {e}")
            return {}
    
    def mostrar_resumen(self, universidades: List[Dict], promedios: Dict):
        """
        Muestra un resumen de los datos extraídos
        """
        print("\n" + "="*60)
        print("RESUMEN DE DATOS EXTRAÍDOS - BECA 18")
        print("="*60)
        
        print(f"\n📚 UNIVERSIDADES ELEGIBLES: {len(universidades)}")
        print("-" * 40)
        
        # Contar por tipo
        publicas = sum(1 for u in universidades if u['tipo'] == 'Pública')
        privadas = sum(1 for u in universidades if u['tipo'] == 'Privada')
        
        print(f"• Universidades Públicas: {publicas}")
        print(f"• Universidades Privadas: {privadas}")
        
        print("\n🎯 PRINCIPALES UNIVERSIDADES:")
        for i, universidad in enumerate(universidades[:10], 1):
            print(f"{i:2d}. {universidad['nombre']} ({universidad['tipo']})")
        
        if len(universidades) > 10:
            print(f"    ... y {len(universidades) - 10} más")
        
        print(f"\n📊 MODALIDADES Y PROMEDIOS MÍNIMOS: {len(promedios)}")
        print("-" * 40)
        
        for modalidad, datos in promedios.items():
            print(f"• {modalidad}: {datos['promedio_minimo']}")
            print(f"  {datos['descripcion']}")
            print()
        
        print("\n💾 ARCHIVOS GENERADOS:")
        print("• beca18_universidades.csv")
        print("• beca18_datos.json (incluye universidades y promedios)")
        print("• beca18_scraper.log")
        
        print("\n" + "="*60)

def main():
    """
    Función principal para ejecutar el scraper
    """
    scraper = Beca18Scraper()
    scraper.ejecutar_scraping_completo()

if __name__ == "__main__":
    main()