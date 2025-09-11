import re
import json
import os
import pandas as pd
from typing import List, Dict, Optional, Any
from datetime import datetime
import asyncio
import time
from pathlib import Path
import logging
from functools import wraps

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_logging(log_file: str = "scraping.log"):
    """Configurar sistema de logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def timing_decorator(func):
    """Decorador para medir tiempo de ejecución"""
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} ejecutado en {execution_time:.2f} segundos")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} falló después de {execution_time:.2f} segundos: {e}")
            raise
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} ejecutado en {execution_time:.2f} segundos")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} falló después de {execution_time:.2f} segundos: {e}")
            raise
    
    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper

class DataValidator:
    """Validador de datos de becas"""
    
    @staticmethod
    def validate_beca_data(beca: Dict) -> Dict:
        """Validar y limpiar datos de una beca"""
        validated_beca = {}
        
        # Campos requeridos
        required_fields = ['nombre_beca', 'institucion']
        for field in required_fields:
            if field not in beca or not beca[field]:
                raise ValueError(f"Campo requerido faltante: {field}")
            validated_beca[field] = str(beca[field]).strip()
        
        # Campos opcionales con limpieza
        optional_fields = {
            'descripcion': 500,  # máximo 500 caracteres
            'promedio_minimo': 10,
            'condicion_socioeconomica': 200,
            'cobertura': 200,
            'requisitos': 500,
            'proceso': 300,
            'url_fuente': 500,
            'fuente': 100,
            'tipo_scraping': 50
        }
        
        for field, max_length in optional_fields.items():
            if field in beca and beca[field]:
                value = str(beca[field]).strip()
                validated_beca[field] = value[:max_length] if len(value) > max_length else value
            else:
                validated_beca[field] = ""
        
        # Agregar timestamp si no existe
        if 'fecha_scraping' not in beca:
            validated_beca['fecha_scraping'] = datetime.now().isoformat()
        else:
            validated_beca['fecha_scraping'] = beca['fecha_scraping']
        
        return validated_beca
    
    @staticmethod
    def validate_promedio(promedio_text: str) -> Optional[float]:
        """Extraer y validar promedio académico"""
        if not promedio_text:
            return None
        
        # Patrones para extraer números
        patterns = [
            r'(\d+(?:\.\d+)?)',  # Número decimal
            r'(\d+)\s*(?:de|/|sobre)\s*(\d+)',  # Formato "15 de 20"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, str(promedio_text))
            if match:
                try:
                    if len(match.groups()) == 1:
                        value = float(match.group(1))
                        # Validar rango razonable
                        if 0 <= value <= 20:
                            return value
                    else:
                        # Formato fraccionario
                        numerator = float(match.group(1))
                        denominator = float(match.group(2))
                        if denominator > 0:
                            # Convertir a escala de 20
                            value = (numerator / denominator) * 20
                            if 0 <= value <= 20:
                                return value
                except ValueError:
                    continue
        
        return None
    
    @staticmethod
    def categorize_socioeconomic_condition(condition_text: str) -> str:
        """Categorizar condición socioeconómica"""
        if not condition_text:
            return "No especificado"
        
        condition_lower = condition_text.lower()
        
        if any(word in condition_lower for word in ['extrema', 'extreme']):
            return "Pobreza extrema"
        elif any(word in condition_lower for word in ['pobreza', 'poverty']):
            return "Pobreza"
        elif any(word in condition_lower for word in ['vulnerable', 'vulnerabilidad']):
            return "Vulnerabilidad económica"
        elif any(word in condition_lower for word in ['limitado', 'limited', 'bajo']):
            return "Ingresos limitados"
        elif any(word in condition_lower for word in ['medio', 'middle']):
            return "Clase media"
        else:
            return "Evaluación socioeconómica"

class TextCleaner:
    """Limpiador de texto para datos scrapeados"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Limpiar texto general"""
        if not text:
            return ""
        
        # Convertir a string si no lo es
        text = str(text)
        
        # Remover caracteres especiales y espacios extra
        text = re.sub(r'\s+', ' ', text)  # Múltiples espacios a uno
        text = re.sub(r'[\r\n\t]', ' ', text)  # Saltos de línea y tabs
        text = text.strip()
        
        return text
    
    @staticmethod
    def clean_beca_name(name: str) -> str:
        """Limpiar nombre de beca"""
        if not name:
            return ""
        
        name = TextCleaner.clean_text(name)
        
        # Capitalizar correctamente
        name = name.title()
        
        # Correcciones específicas
        corrections = {
            'Bcp': 'BCP',
            'Pronabec': 'PRONABEC',
            'Pucp': 'PUCP',
            'Uni': 'UNI',
            'Upc': 'UPC'
        }
        
        for old, new in corrections.items():
            name = name.replace(old, new)
        
        return name
    
    @staticmethod
    def extract_keywords(text: str) -> List[str]:
        """Extraer palabras clave del texto"""
        if not text:
            return []
        
        # Palabras clave relevantes para becas
        keywords = [
            'beca', 'scholarship', 'financiamiento', 'apoyo', 'ayuda',
            'educativo', 'académico', 'universitario', 'pregrado', 'posgrado',
            'excelencia', 'mérito', 'talento', 'socioeconómico', 'vulnerable'
        ]
        
        text_lower = text.lower()
        found_keywords = []
        
        for keyword in keywords:
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords

class ExcelProcessor:
    """Procesador de archivos Excel"""
    
    @staticmethod
    def read_becas_excel(file_path: str) -> List[Dict]:
        """Leer archivo Excel de becas"""
        try:
            df = pd.read_excel(file_path)
            
            # Mapeo de columnas esperadas
            column_mapping = {
                'N°': 'numero',
                'Nombre Beca': 'nombre_beca',
                'Promedio Académico Mínimo': 'promedio_minimo',
                'Condición Socioeconómica': 'condicion_socioeconomica',
                'Documentación': 'documentacion',
                'Beneficios': 'beneficios',
                'Duración del Proceso': 'duracion_proceso',
                'Fuente': 'fuente'
            }
            
            # Renombrar columnas
            df = df.rename(columns=column_mapping)
            
            # Limpiar datos
            for col in df.columns:
                if col in ['nombre_beca', 'condicion_socioeconomica', 'beneficios', 'fuente']:
                    df[col] = df[col].apply(lambda x: TextCleaner.clean_text(str(x)) if pd.notna(x) else "")
            
            return df.to_dict('records')
            
        except Exception as e:
            logger.error(f"Error leyendo Excel: {e}")
            return []
    
    @staticmethod
    def export_comparison_results(comparison_data: Dict, output_path: str) -> bool:
        """Exportar resultados de comparación a Excel"""
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Coincidencias exactas
                if comparison_data.get('exact_matches'):
                    df_exact = pd.DataFrame(comparison_data['exact_matches'])
                    df_exact.to_excel(writer, sheet_name='Coincidencias_Exactas', index=False)
                
                # Coincidencias parciales
                if comparison_data.get('partial_matches'):
                    df_partial = pd.DataFrame(comparison_data['partial_matches'])
                    df_partial.to_excel(writer, sheet_name='Coincidencias_Parciales', index=False)
                
                # Nuevas becas encontradas
                if comparison_data.get('new_becas'):
                    df_new = pd.DataFrame(comparison_data['new_becas'])
                    df_new.to_excel(writer, sheet_name='Nuevas_Becas', index=False)
                
                # Becas faltantes
                if comparison_data.get('missing_becas'):
                    df_missing = pd.DataFrame(comparison_data['missing_becas'])
                    df_missing.to_excel(writer, sheet_name='Becas_Faltantes', index=False)
                
                # Resumen
                summary_data = {
                    'Métrica': ['Total Scrapeadas', 'Total Excel', 'Coincidencias Exactas', 
                               'Coincidencias Parciales', 'Nuevas Encontradas', 'Faltantes'],
                    'Valor': [
                        comparison_data.get('total_scraped', 0),
                        comparison_data.get('total_excel', 0),
                        len(comparison_data.get('exact_matches', [])),
                        len(comparison_data.get('partial_matches', [])),
                        len(comparison_data.get('new_becas', [])),
                        len(comparison_data.get('missing_becas', []))
                    ]
                }
                df_summary = pd.DataFrame(summary_data)
                df_summary.to_excel(writer, sheet_name='Resumen', index=False)
            
            return True
            
        except Exception as e:
            logger.error(f"Error exportando resultados: {e}")
            return False

class URLValidator:
    """Validador de URLs"""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validar si una URL es válida"""
        if not url:
            return False
        
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'  # domain...
            r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # host...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        return url_pattern.match(url) is not None
    
    @staticmethod
    def normalize_url(url: str, base_url: str = "") -> str:
        """Normalizar URL"""
        if not url:
            return ""
        
        url = url.strip()
        
        # Si ya es una URL completa, devolverla
        if url.startswith(('http://', 'https://')):
            return url
        
        # Si es una URL relativa y tenemos base_url
        if base_url and url.startswith('/'):
            base_url = base_url.rstrip('/')
            return base_url + url
        
        return url

class ScrapingStatus:
    """Gestor de estado de scraping"""
    
    def __init__(self):
        self.status = {
            'is_running': False,
            'current_source': '',
            'progress': 0,
            'total_sources': 0,
            'start_time': None,
            'errors': [],
            'results': {
                'total_scraped': 0,
                'by_source': {}
            }
        }
    
    def start_scraping(self, total_sources: int):
        """Iniciar sesión de scraping"""
        self.status.update({
            'is_running': True,
            'current_source': '',
            'progress': 0,
            'total_sources': total_sources,
            'start_time': datetime.now(),
            'errors': [],
            'results': {
                'total_scraped': 0,
                'by_source': {}
            }
        })
    
    def update_progress(self, current_source: str, progress: int):
        """Actualizar progreso"""
        self.status['current_source'] = current_source
        self.status['progress'] = progress
    
    def add_results(self, source: str, count: int):
        """Agregar resultados de una fuente"""
        self.status['results']['by_source'][source] = count
        self.status['results']['total_scraped'] += count
    
    def add_error(self, source: str, error: str):
        """Agregar error"""
        self.status['errors'].append({
            'source': source,
            'error': error,
            'timestamp': datetime.now().isoformat()
        })
    
    def finish_scraping(self):
        """Finalizar sesión de scraping"""
        self.status['is_running'] = False
        self.status['current_source'] = ''
        self.status['progress'] = 100
    
    def get_status(self) -> Dict:
        """Obtener estado actual"""
        status_copy = self.status.copy()
        
        if status_copy['start_time']:
            elapsed = datetime.now() - status_copy['start_time']
            status_copy['elapsed_time'] = str(elapsed)
            status_copy['start_time'] = status_copy['start_time'].isoformat()
        
        return status_copy

# Instancia global del gestor de estado
scraping_status = ScrapingStatus()

def format_duration(seconds: float) -> str:
    """Formatear duración en segundos a formato legible"""
    if seconds < 60:
        return f"{seconds:.1f} segundos"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutos"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} horas"

def create_summary_report(comparison_results: Dict, scraping_stats: Dict) -> Dict:
    """Crear reporte resumen"""
    return {
        'fecha_reporte': datetime.now().isoformat(),
        'resumen_scraping': {
            'total_becas_scrapeadas': scraping_stats.get('total_scraped', 0),
            'fuentes_consultadas': len(scraping_stats.get('by_source', {})),
            'becas_por_fuente': scraping_stats.get('by_source', {})
        },
        'resumen_comparacion': {
            'total_excel': comparison_results.get('total_excel', 0),
            'coincidencias_exactas': len(comparison_results.get('exact_matches', [])),
            'coincidencias_parciales': len(comparison_results.get('partial_matches', [])),
            'nuevas_becas': len(comparison_results.get('new_becas', [])),
            'becas_faltantes': len(comparison_results.get('missing_becas', []))
        },
        'porcentaje_cobertura': (
            (len(comparison_results.get('exact_matches', [])) + 
             len(comparison_results.get('partial_matches', []))) / 
            max(comparison_results.get('total_excel', 1), 1) * 100
        )
    }

class ExcelComparator:
    """Clase para comparar datos scrapeados con Excel existente"""
    
    def __init__(self):
        pass
    
    def compare_with_excel(self, scraped_data: List[Dict], excel_path: str) -> Dict:
        """Comparar datos scrapeados con Excel"""
        try:
            import pandas as pd
            
            # Cargar datos del Excel si existe
            excel_data = []
            if os.path.exists(excel_path):
                df = pd.read_excel(excel_path)
                excel_data = df.to_dict('records')
            
            # Realizar comparación básica
            results = {
                'total_scraped': len(scraped_data),
                'total_excel': len(excel_data),
                'exact_matches': [],
                'partial_matches': [],
                'new_entries': [],  # Inicializar vacío
                'missing_entries': []
            }
            
            # Comparación simple por nombre de beca
            for scraped_item in scraped_data:
                found_match = False
                scraped_name = scraped_item.get('nombre_beca', '').lower().strip()
                
                for excel_item in excel_data:
                    # Usar 'Nombre Beca' (con espacio) que es la columna real del Excel
                    excel_name = str(excel_item.get('Nombre Beca', '')).lower().strip()
                    if scraped_name and excel_name and scraped_name == excel_name:
                        results['exact_matches'].append({
                            'scraped': scraped_item,
                            'excel': excel_item
                        })
                        found_match = True
                        break
                
                if not found_match:
                    results['new_entries'].append(scraped_item)
            
            # Limitar new_entries a las primeras 5 para la respuesta
            results['new_entries'] = results['new_entries'][:5]
            
            return results
            
        except Exception as e:
            logger.error(f"Error comparando con Excel: {e}")
            return {}
    
    def _compare_entries(self, scraped: Dict, excel: Dict) -> bool:
        """Comparar dos entradas para determinar si son iguales"""
        # Comparación simple por nombre de beca
        scraped_name = scraped.get('nombre_beca', '').lower().strip()
        excel_name = str(excel.get('Nombre Beca', '')).lower().strip()
        
        return scraped_name and excel_name and scraped_name == excel_name