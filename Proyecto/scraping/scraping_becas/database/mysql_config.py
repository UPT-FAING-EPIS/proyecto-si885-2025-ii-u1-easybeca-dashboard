import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pymysql

# Configuración de MySQL
MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DATABASE', 'becas_scraping'),
    'charset': 'utf8mb4'
}

def get_mysql_url():
    """Generar URL de conexión a MySQL"""
    config = MYSQL_CONFIG
    return f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}?charset={config['charset']}"

def create_mysql_engine():
    """Crear engine de SQLAlchemy para MySQL"""
    return create_engine(get_mysql_url(), echo=False)

def create_database_if_not_exists():
    """Crear la base de datos si no existe"""
    config = MYSQL_CONFIG
    
    # Conectar sin especificar base de datos
    temp_url = f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}"
    temp_engine = create_engine(temp_url)
    
    try:
        with temp_engine.connect() as conn:
            # Crear base de datos si no existe
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            conn.commit()
        print(f"Base de datos '{config['database']}' creada o ya existe")
    except Exception as e:
        print(f"Error creando base de datos: {e}")
    finally:
        temp_engine.dispose()

def get_session():
    """Obtener sesión de SQLAlchemy"""
    engine = create_mysql_engine()
    Session = sessionmaker(bind=engine)
    return Session()