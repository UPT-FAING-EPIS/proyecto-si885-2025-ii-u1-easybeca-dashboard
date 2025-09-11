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

class PronabecScraper:
    def __init__(self):
        self.base_url = "https://www.pronabec.gob.pe"
        self.becas_url = "https://www.pronabec.gob.pe/becas/"
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
        """Scraping principal de becas PRONABEC"""
        becas_data = []
        
        try:
            # Método 1: Scraping con requests
            becas_requests = await self._scrape_with_requests()
            becas_data.extend(becas_requests)
            
            # Método 2: Scraping con Selenium (para contenido dinámico)
            becas_selenium = await self._scrape_with_selenium()
            becas_data.extend(becas_selenium)
            
            # Eliminar duplicados
            becas_data = self._remove_duplicates(becas_data)
            
            return becas_data
            
        except Exception as e:
            print(f"Error en scraping PRONABEC: {e}")
            return []
    
    async def _scrape_with_requests(self) -> List[Dict]:
        """Scraping usando requests y BeautifulSoup"""
        becas = []
        
        try:
            # Página principal de becas
            response = requests.get(self.becas_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Buscar información de becas en la página
            beca_containers = soup.find_all(['div', 'article', 'section'], class_=lambda x: x and any(keyword in x.lower() for keyword in ['beca', 'programa', 'convocatoria']))
            
            for container in beca_containers:
                beca_info = self._extract_beca_info(container)
                if beca_info:
                    becas.append(beca_info)
            
            # Datos específicos conocidos de PRONABEC
            becas.extend(self._get_known_pronabec_becas())
            
            return becas
            
        except Exception as e:
            print(f"Error en scraping con requests: {e}")
            return []
    
    async def _scrape_with_selenium(self) -> List[Dict]:
        """Scraping usando Selenium para contenido dinámico"""
        becas = []
        driver = None
        
        try:
            driver = self.setup_driver()
            driver.get(self.becas_url)
            
            # Esperar a que cargue la página
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Buscar elementos de becas
            beca_elements = driver.find_elements(By.CSS_SELECTOR, 
                "div[class*='beca'], article[class*='beca'], .programa, .convocatoria")
            
            for element in beca_elements:
                try:
                    beca_info = self._extract_selenium_beca_info(element)
                    if beca_info:
                        becas.append(beca_info)
                except Exception as e:
                    continue
            
            return becas
            
        except Exception as e:
            print(f"Error en scraping con Selenium: {e}")
            return []
        finally:
            if driver:
                driver.quit()
    
    def _extract_beca_info(self, container) -> Dict:
        """Extraer información de beca desde un contenedor HTML"""
        try:
            # Buscar título/nombre de la beca
            title_elem = container.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'b'])
            title = title_elem.get_text(strip=True) if title_elem else ""
            
            # Buscar descripción
            desc_elem = container.find(['p', 'div', 'span'])
            description = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Buscar enlaces
            link_elem = container.find('a')
            link = link_elem.get('href') if link_elem else ""
            if link and not link.startswith('http'):
                link = self.base_url + link
            
            if title and len(title) > 5:  # Filtrar títulos muy cortos
                return {
                    'nombre_beca': title,
                    'institucion': 'PRONABEC',
                    'descripcion': description[:500],  # Limitar descripción
                    'url_fuente': link,
                    'fecha_scraping': datetime.now().isoformat(),
                    'fuente': 'PRONABEC - Web Scraping',
                    'tipo_scraping': 'requests'
                }
            
            return None
            
        except Exception as e:
            return None
    
    def _extract_selenium_beca_info(self, element) -> Dict:
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
                link = ""
            
            if title and len(title) > 5:
                return {
                    'nombre_beca': title,
                    'institucion': 'PRONABEC',
                    'descripcion': description[:500],
                    'url_fuente': link,
                    'fecha_scraping': datetime.now().isoformat(),
                    'fuente': 'PRONABEC - Web Scraping',
                    'tipo_scraping': 'selenium'
                }
            
            return None
            
        except Exception as e:
            return None
    
    def _get_known_pronabec_becas(self) -> List[Dict]:
        """Datos conocidos de becas PRONABEC para validación"""
        return [
            {
                'nombre_beca': 'Beca 18',
                'institucion': 'PRONABEC',
                'descripcion': 'Beca integral para estudios de pregrado dirigida a estudiantes de alto rendimiento académico en situación de pobreza y pobreza extrema.',
                'promedio_minimo': '14',
                'condicion_socioeconomica': 'Pobreza extrema o pobreza',
                'cobertura': 'Financiamiento completo',
                'url_fuente': 'https://www.pronabec.gob.pe/beca18/',
                'fecha_scraping': datetime.now().isoformat(),
                'fuente': 'PRONABEC - Datos Oficiales',
                'tipo_scraping': 'manual'
            },
            {
                'nombre_beca': 'Beca Perú',
                'institucion': 'PRONABEC',
                'descripcion': 'Programa de becas para estudios de posgrado en el extranjero dirigido a profesionales peruanos.',
                'promedio_minimo': '14-15',
                'condicion_socioeconomica': 'Ingreso limitado per cápita',
                'cobertura': 'Matrícula, pensión, manutención, seguro',
                'url_fuente': 'https://www.pronabec.gob.pe/becaperu/',
                'fecha_scraping': datetime.now().isoformat(),
                'fuente': 'PRONABEC - Datos Oficiales',
                'tipo_scraping': 'manual'
            },
            {
                'nombre_beca': 'Beca Permanencia',
                'institucion': 'PRONABEC',
                'descripcion': 'Apoyo económico para estudiantes universitarios en situación de vulnerabilidad económica.',
                'promedio_minimo': 'Variable',
                'condicion_socioeconomica': 'Vulnerabilidad económica',
                'cobertura': 'Apoyo económico continuo',
                'url_fuente': 'https://www.pronabec.gob.pe/becapermanencia/',
                'fecha_scraping': datetime.now().isoformat(),
                'fuente': 'PRONABEC - Datos Oficiales',
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
    
    async def get_beca_details(self, beca_url: str) -> Dict:
        """Obtener detalles específicos de una beca"""
        try:
            response = requests.get(beca_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraer información detallada
            details = {
                'requisitos': self._extract_requisitos(soup),
                'beneficios': self._extract_beneficios(soup),
                'proceso': self._extract_proceso(soup),
                'fechas': self._extract_fechas(soup)
            }
            
            return details
            
        except Exception as e:
            print(f"Error obteniendo detalles de {beca_url}: {e}")
            return {}
    
    def _extract_requisitos(self, soup) -> str:
        """Extraer requisitos de la beca"""
        requisitos_keywords = ['requisito', 'requerimiento', 'condición', 'criterio']
        for keyword in requisitos_keywords:
            elem = soup.find(text=lambda text: text and keyword in text.lower())
            if elem:
                parent = elem.parent
                if parent:
                    return parent.get_text(strip=True)[:300]
        return ""
    
    def _extract_beneficios(self, soup) -> str:
        """Extraer beneficios de la beca"""
        beneficios_keywords = ['beneficio', 'cobertura', 'incluye', 'financia']
        for keyword in beneficios_keywords:
            elem = soup.find(text=lambda text: text and keyword in text.lower())
            if elem:
                parent = elem.parent
                if parent:
                    return parent.get_text(strip=True)[:300]
        return ""
    
    def _extract_proceso(self, soup) -> str:
        """Extraer información del proceso"""
        proceso_keywords = ['proceso', 'etapa', 'paso', 'procedimiento']
        for keyword in proceso_keywords:
            elem = soup.find(text=lambda text: text and keyword in text.lower())
            if elem:
                parent = elem.parent
                if parent:
                    return parent.get_text(strip=True)[:300]
        return ""
    
    def _extract_fechas(self, soup) -> str:
        """Extraer fechas importantes"""
        fechas_keywords = ['fecha', 'plazo', 'cronograma', 'calendario']
        for keyword in fechas_keywords:
            elem = soup.find(text=lambda text: text and keyword in text.lower())
            if elem:
                parent = elem.parent
                if parent:
                    return parent.get_text(strip=True)[:200]
        return ""