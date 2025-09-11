import sqlite3
import pandas as pd
import json
from typing import List, Dict, Optional
from datetime import datetime
import os
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path: str = "becas_scraping.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Inicializar la base de datos con las tablas necesarias"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla principal de becas scrapeadas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS becas_scrapeadas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_beca TEXT NOT NULL,
                institucion TEXT NOT NULL,
                descripcion TEXT,
                promedio_minimo TEXT,
                condicion_socioeconomica TEXT,
                cobertura TEXT,
                requisitos TEXT,
                proceso TEXT,
                url_fuente TEXT,
                fecha_scraping TEXT,
                fuente TEXT,
                tipo_scraping TEXT,
                activo BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de becas del Excel original
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS becas_excel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero INTEGER,
                nombre_beca TEXT NOT NULL,
                promedio_minimo TEXT,
                condicion_socioeconomica TEXT,
                documentacion TEXT,
                beneficios TEXT,
                duracion_proceso TEXT,
                fuente TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de comparaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comparaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                beca_scrapeada_id INTEGER,
                beca_excel_id INTEGER,
                tipo_match TEXT, -- 'exact', 'partial', 'new', 'missing'
                similitud_score REAL,
                observaciones TEXT,
                fecha_comparacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (beca_scrapeada_id) REFERENCES becas_scrapeadas (id),
                FOREIGN KEY (beca_excel_id) REFERENCES becas_excel (id)
            )
        ''')
        
        # Tabla de logs de scraping
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scraping_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fuente TEXT NOT NULL,
                total_becas INTEGER,
                becas_nuevas INTEGER,
                errores INTEGER,
                tiempo_ejecucion REAL,
                estado TEXT, -- 'success', 'error', 'partial'
                detalles TEXT,
                fecha_ejecucion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de fuentes de datos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fuentes_datos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                url TEXT,
                tipo TEXT, -- 'pronabec', 'universidad', 'banco', 'otro'
                activo BOOLEAN DEFAULT 1,
                ultima_actualizacion TIMESTAMP,
                total_becas INTEGER DEFAULT 0,
                observaciones TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Insertar fuentes de datos por defecto
        self._insert_default_sources()
    
    def _insert_default_sources(self):
        """Insertar fuentes de datos por defecto"""
        default_sources = [
            {
                'nombre': 'PRONABEC',
                'url': 'https://www.pronabec.gob.pe',
                'tipo': 'pronabec',
                'observaciones': 'Programa Nacional de Becas y Crédito Educativo'
            },
            {
                'nombre': 'Banco de Crédito del Perú (BCP)',
                'url': 'https://www.viabcp.com',
                'tipo': 'banco',
                'observaciones': 'Programas de responsabilidad social en educación'
            },
            {
                'nombre': 'Universidad Nacional Mayor de San Marcos',
                'url': 'https://unmsm.edu.pe',
                'tipo': 'universidad',
                'observaciones': 'Universidad pública'
            },
            {
                'nombre': 'Pontificia Universidad Católica del Perú',
                'url': 'https://www.pucp.edu.pe',
                'tipo': 'universidad',
                'observaciones': 'Universidad privada'
            },
            {
                'nombre': 'Universidad Peruana de Ciencias Aplicadas',
                'url': 'https://www.upc.edu.pe',
                'tipo': 'universidad',
                'observaciones': 'Universidad privada'
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for source in default_sources:
            cursor.execute('''
                INSERT OR IGNORE INTO fuentes_datos (nombre, url, tipo, observaciones)
                VALUES (?, ?, ?, ?)
            ''', (source['nombre'], source['url'], source['tipo'], source['observaciones']))
        
        conn.commit()
        conn.close()
    
    def insert_scraped_becas(self, becas: List[Dict]) -> int:
        """Insertar becas scrapeadas en la base de datos"""
        if not becas:
            return 0
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        inserted_count = 0
        
        for beca in becas:
            try:
                # Verificar si ya existe
                cursor.execute('''
                    SELECT id FROM becas_scrapeadas 
                    WHERE nombre_beca = ? AND institucion = ?
                ''', (beca.get('nombre_beca', ''), beca.get('institucion', '')))
                
                if cursor.fetchone() is None:
                    cursor.execute('''
                        INSERT INTO becas_scrapeadas (
                            nombre_beca, institucion, descripcion, promedio_minimo,
                            condicion_socioeconomica, cobertura, requisitos, proceso,
                            url_fuente, fecha_scraping, fuente, tipo_scraping
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        beca.get('nombre_beca', ''),
                        beca.get('institucion', ''),
                        beca.get('descripcion', ''),
                        beca.get('promedio_minimo', ''),
                        beca.get('condicion_socioeconomica', ''),
                        beca.get('cobertura', ''),
                        beca.get('requisitos', ''),
                        beca.get('proceso', ''),
                        beca.get('url_fuente', ''),
                        beca.get('fecha_scraping', datetime.now().isoformat()),
                        beca.get('fuente', ''),
                        beca.get('tipo_scraping', '')
                    ))
                    inserted_count += 1
            
            except Exception as e:
                print(f"Error insertando beca {beca.get('nombre_beca', 'Unknown')}: {e}")
                continue
        
        conn.commit()
        conn.close()
        
        return inserted_count
    
    def load_excel_data(self, excel_path: str) -> int:
        """Cargar datos del Excel a la base de datos"""
        try:
            # Leer el archivo Excel
            df = pd.read_excel(excel_path)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Limpiar tabla anterior
            cursor.execute('DELETE FROM becas_excel')
            
            inserted_count = 0
            
            for _, row in df.iterrows():
                try:
                    cursor.execute('''
                        INSERT INTO becas_excel (
                            numero, nombre_beca, promedio_minimo, condicion_socioeconomica,
                            documentacion, beneficios, duracion_proceso, fuente
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        str(row.get('N°', '')),
                        str(row.get('Nombre Beca', '')),
                        str(row.get('Requisitos Principales', '')),  # Mapeo correcto
                        str(row.get('Institución o Programa', '')),  # Mapeo correcto
                        str(row.get('Requisitos Principales', '')),  # Usar requisitos como documentación
                        str(row.get('Beneficios / Cobertura', '')),  # Mapeo correcto
                        'No especificado',  # No hay duración en el Excel
                        str(row.get('Observaciones / Fuente', ''))  # Mapeo correcto
                    ))
                    inserted_count += 1
                
                except Exception as e:
                    print(f"Error insertando fila del Excel: {e}")
                    continue
            
            conn.commit()
            conn.close()
            
            return inserted_count
            
        except Exception as e:
            print(f"Error cargando Excel: {e}")
            return 0
    
    def compare_data(self) -> Dict:
        """Comparar datos scrapeados con datos del Excel"""
        conn = sqlite3.connect(self.db_path)
        
        # Obtener datos
        scraped_df = pd.read_sql_query('SELECT * FROM becas_scrapeadas WHERE activo = 1', conn)
        excel_df = pd.read_sql_query('SELECT * FROM becas_excel', conn)
        
        comparison_results = {
            'total_scraped': len(scraped_df),
            'total_excel': len(excel_df),
            'exact_matches': [],
            'partial_matches': [],
            'new_becas': [],
            'missing_becas': [],
            'comparison_date': datetime.now().isoformat()
        }
        
        # Limpiar tabla de comparaciones anterior
        cursor = conn.cursor()
        cursor.execute('DELETE FROM comparaciones')
        
        # Comparar cada beca scrapeada con las del Excel
        for _, scraped_row in scraped_df.iterrows():
            best_match = None
            best_score = 0
            match_type = 'new'
            
            scraped_name = scraped_row['nombre_beca'].lower().strip()
            
            for _, excel_row in excel_df.iterrows():
                excel_name = str(excel_row['nombre_beca']).lower().strip()
                
                # Calcular similitud
                score = self._calculate_similarity(scraped_name, excel_name)
                
                if score > best_score:
                    best_score = score
                    best_match = excel_row
                    
                    if score >= 0.9:
                        match_type = 'exact'
                    elif score >= 0.6:
                        match_type = 'partial'
            
            # Registrar comparación
            if best_match is not None and best_score >= 0.6:
                cursor.execute('''
                    INSERT INTO comparaciones (
                        beca_scrapeada_id, beca_excel_id, tipo_match, similitud_score, observaciones
                    ) VALUES (?, ?, ?, ?, ?)
                ''', (
                    scraped_row['id'],
                    best_match['id'],
                    match_type,
                    best_score,
                    f'Match encontrado con score {best_score:.2f}'
                ))
                
                match_info = {
                    'scraped_name': scraped_row['nombre_beca'],
                    'excel_name': best_match['nombre_beca'],
                    'score': best_score,
                    'scraped_source': scraped_row['fuente'],
                    'excel_source': best_match['fuente']
                }
                
                if match_type == 'exact':
                    comparison_results['exact_matches'].append(match_info)
                else:
                    comparison_results['partial_matches'].append(match_info)
            else:
                # Nueva beca encontrada
                comparison_results['new_becas'].append({
                    'name': scraped_row['nombre_beca'],
                    'institution': scraped_row['institucion'],
                    'source': scraped_row['fuente']
                })
        
        # Identificar becas del Excel que no se encontraron
        for _, excel_row in excel_df.iterrows():
            found = False
            excel_name = str(excel_row['nombre_beca']).lower().strip()
            
            for _, scraped_row in scraped_df.iterrows():
                scraped_name = scraped_row['nombre_beca'].lower().strip()
                if self._calculate_similarity(excel_name, scraped_name) >= 0.6:
                    found = True
                    break
            
            if not found:
                comparison_results['missing_becas'].append({
                    'name': excel_row['nombre_beca'],
                    'source': excel_row['fuente']
                })
        
        conn.commit()
        conn.close()
        
        return comparison_results
    
    def _calculate_similarity(self, name1: str, name2: str) -> float:
        """Calcular similitud entre dos nombres de becas"""
        import difflib
        
        # Normalizar nombres
        name1 = name1.lower().strip()
        name2 = name2.lower().strip()
        
        # Similitud básica
        basic_similarity = difflib.SequenceMatcher(None, name1, name2).ratio()
        
        # Bonus por palabras clave comunes
        words1 = set(name1.split())
        words2 = set(name2.split())
        common_words = words1.intersection(words2)
        
        word_bonus = len(common_words) / max(len(words1), len(words2)) * 0.3
        
        return min(basic_similarity + word_bonus, 1.0)
    
    def get_scraped_becas(self, limit: Optional[int] = None) -> List[Dict]:
        """Obtener becas scrapeadas"""
        conn = sqlite3.connect(self.db_path)
        
        query = 'SELECT * FROM becas_scrapeadas WHERE activo = 1 ORDER BY created_at DESC'
        if limit:
            query += f' LIMIT {limit}'
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df.to_dict('records')
    
    def get_excel_becas(self) -> List[Dict]:
        """Obtener becas del Excel"""
        conn = sqlite3.connect(self.db_path)
        df = pd.read_sql_query('SELECT * FROM becas_excel ORDER BY numero', conn)
        conn.close()
        
        return df.to_dict('records')
    
    def get_comparison_results(self) -> List[Dict]:
        """Obtener resultados de comparación"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                c.*,
                bs.nombre_beca as scraped_name,
                bs.institucion as scraped_institution,
                bs.fuente as scraped_source,
                be.nombre_beca as excel_name,
                be.fuente as excel_source
            FROM comparaciones c
            LEFT JOIN becas_scrapeadas bs ON c.beca_scrapeada_id = bs.id
            LEFT JOIN becas_excel be ON c.beca_excel_id = be.id
            ORDER BY c.similitud_score DESC
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        return df.to_dict('records')
    
    def log_scraping_session(self, fuente: str, total_becas: int, becas_nuevas: int, 
                           errores: int, tiempo_ejecucion: float, estado: str, detalles: str = ""):
        """Registrar sesión de scraping"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO scraping_logs (
                fuente, total_becas, becas_nuevas, errores, tiempo_ejecucion, estado, detalles
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (fuente, total_becas, becas_nuevas, errores, tiempo_ejecucion, estado, detalles))
        
        conn.commit()
        conn.close()
    
    def get_scraping_stats(self) -> Dict:
        """Obtener estadísticas de scraping"""
        conn = sqlite3.connect(self.db_path)
        
        stats = {}
        
        # Estadísticas generales
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM becas_scrapeadas WHERE activo = 1')
        stats['total_scraped'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM becas_excel')
        stats['total_excel'] = cursor.fetchone()[0]
        
        # Estadísticas por fuente
        df_sources = pd.read_sql_query('''
            SELECT fuente, COUNT(*) as count 
            FROM becas_scrapeadas 
            WHERE activo = 1 
            GROUP BY fuente
        ''', conn)
        stats['by_source'] = df_sources.to_dict('records')
        
        # Últimas sesiones de scraping
        df_logs = pd.read_sql_query('''
            SELECT * FROM scraping_logs 
            ORDER BY fecha_ejecucion DESC 
            LIMIT 10
        ''', conn)
        stats['recent_sessions'] = df_logs.to_dict('records')
        
        conn.close()
        
        return stats
    
    def export_to_excel(self, output_path: str) -> bool:
        """Exportar datos a Excel"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Becas scrapeadas
                df_scraped = pd.read_sql_query('SELECT * FROM becas_scrapeadas WHERE activo = 1', conn)
                df_scraped.to_excel(writer, sheet_name='Becas_Scrapeadas', index=False)
                
                # Becas del Excel original
                df_excel = pd.read_sql_query('SELECT * FROM becas_excel', conn)
                df_excel.to_excel(writer, sheet_name='Becas_Excel_Original', index=False)
                
                # Comparaciones
                df_comparisons = pd.read_sql_query('''
                    SELECT 
                        c.tipo_match,
                        c.similitud_score,
                        bs.nombre_beca as scraped_name,
                        bs.institucion as scraped_institution,
                        be.nombre_beca as excel_name,
                        c.fecha_comparacion
                    FROM comparaciones c
                    LEFT JOIN becas_scrapeadas bs ON c.beca_scrapeada_id = bs.id
                    LEFT JOIN becas_excel be ON c.beca_excel_id = be.id
                ''', conn)
                df_comparisons.to_excel(writer, sheet_name='Comparaciones', index=False)
                
                # Estadísticas
                stats = self.get_scraping_stats()
                df_stats = pd.DataFrame([stats])
                df_stats.to_excel(writer, sheet_name='Estadisticas', index=False)
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error exportando a Excel: {e}")
            return False
    
    def get_data_by_source(self, source: str) -> List[Dict]:
        """Obtener datos scrapeados filtrados por fuente"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    nombre_beca,
                    institucion,
                    descripcion,
                    promedio_minimo,
                    condicion_socioeconomica,
                    cobertura,
                    requisitos,
                    proceso,
                    url_fuente,
                    fecha_scraping,
                    fuente,
                    tipo_scraping
                FROM becas_scrapeadas 
                WHERE fuente = ? AND activo = 1
                ORDER BY fecha_scraping DESC
            ''', (source,))
            
            columns = [description[0] for description in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                row_dict = dict(zip(columns, row))
                results.append(row_dict)
            
            conn.close()
            return results
            
        except Exception as e:
            print(f"Error obteniendo datos por fuente {source}: {e}")
            return []
    
    def get_all_data(self) -> List[Dict]:
        """Obtener todos los datos scrapeados"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    nombre_beca,
                    institucion,
                    descripcion,
                    promedio_minimo,
                    condicion_socioeconomica,
                    cobertura,
                    requisitos,
                    proceso,
                    url_fuente,
                    fecha_scraping,
                    fuente,
                    tipo_scraping
                FROM becas_scrapeadas 
                WHERE activo = 1
                ORDER BY fecha_scraping DESC
            ''')
            
            columns = [description[0] for description in cursor.description]
            results = []
            
            for row in cursor.fetchall():
                row_dict = dict(zip(columns, row))
                # Agregar campo 'source' para compatibilidad
                row_dict['source'] = row_dict.get('fuente', '')
                results.append(row_dict)
            
            conn.close()
            return results
            
        except Exception as e:
            print(f"Error obteniendo todos los datos: {e}")
            return []
    
    def save_scraped_data(self, source: str, data: List[Dict]) -> int:
        """Alias para insert_scraped_becas - mantiene compatibilidad"""
        # Agregar la fuente a cada elemento de datos
        for item in data:
            item['fuente'] = source
        return self.insert_scraped_becas(data)