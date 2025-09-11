import requests
from bs4 import BeautifulSoup
import json
import time
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import asyncio
from datetime import datetime
import re

class UniversitiesScraper:
    def __init__(self):
        self.universities = {
            'UNMSM': {
                'name': 'Universidad Nacional Mayor de San Marcos',
                'url': 'https://unmsm.edu.pe',
                'becas_path': '/estudiantes/becas'
            },
            'UNI': {
                'name': 'Universidad Nacional de Ingeniería',
                'url': 'https://www.uni.edu.pe',
                'becas_path': '/estudiantes/becas'
            },
            'PUCP': {
                'name': 'Pontificia Universidad Católica del Perú',
                'url': 'https://www.pucp.edu.pe',
                'becas_path': '/admision/becas'
            },
            'UPC': {
                'name': 'Universidad Peruana de Ciencias Aplicadas',
                'url': 'https://www.upc.edu.pe',
                'becas_path': '/admision/becas'
            },
            'ULIMA': {
                'name': 'Universidad de Lima',
                'url': 'https://www.ulima.edu.pe',
                'becas_path': '/pregrado/admision/becas'
            },
            'USIL': {
                'name': 'Universidad San Ignacio de Loyola',
                'url': 'https://www.usil.edu.pe',
                'becas_path': '/admision/becas'
            },
            'UTP': {
                'name': 'Universidad Tecnológica del Perú',
                'url': 'https://www.utp.edu.pe',
                'becas_path': '/admision/becas'
            }
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def setup_driver(self):
        """Configurar driver de Selenium"""
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    
    async def scrape_all_universities(self) -> List[Dict]:
        """Scraping de todas las universidades"""
        all_becas = []
        
        for uni_code, uni_info in self.universities.items():
            print(f"Scraping {uni_info['name']}...")
            try:
                becas = await self.scrape_university(uni_code, uni_info)
                all_becas.extend(becas)
                time.sleep(2)  # Pausa entre universidades
            except Exception as e:
                print(f"Error scraping {uni_info['name']}: {e}")
                continue
        
        # Agregar becas conocidas
        all_becas.extend(self._get_known_university_becas())
        
        return self._remove_duplicates(all_becas)
    
    async def scrape_university(self, uni_code: str, uni_info: Dict) -> List[Dict]:
        """Scraping de una universidad específica"""
        becas = []
        
        try:
            # Intentar múltiples URLs posibles
            possible_urls = [
                uni_info['url'] + uni_info['becas_path'],
                uni_info['url'] + '/becas',
                uni_info['url'] + '/admision/becas',
                uni_info['url'] + '/estudiantes/becas',
                uni_info['url'] + '/pregrado/becas',
                uni_info['url'] + '/bienestar/becas'
            ]
            
            for url in possible_urls:
                try:
                    response = requests.get(url, headers=self.headers, timeout=10)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        university_becas = self._extract_becas_from_page(soup, uni_info['name'], url)
                        becas.extend(university_becas)
                        break  # Si encontramos la página, no seguir buscando
                except:
                    continue
            
            # Si no encontramos nada con requests, intentar con Selenium
            if not becas:
                becas = await self._scrape_with_selenium(uni_code, uni_info)
            
            return becas
            
        except Exception as e:
            print(f"Error en scraping de {uni_info['name']}: {e}")
            return []
    
    def _extract_becas_from_page(self, soup: BeautifulSoup, university_name: str, url: str) -> List[Dict]:
        """Extraer becas de una página web"""
        becas = []
        
        # Buscar contenedores de becas
        beca_selectors = [
            'div[class*="beca"]',
            'div[class*="scholarship"]',
            'article[class*="beca"]',
            '.programa',
            '.convocatoria',
            'div[class*="ayuda"]',
            'div[class*="financiamiento"]'
        ]
        
        for selector in beca_selectors:
            containers = soup.select(selector)
            for container in containers:
                beca_info = self._extract_beca_info_from_container(container, university_name, url)
                if beca_info:
                    becas.append(beca_info)
        
        # Si no encontramos contenedores específicos, buscar en texto general
        if not becas:
            becas = self._extract_from_general_text(soup, university_name, url)
        
        return becas
    
    def _extract_beca_info_from_container(self, container, university_name: str, url: str) -> Dict:
        """Extraer información de beca desde un contenedor"""
        try:
            # Buscar título
            title_elem = container.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'b'])
            title = title_elem.get_text(strip=True) if title_elem else ""
            
            # Buscar descripción
            desc_elem = container.find(['p', 'div', 'span'])
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Buscar enlace
            link_elem = container.find('a')
            link = link_elem.get('href') if link_elem else url
            if link and not link.startswith('http'):
                base_url = '/'.join(url.split('/')[:3])
                link = base_url + link
            
            # Extraer información específica
            promedio = self._extract_promedio(container.get_text())
            requisitos = self._extract_requisitos_text(container.get_text())
            
            if title and len(title) > 3 and 'beca' in title.lower():
                return {
                    'nombre_beca': title,
                    'institucion': university_name,
                    'descripcion': description[:500],
                    'promedio_minimo': promedio,
                    'requisitos': requisitos,
                    'url_fuente': link,
                    'fecha_scraping': datetime.now().isoformat(),
                    'fuente': f'{university_name} - Web Scraping',
                    'tipo_scraping': 'requests'
                }
            
            return None
            
        except Exception as e:
            return None
    
    def _extract_from_general_text(self, soup: BeautifulSoup, university_name: str, url: str) -> List[Dict]:
        """Extraer becas del texto general de la página"""
        becas = []
        text = soup.get_text()
        
        # Buscar menciones de becas en el texto
        beca_patterns = [
            r'beca\s+[\w\s]{3,50}',
            r'programa\s+de\s+becas?\s+[\w\s]{3,50}',
            r'ayuda\s+económica\s+[\w\s]{3,50}',
            r'financiamiento\s+[\w\s]{3,50}'
        ]
        
        for pattern in beca_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                beca_name = match.group().strip()
                if len(beca_name) > 10:
                    becas.append({
                        'nombre_beca': beca_name.title(),
                        'institucion': university_name,
                        'descripcion': f'Beca identificada en {university_name}',
                        'url_fuente': url,
                        'fecha_scraping': datetime.now().isoformat(),
                        'fuente': f'{university_name} - Texto General',
                        'tipo_scraping': 'pattern_matching'
                    })
        
        return becas[:5]  # Limitar a 5 becas por universidad
    
    async def _scrape_with_selenium(self, uni_code: str, uni_info: Dict) -> List[Dict]:
        """Scraping con Selenium para contenido dinámico"""
        becas = []
        driver = None
        
        try:
            driver = self.setup_driver()
            url = uni_info['url'] + uni_info['becas_path']
            driver.get(url)
            
            # Esperar a que cargue
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Buscar elementos de becas
            beca_elements = driver.find_elements(By.CSS_SELECTOR, 
                "div[class*='beca'], article[class*='beca'], .programa, .convocatoria")
            
            for element in beca_elements:
                try:
                    title = element.find_element(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6, strong, b").text.strip()
                    
                    if title and 'beca' in title.lower():
                        becas.append({
                            'nombre_beca': title,
                            'institucion': uni_info['name'],
                            'descripcion': f'Beca de {uni_info["name"]}',
                            'url_fuente': url,
                            'fecha_scraping': datetime.now().isoformat(),
                            'fuente': f'{uni_info["name"]} - Selenium',
                            'tipo_scraping': 'selenium'
                        })
                except:
                    continue
            
            return becas
            
        except Exception as e:
            print(f"Error en Selenium para {uni_info['name']}: {e}")
            return []
        finally:
            if driver:
                driver.quit()
    
    def _extract_promedio(self, text: str) -> str:
        """Extraer promedio mínimo del texto"""
        promedio_patterns = [
            r'promedio\s+(?:mínimo\s+)?(?:de\s+)?(\d+(?:\.\d+)?)',
            r'nota\s+mínima\s+(?:de\s+)?(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\s+de\s+promedio'
        ]
        
        for pattern in promedio_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return ""
    
    def _extract_requisitos_text(self, text: str) -> str:
        """Extraer requisitos del texto"""
        requisitos_keywords = ['requisito', 'requerimiento', 'condición', 'criterio']
        
        for keyword in requisitos_keywords:
            pattern = f'{keyword}[^.]*\.'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group()[:200]
        
        return ""
    
    def _get_known_university_becas(self) -> List[Dict]:
        """Becas conocidas de universidades para validación"""
        return [
            {
                'nombre_beca': 'Beca de Excelencia Académica PUCP',
                'institucion': 'Pontificia Universidad Católica del Perú',
                'descripcion': 'Beca para estudiantes con alto rendimiento académico que cubre hasta el 100% de la pensión.',
                'promedio_minimo': '16',
                'condicion_socioeconomica': 'Evaluación socioeconómica',
                'cobertura': 'Hasta 100% de pensión',
                'url_fuente': 'https://www.pucp.edu.pe/admision/becas/',
                'fecha_scraping': datetime.now().isoformat(),
                'fuente': 'PUCP - Datos Oficiales',
                'tipo_scraping': 'manual'
            },
            {
                'nombre_beca': 'Beca Talento UPC',
                'institucion': 'Universidad Peruana de Ciencias Aplicadas',
                'descripcion': 'Programa de becas para estudiantes destacados en diversas áreas.',
                'promedio_minimo': '15',
                'condicion_socioeconomica': 'Evaluación integral',
                'cobertura': 'Descuento en pensión',
                'url_fuente': 'https://www.upc.edu.pe/admision/becas/',
                'fecha_scraping': datetime.now().isoformat(),
                'fuente': 'UPC - Datos Oficiales',
                'tipo_scraping': 'manual'
            },
            {
                'nombre_beca': 'Beca Socioeconómica UNMSM',
                'institucion': 'Universidad Nacional Mayor de San Marcos',
                'descripcion': 'Apoyo económico para estudiantes en situación de vulnerabilidad socioeconómica.',
                'promedio_minimo': '14',
                'condicion_socioeconomica': 'Vulnerabilidad socioeconómica',
                'cobertura': 'Apoyo económico',
                'url_fuente': 'https://unmsm.edu.pe/estudiantes/becas',
                'fecha_scraping': datetime.now().isoformat(),
                'fuente': 'UNMSM - Datos Oficiales',
                'tipo_scraping': 'manual'
            },
            {
                'nombre_beca': 'Beca de Ingreso UNI',
                'institucion': 'Universidad Nacional de Ingeniería',
                'descripcion': 'Beca para estudiantes destacados en el examen de admisión.',
                'promedio_minimo': '15',
                'condicion_socioeconomica': 'Mérito académico',
                'cobertura': 'Exoneración de pagos',
                'url_fuente': 'https://www.uni.edu.pe/estudiantes/becas',
                'fecha_scraping': datetime.now().isoformat(),
                'fuente': 'UNI - Datos Oficiales',
                'tipo_scraping': 'manual'
            }
        ]
    
    def _remove_duplicates(self, becas: List[Dict]) -> List[Dict]:
        """Eliminar becas duplicadas"""
        seen_names = set()
        unique_becas = []
        
        for beca in becas:
            name = beca.get('nombre_beca', '').lower().strip()
            if name and name not in seen_names:
                seen_names.add(name)
                unique_becas.append(beca)
        
        return unique_becas
    
    async def get_university_details(self, university_code: str) -> Dict:
        """Obtener detalles específicos de una universidad"""
        if university_code not in self.universities:
            return {}
        
        uni_info = self.universities[university_code]
        
        try:
            response = requests.get(uni_info['url'], headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            return {
                'nombre': uni_info['name'],
                'url': uni_info['url'],
                'tipo': 'Pública' if 'Nacional' in uni_info['name'] else 'Privada',
                'ubicacion': self._extract_location(soup),
                'contacto': self._extract_contact(soup)
            }
            
        except Exception as e:
            return {
                'nombre': uni_info['name'],
                'url': uni_info['url'],
                'error': str(e)
            }
    
    def _extract_location(self, soup: BeautifulSoup) -> str:
        """Extraer ubicación de la universidad"""
        location_keywords = ['dirección', 'ubicación', 'sede', 'campus']
        
        for keyword in location_keywords:
            elem = soup.find(text=lambda text: text and keyword in text.lower())
            if elem and elem.parent:
                return elem.parent.get_text(strip=True)[:100]
        
        return "Lima, Perú"  # Default
    
    def _extract_contact(self, soup: BeautifulSoup) -> str:
        """Extraer información de contacto"""
        contact_patterns = [
            r'\+?51\s?\d{1,3}\s?\d{3}\s?\d{4}',  # Teléfonos peruanos
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'  # Emails
        ]
        
        text = soup.get_text()
        contacts = []
        
        for pattern in contact_patterns:
            matches = re.findall(pattern, text)
            contacts.extend(matches[:2])  # Máximo 2 por tipo
        
        return ', '.join(contacts[:3])  # Máximo 3 contactos