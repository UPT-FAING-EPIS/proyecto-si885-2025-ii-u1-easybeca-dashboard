import requests
import pdfplumber
import pandas as pd
import re
import os
from pathlib import Path

# URL del PDF
PDF_URL = "https://cdn.www.gob.pe/uploads/document/file/3157095/Memoria%20Anual%20del%20Pronabec%202021.pdf?v=1653683954"
PDF_FILE = "Memoria_Pronabec_2021.pdf"

def download_pdf(url, filename):
    """Descarga el PDF desde la URL"""
    print(f"Descargando PDF desde {url}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"PDF descargado exitosamente: {filename}")
        return True
    except Exception as e:
        print(f"Error descargando PDF: {e}")
        return False

def extract_text_from_pdf(pdf_path):
    """Extrae todo el texto del PDF"""
    print(f"Extrayendo texto del PDF...")
    text_content = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                print(f"Procesando página {i+1}/{len(pdf.pages)}")
                text = page.extract_text()
                if text:
                    text_content.append({
                        'page': i+1,
                        'text': text
                    })
        print(f"Texto extraído de {len(text_content)} páginas")
        return text_content
    except Exception as e:
        print(f"Error extrayendo texto: {e}")
        return []

def extract_tables_from_pdf(pdf_path):
    """Extrae todas las tablas del PDF"""
    print(f"Extrayendo tablas del PDF...")
    all_tables = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                if tables:
                    print(f"Encontradas {len(tables)} tabla(s) en página {i+1}")
                    for j, table in enumerate(tables):
                        all_tables.append({
                            'page': i+1,
                            'table_number': j+1,
                            'data': table
                        })
        print(f"Total de tablas extraídas: {len(all_tables)}")
        return all_tables
    except Exception as e:
        print(f"Error extrayendo tablas: {e}")
        return []

def search_keywords_in_text(text_content):
    """Busca palabras clave relacionadas con las becas en el texto"""
    keywords = [
        'beca', 'becario', 'departamento', 'carrera', 'modalidad',
        'estrato', 'migración', 'institución', 'universidad', 'programa',
        'socioeconómico', 'pobre', 'confirmados', '2021'
    ]
    
    results = []
    for page_data in text_content:
        text = page_data['text'].lower()
        for keyword in keywords:
            if keyword in text:
                # Extraer contexto alrededor de la palabra clave
                lines = page_data['text'].split('\n')
                for line in lines:
                    if keyword in line.lower():
                        results.append({
                            'page': page_data['page'],
                            'keyword': keyword,
                            'context': line.strip()
                        })
    
    return results

def analyze_tables_for_data(all_tables):
    """Analiza las tablas en busca de datos relevantes"""
    print("\n=== ANÁLISIS DE TABLAS ===")
    
    relevant_tables = []
    
    for table_info in all_tables:
        table = table_info['data']
        page = table_info['page']
        
        if not table or len(table) == 0:
            continue
        
        # Convertir a DataFrame para análisis
        try:
            df = pd.DataFrame(table[1:], columns=table[0]) if len(table) > 1 else pd.DataFrame(table)
            
            # Buscar columnas relevantes
            columns_str = ' '.join([str(col).lower() for col in df.columns if col])
            
            relevant_keywords = [
                'beca', 'becario', 'departamento', 'carrera', 'modalidad',
                'estrato', 'migración', 'institución', 'universidad', 'programa',
                'región', 'cantidad', 'número', 'total', '2021'
            ]
            
            has_relevant_data = any(keyword in columns_str for keyword in relevant_keywords)
            
            if has_relevant_data or len(df) > 5:  # Tablas con datos relevantes o suficientemente grandes
                print(f"\n--- Tabla en página {page} ---")
                print(f"Dimensiones: {df.shape}")
                print(f"Columnas: {df.columns.tolist()}")
                print(f"Primeras filas:\n{df.head()}")
                
                relevant_tables.append({
                    'page': page,
                    'dataframe': df,
                    'table_number': table_info['table_number']
                })
        except Exception as e:
            print(f"Error procesando tabla en página {page}: {e}")
    
    return relevant_tables

def save_results(text_content, all_tables, relevant_tables, keywords_results):
    """Guarda los resultados en archivos"""
    
    # Guardar texto completo
    with open('texto_completo_2021.txt', 'w', encoding='utf-8') as f:
        for page_data in text_content:
            f.write(f"\n{'='*80}\n")
            f.write(f"PÁGINA {page_data['page']}\n")
            f.write(f"{'='*80}\n")
            f.write(page_data['text'])
            f.write('\n')
    print("Texto completo guardado en: texto_completo_2021.txt")
    
    # Guardar palabras clave encontradas
    if keywords_results:
        df_keywords = pd.DataFrame(keywords_results)
        df_keywords.to_excel('palabras_clave_encontradas_2021.xlsx', index=False)
        print("Palabras clave guardadas en: palabras_clave_encontradas_2021.xlsx")
    
    # Guardar tablas relevantes
    if relevant_tables:
        with pd.ExcelWriter('tablas_relevantes_2021.xlsx') as writer:
            for i, table_info in enumerate(relevant_tables):
                sheet_name = f"Pag_{table_info['page']}_Tabla_{table_info['table_number']}"
                table_info['dataframe'].to_excel(writer, sheet_name=sheet_name, index=False)
        print("Tablas relevantes guardadas en: tablas_relevantes_2021.xlsx")
    
    # Guardar todas las tablas
    if all_tables:
        with pd.ExcelWriter('todas_las_tablas_2021.xlsx') as writer:
            for i, table_info in enumerate(all_tables):
                try:
                    table = table_info['data']
                    df = pd.DataFrame(table[1:], columns=table[0]) if len(table) > 1 else pd.DataFrame(table)
                    sheet_name = f"P{table_info['page']}_T{table_info['table_number']}"[:31]  # Excel limit
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                except Exception as e:
                    print(f"Error guardando tabla {i}: {e}")
        print("Todas las tablas guardadas en: todas_las_tablas_2021.xlsx")

def main():
    print("="*80)
    print("SCRAPING DE MEMORIA ANUAL PRONABEC 2021")
    print("="*80)
    
    # Descargar PDF
    if not os.path.exists(PDF_FILE):
        if not download_pdf(PDF_URL, PDF_FILE):
            print("No se pudo descargar el PDF. Terminando.")
            return
    else:
        print(f"PDF ya existe: {PDF_FILE}")
    
    # Extraer texto
    text_content = extract_text_from_pdf(PDF_FILE)
    if not text_content:
        print("No se pudo extraer texto del PDF.")
        return
    
    # Extraer tablas
    all_tables = extract_tables_from_pdf(PDF_FILE)
    
    # Buscar palabras clave
    print("\nBuscando palabras clave relevantes...")
    keywords_results = search_keywords_in_text(text_content)
    print(f"Encontradas {len(keywords_results)} menciones de palabras clave")
    
    # Analizar tablas
    relevant_tables = analyze_tables_for_data(all_tables)
    
    # Guardar resultados
    print("\n" + "="*80)
    print("GUARDANDO RESULTADOS")
    print("="*80)
    save_results(text_content, all_tables, relevant_tables, keywords_results)
    
    print("\n" + "="*80)
    print("PROCESO COMPLETADO")
    print("="*80)
    print("\nArchivos generados:")
    print("1. Memoria_Pronabec_2021.pdf - PDF descargado")
    print("2. texto_completo_2021.txt - Texto completo extraído")
    print("3. palabras_clave_encontradas_2021.xlsx - Menciones de palabras clave")
    print("4. tablas_relevantes_2021.xlsx - Tablas con datos relevantes")
    print("5. todas_las_tablas_2021.xlsx - Todas las tablas extraídas")
    print("\nRevisa estos archivos para identificar los datos específicos que necesitas.")

if __name__ == "__main__":
    main()
