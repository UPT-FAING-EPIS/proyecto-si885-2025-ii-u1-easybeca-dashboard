"""
Parser para extraer datos estructurados de becas del archivo JSON
generado por el scraper principal
"""

import json
import pandas as pd
import re

def parse_beca_18_por_region(tables):
    """
    Extrae datos de Beca 18 por región (página 104)
    """
    data = []
    for table in tables:
        if table['page'] == 104:
            table_data = table['data']
            headers = table_data[0]
            
            for row in table_data[1:]:
                if row[0] and row[0] != 'Total':
                    data.append({
                        'NombreBeca': 'Beca 18',
                        'AnioBecariosConfirmados': 2020,
                        'Departamento': row[0],
                        'BecariosNuevos': int(row[1].replace(' ', '')) if row[1] else 0,
                        'BecariosContinuadores': int(row[2].replace(' ', '')) if row[2] else 0,
                        'TotalBecarios': int(row[3].replace(' ', '')) if row[3] else 0,
                        'Modalidad': 'Beca 18'
                    })
    
    return data

def parse_beca_18_por_area_estudio(tables):
    """
    Extrae datos de Beca 18 por área de estudio (página 105)
    """
    data = []
    for table in tables:
        if table['page'] == 105 and table['table_number'] == 1:
            table_data = table['data']
            
            for row in table_data[1:]:
                if row[0] and row[0] != 'Total':
                    # Limpiar nombre de carrera/área
                    area_estudio = row[0].replace('\n', ' ').strip()
                    
                    data.append({
                        'NombreBeca': 'Beca 18',
                        'AnioBecariosConfirmados': 2020,
                        'Carrera': area_estudio,
                        'BecariosNuevos': int(row[1].replace(' ', '')) if row[1] else 0,
                        'BecariosContinuadores': int(row[2].replace(' ', '')) if row[2] else 0,
                        'TotalBecarios': int(row[3].replace(' ', '')) if row[3] else 0,
                        'Modalidad': 'Beca 18'
                    })
    
    return data

def parse_beca_18_por_tipo_institucion(tables):
    """
    Extrae datos de Beca 18 por tipo de institución (página 105)
    """
    data = []
    for table in tables:
        if table['page'] == 105 and table['table_number'] == 2:
            table_data = table['data']
            
            for row in table_data[1:]:
                if row[0] and row[0] != 'Total':
                    data.append({
                        'NombreBeca': 'Beca 18',
                        'AnioBecariosConfirmados': 2020,
                        'Institucion': row[0].replace('\n', ' ').strip(),
                        'BecariosNuevos': int(row[1].replace(' ', '')) if row[1] else 0,
                        'BecariosContinuadores': int(row[2].replace(' ', '')) if row[2] else 0,
                        'TotalBecarios': int(row[3].replace(' ', '')) if row[3] else 0,
                        'Modalidad': 'Beca 18'
                    })
    
    return data

def parse_beca_posgrado_por_pais(tables):
    """
    Extrae datos de becas de posgrado por país (página 106)
    """
    data = []
    for table in tables:
        if table['page'] == 106 and table['table_number'] == 1:
            table_data = table['data']
            
            for row in table_data[1:]:
                if row[0] and row[0] != 'Total':
                    data.append({
                        'NombreBeca': 'Beca Posgrado',
                        'AnioBecariosConfirmados': 2020,
                        'PaisEstudio': row[0],
                        'BecariosNuevos': int(row[1].replace(' ', '')) if row[1] else 0,
                        'BecariosContinuadores': int(row[2].replace(' ', '')) if row[2] else 0,
                        'TotalBecarios': int(row[3].replace(' ', '')) if row[3] else 0,
                        'Modalidad': 'Beca Posgrado Internacional'
                    })
    
    return data

def parse_beca_posgrado_por_tipo_programa(tables):
    """
    Extrae datos de becas de posgrado por tipo de programa (página 106)
    """
    data = []
    for table in tables:
        if table['page'] == 106 and table['table_number'] == 2:
            table_data = table['data']
            
            for row in table_data[1:]:
                if row[0] and row[0] != 'Total':
                    data.append({
                        'NombreBeca': 'Beca Posgrado',
                        'AnioBecariosConfirmados': 2020,
                        'TipoPrograma': row[0],
                        'BecariosNuevos': int(row[1].replace(' ', '')) if row[1] else 0,
                        'BecariosContinuadores': int(row[2].replace(' ', '')) if row[2] else 0,
                        'TotalBecarios': int(row[3].replace(' ', '')) if row[3] else 0,
                        'Modalidad': 'Beca Posgrado Internacional'
                    })
    
    return data

def parse_modalidades_continuadores(tables):
    """
    Extrae datos de continuadores por modalidad (páginas 64, 69, 76)
    """
    data = []
    
    # Página 64 - Diferentes becas
    for table in tables:
        if table['page'] == 64:
            table_data = table['data']
            for row in table_data[1:]:
                if row[0] and len(row) >= 2:
                    nombre_beca = row[0].replace('\n', ' ').strip()
                    continuadores = row[1]
                    
                    # Convertir a número
                    try:
                        continuadores = int(continuadores.replace(' ', '').replace(',', ''))
                    except:
                        continue
                    
                    data.append({
                        'NombreBeca': nombre_beca,
                        'AnioBecariosConfirmados': 2020,
                        'BecariosContinuadores': continuadores,
                        'Modalidad': nombre_beca
                    })
    
    return data

def parse_credito_educativo(tables):
    """
    Extrae datos de créditos educativos (páginas 79-81, 107-110)
    """
    data = []
    
    # Página 79 - Créditos por modalidad
    for table in tables:
        if table['page'] == 79:
            table_data = table['data']
            for row in table_data[1:]:
                if row[0] and len(row) >= 4:
                    modalidad = row[0].replace('\n', ' ').strip()
                    cantidad = row[1]
                    monto = row[2]
                    
                    try:
                        cantidad = int(cantidad.replace(' ', '').replace(',', ''))
                        # Limpiar monto (quitar espacios y convertir)
                        monto_clean = re.sub(r'[^\d.]', '', monto.replace(' ', ''))
                        monto = float(monto_clean) if monto_clean else 0
                    except:
                        continue
                    
                    data.append({
                        'TipoCredito': modalidad,
                        'AnioBecariosConfirmados': 2020,
                        'CantidadCreditos': cantidad,
                        'MontoDesembolsado': monto,
                        'Modalidad': 'Crédito Educativo'
                    })
    
    return data

def buscar_datos_estratos(text_pages):
    """
    Busca información sobre estratos socioeconómicos en el texto
    """
    data = []
    
    # Buscar en páginas de texto menciones a estratos
    for page_info in text_pages:
        text = page_info['text'].lower()
        
        # Buscar patrones de estratos
        if 'pobre extremo' in text or 'pobre extrema' in text:
            # Extraer contexto
            pass
        
        if 'no pobre' in text:
            # Extraer contexto
            pass
    
    return data

def buscar_datos_migracion(text_pages):
    """
    Busca información sobre migración de becarios
    """
    data = []
    
    # Buscar menciones de migración
    for page_info in text_pages:
        text = page_info['text']
        page = page_info['page']
        
        if 'migr' in text.lower() and '2020' in text:
            # Extraer información relevante
            data.append({
                'pagina': page,
                'texto_relevante': text[:500]
            })
    
    return data

def main():
    print("=" * 60)
    print("PARSER DE DATOS DE BECAS PRONABEC 2020")
    print("=" * 60)
    
    # Cargar tablas extraídas
    with open('tablas_extraidas.json', 'r', encoding='utf-8') as f:
        tables = json.load(f)
    
    # Cargar texto extraído
    with open('texto_extraido.json', 'r', encoding='utf-8') as f:
        text_pages = json.load(f)
    
    print(f"\nTablas cargadas: {len(tables)}")
    print(f"Páginas de texto cargadas: {len(text_pages)}")
    
    # Parsear diferentes tipos de datos
    print("\n" + "-" * 60)
    print("Extrayendo datos...")
    
    # 1. Beca 18 por región
    beca18_region = parse_beca_18_por_region(tables)
    print(f"✓ Beca 18 por región: {len(beca18_region)} registros")
    
    # 2. Beca 18 por área de estudio
    beca18_area = parse_beca_18_por_area_estudio(tables)
    print(f"✓ Beca 18 por área de estudio: {len(beca18_area)} registros")
    
    # 3. Beca 18 por tipo de institución
    beca18_institucion = parse_beca_18_por_tipo_institucion(tables)
    print(f"✓ Beca 18 por tipo de institución: {len(beca18_institucion)} registros")
    
    # 4. Beca Posgrado por país
    posgrado_pais = parse_beca_posgrado_por_pais(tables)
    print(f"✓ Beca Posgrado por país: {len(posgrado_pais)} registros")
    
    # 5. Beca Posgrado por tipo de programa
    posgrado_programa = parse_beca_posgrado_por_tipo_programa(tables)
    print(f"✓ Beca Posgrado por tipo de programa: {len(posgrado_programa)} registros")
    
    # 6. Continuadores por modalidad
    continuadores = parse_modalidades_continuadores(tables)
    print(f"✓ Continuadores por modalidad: {len(continuadores)} registros")
    
    # 7. Créditos educativos
    creditos = parse_credito_educativo(tables)
    print(f"✓ Créditos educativos: {len(creditos)} registros")
    
    # Guardar datasets
    print("\n" + "-" * 60)
    print("Guardando datasets...")
    
    # Dataset 1: Beca 18 por región (con departamento)
    if beca18_region:
        df1 = pd.DataFrame(beca18_region)
        df1.to_csv('beca18_por_departamento_2020.csv', index=False, encoding='utf-8-sig')
        df1.to_excel('beca18_por_departamento_2020.xlsx', index=False)
        print(f"✓ beca18_por_departamento_2020.csv ({len(df1)} registros)")
    
    # Dataset 2: Beca 18 por área de estudio (carrera)
    if beca18_area:
        df2 = pd.DataFrame(beca18_area)
        df2.to_csv('beca18_por_carrera_2020.csv', index=False, encoding='utf-8-sig')
        df2.to_excel('beca18_por_carrera_2020.xlsx', index=False)
        print(f"✓ beca18_por_carrera_2020.csv ({len(df2)} registros)")
    
    # Dataset 3: Beca 18 por tipo de institución
    if beca18_institucion:
        df3 = pd.DataFrame(beca18_institucion)
        df3.to_csv('beca18_por_institucion_2020.csv', index=False, encoding='utf-8-sig')
        df3.to_excel('beca18_por_institucion_2020.xlsx', index=False)
        print(f"✓ beca18_por_institucion_2020.csv ({len(df3)} registros)")
    
    # Dataset 4: Becas de Posgrado por país
    if posgrado_pais:
        df4 = pd.DataFrame(posgrado_pais)
        df4.to_csv('beca_posgrado_por_pais_2020.csv', index=False, encoding='utf-8-sig')
        df4.to_excel('beca_posgrado_por_pais_2020.xlsx', index=False)
        print(f"✓ beca_posgrado_por_pais_2020.csv ({len(df4)} registros)")
    
    # Dataset 5: Becas de Posgrado por tipo de programa
    if posgrado_programa:
        df5 = pd.DataFrame(posgrado_programa)
        df5.to_csv('beca_posgrado_por_programa_2020.csv', index=False, encoding='utf-8-sig')
        df5.to_excel('beca_posgrado_por_programa_2020.xlsx', index=False)
        print(f"✓ beca_posgrado_por_programa_2020.csv ({len(df5)} registros)")
    
    # Dataset 6: Continuadores por modalidad
    if continuadores:
        df6 = pd.DataFrame(continuadores)
        df6.to_csv('becarios_continuadores_por_modalidad_2020.csv', index=False, encoding='utf-8-sig')
        df6.to_excel('becarios_continuadores_por_modalidad_2020.xlsx', index=False)
        print(f"✓ becarios_continuadores_por_modalidad_2020.csv ({len(df6)} registros)")
    
    # Dataset 7: Créditos educativos
    if creditos:
        df7 = pd.DataFrame(creditos)
        df7.to_csv('creditos_educativos_2020.csv', index=False, encoding='utf-8-sig')
        df7.to_excel('creditos_educativos_2020.xlsx', index=False)
        print(f"✓ creditos_educativos_2020.csv ({len(df7)} registros)")
    
    # Dataset consolidado
    print("\n" + "-" * 60)
    print("Creando dataset consolidado...")
    
    # Combinar datos para un dataset general
    all_data = []
    
    # Agregar Beca 18 por región
    for record in beca18_region:
        all_data.append({
            'NombreBeca': record['NombreBeca'],
            'Institucion': None,
            'AnioBecariosConfirmados': record['AnioBecariosConfirmados'],
            'Departamento': record['Departamento'],
            'Carrera': None,
            'Modalidad': record['Modalidad'],
            'BecariosNuevos': record['BecariosNuevos'],
            'BecariosContinuadores': record['BecariosContinuadores'],
            'TotalBecarios': record['TotalBecarios']
        })
    
    # Crear DataFrame consolidado
    if all_data:
        df_consolidado = pd.DataFrame(all_data)
        df_consolidado.to_csv('datos_becas_consolidado_2020.csv', index=False, encoding='utf-8-sig')
        df_consolidado.to_excel('datos_becas_consolidado_2020.xlsx', index=False)
        print(f"✓ datos_becas_consolidado_2020.csv ({len(df_consolidado)} registros)")
    
    print("\n" + "=" * 60)
    print("PROCESO COMPLETADO")
    print("=" * 60)
    print("\nArchivos generados:")
    print("  • CSV y Excel por departamento, carrera, institución")
    print("  • Datos de becas de posgrado internacional")
    print("  • Datos de créditos educativos")
    print("  • Dataset consolidado")
    print("\nLos archivos están listos para ser usados en un dashboard.")

if __name__ == "__main__":
    main()
