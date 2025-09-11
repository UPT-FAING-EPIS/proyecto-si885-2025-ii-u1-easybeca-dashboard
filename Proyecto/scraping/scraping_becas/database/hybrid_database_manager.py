import sqlite3
import pymysql
import pandas as pd
import json
from typing import List, Dict, Optional
from datetime import datetime
import os
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from .mysql_config import create_mysql_engine, create_database_if_not_exists, MYSQL_CONFIG

class HybridDatabaseManager:
    def __init__(self, prefer_mysql: bool = True):
        self.use_mysql = False
        self.db_path = "becas_scraping.db"
        self.engine = None
        self.Session = None
        
        if prefer_mysql:
            try:
                # Intentar conectar a MySQL
                create_database_if_not_exists()
                self.engine = create_mysql_engine()
                self.Session = sessionmaker(bind=self.engine)
                self._create_mysql_tables()
                self.use_mysql = True
                print("Usando base de datos MySQL")
            except Exception as e:
                print(f"MySQL no disponible, usando SQLite como fallback: {e}")
                self._init_sqlite()
        else:
            self._init_sqlite()
    
    def _init_sqlite(self):
        """Inicializar SQLite como fallback"""
        self.use_mysql = False
        self._create_sqlite_tables()
        print("Usando base de datos SQLite")
    
    def _create_sqlite_tables(self):
        """Crear tablas en SQLite"""
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
        
        conn.commit()
        conn.close()
    
    def _create_mysql_tables(self):
        """Crear tablas en MySQL"""
        with self.engine.connect() as conn:
            # Tabla principal de becas scrapeadas
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS becas_scrapeadas (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre_beca VARCHAR(500) NOT NULL,
                    institucion VARCHAR(200) NOT NULL,
                    descripcion TEXT,
                    promedio_minimo VARCHAR(50),
                    condicion_socioeconomica VARCHAR(200),
                    cobertura TEXT,
                    requisitos TEXT,
                    proceso TEXT,
                    url_fuente VARCHAR(1000),
                    fecha_scraping DATETIME,
                    fuente VARCHAR(100),
                    tipo_scraping VARCHAR(50),
                    activo BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_fuente (fuente),
                    INDEX idx_activo (activo),
                    INDEX idx_fecha_scraping (fecha_scraping)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            conn.commit()
    
    def save_scraped_data(self, source: str, data: List[Dict]):
        """Guardar datos scrapeados"""
        if not data:
            return 0
        
        # Agregar fuente a cada elemento
        for item in data:
            item['fuente'] = source
            if 'fecha_scraping' not in item:
                item['fecha_scraping'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return self.insert_scraped_becas(data)
    
    def insert_scraped_becas(self, becas_data: List[Dict]) -> int:
        """Insertar becas scrapeadas"""
        if not becas_data:
            return 0
        
        if self.use_mysql:
            return self._insert_mysql(becas_data)
        else:
            return self._insert_sqlite(becas_data)
    
    def _insert_mysql(self, becas_data: List[Dict]) -> int:
        """Insertar en MySQL"""
        inserted_count = 0
        
        try:
            with self.engine.connect() as conn:
                for beca in becas_data:
                    # Verificar si ya existe
                    existing = conn.execute(text("""
                        SELECT id FROM becas_scrapeadas 
                        WHERE nombre_beca = :nombre AND fuente = :fuente
                    """), {
                        'nombre': beca.get('titulo', beca.get('nombre_beca', '')),
                        'fuente': beca.get('fuente', '')
                    }).fetchone()
                    
                    if not existing:
                        # Insertar nueva beca
                        conn.execute(text("""
                            INSERT INTO becas_scrapeadas (
                                nombre_beca, institucion, descripcion, promedio_minimo,
                                condicion_socioeconomica, cobertura, requisitos, proceso,
                                url_fuente, fecha_scraping, fuente, tipo_scraping, activo
                            ) VALUES (
                                :nombre_beca, :institucion, :descripcion, :promedio_minimo,
                                :condicion_socioeconomica, :cobertura, :requisitos, :proceso,
                                :url_fuente, :fecha_scraping, :fuente, :tipo_scraping, :activo
                            )
                        """), {
                            'nombre_beca': beca.get('titulo', beca.get('nombre_beca', '')),
                            'institucion': beca.get('institucion', ''),
                            'descripcion': beca.get('descripcion', ''),
                            'promedio_minimo': beca.get('promedio_minimo', ''),
                            'condicion_socioeconomica': beca.get('condicion_socioeconomica', ''),
                            'cobertura': beca.get('cobertura', ''),
                            'requisitos': beca.get('requisitos', ''),
                            'proceso': beca.get('proceso', ''),
                            'url_fuente': beca.get('url', beca.get('url_fuente', '')),
                            'fecha_scraping': beca.get('fecha_scraping', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                            'fuente': beca.get('fuente', ''),
                            'tipo_scraping': beca.get('tipo_scraping', 'automatico'),
                            'activo': True
                        })
                        inserted_count += 1
                
                conn.commit()
                
        except Exception as e:
            print(f"Error insertando becas en MySQL: {e}")
            raise
        
        return inserted_count
    
    def _insert_sqlite(self, becas_data: List[Dict]) -> int:
        """Insertar en SQLite"""
        inserted_count = 0
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for beca in becas_data:
                # Verificar si ya existe
                cursor.execute("""
                    SELECT id FROM becas_scrapeadas 
                    WHERE nombre_beca = ? AND fuente = ?
                """, (beca.get('titulo', beca.get('nombre_beca', '')), beca.get('fuente', '')))
                
                if not cursor.fetchone():
                    # Insertar nueva beca
                    cursor.execute("""
                        INSERT INTO becas_scrapeadas (
                            nombre_beca, institucion, descripcion, promedio_minimo,
                            condicion_socioeconomica, cobertura, requisitos, proceso,
                            url_fuente, fecha_scraping, fuente, tipo_scraping, activo
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        beca.get('titulo', beca.get('nombre_beca', '')),
                        beca.get('institucion', ''),
                        beca.get('descripcion', ''),
                        beca.get('promedio_minimo', ''),
                        beca.get('condicion_socioeconomica', ''),
                        beca.get('cobertura', ''),
                        beca.get('requisitos', ''),
                        beca.get('proceso', ''),
                        beca.get('url', beca.get('url_fuente', '')),
                        beca.get('fecha_scraping', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                        beca.get('fuente', ''),
                        beca.get('tipo_scraping', 'automatico'),
                        True
                    ))
                    inserted_count += 1
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error insertando becas en SQLite: {e}")
            raise
        
        return inserted_count
    
    def get_all_scraped_data(self) -> List[Dict]:
        """Obtener todos los datos scrapeados"""
        if self.use_mysql:
            return self._get_all_mysql()
        else:
            return self._get_all_sqlite()
    
    def _get_all_mysql(self) -> List[Dict]:
        """Obtener datos de MySQL"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT * FROM becas_scrapeadas 
                    WHERE activo = TRUE 
                    ORDER BY fecha_scraping DESC
                """))
                
                columns = result.keys()
                data = [dict(zip(columns, row)) for row in result.fetchall()]
                
                # Convertir datetime a string para JSON
                for item in data:
                    for key, value in item.items():
                        if isinstance(value, datetime):
                            item[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                
                return data
                
        except Exception as e:
            print(f"Error obteniendo datos de MySQL: {e}")
            return []
    
    def _get_all_sqlite(self) -> List[Dict]:
        """Obtener datos de SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM becas_scrapeadas 
                WHERE activo = 1 
                ORDER BY fecha_scraping DESC
            """)
            
            rows = cursor.fetchall()
            data = [dict(row) for row in rows]
            conn.close()
            
            return data
            
        except Exception as e:
            print(f"Error obteniendo datos de SQLite: {e}")
            return []
    
    def get_scraped_data_by_source(self, source: str) -> List[Dict]:
        """Obtener datos scrapeados por fuente"""
        if self.use_mysql:
            return self._get_by_source_mysql(source)
        else:
            return self._get_by_source_sqlite(source)
    
    def _get_by_source_mysql(self, source: str) -> List[Dict]:
        """Obtener datos por fuente de MySQL"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT * FROM becas_scrapeadas 
                    WHERE UPPER(fuente) = UPPER(:source) AND activo = TRUE 
                    ORDER BY fecha_scraping DESC
                """), {'source': source})
                
                columns = result.keys()
                data = [dict(zip(columns, row)) for row in result.fetchall()]
                
                # Convertir datetime a string para JSON
                for item in data:
                    for key, value in item.items():
                        if isinstance(value, datetime):
                            item[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                
                return data
                
        except Exception as e:
            print(f"Error obteniendo datos por fuente de MySQL: {e}")
            return []
    
    def _get_by_source_sqlite(self, source: str) -> List[Dict]:
        """Obtener datos por fuente de SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM becas_scrapeadas 
                WHERE UPPER(fuente) = UPPER(?) AND activo = 1 
                ORDER BY fecha_scraping DESC
            """, (source,))
            
            rows = cursor.fetchall()
            data = [dict(row) for row in rows]
            conn.close()
            
            return data
            
        except Exception as e:
            print(f"Error obteniendo datos por fuente de SQLite: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Obtener estadísticas de la base de datos"""
        if self.use_mysql:
            return self._get_stats_mysql()
        else:
            return self._get_stats_sqlite()
    
    def _get_stats_mysql(self) -> Dict:
        """Obtener estadísticas de MySQL"""
        try:
            with self.engine.connect() as conn:
                # Total de becas activas
                total_result = conn.execute(text("""
                    SELECT COUNT(*) as total FROM becas_scrapeadas WHERE activo = TRUE
                """))
                total = total_result.fetchone()[0]
                
                # Por fuente
                sources_result = conn.execute(text("""
                    SELECT fuente, COUNT(*) as count 
                    FROM becas_scrapeadas 
                    WHERE activo = TRUE 
                    GROUP BY fuente
                """))
                
                sources = {row[0]: row[1] for row in sources_result.fetchall()}
                
                return {
                    'total': total,
                    'by_source': sources,
                    'database_type': 'MySQL',
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
        except Exception as e:
            print(f"Error obteniendo estadísticas de MySQL: {e}")
            return {'total': 0, 'by_source': {}, 'database_type': 'MySQL', 'last_updated': ''}
    
    def _get_stats_sqlite(self) -> Dict:
        """Obtener estadísticas de SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total de becas activas
            cursor.execute("SELECT COUNT(*) FROM becas_scrapeadas WHERE activo = 1")
            total = cursor.fetchone()[0]
            
            # Por fuente
            cursor.execute("""
                SELECT fuente, COUNT(*) 
                FROM becas_scrapeadas 
                WHERE activo = 1 
                GROUP BY fuente
            """)
            
            sources = {row[0]: row[1] for row in cursor.fetchall()}
            conn.close()
            
            return {
                'total': total,
                'by_source': sources,
                'database_type': 'SQLite',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            print(f"Error obteniendo estadísticas de SQLite: {e}")
            return {'total': 0, 'by_source': {}, 'database_type': 'SQLite', 'last_updated': ''}
    
    def load_excel_data(self, excel_path: str) -> int:
        """Cargar datos del Excel a la base de datos"""
        try:
            # Leer el archivo Excel
            df = pd.read_excel(excel_path)
            
            if self.use_mysql:
                return self._load_excel_mysql(df)
            else:
                return self._load_excel_sqlite(df)
                
        except Exception as e:
            print(f"Error cargando Excel: {e}")
            return 0
    
    def _load_excel_mysql(self, df: pd.DataFrame) -> int:
        """Cargar datos del Excel en MySQL"""
        try:
            with self.engine.connect() as conn:
                # Crear tabla becas_excel si no existe
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS becas_excel (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        numero VARCHAR(10),
                        nombre_beca VARCHAR(500),
                        promedio_minimo TEXT,
                        condicion_socioeconomica TEXT,
                        documentacion TEXT,
                        beneficios TEXT,
                        duracion_proceso VARCHAR(100),
                        fuente TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
                """))
                
                # Limpiar tabla anterior
                conn.execute(text('DELETE FROM becas_excel'))
                
                inserted_count = 0
                
                for _, row in df.iterrows():
                    try:
                        conn.execute(text("""
                            INSERT INTO becas_excel (
                                numero, nombre_beca, promedio_minimo, condicion_socioeconomica,
                                documentacion, beneficios, duracion_proceso, fuente
                            ) VALUES (:numero, :nombre_beca, :promedio_minimo, :condicion_socioeconomica,
                                     :documentacion, :beneficios, :duracion_proceso, :fuente)
                        """), {
                            'numero': str(row.get('N°', '')),
                            'nombre_beca': str(row.get('Nombre Beca', '')),
                            'promedio_minimo': str(row.get('Requisitos Principales', '')),
                            'condicion_socioeconomica': str(row.get('Institución o Programa', '')),
                            'documentacion': str(row.get('Requisitos Principales', '')),
                            'beneficios': str(row.get('Beneficios / Cobertura', '')),
                            'duracion_proceso': 'No especificado',
                            'fuente': str(row.get('Observaciones / Fuente', ''))
                        })
                        inserted_count += 1
                    
                    except Exception as e:
                        print(f"Error insertando fila del Excel en MySQL: {e}")
                        continue
                
                conn.commit()
                return inserted_count
                
        except Exception as e:
            print(f"Error cargando Excel en MySQL: {e}")
            return 0
    
    def _load_excel_sqlite(self, df: pd.DataFrame) -> int:
        """Cargar datos del Excel en SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Crear tabla becas_excel si no existe
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS becas_excel (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero TEXT,
                    nombre_beca TEXT,
                    promedio_minimo TEXT,
                    condicion_socioeconomica TEXT,
                    documentacion TEXT,
                    beneficios TEXT,
                    duracion_proceso TEXT,
                    fuente TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
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
                        str(row.get('Requisitos Principales', '')),
                        str(row.get('Institución o Programa', '')),
                        str(row.get('Requisitos Principales', '')),
                        str(row.get('Beneficios / Cobertura', '')),
                        'No especificado',
                        str(row.get('Observaciones / Fuente', ''))
                    ))
                    inserted_count += 1
                
                except Exception as e:
                    print(f"Error insertando fila del Excel en SQLite: {e}")
                    continue
            
            conn.commit()
            conn.close()
            
            return inserted_count
            
        except Exception as e:
            print(f"Error cargando Excel en SQLite: {e}")
            return 0

    def get_excel_becas(self) -> List[Dict]:
        """Obtener becas del Excel"""
        if self.use_mysql:
            return self._get_excel_becas_mysql()
        else:
            return self._get_excel_becas_sqlite()
    
    def _get_excel_becas_mysql(self) -> List[Dict]:
        """Obtener becas del Excel desde MySQL"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT * FROM becas_excel ORDER BY numero"))
                columns = result.keys()
                data = [dict(zip(columns, row)) for row in result.fetchall()]
                return data
        except Exception as e:
            print(f"Error obteniendo datos de Excel desde MySQL: {e}")
            return []
    
    def _get_excel_becas_sqlite(self) -> List[Dict]:
        """Obtener becas del Excel desde SQLite"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM becas_excel ORDER BY numero')
            rows = cursor.fetchall()
            data = [dict(row) for row in rows]
            conn.close()
            return data
        except Exception as e:
            print(f"Error obteniendo datos de Excel desde SQLite: {e}")
            return []

    def close(self):
        """Cerrar conexión a la base de datos"""
        if self.use_mysql and self.engine:
            self.engine.dispose()