"""
Web Scraping MEJORADO de PRONABEC 2024 - Memoria Anual
Extrae datos detallados de becarios 2024
"""

import requests
import pdfplumber
import pandas as pd
import re
from io import BytesIO
from typing import List, Dict, Tuple
import json

PDF_URL = "https://cdn.www.gob.pe/uploads/document/file/8154351/6826853-memoria-anual-2024%282%29.pdf?v=1752678425"

def descargar_pdf(url: str) -> BytesIO:
    """Descarga el PDF desde la URL"""
    print(f"📥 Descargando PDF desde: {url}")
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    print("✅ PDF descargado exitosamente")
    return BytesIO(response.content)

def extraer_info_becas_por_tipo(texto: str, pagina: int) -> List[Dict]:
    """Extrae información sobre tipos de becas y sus cifras"""
    datos = []
    
    # Patrones para buscar información de becas
    patrones_becas = [
        r'Beca 18[:\s]+(\d+)',
        r'Beca Permanencia[:\s]+(\d+)',
        r'Beca Vocación[:\s]+(\d+)',
        r'Beca Inclusión[:\s]+(\d+)',
        r'Beca Excelencia[:\s]+(\d+)',
        r'Beca Especial[:\s]+(\d+)',
        r'(\w+\s*\w*)\s+becas?\s+otorgadas[:\s]+(\d+)',
    ]
    
    for patron in patrones_becas:
        matches = re.finditer(patron, texto, re.IGNORECASE)
        for match in matches:
            if len(match.groups()) == 2:
                datos.append({
                    'NombreBeca': match.group(1).strip(),
                    'Cantidad': int(match.group(2)),
                    'Pagina': pagina
                })
            elif len(match.groups()) == 1:
                # Extraer el nombre de la beca del contexto
                inicio = max(0, match.start() - 50)
                contexto = texto[inicio:match.start()]
                nombre = contexto.split('\n')[-1].strip() if '\n' in contexto else 'Beca'
                datos.append({
                    'NombreBeca': nombre,
                    'Cantidad': int(match.group(1)),
                    'Pagina': pagina
                })
    
    return datos

def extraer_info_departamentos(texto: str, pagina: int) -> List[Dict]:
    """Extrae información por departamento"""
    datos = []
    
    departamentos_peru = [
        'Amazonas', 'Áncash', 'Ancash', 'Apurímac', 'Apurimac', 'Arequipa', 
        'Ayacucho', 'Cajamarca', 'Callao', 'Cusco', 'Cuzco', 'Huancavelica',
        'Huánuco', 'Huanuco', 'Ica', 'Junín', 'Junin', 'La Libertad', 
        'Lambayeque', 'Lima', 'Loreto', 'Madre de Dios', 'Moquegua',
        'Pasco', 'Piura', 'Puno', 'San Martín', 'San Martin', 'Tacna',
        'Tumbes', 'Ucayali'
    ]
    
    for dept in departamentos_peru:
        # Buscar menciones del departamento con números
        patron = rf'{dept}[:\s]+(\d+)'
        matches = re.finditer(patron, texto, re.IGNORECASE)
        for match in matches:
            datos.append({
                'Departamento': dept.title(),
                'Cantidad': int(match.group(1)),
                'Pagina': pagina
            })
    
    return datos

def extraer_info_estratos(texto: str, pagina: int) -> List[Dict]:
    """Extrae información sobre estratos socioeconómicos"""
    datos = []
    
    estratos = ['pobre extremo', 'pobre', 'no pobre', 'vulnerable']
    
    for estrato in estratos:
        patron = rf'{estrato}[:\s]+(\d+)'
        matches = re.finditer(patron, texto, re.IGNORECASE)
        for match in matches:
            datos.append({
                'EstratoSocioeconomico': estrato.title(),
                'Cantidad': int(match.group(1)),
                'Pagina': pagina
            })
    
    return datos

def extraer_info_migracion(texto: str, pagina: int) -> List[Dict]:
    """Extrae información sobre migración de becarios"""
    datos = []
    
    patrones = [
        r'migr[óo]\s+(\d+)',
        r'no\s+migr[óo]\s+(\d+)',
        r'movilidad.*?(\d+)',
        r'origen.*?departamento.*?(\d+)',
    ]
    
    for patron in patrones:
        matches = re.finditer(patron, texto, re.IGNORECASE)
        for match in matches:
            # Determinar el contexto
            inicio = max(0, match.start() - 30)
            contexto = texto[inicio:match.start()].lower()
            
            tipo_migracion = 'Migró' if 'no' not in contexto and 'migr' in contexto else 'No migró'
            
            datos.append({
                'TipoMigracion': tipo_migracion,
                'Cantidad': int(match.group(1)),
                'Pagina': pagina
            })
    
    return datos

def extraer_tablas_detalladas(pdf_buffer: BytesIO) -> Tuple[List[Dict], Dict]:
    """Extrae todas las tablas y analiza el contenido del PDF"""
    
    todas_tablas = []
    info_adicional = {
        'becas_por_tipo': [],
        'becas_por_departamento': [],
        'becas_por_estrato': [],
        'becas_por_migracion': [],
        'instituciones': [],
        'carreras': []
    }
    
    with pdfplumber.open(pdf_buffer) as pdf:
        print(f"📄 Total de páginas: {len(pdf.pages)}")
        
        for i, page in enumerate(pdf.pages, 1):
            if i % 10 == 0:
                print(f"  Procesando página {i}/{len(pdf.pages)}...")
            
            # Extraer texto
            texto = page.extract_text() or ""
            
            # Buscar información relevante solo si menciona 2024
            if '2024' in texto:
                # Extraer información de diferentes categorías
                info_adicional['becas_por_tipo'].extend(extraer_info_becas_por_tipo(texto, i))
                info_adicional['becas_por_departamento'].extend(extraer_info_departamentos(texto, i))
                info_adicional['becas_por_estrato'].extend(extraer_info_estratos(texto, i))
                info_adicional['becas_por_migracion'].extend(extraer_info_migracion(texto, i))
            
            # Extraer tablas
            tables = page.extract_tables()
            
            if tables:
                for j, table in enumerate(tables):
                    if table and len(table) > 1:
                        try:
                            # Convertir a DataFrame
                            headers = table[0] if table[0] else [f"Col{k}" for k in range(len(table[1]))]
                            df = pd.DataFrame(table[1:], columns=headers)
                            
                            # Verificar si contiene datos de 2024
                            texto_tabla = df.to_string()
                            if '2024' in texto_tabla or '2024' in texto:
                                todas_tablas.append({
                                    'pagina': i,
                                    'tabla_num': j+1,
                                    'dataframe': df,
                                    'tipo': identificar_tipo_tabla(df, texto)
                                })
                        except Exception as e:
                            continue
    
    return todas_tablas, info_adicional

def identificar_tipo_tabla(df: pd.DataFrame, contexto: str) -> str:
    """Identifica el tipo de tabla basándose en sus columnas y contexto"""
    
    columnas_str = ' '.join([str(col).lower() for col in df.columns if col])
    
    if any(palabra in columnas_str for palabra in ['departamento', 'región', 'region']):
        return 'departamentos'
    elif any(palabra in columnas_str for palabra in ['carrera', 'especialidad', 'área']):
        return 'carreras'
    elif any(palabra in columnas_str for palabra in ['institución', 'institucion', 'universidad']):
        return 'instituciones'
    elif any(palabra in columnas_str for palabra in ['beca', 'modalidad', 'tipo']):
        return 'becas'
    elif any(palabra in columnas_str for palabra in ['estrato', 'socioeconómico']):
        return 'estratos'
    elif any(palabra in columnas_str for palabra in ['migración', 'migracion', 'movilidad']):
        return 'migracion'
    else:
        return 'otros'

def procesar_tablas_por_tipo(tablas: List[Dict]) -> Dict[str, pd.DataFrame]:
    """Agrupa y procesa las tablas por tipo"""
    
    tablas_por_tipo = {
        'departamentos': [],
        'carreras': [],
        'instituciones': [],
        'becas': [],
        'estratos': [],
        'migracion': [],
        'otros': []
    }
    
    for tabla_info in tablas:
        tipo = tabla_info['tipo']
        df = tabla_info['dataframe']
        df['Pagina'] = tabla_info['pagina']
        tablas_por_tipo[tipo].append(df)
    
    # Consolidar tablas del mismo tipo
    resultado = {}
    for tipo, lista_dfs in tablas_por_tipo.items():
        if lista_dfs:
            try:
                df_consolidado = pd.concat(lista_dfs, ignore_index=True)
                resultado[tipo] = df_consolidado
                print(f"  ✓ {tipo.upper()}: {len(df_consolidado)} registros")
            except Exception as e:
                print(f"  ⚠ Error consolidando {tipo}: {e}")
    
    return resultado

def crear_dataset_completo(tablas_procesadas: Dict, info_adicional: Dict) -> pd.DataFrame:
    """Crea un dataset completo combinando todas las fuentes"""
    
    registros = []
    
    # Procesar becas por departamento
    if info_adicional['becas_por_departamento']:
        df_temp = pd.DataFrame(info_adicional['becas_por_departamento'])
        df_temp = df_temp.groupby('Departamento').agg({
            'Cantidad': 'sum',
            'Pagina': 'first'
        }).reset_index()
        
        for _, row in df_temp.iterrows():
            registros.append({
                'NombreBeca': 'N/A',
                'Institucion': 'N/A',
                'AnioBecariosConfirmados': 2024,
                'Departamento': row['Departamento'],
                'Carrera': 'N/A',
                'Modalidad': 'N/A',
                'EstratoSocioeconomico': 'N/A',
                'BecasSegunMigracion': 'N/A',
                'CantidadBecarios': row['Cantidad'],
                'FuentePagina': row['Pagina']
            })
    
    # Procesar becas por tipo
    if info_adicional['becas_por_tipo']:
        df_temp = pd.DataFrame(info_adicional['becas_por_tipo'])
        df_temp = df_temp.groupby('NombreBeca').agg({
            'Cantidad': 'sum',
            'Pagina': 'first'
        }).reset_index()
        
        for _, row in df_temp.iterrows():
            registros.append({
                'NombreBeca': row['NombreBeca'],
                'Institucion': 'N/A',
                'AnioBecariosConfirmados': 2024,
                'Departamento': 'N/A',
                'Carrera': 'N/A',
                'Modalidad': 'N/A',
                'EstratoSocioeconomico': 'N/A',
                'BecasSegunMigracion': 'N/A',
                'CantidadBecarios': row['Cantidad'],
                'FuentePagina': row['Pagina']
            })
    
    # Procesar becas por estrato
    if info_adicional['becas_por_estrato']:
        df_temp = pd.DataFrame(info_adicional['becas_por_estrato'])
        df_temp = df_temp.groupby('EstratoSocioeconomico').agg({
            'Cantidad': 'sum',
            'Pagina': 'first'
        }).reset_index()
        
        for _, row in df_temp.iterrows():
            registros.append({
                'NombreBeca': 'N/A',
                'Institucion': 'N/A',
                'AnioBecariosConfirmados': 2024,
                'Departamento': 'N/A',
                'Carrera': 'N/A',
                'Modalidad': 'N/A',
                'EstratoSocioeconomico': row['EstratoSocioeconomico'],
                'BecasSegunMigracion': 'N/A',
                'CantidadBecarios': row['Cantidad'],
                'FuentePagina': row['Pagina']
            })
    
    # Procesar becas por migración
    if info_adicional['becas_por_migracion']:
        df_temp = pd.DataFrame(info_adicional['becas_por_migracion'])
        df_temp = df_temp.groupby('TipoMigracion').agg({
            'Cantidad': 'sum',
            'Pagina': 'first'
        }).reset_index()
        
        for _, row in df_temp.iterrows():
            registros.append({
                'NombreBeca': 'N/A',
                'Institucion': 'N/A',
                'AnioBecariosConfirmados': 2024,
                'Departamento': 'N/A',
                'Carrera': 'N/A',
                'Modalidad': 'N/A',
                'EstratoSocioeconomico': 'N/A',
                'BecasSegunMigracion': row['TipoMigracion'],
                'CantidadBecarios': row['Cantidad'],
                'FuentePagina': row['Pagina']
            })
    
    # Procesar tablas estructuradas
    for tipo, df in tablas_procesadas.items():
        if tipo == 'departamentos':
            # Extraer información de departamentos
            for col in df.columns:
                if 'departamento' in str(col).lower() or 'región' in str(col).lower():
                    for _, row in df.iterrows():
                        if pd.notna(row[col]) and str(row[col]).strip():
                            registros.append({
                                'NombreBeca': 'N/A',
                                'Institucion': 'N/A',
                                'AnioBecariosConfirmados': 2024,
                                'Departamento': str(row[col]),
                                'Carrera': 'N/A',
                                'Modalidad': 'N/A',
                                'EstratoSocioeconomico': 'N/A',
                                'BecasSegunMigracion': 'N/A',
                                'CantidadBecarios': 1,
                                'FuentePagina': row.get('Pagina', 0)
                            })
    
    if registros:
        df_final = pd.DataFrame(registros)
        # Eliminar duplicados
        df_final = df_final.drop_duplicates()
        # Reemplazar N/A por valores nulos para mejor manejo
        df_final = df_final.replace('N/A', pd.NA)
        return df_final
    else:
        return pd.DataFrame()

def main():
    """Función principal mejorada"""
    try:
        print("\n" + "="*70)
        print("  WEB SCRAPING PRONABEC 2024 - MEMORIA ANUAL")
        print("="*70 + "\n")
        
        # Descargar PDF
        pdf_buffer = descargar_pdf(PDF_URL)
        
        # Extraer tablas y datos
        print("\n📊 EXTRAYENDO DATOS DEL PDF...")
        tablas, info_adicional = extraer_tablas_detalladas(pdf_buffer)
        print(f"✅ {len(tablas)} tablas encontradas con datos de 2024")
        
        # Procesar tablas por tipo
        print("\n🔄 PROCESANDO TABLAS POR CATEGORÍA...")
        tablas_procesadas = procesar_tablas_por_tipo(tablas)
        
        # Crear dataset completo
        print("\n📋 CREANDO DATASET CONSOLIDADO...")
        df_final = crear_dataset_completo(tablas_procesadas, info_adicional)
        
        if not df_final.empty:
            print(f"\n✅ Dataset creado: {len(df_final)} registros")
            
            # Mostrar estadísticas
            print("\n📈 ESTADÍSTICAS DE DATOS EXTRAÍDOS:")
            print(f"  • Total de registros: {len(df_final)}")
            print(f"  • Becas con nombre: {df_final['NombreBeca'].notna().sum()}")
            print(f"  • Departamentos identificados: {df_final['Departamento'].notna().sum()}")
            print(f"  • Estratos identificados: {df_final['EstratoSocioeconomico'].notna().sum()}")
            print(f"  • Datos de migración: {df_final['BecasSegunMigracion'].notna().sum()}")
            
            # Vista previa
            print("\n📄 VISTA PREVIA DE LOS DATOS:")
            print(df_final.head(15).to_string())
            
            # Guardar archivos
            print("\n💾 GUARDANDO ARCHIVOS...")
            
            # CSV principal
            archivo_csv = "pronabec_becarios_2024_completo.csv"
            df_final.to_csv(archivo_csv, index=False, encoding='utf-8-sig')
            print(f"  ✓ {archivo_csv}")
            
            # Excel principal
            archivo_excel = "pronabec_becarios_2024_completo.xlsx"
            df_final.to_excel(archivo_excel, index=False, engine='openpyxl')
            print(f"  ✓ {archivo_excel}")
            
            # Guardar tablas individuales por categoría
            for tipo, df in tablas_procesadas.items():
                if not df.empty:
                    archivo = f"pronabec_2024_{tipo}.csv"
                    df.to_csv(archivo, index=False, encoding='utf-8-sig')
                    print(f"  ✓ {archivo}")
            
            # Guardar información adicional en JSON
            info_json = {k: v for k, v in info_adicional.items() if v}
            if info_json:
                with open('pronabec_2024_info_adicional.json', 'w', encoding='utf-8') as f:
                    json.dump(info_json, f, indent=2, ensure_ascii=False)
                print(f"  ✓ pronabec_2024_info_adicional.json")
            
        else:
            print("\n⚠ No se pudieron extraer datos estructurados")
            print("Guardando tablas sin procesar...")
            
            for tabla_info in tablas:
                df = tabla_info['dataframe']
                archivo = f"tabla_pag{tabla_info['pagina']}_tipo_{tabla_info['tipo']}.csv"
                df.to_csv(archivo, index=False, encoding='utf-8-sig')
                print(f"  - {archivo}")
        
        print("\n" + "="*70)
        print("  ✅ PROCESO COMPLETADO EXITOSAMENTE")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
