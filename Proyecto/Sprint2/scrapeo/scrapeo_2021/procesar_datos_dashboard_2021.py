import pandas as pd
import re
import json

def procesar_datos_para_dashboard():
    """
    Procesa los datos extraídos del PDF para crear un dataset estructurado
    para el dashboard de becas 2021
    """
    
    print("="*80)
    print("PROCESAMIENTO DE DATOS PARA DASHBOARD - PRONABEC 2021")
    print("="*80)
    
    # Leer todas las tablas extraídas
    all_tables = pd.read_excel('todas_las_tablas_2021.xlsx', sheet_name=None)
    
    # Datasets principales para el dashboard
    dataset_becarios_region = []
    dataset_creditos_educativos = []
    dataset_tipo_gestion = []
    dataset_becarios_pais = []
    dataset_genero = []
    
    # DATOS DE BECARIOS POR REGIÓN (Página 73)
    # Esta tabla contiene: Región, Becarios y becarias, Porcentaje
    if 'P73_T1' in all_tables:
        df_region = all_tables['P73_T1']
        print("\n--- BECARIOS POR REGIÓN (2021) ---")
        print(df_region)
        
        # Limpiar y estructurar datos
        for idx, row in df_region.iterrows():
            if row['Región'] and row['Región'] != 'Región':
                try:
                    becarios = int(str(row['Becarios y becarias']).replace(',', '').replace(' ', ''))
                    porcentaje = str(row['Porcentaje']).replace('%', '').replace(' ', '')
                    
                    dataset_becarios_region.append({
                        'NombreBeca': 'Beca 18',  # Programa principal
                        'Institucion': 'Varias',
                        'AnioBecariosConfirmados': 2021,
                        'Departamento': row['Región'],
                        'Carrera': 'Varias',
                        'Modalidad': 'General',
                        'EstratoSocioeconomico': 'No especificado',
                        'Migracion': 'No especificado',
                        'CantidadBecarios': becarios,
                        'PorcentajeRegional': porcentaje
                    })
                except Exception as e:
                    print(f"Error procesando región {row['Región']}: {e}")
    
    # DATOS DE TIPO DE GESTIÓN Y MIGRACIÓN (Páginas 74-75)
    # Convocatoria 2021 - Tipo de gestión (Asociativa, Societaria, Pública)
    if 'P74_T1' in all_tables:
        df_gestion = all_tables['P74_T1']
        print("\n--- TIPO DE GESTIÓN INSTITUCIONAL (2021) ---")
        print(df_gestion)
        
        for idx, row in df_gestion.iterrows():
            tipo_gestion = row['Tipo de gestión']
            if tipo_gestion and tipo_gestion not in ['None', None, 'Total']:
                try:
                    # Buscar columna de convocatoria 2021
                    cantidad_2021 = None
                    for col in df_gestion.columns:
                        if '2021' in str(col):
                            cantidad_2021 = df_gestion.loc[idx, col]
                            break
                    
                    if cantidad_2021 and str(cantidad_2021).strip().replace(' ', '').isdigit():
                        cantidad = int(str(cantidad_2021).replace(' ', '').replace(',', ''))
                        dataset_tipo_gestion.append({
                            'NombreBeca': 'Beca 18',
                            'AnioBecariosConfirmados': 2021,
                            'TipoGestion': tipo_gestion,
                            'CantidadBecarios': cantidad
                        })
                except Exception as e:
                    print(f"Error procesando tipo gestión: {e}")
    
    # DATOS DE MIGRACIÓN (Página 74 - segunda tabla y 75)
    # Región Lima vs Otras regiones (origen y destino)
    if 'P74_T2' in all_tables:
        df_migracion_origen = all_tables['P74_T2']
        print("\n--- MIGRACIÓN - REGIÓN DE ORIGEN (2021) ---")
        print(df_migracion_origen)
    
    if 'P75_T1' in all_tables:
        df_migracion_destino = all_tables['P75_T1']
        print("\n--- MIGRACIÓN - REGIÓN DE DESTINO (2021) ---")
        print(df_migracion_destino)
    
    # DATOS DE BECARIOS POR PAÍS (Página 75)
    if 'P75_T2' in all_tables:
        df_pais = all_tables['P75_T2']
        print("\n--- BECARIOS POR PAÍS (2021) ---")
        print(df_pais)
        
        for idx, row in df_pais.iterrows():
            if row['País'] and row['País'] != 'País':
                try:
                    cantidad = int(str(row['n.º de becarios y becarias']).replace(',', '').replace(' ', ''))
                    dataset_becarios_pais.append({
                        'NombreBeca': 'Becas en el Extranjero',
                        'Institucion': 'Internacional',
                        'AnioBecariosConfirmados': 2021,
                        'Pais': row['País'],
                        'CantidadBecarios': cantidad
                    })
                except Exception as e:
                    print(f"Error procesando país: {e}")
    
    # DATOS DE CRÉDITOS EDUCATIVOS (Páginas 77-82)
    # Género y región para créditos
    credito_genero_pages = ['P77_T1', 'P79_T1', 'P80_T1', 'P81_T1']
    credito_tipos = ['Crédito General', 'Crédito Talento', 'Crédito 18', 'Crédito Continuidad']
    
    for i, page_key in enumerate(credito_genero_pages):
        if page_key in all_tables:
            df_credito_genero = all_tables[page_key]
            print(f"\n--- {credito_tipos[i]} - GÉNERO (2021) ---")
            print(df_credito_genero)
            
            for idx, row in df_credito_genero.iterrows():
                genero = row['Género']
                if genero and genero not in ['None', None, 'Total']:
                    try:
                        cantidad = int(str(row['Cantidad de créditos']).replace(',', '').replace(' ', ''))
                        dataset_genero.append({
                            'NombreBeca': credito_tipos[i],
                            'AnioBecariosConfirmados': 2021,
                            'Genero': genero,
                            'CantidadCreditos': cantidad
                        })
                    except Exception as e:
                        print(f"Error procesando género: {e}")
    
    # DATOS DE CRÉDITOS POR REGIÓN (Páginas 78-82)
    credito_region_pages = {
        'P78_T1': 'Crédito General',
        'P79_T2': 'Crédito Talento',
        'P80_T2': 'Crédito 18',
        'P82_T1': 'Crédito Continuidad'
    }
    
    for page_key, tipo_credito in credito_region_pages.items():
        if page_key in all_tables:
            df_credito_region = all_tables[page_key]
            print(f"\n--- {tipo_credito} - REGIÓN (2021) ---")
            print(df_credito_region.head(10))
            
            # Determinar nombre de columna de región
            col_region = None
            for col in df_credito_region.columns:
                if 'región' in str(col).lower() or 'procedencia' in str(col).lower():
                    col_region = col
                    break
            
            if col_region:
                for idx, row in df_credito_region.iterrows():
                    region = row[col_region]
                    if region and region not in ['None', None]:
                        try:
                            cantidad_col = 'Cantidad de\ncréditos'
                            if cantidad_col in df_credito_region.columns:
                                cantidad = int(str(row[cantidad_col]).replace(',', '').replace(' ', ''))
                                
                                monto_col = 'Monto\ndesembolsado (S/)'
                                monto = 0
                                if monto_col in df_credito_region.columns:
                                    monto_str = str(row[monto_col]).replace(',', '').replace(' ', '')
                                    if monto_str.replace('.', '').isdigit():
                                        monto = float(monto_str)
                                
                                dataset_creditos_educativos.append({
                                    'NombreBeca': tipo_credito,
                                    'AnioBecariosConfirmados': 2021,
                                    'Departamento': region,
                                    'CantidadCreditos': cantidad,
                                    'MontoDesembolsado': monto
                                })
                        except Exception as e:
                            print(f"Error procesando crédito región: {e}")
    
    # CREAR DATASET CONSOLIDADO PRINCIPAL
    print("\n" + "="*80)
    print("CONSOLIDANDO DATOS")
    print("="*80)
    
    # Dataset de becarios por región
    if dataset_becarios_region:
        df_becarios_region = pd.DataFrame(dataset_becarios_region)
        df_becarios_region.to_excel('dataset_becarios_region_2021.xlsx', index=False)
        df_becarios_region.to_csv('dataset_becarios_region_2021.csv', index=False, encoding='utf-8-sig')
        print(f"\n✓ Dataset becarios por región: {len(df_becarios_region)} registros")
        print(df_becarios_region.head())
    
    # Dataset de tipo de gestión
    if dataset_tipo_gestion:
        df_tipo_gestion = pd.DataFrame(dataset_tipo_gestion)
        df_tipo_gestion.to_excel('dataset_tipo_gestion_2021.xlsx', index=False)
        df_tipo_gestion.to_csv('dataset_tipo_gestion_2021.csv', index=False, encoding='utf-8-sig')
        print(f"\n✓ Dataset tipo de gestión: {len(df_tipo_gestion)} registros")
        print(df_tipo_gestion)
    
    # Dataset de becarios por país
    if dataset_becarios_pais:
        df_becarios_pais = pd.DataFrame(dataset_becarios_pais)
        df_becarios_pais.to_excel('dataset_becarios_pais_2021.xlsx', index=False)
        df_becarios_pais.to_csv('dataset_becarios_pais_2021.csv', index=False, encoding='utf-8-sig')
        print(f"\n✓ Dataset becarios por país: {len(df_becarios_pais)} registros")
        print(df_becarios_pais.head(10))
    
    # Dataset de género
    if dataset_genero:
        df_genero = pd.DataFrame(dataset_genero)
        df_genero.to_excel('dataset_genero_2021.xlsx', index=False)
        df_genero.to_csv('dataset_genero_2021.csv', index=False, encoding='utf-8-sig')
        print(f"\n✓ Dataset género: {len(df_genero)} registros")
        print(df_genero)
    
    # Dataset de créditos educativos por región
    if dataset_creditos_educativos:
        df_creditos = pd.DataFrame(dataset_creditos_educativos)
        df_creditos.to_excel('dataset_creditos_educativos_2021.xlsx', index=False)
        df_creditos.to_csv('dataset_creditos_educativos_2021.csv', index=False, encoding='utf-8-sig')
        print(f"\n✓ Dataset créditos educativos: {len(df_creditos)} registros")
        print(df_creditos.head(10))
    
    # CREAR DATASET MAESTRO CONSOLIDADO
    # Combinar información de becas y créditos
    dataset_maestro = []
    
    # Agregar becarios por región
    for registro in dataset_becarios_region:
        dataset_maestro.append({
            'NombreBeca': registro['NombreBeca'],
            'Institucion': registro['Institucion'],
            'AnioBecariosConfirmados': registro['AnioBecariosConfirmados'],
            'Departamento': registro['Departamento'],
            'Carrera': registro['Carrera'],
            'Modalidad': registro['Modalidad'],
            'EstratoSocioeconomico': registro['EstratoSocioeconomico'],
            'Migracion': registro['Migracion'],
            'CantidadBecarios': registro['CantidadBecarios'],
            'TipoBeneficio': 'Beca',
            'MontoDesembolsado': None
        })
    
    # Agregar créditos educativos
    for registro in dataset_creditos_educativos:
        dataset_maestro.append({
            'NombreBeca': registro['NombreBeca'],
            'Institucion': 'Diversas',
            'AnioBecariosConfirmados': registro['AnioBecariosConfirmados'],
            'Departamento': registro['Departamento'],
            'Carrera': 'Diversas',
            'Modalidad': 'Crédito Educativo',
            'EstratoSocioeconomico': 'No especificado',
            'Migracion': 'No especificado',
            'CantidadBecarios': registro['CantidadCreditos'],
            'TipoBeneficio': 'Crédito',
            'MontoDesembolsado': registro['MontoDesembolsado']
        })
    
    if dataset_maestro:
        df_maestro = pd.DataFrame(dataset_maestro)
        df_maestro.to_excel('dataset_maestro_pronabec_2021.xlsx', index=False)
        df_maestro.to_csv('dataset_maestro_pronabec_2021.csv', index=False, encoding='utf-8-sig')
        print(f"\n✓ Dataset maestro consolidado: {len(df_maestro)} registros")
        print("\nPrimeros registros del dataset maestro:")
        print(df_maestro.head(10))
    
    # GENERAR RESUMEN ESTADÍSTICO
    print("\n" + "="*80)
    print("RESUMEN ESTADÍSTICO - PRONABEC 2021")
    print("="*80)
    
    if dataset_becarios_region:
        total_becarios = sum([x['CantidadBecarios'] for x in dataset_becarios_region])
        print(f"\n📊 Total de becarios Beca 18 (2021): {total_becarios:,}")
    
    if dataset_creditos_educativos:
        total_creditos = sum([x['CantidadCreditos'] for x in dataset_creditos_educativos])
        total_monto = sum([x['MontoDesembolsado'] for x in dataset_creditos_educativos])
        print(f"💳 Total de créditos educativos (2021): {total_creditos:,}")
        print(f"💰 Monto total desembolsado: S/ {total_monto:,.2f}")
    
    if dataset_becarios_pais:
        total_extranjero = sum([x['CantidadBecarios'] for x in dataset_becarios_pais])
        print(f"🌍 Total de becarios en el extranjero (2021): {total_extranjero}")
    
    if dataset_genero:
        print("\n👥 Distribución por género (créditos):")
        for registro in dataset_genero:
            print(f"   - {registro['Genero']}: {registro['CantidadCreditos']} créditos")
    
    print("\n" + "="*80)
    print("ARCHIVOS GENERADOS PARA DASHBOARD")
    print("="*80)
    print("\n📁 Datasets principales:")
    print("   1. dataset_maestro_pronabec_2021.xlsx/csv - Dataset consolidado completo")
    print("   2. dataset_becarios_region_2021.xlsx/csv - Becarios por región")
    print("   3. dataset_tipo_gestion_2021.xlsx/csv - Tipo de gestión institucional")
    print("   4. dataset_becarios_pais_2021.xlsx/csv - Becarios por país")
    print("   5. dataset_genero_2021.xlsx/csv - Distribución por género")
    print("   6. dataset_creditos_educativos_2021.xlsx/csv - Créditos por región")
    
    print("\n✅ PROCESAMIENTO COMPLETADO")
    print("Los datos están listos para importar en tu dashboard de visualización")

if __name__ == "__main__":
    procesar_datos_para_dashboard()
