"""
Script para extraer datos de la Memoria Anual del Pronabec 2023
Extrae información sobre Beca 18: instituciones, departamentos, carreras, modalidades, etc.
"""

import requests
import PyPDF2
import pandas as pd
import re
from io import BytesIO
import json

# URL del PDF
PDF_URL = "https://cdn.www.gob.pe/uploads/document/file/6317263/5552590-memoria-anual-del-pronabec-2023.pdf?v=1715184066"

def descargar_pdf(url):
    """Descarga el PDF desde la URL"""
    print(f"Descargando PDF desde: {url}")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        print("✓ PDF descargado exitosamente")
        return BytesIO(response.content)
    except Exception as e:
        print(f"✗ Error al descargar el PDF: {e}")
        return None

def extraer_texto_pdf(pdf_file):
    """Extrae todo el texto del PDF"""
    print("\nExtrayendo texto del PDF...")
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        texto_completo = []
        
        total_paginas = len(pdf_reader.pages)
        print(f"Total de páginas: {total_paginas}")
        
        for i, page in enumerate(pdf_reader.pages):
            texto = page.extract_text()
            texto_completo.append({
                'pagina': i + 1,
                'texto': texto
            })
            if (i + 1) % 10 == 0:
                print(f"  Procesadas {i + 1}/{total_paginas} páginas...")
        
        print("✓ Texto extraído exitosamente")
        return texto_completo
    except Exception as e:
        print(f"✗ Error al extraer texto: {e}")
        return None

def buscar_tablas_datos(texto_paginas):
    """Busca y extrae datos relevantes del texto"""
    print("\nBuscando datos relevantes en el documento...")
    
    datos_encontrados = {
        'becarios_por_departamento': [],
        'becarios_por_institucion': [],
        'becarios_por_carrera': [],
        'becarios_por_modalidad': [],
        'becarios_por_estrato': [],
        'becarios_migracion': [],
        'estadisticas_generales': []
    }
    
    # Palabras clave para buscar
    keywords = {
        'departamento': ['departamento', 'región', 'lima', 'cusco', 'arequipa', 'piura'],
        'institucion': ['universidad', 'instituto', 'IES', 'institución educativa'],
        'carrera': ['carrera', 'ingeniería', 'medicina', 'derecho', 'administración'],
        'modalidad': ['modalidad', 'beca 18', 'ordinaria', 'especial', 'permanencia'],
        'estrato': ['pobreza', 'pobre extremo', 'estrato', 'socioeconómico'],
        'migracion': ['migración', 'migró', 'traslado', 'movilidad']
    }
    
    for pagina_info in texto_paginas:
        pagina_num = pagina_info['pagina']
        texto = pagina_info['texto']
        texto_lower = texto.lower()
        
        # Buscar menciones de Beca 18 y datos del 2023
        if 'beca 18' in texto_lower and '2023' in texto:
            # Buscar números y datos relevantes
            lineas = texto.split('\n')
            for i, linea in enumerate(lineas):
                linea_lower = linea.lower()
                
                # Buscar datos de departamentos
                if any(kw in linea_lower for kw in keywords['departamento']):
                    # Buscar números en las líneas cercanas
                    numeros = re.findall(r'\b\d{1,5}\b', linea)
                    if numeros:
                        datos_encontrados['becarios_por_departamento'].append({
                            'pagina': pagina_num,
                            'texto': linea.strip(),
                            'numeros': numeros
                        })
                
                # Buscar datos de instituciones
                if any(kw in linea_lower for kw in keywords['institucion']):
                    datos_encontrados['becarios_por_institucion'].append({
                        'pagina': pagina_num,
                        'texto': linea.strip()
                    })
                
                # Buscar datos de carreras
                if any(kw in linea_lower for kw in keywords['carrera']):
                    datos_encontrados['becarios_por_carrera'].append({
                        'pagina': pagina_num,
                        'texto': linea.strip()
                    })
                
                # Buscar datos de modalidades
                if any(kw in linea_lower for kw in keywords['modalidad']):
                    datos_encontrados['becarios_por_modalidad'].append({
                        'pagina': pagina_num,
                        'texto': linea.strip()
                    })
                
                # Buscar datos de estrato socioeconómico
                if any(kw in linea_lower for kw in keywords['estrato']):
                    datos_encontrados['becarios_por_estrato'].append({
                        'pagina': pagina_num,
                        'texto': linea.strip()
                    })
                
                # Buscar datos de migración
                if any(kw in linea_lower for kw in keywords['migracion']):
                    datos_encontrados['becarios_migracion'].append({
                        'pagina': pagina_num,
                        'texto': linea.strip()
                    })
    
    return datos_encontrados

def guardar_texto_completo(texto_paginas, filename='texto_completo_pronabec_2023.txt'):
    """Guarda el texto completo extraído para análisis manual"""
    print(f"\nGuardando texto completo en: {filename}")
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for pagina_info in texto_paginas:
                f.write(f"\n{'='*80}\n")
                f.write(f"PÁGINA {pagina_info['pagina']}\n")
                f.write(f"{'='*80}\n\n")
                f.write(pagina_info['texto'])
                f.write("\n\n")
        print(f"✓ Texto completo guardado en: {filename}")
    except Exception as e:
        print(f"✗ Error al guardar texto: {e}")

def guardar_datos_json(datos, filename='datos_pronabec_2023.json'):
    """Guarda los datos extraídos en formato JSON"""
    print(f"\nGuardando datos en: {filename}")
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
        print(f"✓ Datos guardados en: {filename}")
    except Exception as e:
        print(f"✗ Error al guardar datos: {e}")

def mostrar_resumen(datos):
    """Muestra un resumen de los datos encontrados"""
    print("\n" + "="*80)
    print("RESUMEN DE DATOS ENCONTRADOS")
    print("="*80)
    
    for categoria, items in datos.items():
        print(f"\n{categoria.upper().replace('_', ' ')}:")
        print(f"  Total de menciones encontradas: {len(items)}")
        
        # Mostrar los primeros 3 items como ejemplo
        if items:
            print("  Ejemplos:")
            for i, item in enumerate(items[:3]):
                if isinstance(item, dict):
                    if 'texto' in item:
                        texto_corto = item['texto'][:100] + "..." if len(item['texto']) > 100 else item['texto']
                        print(f"    {i+1}. [Pág. {item.get('pagina', '?')}] {texto_corto}")

def main():
    print("="*80)
    print("EXTRACTOR DE DATOS - MEMORIA ANUAL PRONABEC 2023")
    print("="*80)
    
    # 1. Descargar PDF
    pdf_file = descargar_pdf(PDF_URL)
    if not pdf_file:
        print("\n✗ No se pudo descargar el PDF. Abortando.")
        return
    
    # 2. Extraer texto
    texto_paginas = extraer_texto_pdf(pdf_file)
    if not texto_paginas:
        print("\n✗ No se pudo extraer el texto del PDF. Abortando.")
        return
    
    # 3. Guardar texto completo para análisis manual
    guardar_texto_completo(texto_paginas)
    
    # 4. Buscar y extraer datos relevantes
    datos = buscar_tablas_datos(texto_paginas)
    
    # 5. Guardar datos extraídos
    guardar_datos_json(datos)
    
    # 6. Mostrar resumen
    mostrar_resumen(datos)
    
    print("\n" + "="*80)
    print("PROCESO COMPLETADO")
    print("="*80)
    print("\nArchivos generados:")
    print("  1. texto_completo_pronabec_2023.txt - Texto completo del PDF")
    print("  2. datos_pronabec_2023.json - Datos extraídos estructurados")
    print("\nRECOMENDACIÓN: Revisa el archivo 'texto_completo_pronabec_2023.txt'")
    print("para identificar manualmente las tablas y datos específicos del 2023.")

if __name__ == "__main__":
    main()
