import requests
import pdfplumber
import pandas as pd
import re
import io
from pathlib import Path

# URL del PDF
PDF_URL = "https://cdn.www.gob.pe/uploads/document/file/4498935/Memoria%20Anual%20del%20Pronabec%202022.pdf?v=1683306322"

def descargar_pdf(url):
    """Descarga el PDF desde la URL"""
    print("Descargando PDF...")
    response = requests.get(url)
    if response.status_code == 200:
        print("PDF descargado exitosamente")
        return io.BytesIO(response.content)
    else:
        raise Exception(f"Error al descargar el PDF: {response.status_code}")

def extraer_tablas_del_pdf(pdf_bytes):
    """Extrae todas las tablas del PDF"""
    tablas_extraidas = []
    
    with pdfplumber.open(pdf_bytes) as pdf:
        print(f"Total de páginas: {len(pdf.pages)}")
        
        for i, page in enumerate(pdf.pages):
            print(f"Procesando página {i+1}...")
            
            # Extraer texto de la página para contexto
            texto = page.extract_text()
            
            # Extraer tablas
            tablas = page.extract_tables()
            
            if tablas:
                for j, tabla in enumerate(tablas):
                    if tabla and len(tabla) > 0:
                        tablas_extraidas.append({
                            'pagina': i+1,
                            'tabla_num': j+1,
                            'datos': tabla,
                            'contexto': texto[:500]  # Primeros 500 caracteres de contexto
                        })
    
    print(f"Total de tablas extraídas: {len(tablas_extraidas)}")
    return tablas_extraidas

def limpiar_y_procesar_datos(tablas_extraidas):
    """Procesa y limpia los datos extraídos"""
    datasets = []
    
    for tabla_info in tablas_extraidas:
        tabla = tabla_info['datos']
        pagina = tabla_info['pagina']
        
        # Convertir a DataFrame
        if len(tabla) > 1:
            try:
                # Usar la primera fila como encabezado
                headers = tabla[0]
                data = tabla[1:]
                
                df = pd.DataFrame(data, columns=headers)
                
                # Limpiar valores None y espacios
                df = df.fillna('')
                df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
                
                # Filtrar filas vacías
                df = df[df.apply(lambda row: any(row.astype(str).str.strip() != ''), axis=1)]
                
                if not df.empty:
                    df['pagina_origen'] = pagina
                    datasets.append({
                        'dataframe': df,
                        'pagina': pagina,
                        'contexto': tabla_info['contexto']
                    })
            except Exception as e:
                print(f"Error procesando tabla en página {pagina}: {e}")
    
    return datasets

def identificar_datasets_relevantes(datasets):
    """Identifica los datasets relevantes basados en palabras clave"""
    keywords_relevantes = [
        'beca', 'becario', 'departamento', 'carrera', 'institución', 
        'modalidad', 'estrato', 'migración', 'pobreza', 'programa',
        'universidad', 'instituto', '2022'
    ]
    
    datasets_relevantes = []
    
    for dataset in datasets:
        df = dataset['dataframe']
        contexto = dataset['contexto'].lower()
        
        # Verificar si el contexto o las columnas contienen palabras clave
        columnas_str = ' '.join([str(col).lower() for col in df.columns])
        contenido = contexto + ' ' + columnas_str
        
        score = sum(1 for keyword in keywords_relevantes if keyword in contenido)
        
        if score > 2:  # Al menos 3 palabras clave coincidentes
            dataset['relevancia_score'] = score
            datasets_relevantes.append(dataset)
    
    # Ordenar por relevancia
    datasets_relevantes.sort(key=lambda x: x['relevancia_score'], reverse=True)
    
    return datasets_relevantes

def main():
    try:
        # Descargar PDF
        pdf_bytes = descargar_pdf(PDF_URL)
        
        # Extraer tablas
        tablas = extraer_tablas_del_pdf(pdf_bytes)
        
        # Procesar datos
        datasets = limpiar_y_procesar_datos(tablas)
        
        # Identificar datasets relevantes
        datasets_relevantes = identificar_datasets_relevantes(datasets)
        
        print(f"\n{'='*60}")
        print(f"DATASETS RELEVANTES ENCONTRADOS: {len(datasets_relevantes)}")
        print(f"{'='*60}\n")
        
        # Guardar cada dataset relevante
        output_dir = Path("datos_extraidos")
        output_dir.mkdir(exist_ok=True)
        
        # Crear un Excel con múltiples hojas
        excel_path = output_dir / "pronabec_2022_datos.xlsx"
        
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            for idx, dataset in enumerate(datasets_relevantes[:10]):  # Limitar a los 10 más relevantes
                df = dataset['dataframe']
                pagina = dataset['pagina']
                relevancia = dataset['relevancia_score']
                
                sheet_name = f"Pagina_{pagina}_Tabla_{idx+1}"[:31]  # Excel limita a 31 caracteres
                
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                print(f"Dataset {idx+1}:")
                print(f"  - Página: {pagina}")
                print(f"  - Relevancia: {relevancia}")
                print(f"  - Dimensiones: {df.shape}")
                print(f"  - Columnas: {list(df.columns)}")
                print(f"  - Primeras filas:")
                print(df.head(3))
                print(f"\n{'-'*60}\n")
        
        print(f"\n✓ Datos guardados en: {excel_path}")
        
        # También guardar todos los datasets como CSV individuales
        for idx, dataset in enumerate(datasets_relevantes[:10]):
            df = dataset['dataframe']
            pagina = dataset['pagina']
            csv_path = output_dir / f"tabla_pagina_{pagina}_dataset_{idx+1}.csv"
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        
        print(f"✓ Archivos CSV individuales guardados en: {output_dir}")
        
        # Crear un resumen
        resumen = []
        for idx, dataset in enumerate(datasets_relevantes):
            resumen.append({
                'Dataset': idx + 1,
                'Pagina': dataset['pagina'],
                'Relevancia': dataset['relevancia_score'],
                'Filas': dataset['dataframe'].shape[0],
                'Columnas': dataset['dataframe'].shape[1],
                'Columnas_nombres': ', '.join(dataset['dataframe'].columns)
            })
        
        df_resumen = pd.DataFrame(resumen)
        resumen_path = output_dir / "resumen_datasets.csv"
        df_resumen.to_csv(resumen_path, index=False, encoding='utf-8-sig')
        print(f"✓ Resumen guardado en: {resumen_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
