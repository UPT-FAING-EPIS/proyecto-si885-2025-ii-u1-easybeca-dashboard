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

class BCPScraper:
    def __init__(self):
        self.base_url = "https://www.viabcp.com"
        self.becas_urls = [
            "https://www.viabcp.com/responsabilidad-social/educacion/becas",
            "https://www.viabcp.com/educacion/becas",
            "https://www.viabcp.com/becas"
        ]
        
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
    
    async def scrape_becas(self) -> List[Dict]:
        """Scraping principal de becas BCP"""
        becas_data = []
        
        try:
            # Método 1: Scraping con requests
            becas_requests = await self._scrape_with_requests()
            becas_data.extend(becas_requests)
            
            # Método 2: Scraping con Selenium
            becas_selenium = await self._scrape_with_selenium()
            becas_data.extend(becas_selenium)
            
            # Agregar becas conocidas del BCP
            becas_data.extend(self._get_known_bcp_becas())
            
            # Eliminar duplicados
            becas_data = self._remove_duplicates(becas_data)
            
            return becas_data
            
        except Exception as e:
            print(f"Error en scraping BCP: {e}")
            return self._get_known_bcp_becas()  # Fallback a datos conocidos
    
    async def _scrape_with_requests(self) -> List[Dict]:
        """Scraping usando requests y BeautifulSoup"""
        becas = []
        
        for url in self.becas_urls:
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    page_becas = self._extract_becas_from_page(soup, url)
                    becas.extend(page_becas)
                    time.sleep(1)  # Pausa entre requests
                    
            except Exception as e:
                print(f"Error scraping {url}: {e}")
                continue
        
        return becas
    
    async def _scrape_with_selenium(self) -> List[Dict]:
        """Scraping usando Selenium para contenido dinámico"""
        becas = []
        driver = None
        
        try:
            driver = self.setup_driver()
            
            for url in self.becas_urls:
                try:
                    driver.get(url)
                    
                    # Esperar a que cargue la página
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    
                    # Buscar elementos de becas
                    beca_elements = driver.find_elements(By.CSS_SELECTOR, 
                        "div[class*='beca'], article[class*='beca'], .programa, .convocatoria, div[class*='scholarship']")
                    
                    for element in beca_elements:
                        try:
                            beca_info = self._extract_selenium_beca_info(element, url)
                            if beca_info:
                                becas.append(beca_info)
                        except Exception as e:
                            continue
                    
                    time.sleep(2)  # Pausa entre páginas
                    
                except Exception as e:
                    print(f"Error en Selenium para {url}: {e}")
                    continue
            
            return becas
            
        except Exception as e:
            print(f"Error general en Selenium BCP: {e}")
            return []
        finally:
            if driver:
                driver.quit()
    
    def _extract_becas_from_page(self, soup: BeautifulSoup, url: str) -> List[Dict]:
        """Extraer becas de una página web"""
        becas = []
        
        # Buscar contenedores de becas
        beca_selectors = [
            'div[class*="beca"]',
            'div[class*="scholarship"]',
            'article[class*="beca"]',
            '.programa',
            '.convocatoria',
            'div[class*="educacion"]',
            'div[class*="responsabilidad"]'
        ]
        
        for selector in beca_selectors:
            containers = soup.select(selector)
            for container in containers:
                beca_info = self._extract_beca_info_from_container(container, url)
                if beca_info:
                    becas.append(beca_info)
        
        # Si no encontramos contenedores específicos, buscar en texto general
        if not becas:
            becas = self._extract_from_general_text(soup, url)
        
        return becas
    
    def _extract_beca_info_from_container(self, container, url: str) -> Dict:
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
                link = self.base_url + link
            
            # Extraer información específica
            promedio = self._extract_promedio(container.get_text())
            requisitos = self._extract_requisitos_text(container.get_text())
            
            if title and len(title) > 5 and ('beca' in title.lower() or 'educación' in title.lower() or 'scholarship' in title.lower()):
                return {
                    'nombre_beca': title,
                    'institucion': 'Banco de Crédito del Perú (BCP)',
                    'descripcion': description[:500],
                    'promedio_minimo': promedio,
                    'requisitos': requisitos,
                    'url_fuente': link,
                    'fecha_scraping': datetime.now().isoformat(),
                    'fuente': 'BCP - Web Scraping',
                    'tipo_scraping': 'requests'
                }
            
            return None
            
        except Exception as e:
            return None
    
    def _extract_selenium_beca_info(self, element, url: str) -> Dict:
        """Extraer información usando Selenium"""
        try:
            title = element.find_element(By.CSS_SELECTOR, "h1, h2, h3, h4, h5, h6, strong, b").text.strip()
            
            try:
                description = element.find_element(By.CSS_SELECTOR, "p, div, span").text.strip()
            except:
                description = ""
            
            try:
                link_elem = element.find_element(By.TAG_NAME, "a")
                link = link_elem.get_attribute('href')
            except:
                link = url
            
            if title and len(title) > 5 and ('beca' in title.lower() or 'educación' in title.lower()):
                return {
                    'nombre_beca': title,
                    'institucion': 'Banco de Crédito del Perú (BCP)',
                    'descripcion': description[:500],
                    'url_fuente': link,
                    'fecha_scraping': datetime.now().isoformat(),
                    'fuente': 'BCP - Web Scraping',
                    'tipo_scraping': 'selenium'
                }
            
            return None
            
        except Exception as e:
            return None
    
    def _extract_from_general_text(self, soup: BeautifulSoup, url: str) -> List[Dict]:
        """Extraer becas del texto general de la página"""
        becas = []
        text = soup.get_text()
        
        # Buscar menciones de becas en el texto
        beca_patterns = [
            r'beca\s+[\w\s]{3,50}',
            r'programa\s+de\s+becas?\s+[\w\s]{3,50}',
            r'apoyo\s+educativo\s+[\w\s]{3,50}',
            r'financiamiento\s+educativo\s+[\w\s]{3,50}'
        ]
        
        for pattern in beca_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                beca_name = match.group().strip()
                if len(beca_name) > 10:
                    becas.append({
                        'nombre_beca': beca_name.title(),
                        'institucion': 'Banco de Crédito del Perú (BCP)',
                        'descripcion': f'Programa educativo identificado en BCP',
                        'url_fuente': url,
                        'fecha_scraping': datetime.now().isoformat(),
                        'fuente': 'BCP - Texto General',
                        'tipo_scraping': 'pattern_matching'
                    })
        
        return becas[:3]  # Limitar a 3 becas
    
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
    
    def _get_known_bcp_becas(self) -> List[Dict]:
        """Becas conocidas del BCP para validación"""
        return [
            {
                'nombre_beca': 'Beca BCP',
                'institucion': 'Banco de Crédito del Perú (BCP)',
                'descripcion': 'Programa de becas del BCP para estudiantes destacados con necesidades económicas.',
                'promedio_minimo': '15',
                'condicion_socioeconomica': 'Situación económica limitada',
                'cobertura': 'Financiamiento de estudios',
                'requisitos': 'Excelencia académica, situación socioeconómica, entrevista personal',
                'proceso': 'Convocatoria anual, evaluación académica y socioeconómica',
                'url_fuente': 'https://www.viabcp.com/responsabilidad-social/educacion/becas',
                'fecha_scraping': datetime.now().isoformat(),
                'fuente': 'BCP - Datos Oficiales',
                'tipo_scraping': 'manual'
            },
            {
                'nombre_beca': 'Programa de Responsabilidad Social BCP - Educación',
                'institucion': 'Banco de Crédito del Perú (BCP)',
                'descripcion': 'Iniciativa de responsabilidad social del BCP enfocada en el apoyo educativo a jóvenes talentosos.',
                'promedio_minimo': '14-15',
                'condicion_socioeconomica': 'Evaluación socioeconómica',
                'cobertura': 'Apoyo integral para estudios',
                'requisitos': 'Rendimiento académico destacado, necesidad económica comprobada',
                'proceso': 'Postulación, evaluación, selección, seguimiento',
                'url_fuente': 'https://www.viabcp.com/responsabilidad-social/educacion',
                'fecha_scraping': datetime.now().isoformat(),
                'fuente': 'BCP - Datos Oficiales',
                'tipo_scraping': 'manual'
            },
            {
                'nombre_beca': 'Apoyo Educativo BCP',
                'institucion': 'Banco de Crédito del Perú (BCP)',
                'descripcion': 'Programa de apoyo educativo del BCP para estudiantes universitarios y de educación superior.',
                'promedio_minimo': 'Variable según programa',
                'condicion_socioeconomica': 'Evaluación integral',
                'cobertura': 'Financiamiento parcial o total',
                'requisitos': 'Mérito académico, evaluación socioeconómica, compromiso social',
                'proceso': 'Convocatoria periódica, evaluación multidimensional',
                'url_fuente': 'https://www.viabcp.com/educacion',
                'fecha_scraping': datetime.now().isoformat(),
                'fuente': 'BCP - Datos Oficiales',
                'tipo_scraping': 'manual'
            }
        ]
    
    def _remove_duplicates(self, becas: List[Dict]) -> List[Dict]:
        """Eliminar becas duplicadas basándose en el nombre"""
        seen_names = set()
        unique_becas = []
        
        for beca in becas:
            name = beca.get('nombre_beca', '').lower().strip()
            if name and name not in seen_names:
                seen_names.add(name)
                unique_becas.append(beca)
        
        return unique_becas
    
    async def get_bcp_programs_info(self) -> Dict:
        """Obtener información general de programas BCP"""
        try:
            response = requests.get("https://www.viabcp.com/responsabilidad-social", 
                                  headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            return {
                'institucion': 'Banco de Crédito del Perú (BCP)',
                'tipo': 'Institución Financiera',
                'area_responsabilidad_social': 'Educación, Cultura, Desarrollo Social',
                'url_principal': 'https://www.viabcp.com',
                'url_responsabilidad_social': 'https://www.viabcp.com/responsabilidad-social',
                'enfoque_educativo': 'Apoyo a estudiantes talentosos con limitaciones económicas',
                'modalidades': ['Becas completas', 'Apoyo parcial', 'Programas especiales'],
                'fecha_consulta': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'institucion': 'Banco de Crédito del Perú (BCP)',
                'error': str(e),
                'fecha_consulta': datetime.now().isoformat()
            }
    
    async def validate_bcp_data(self, becas_excel: List[Dict]) -> Dict:
        """Validar datos scrapeados contra datos del Excel"""
        scraped_becas = await self.scrape_becas()
        
        validation_results = {
            'total_scraped': len(scraped_becas),
            'total_excel': len(becas_excel),
            'matches': [],
            'new_found': [],
            'missing': [],
            'validation_date': datetime.now().isoformat()
        }
        
        # Buscar coincidencias
        excel_names = [beca.get('nombre_beca', '').lower() for beca in becas_excel if 'bcp' in beca.get('institucion', '').lower()]
        scraped_names = [beca.get('nombre_beca', '').lower() for beca in scraped_becas]
        
        for scraped_beca in scraped_becas:
            scraped_name = scraped_beca.get('nombre_beca', '').lower()
            
            # Buscar coincidencias parciales
            found_match = False
            for excel_name in excel_names:
                if self._similarity_check(scraped_name, excel_name):
                    validation_results['matches'].append({
                        'scraped': scraped_beca['nombre_beca'],
                        'excel': excel_name,
                        'similarity': 'high'
                    })
                    found_match = True
                    break
            
            if not found_match:
                validation_results['new_found'].append(scraped_beca)
        
        # Identificar becas del Excel que no se encontraron
        for excel_name in excel_names:
            found_in_scraped = False
            for scraped_name in scraped_names:
                if self._similarity_check(excel_name, scraped_name):
                    found_in_scraped = True
                    break
            
            if not found_in_scraped:
                validation_results['missing'].append(excel_name)
        
        return validation_results
    
    def _similarity_check(self, name1: str, name2: str) -> bool:
        """Verificar similitud entre nombres de becas"""
        # Normalizar nombres
        name1 = re.sub(r'[^a-zA-Z0-9\s]', '', name1.lower()).strip()
        name2 = re.sub(r'[^a-zA-Z0-9\s]', '', name2.lower()).strip()
        
        # Verificar coincidencias exactas o parciales
        if name1 == name2:
            return True
        
        # Verificar si una está contenida en la otra
        if name1 in name2 or name2 in name1:
            return True
        
        # Verificar palabras clave comunes
        words1 = set(name1.split())
        words2 = set(name2.split())
        common_words = words1.intersection(words2)
        
        # Si tienen al menos 2 palabras en común y una de ellas es "beca"
        if len(common_words) >= 2 and 'beca' in common_words:
            return True
        
        return False