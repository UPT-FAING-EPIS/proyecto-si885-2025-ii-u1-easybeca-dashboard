"""
Web Scraper para extraer datos de becas Pronabec 2020
Extrae información de la Memoria Anual del Pronabec 2020
"""

import requests
import pdfplumber
import pandas as pd
import re
from io import BytesIO
import json

# URL del PDF
PDF_URL = "https://cdn.www.gob.pe/uploads/document/file/1984259/Memoria%20Anual%20del%20Pronabec%202020.pdf.pdf?v=1625074615"

def download_pdf(url):
    """Descarga el PDF desde la URL"""
    print(f"Descargando PDF desde: {url}")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        print("PDF descargado exitosamente")
        return BytesIO(response.content)
    except Exception as e:
        print(f"Error al descargar el PDF: {e}")
        return None

def extract_text_from_pdf(pdf_file):
    """Extrae texto de todas las páginas del PDF"""
    print("Extrayendo texto del PDF...")
    all_text = []
    try:
        with pdfplumber.open(pdf_file) as pdf:
            print(f"Total de páginas: {len(pdf.pages)}")
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    all_text.append({
                        'page': i + 1,
                        'text': text
                    })
        print(f"Texto extraído de {len(all_text)} páginas")
        return all_text
    except Exception as e:
        print(f"Error al extraer texto: {e}")
        return []

def extract_tables_from_pdf(pdf_file):
    """Extrae todas las tablas del PDF"""
    print("Extrayendo tablas del PDF...")
    all_tables = []
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for i, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                if tables:
                    for j, table in enumerate(tables):
                        all_tables.append({
                            'page': i + 1,
                            'table_number': j + 1,
                            'data': table
                        })
        print(f"Se encontraron {len(all_tables)} tablas")
        return all_tables
    except Exception as e:
        print(f"Error al extraer tablas: {e}")
        return []

def parse_scholarship_data(tables, text_pages):
    """
    Parsea los datos de becas según los campos requeridos:
    - NombreBeca
    - Institucion
    - AnioBecariosConfirmados
    - Departamento
    - Carrera
    - Modalidad
    - Estrato socieconomico
    - Becas según migración
    """
    print("\nAnalizando datos de becas...")
    
    scholarship_data = []
    
    # Buscar patrones específicos en las tablas
    for table_info in tables:
        page = table_info['page']
        table = table_info['data']
        
        if not table or len(table) == 0:
            continue
            
        print(f"\nProcesando tabla en página {page}:")
        print(f"  Filas: {len(table)}, Columnas: {len(table[0]) if table else 0}")
        
        # Mostrar encabezados de la tabla
        if len(table) > 0:
            print(f"  Encabezados: {table[0]}")
    
    return scholarship_data

def find_relevant_sections(text_pages):
    """Encuentra secciones relevantes en el texto"""
    relevant_keywords = [
        'beca', 'becario', 'programa', 'institución', 'universidad',
        'departamento', 'carrera', 'modalidad', 'estrato', 'migración',
        '2020', 'beneficiario'
    ]
    
    relevant_sections = []
    
    for page_info in text_pages:
        page = page_info['page']
        text = page_info['text'].lower()
        
        # Contar palabras clave
        keyword_count = sum(1 for keyword in relevant_keywords if keyword in text)
        
        if keyword_count >= 3:  # Si tiene al menos 3 palabras clave
            relevant_sections.append({
                'page': page,
                'keywords_found': keyword_count,
                'text': page_info['text'][:500]  # Primeros 500 caracteres
            })
    
    return relevant_sections

def save_data(data, filename):
    """Guarda los datos extraídos"""
    if isinstance(data, list):
        # Guardar como JSON
        json_filename = filename.replace('.csv', '.json')
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\nDatos guardados en: {json_filename}")
        
        # Si hay datos estructurados, guardar como CSV
        if data and isinstance(data[0], dict):
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"Datos guardados en: {filename}")
    else:
        print("No hay datos para guardar")

def main():
    print("=" * 60)
    print("SCRAPER PRONABEC 2020")
    print("=" * 60)
    
    # Descargar PDF
    pdf_file = download_pdf(PDF_URL)
    
    if pdf_file is None:
        print("No se pudo descargar el PDF. Verifica la URL y tu conexión.")
        return
    
    # Extraer texto
    text_pages = extract_text_from_pdf(pdf_file)
    
    # Reiniciar el buffer para leer de nuevo
    pdf_file.seek(0)
    
    # Extraer tablas
    tables = extract_tables_from_pdf(pdf_file)
    
    # Guardar texto crudo para análisis
    if text_pages:
        with open('texto_extraido.json', 'w', encoding='utf-8') as f:
            json.dump(text_pages, f, ensure_ascii=False, indent=2)
        print("\nTexto extraído guardado en: texto_extraido.json")
    
    # Guardar tablas crudas
    if tables:
        with open('tablas_extraidas.json', 'w', encoding='utf-8') as f:
            json.dump(tables, f, ensure_ascii=False, indent=2)
        print("Tablas extraídas guardadas en: tablas_extraidas.json")
    
    # Encontrar secciones relevantes
    relevant_sections = find_relevant_sections(text_pages)
    print(f"\n{len(relevant_sections)} páginas relevantes encontradas:")
    for section in relevant_sections[:10]:  # Mostrar primeras 10
        print(f"  - Página {section['page']}: {section['keywords_found']} palabras clave")
    
    # Parsear datos de becas
    scholarship_data = parse_scholarship_data(tables, text_pages)
    
    print("\n" + "=" * 60)
    print("RESUMEN DE EXTRACCIÓN")
    print("=" * 60)
    print(f"Páginas procesadas: {len(text_pages)}")
    print(f"Tablas encontradas: {len(tables)}")
    print(f"Páginas relevantes: {len(relevant_sections)}")
    print(f"Registros de becas extraídos: {len(scholarship_data)}")
    
    # Guardar datos
    if scholarship_data:
        save_data(scholarship_data, 'becas_pronabec_2020.csv')
    
    print("\n¡Proceso completado!")
    print("\nNOTA: Revisa los archivos JSON generados para analizar")
    print("      la estructura de las tablas y ajustar el parser.")

if __name__ == "__main__":
    main()
