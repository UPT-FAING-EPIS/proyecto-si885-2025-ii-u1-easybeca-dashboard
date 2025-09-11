import pymysql
import pandas as pd
import json
from typing import List, Dict, Optional
from datetime import datetime
import os
from pathlib import Path
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, Text, Boolean, DateTime, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .mysql_config import create_mysql_engine, create_database_if_not_exists, MYSQL_CONFIG

Base = declarative_base()

class MySQLDatabaseManager:
    def __init__(self):
        self.engine = None
        self.Session = None
        self.init_database()
    
    def init_database(self):
        """Inicializar la base de datos MySQL con las tablas necesarias"""
        try:
            # Crear base de datos si no existe
            create_database_if_not_exists()
            
            # Crear engine y sesión
            self.engine = create_mysql_engine()
            self.Session = sessionmaker(bind=self.engine)
            
            # Crear tablas
            self._create_tables()
            print("Base de datos MySQL inicializada correctamente")
            
        except Exception as e:
            print(f"Error inicializando base de datos MySQL: {e}")
            raise
    
    def _create_tables(self):
        """Crear las tablas necesarias en MySQL"""
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
            
            # Tabla de becas del Excel original
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS becas_excel (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    numero INT,
                    nombre_beca VARCHAR(500) NOT NULL,
                    promedio_minimo VARCHAR(50),
                    condicion_socioeconomica VARCHAR(200),
                    documentacion TEXT,
                    beneficios TEXT,
                    duracion_proceso VARCHAR(100),
                    observaciones TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_nombre_beca (nombre_beca)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            
            # Tabla de comparaciones
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS comparaciones (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    beca_scrapeada_id INT,
                    beca_excel_id INT,
                    similitud FLOAT,
                    tipo_match VARCHAR(50),
                    fecha_comparacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (beca_scrapeada_id) REFERENCES becas_scrapeadas(id),
                    FOREIGN KEY (beca_excel_id) REFERENCES becas_excel(id),
                    INDEX idx_similitud (similitud),
                    INDEX idx_tipo_match (tipo_match)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """))
            
            conn.commit()
    
    def save_scraped_data(self, source: str, data: List[Dict]):
        """Guardar datos scrapeados en MySQL"""
        if not data:
            return 0
        
        # Agregar fuente a cada elemento
        for item in data:
            item['fuente'] = source
            if 'fecha_scraping' not in item:
                item['fecha_scraping'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return self.insert_scraped_becas(data)
    
    def insert_scraped_becas(self, becas_data: List[Dict]) -> int:
        """Insertar becas scrapeadas en MySQL"""
        if not becas_data:
            return 0
        
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
    
    def get_all_scraped_data(self) -> List[Dict]:
        """Obtener todos los datos scrapeados de MySQL"""
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
    
    def get_scraped_data_by_source(self, source: str) -> List[Dict]:
        """Obtener datos scrapeados por fuente"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("""
                    SELECT * FROM becas_scrapeadas 
                    WHERE fuente = :source AND activo = TRUE 
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
    
    def get_statistics(self) -> Dict:
        """Obtener estadísticas de la base de datos"""
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
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
        except Exception as e:
            print(f"Error obteniendo estadísticas de MySQL: {e}")
            return {'total': 0, 'by_source': {}, 'last_updated': ''}
    
    def close(self):
        """Cerrar conexión a la base de datos"""
        if self.engine:
            self.engine.dispose()