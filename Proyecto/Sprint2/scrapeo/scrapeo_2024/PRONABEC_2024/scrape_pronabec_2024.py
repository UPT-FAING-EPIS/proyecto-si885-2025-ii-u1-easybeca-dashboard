"""
Web Scraping de PRONABEC 2024 - Memoria Anual
Extrae datos de becarios del año 2024 del documento PDF oficial
"""

import requests
import pdfplumber
import pandas as pd
import re
from io import BytesIO
from typing import List, Dict

# URL del PDF
PDF_URL = "https://cdn.www.gob.pe/uploads/document/file/8154351/6826853-memoria-anual-2024%282%29.pdf?v=1752678425"

def descargar_pdf(url: str) -> BytesIO:
    """Descarga el PDF desde la URL"""
    print(f"Descargando PDF desde: {url}")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    print("PDF descargado exitosamente")
    return BytesIO(response.content)

def extraer_tablas_pdf(pdf_buffer: BytesIO) -> List[pd.DataFrame]:
    """Extrae todas las tablas del PDF"""
    tablas = []
    
    with pdfplumber.open(pdf_buffer) as pdf:
        print(f"Total de páginas: {len(pdf.pages)}")
        
        for i, page in enumerate(pdf.pages):
            print(f"Procesando página {i+1}/{len(pdf.pages)}")
            
            # Extraer texto para buscar menciones de 2024
            texto = page.extract_text()
            
            # Extraer tablas
            tables = page.extract_tables()
            
            if tables:
                for table in tables:
                    if table and len(table) > 1:  # Verificar que tenga contenido
                        # Convertir a DataFrame
                        df = pd.DataFrame(table[1:], columns=table[0])
                        
                        # Verificar si contiene datos de 2024
                        texto_tabla = df.to_string()
                        if '2024' in texto_tabla or '2024' in str(texto):
                            tablas.append({
                                'pagina': i+1,
                                'dataframe': df,
                                'texto_contexto': texto[:500] if texto else ""
                            })
                            print(f"  ✓ Tabla encontrada con posible referencia a 2024")
    
    return tablas

def procesar_datos_becarios(tablas: List[Dict]) -> pd.DataFrame:
    """Procesa las tablas extraídas y estructura los datos de becarios"""
    
    datos_becarios = []
    
    for tabla_info in tablas:
        df = tabla_info['dataframe']
        pagina = tabla_info['pagina']
        
        print(f"\nAnalizando tabla de página {pagina}")
        print(f"Columnas encontradas: {df.columns.tolist()}")
        print(f"Shape: {df.shape}")
        
        # Buscar columnas relevantes (nombres pueden variar)
        columnas_mapping = {
            'programa': ['programa', 'nombre', 'beca', 'tipo de beca', 'nombre del programa'],
            'institucion': ['institución', 'institucion', 'universidad', 'centro educativo'],
            'departamento': ['departamento', 'región', 'region', 'ubicación'],
            'carrera': ['carrera', 'especialidad', 'programa académico', 'área'],
            'modalidad': ['modalidad', 'categoría', 'categoria', 'tipo'],
            'estrato': ['estrato', 'nivel socioeconómico', 'condición socioeconómica'],
            'migracion': ['migración', 'migracion', 'movilidad', 'origen'],
            'anio': ['año', 'anio', 'periodo']
        }
        
        # Intentar identificar columnas
        columnas_encontradas = {}
        for key, posibles_nombres in columnas_mapping.items():
            for col in df.columns:
                if col and any(nombre.lower() in str(col).lower() for nombre in posibles_nombres):
                    columnas_encontradas[key] = col
                    break
        
        print(f"Columnas identificadas: {columnas_encontradas}")
        
        # Si encontramos columnas relevantes, extraer datos
        if columnas_encontradas:
            for idx, row in df.iterrows():
                try:
                    registro = {
                        'NombreBeca': row.get(columnas_encontradas.get('programa', ''), ''),
                        'Institucion': row.get(columnas_encontradas.get('institucion', ''), ''),
                        'AnioBecariosConfirmados': 2024,  # Por defecto 2024
                        'Departamento': row.get(columnas_encontradas.get('departamento', ''), ''),
                        'Carrera': row.get(columnas_encontradas.get('carrera', ''), ''),
                        'Modalidad': row.get(columnas_encontradas.get('modalidad', ''), ''),
                        'EstratoSocioeconomico': row.get(columnas_encontradas.get('estrato', ''), ''),
                        'BecasSegunMigracion': row.get(columnas_encontradas.get('migracion', ''), ''),
                        'Pagina': pagina
                    }
                    
                    # Solo agregar si tiene al menos un dato relevante
                    if any(registro[k] for k in ['NombreBeca', 'Institucion', 'Carrera']):
                        datos_becarios.append(registro)
                except Exception as e:
                    print(f"Error procesando fila {idx}: {e}")
                    continue
    
    if datos_becarios:
        df_final = pd.DataFrame(datos_becarios)
        # Limpiar datos vacíos
        df_final = df_final.replace('', pd.NA)
        return df_final
    else:
        return pd.DataFrame()

def extraer_texto_completo(pdf_buffer: BytesIO) -> str:
    """Extrae todo el texto del PDF para análisis adicional"""
    texto_completo = []
    
    with pdfplumber.open(pdf_buffer) as pdf:
        for page in pdf.pages:
            texto = page.extract_text()
            if texto:
                texto_completo.append(texto)
    
    return "\n".join(texto_completo)

def main():
    """Función principal"""
    try:
        # Descargar PDF
        pdf_buffer = descargar_pdf(PDF_URL)
        
        # Extraer tablas
        print("\n" + "="*50)
        print("EXTRAYENDO TABLAS DEL PDF")
        print("="*50)
        tablas = extraer_tablas_pdf(pdf_buffer)
        print(f"\nTotal de tablas encontradas: {len(tablas)}")
        
        # Procesar datos
        print("\n" + "="*50)
        print("PROCESANDO DATOS DE BECARIOS 2024")
        print("="*50)
        
        if tablas:
            df_becarios = procesar_datos_becarios(tablas)
            
            if not df_becarios.empty:
                print(f"\n✓ Datos extraídos exitosamente: {len(df_becarios)} registros")
                print("\nVista previa de los datos:")
                print(df_becarios.head(10))
                print("\nResumen de datos:")
                print(df_becarios.info())
                
                # Guardar a CSV
                archivo_salida = "pronabec_becarios_2024.csv"
                df_becarios.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
                print(f"\n✓ Datos guardados en: {archivo_salida}")
                
                # Guardar también en Excel
                archivo_excel = "pronabec_becarios_2024.xlsx"
                df_becarios.to_excel(archivo_excel, index=False, engine='openpyxl')
                print(f"✓ Datos guardados en: {archivo_excel}")
            else:
                print("\n⚠ No se pudieron estructurar los datos automáticamente")
                print("Guardando tablas sin procesar para revisión manual...")
                
                # Guardar tablas sin procesar
                for i, tabla_info in enumerate(tablas):
                    df = tabla_info['dataframe']
                    archivo = f"tabla_pagina_{tabla_info['pagina']}_num_{i+1}.csv"
                    df.to_csv(archivo, index=False, encoding='utf-8-sig')
                    print(f"  - Guardada: {archivo}")
        else:
            print("\n⚠ No se encontraron tablas en el PDF")
            print("Extrayendo texto completo para análisis manual...")
            
            # Reiniciar buffer
            pdf_buffer.seek(0)
            texto = extraer_texto_completo(pdf_buffer)
            
            with open("pronabec_2024_texto_completo.txt", "w", encoding="utf-8") as f:
                f.write(texto)
            print("✓ Texto completo guardado en: pronabec_2024_texto_completo.txt")
        
        print("\n" + "="*50)
        print("PROCESO COMPLETADO")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
