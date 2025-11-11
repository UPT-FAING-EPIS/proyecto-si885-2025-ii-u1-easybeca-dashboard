"""
Script para extraer datos del año 2025 de archivos CSV y JSON
para generar un dataset consolidado para el dashboard de becas.

Campos del dashboard:
- NombreBeca: Nombre del programa
- Institucion: Institución donde el becario estudiará o estudió
- AnioBecariosConfirmados: Año de becarios confirmados
- Departamento: Departamento donde está ubicada la institución educativa
- Carrera: Carrera financiada por la beca
- Modalidad: Categoría específica de la beca
- Estrato socioeconómico: Clasificación social (pobre, pobre extrema, no pobre)
- Becas según migración: Becarios que se trasladaron a otro departamento para estudiar
"""

import pandas as pd
import json
from datetime import datetime
import os

def extraer_datos_beca18_expandido():
    """Extrae datos de Beca 18 con información detallada de universidades"""
    print("Extrayendo datos de beca18_datos_expandido.csv...")
    
    try:
        df = pd.read_csv('beca18_datos_expandido.csv')
        
        # Filtrar por convocatoria 2025
        df_2025 = df[df['convocatoria'] == 2025].copy()
        
        # Crear dataset para dashboard
        datos_dashboard = []
        
        for _, row in df_2025.iterrows():
            # Extraer estrato socioeconómico de la descripción y modalidad
            estrato = "No especificado"
            if row['modalidad'] in ['Ordinaria', 'Huallaga', 'Vraem']:
                estrato = "Pobre o Pobre Extrema"
            elif row['modalidad'] in ['EIB', 'Protección', 'CNA y PA', 'FF.AA.']:
                estrato = "Variable"
            elif row['modalidad'] == 'Repared':
                estrato = "Víctimas de violencia"
            
            registro = {
                'NombreBeca': 'Beca 18',
                'Institucion': row['nombre_universidad'],
                'AnioBecariosConfirmados': 2025,
                'Departamento': row['ubicacion'] if pd.notna(row['ubicacion']) and row['ubicacion'] != '' else 'No especificado',
                'Carrera': 'Todas las carreras elegibles',  # Beca 18 no especifica carreras específicas
                'Modalidad': row['modalidad'],
                'Estrato_socioeconomico': estrato,
                'TipoUniversidad': row['tipo_universidad'],
                'Estado': row['estado'],
                'Quintil': row['quintil'],
                'NotaMinima': row['nota_minima'],
                'Fuente': row['fuente']
            }
            
            datos_dashboard.append(registro)
        
        df_result = pd.DataFrame(datos_dashboard)
        print(f"  ✓ Extraídos {len(df_result)} registros de Beca 18")
        return df_result
        
    except Exception as e:
        print(f"  ✗ Error al procesar beca18_datos_expandido.csv: {e}")
        return pd.DataFrame()


def extraer_datos_instituciones_beca18():
    """Extrae datos de instituciones de Beca 18"""
    print("Extrayendo datos de instituciones_beca_18.csv...")
    
    try:
        df = pd.read_csv('instituciones_beca_18.csv')
        
        datos_dashboard = []
        
        for _, row in df.iterrows():
            registro = {
                'NombreBeca': row['nombre_beca'],
                'Institucion': row['nombre_institucion'],
                'AnioBecariosConfirmados': 2025,
                'Departamento': row['ubicacion'] if row['ubicacion'] != 'No especificada' else 'Nacional',
                'Carrera': 'Según modalidad',
                'Modalidad': row['modalidad_programa'],
                'Estrato_socioeconomico': 'Variable según modalidad',
                'TipoInstitucion': row['tipo_institucion'],
                'Region': row['region'],
                'CodigoBeca': row['codigo_beca']
            }
            
            datos_dashboard.append(registro)
        
        df_result = pd.DataFrame(datos_dashboard)
        print(f"  ✓ Extraídos {len(df_result)} registros de instituciones Beca 18")
        return df_result
        
    except Exception as e:
        print(f"  ✗ Error al procesar instituciones_beca_18.csv: {e}")
        return pd.DataFrame()


def extraer_datos_beca_tec():
    """Extrae datos de Beca Tec"""
    print("Extrayendo datos de Beca Tec...")
    
    try:
        # Leer instituciones_beca_tec.csv
        df = pd.read_csv('instituciones_beca_tec.csv')
        
        datos_dashboard = []
        
        for _, row in df.iterrows():
            # Extraer región del campo ubicacion
            departamento = row['region'] if pd.notna(row['region']) else 'No especificado'
            
            registro = {
                'NombreBeca': 'Beca Tec',
                'Institucion': row['nombre_institucion'],
                'AnioBecariosConfirmados': 2025,
                'Departamento': departamento,
                'Carrera': row['programa'],
                'Modalidad': row['modalidad_programa'],
                'Estrato_socioeconomico': 'Estudiantes de institutos técnicos',
                'TipoInstitucion': row['tipo_institucion'],
                'Ubicacion': row['ubicacion'],
                'CodigoBeca': row['codigo_beca']
            }
            
            datos_dashboard.append(registro)
        
        df_result = pd.DataFrame(datos_dashboard)
        print(f"  ✓ Extraídos {len(df_result)} registros de Beca Tec")
        return df_result
        
    except Exception as e:
        print(f"  ✗ Error al procesar Beca Tec: {e}")
        return pd.DataFrame()


def extraer_datos_beca_peru():
    """Extrae datos de Beca Perú"""
    print("Extrayendo datos de Beca Perú...")
    
    try:
        df = pd.read_csv('instituciones_beca_peru.csv')
        
        datos_dashboard = []
        
        for _, row in df.iterrows():
            departamento = row['region'] if pd.notna(row['region']) and row['region'] != 'Nacional' else 'Lima'
            
            registro = {
                'NombreBeca': 'Beca Perú',
                'Institucion': row['nombre_institucion'],
                'AnioBecariosConfirmados': 2025,
                'Departamento': departamento,
                'Carrera': row['programa'],
                'Modalidad': row['modalidad_programa'],
                'Estrato_socioeconomico': 'Variable según universidad',
                'TipoInstitucion': row['tipo_institucion'],
                'Ubicacion': row['ubicacion'],
                'CodigoBeca': row['codigo_beca']
            }
            
            datos_dashboard.append(registro)
        
        df_result = pd.DataFrame(datos_dashboard)
        print(f"  ✓ Extraídos {len(df_result)} registros de Beca Perú")
        return df_result
        
    except Exception as e:
        print(f"  ✗ Error al procesar Beca Perú: {e}")
        return pd.DataFrame()


def extraer_datos_becas_internacionales():
    """Extrae datos de becas internacionales (Chevening, Fulbright)"""
    print("Extrayendo datos de becas internacionales...")
    
    datos_dashboard = []
    
    # Chevening
    try:
        df_chev = pd.read_csv('instituciones_chevening.csv')
        for _, row in df_chev.iterrows():
            registro = {
                'NombreBeca': 'Becas Chevening',
                'Institucion': row['nombre_institucion'],
                'AnioBecariosConfirmados': 2025,
                'Departamento': 'Reino Unido',
                'Carrera': row['programa'],
                'Modalidad': 'Internacional - Maestría',
                'Estrato_socioeconomico': 'Profesionales con liderazgo',
                'TipoInstitucion': row['tipo_institucion'],
                'Ubicacion': row['ubicacion'],
                'CodigoBeca': row['codigo_beca']
            }
            datos_dashboard.append(registro)
        print(f"  ✓ Extraídos {len(df_chev)} registros de Chevening")
    except Exception as e:
        print(f"  ✗ Error al procesar Chevening: {e}")
    
    # Fulbright
    try:
        df_fulb = pd.read_csv('instituciones_fulbright.csv')
        for _, row in df_fulb.iterrows():
            registro = {
                'NombreBeca': 'Becas Fulbright',
                'Institucion': row['nombre_institucion'],
                'AnioBecariosConfirmados': 2025,
                'Departamento': 'Estados Unidos',
                'Carrera': row['programa'],
                'Modalidad': 'Internacional - Posgrado',
                'Estrato_socioeconomico': 'Profesionales destacados',
                'TipoInstitucion': row['tipo_institucion'],
                'Ubicacion': row['ubicacion'],
                'CodigoBeca': row['codigo_beca']
            }
            datos_dashboard.append(registro)
        print(f"  ✓ Extraídos {len(df_fulb)} registros de Fulbright")
    except Exception as e:
        print(f"  ✗ Error al procesar Fulbright: {e}")
    
    return pd.DataFrame(datos_dashboard) if datos_dashboard else pd.DataFrame()


def extraer_datos_becas_integrales():
    """Extrae datos del archivo becas_integrales_completo.csv"""
    print("Extrayendo datos de becas integrales...")
    
    try:
        df = pd.read_csv('becas_integrales_completo.csv')
        
        # Filtrar solo becas activas para 2025
        df_activas = df[df['estado'] == 'Activa'].copy()
        
        datos_dashboard = []
        
        for _, row in df_activas.iterrows():
            # Determinar departamento según país destino
            if pd.notna(row['pais_destino']) and row['pais_destino'] == 'Perú':
                departamento = 'Nacional'
            elif pd.notna(row['pais_destino']):
                departamento = row['pais_destino']
            else:
                departamento = 'No especificado'
            
            # Determinar estrato socioeconómico
            estrato = 'No especificado'
            if 'beca_18' in row['codigo_beca']:
                estrato = 'Pobre o Pobre Extrema'
            elif 'vocacion_maestro' in row['codigo_beca']:
                estrato = 'Variable'
            
            registro = {
                'NombreBeca': row['nombre'],
                'Institucion': row['institucion'],
                'AnioBecariosConfirmados': 2025,
                'Departamento': departamento,
                'Carrera': row['tipo_estudio'] if pd.notna(row['tipo_estudio']) else 'Variable',
                'Modalidad': row['modalidad'] if pd.notna(row['modalidad']) else row['categoria'],
                'Estrato_socioeconomico': estrato,
                'Categoria': row['categoria'],
                'Cobertura': row['cobertura'],
                'CodigoBeca': row['codigo_beca'],
                'Estado': row['estado'],
                'URL_Oficial': row['url_oficial'] if pd.notna(row['url_oficial']) else ''
            }
            
            datos_dashboard.append(registro)
        
        df_result = pd.DataFrame(datos_dashboard)
        print(f"  ✓ Extraídos {len(df_result)} registros de becas integrales")
        return df_result
        
    except Exception as e:
        print(f"  ✗ Error al procesar becas_integrales_completo.csv: {e}")
        return pd.DataFrame()


def generar_campo_migracion(df):
    """
    Genera el campo de migración basado en el departamento de la institución
    vs el departamento de origen (asumiendo que la mayoría proviene de Lima y regiones)
    """
    print("Generando campo de migración...")
    
    if 'Departamento' in df.columns:
        def clasificar_migracion(row):
            dept = str(row['Departamento']).lower()
            
            # Si es nacional o no especificado, se considera sin migración específica
            if dept in ['nacional', 'no especificado', 'no especificada']:
                return 'Nacional - Sin especificar'
            
            # Si es internacional
            if dept not in ['lima', 'arequipa', 'cusco', 'puno', 'ayacucho', 'lambayeque', 
                           'tacna', 'huacho', 'tarapoto', 'huancayo', 'trujillo', 'pasco',
                           'huaraz', 'iquitos', 'chimbote', 'sullana', 'piura', 'cajamarca',
                           'ucayali', 'tumbes', 'huancavelica', 'junín', 'loreto', 'madre de dios']:
                return 'Internacional'
            
            # Para becas en provincias, asumimos migración desde Lima u otras regiones
            if dept != 'lima':
                return 'Posible migración'
            else:
                return 'Lima - Sin migración'
        
        df['Migracion'] = df.apply(clasificar_migracion, axis=1)
        print(f"  ✓ Campo de migración generado")
    
    return df


def consolidar_datos():
    """Consolida todos los datos extraídos en un único dataset"""
    print("\n" + "="*60)
    print("CONSOLIDACIÓN DE DATOS PARA DASHBOARD 2025")
    print("="*60 + "\n")
    
    datasets = []
    
    # Extraer de cada fuente
    df_beca18_expandido = extraer_datos_beca18_expandido()
    if not df_beca18_expandido.empty:
        datasets.append(df_beca18_expandido)
    
    df_beca18_inst = extraer_datos_instituciones_beca18()
    if not df_beca18_inst.empty:
        datasets.append(df_beca18_inst)
    
    df_beca_tec = extraer_datos_beca_tec()
    if not df_beca_tec.empty:
        datasets.append(df_beca_tec)
    
    df_beca_peru = extraer_datos_beca_peru()
    if not df_beca_peru.empty:
        datasets.append(df_beca_peru)
    
    df_internacionales = extraer_datos_becas_internacionales()
    if not df_internacionales.empty:
        datasets.append(df_internacionales)
    
    df_integrales = extraer_datos_becas_integrales()
    if not df_integrales.empty:
        datasets.append(df_integrales)
    
    # Consolidar todos los datasets
    if datasets:
        print("\nConsolidando datasets...")
        df_consolidado = pd.concat(datasets, ignore_index=True, sort=False)
        
        # Generar campo de migración
        df_consolidado = generar_campo_migracion(df_consolidado)
        
        # Ordenar por beca y departamento
        df_consolidado = df_consolidado.sort_values(['NombreBeca', 'Departamento'])
        
        # Guardar archivo consolidado
        archivo_salida = 'dashboard_becas_2025_consolidado.csv'
        df_consolidado.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
        print(f"\n✓ Datos consolidados guardados en: {archivo_salida}")
        
        # Generar también versión JSON
        archivo_json = 'dashboard_becas_2025_consolidado.json'
        df_consolidado.to_json(archivo_json, orient='records', indent=2, force_ascii=False)
        print(f"✓ Datos consolidados guardados en: {archivo_json}")
        
        # Generar reporte de estadísticas
        generar_reporte_estadisticas(df_consolidado)
        
        return df_consolidado
    else:
        print("\n✗ No se encontraron datos para consolidar")
        return None


def generar_reporte_estadisticas(df):
    """Genera un reporte con estadísticas del dataset consolidado"""
    print("\n" + "="*60)
    print("ESTADÍSTICAS DEL DATASET CONSOLIDADO")
    print("="*60)
    
    print(f"\nTotal de registros: {len(df)}")
    print(f"\nBecas únicas: {df['NombreBeca'].nunique()}")
    print("\nDistribución por beca:")
    print(df['NombreBeca'].value_counts())
    
    print(f"\nInstituciones únicas: {df['Institucion'].nunique()}")
    
    print(f"\nDepartamentos únicos: {df['Departamento'].nunique()}")
    print("\nDistribución por departamento:")
    print(df['Departamento'].value_counts().head(10))
    
    if 'Modalidad' in df.columns:
        print(f"\nModalidades únicas: {df['Modalidad'].nunique()}")
        print("\nDistribución por modalidad:")
        print(df['Modalidad'].value_counts().head(10))
    
    if 'Estrato_socioeconomico' in df.columns:
        print("\nDistribución por estrato socioeconómico:")
        print(df['Estrato_socioeconomico'].value_counts())
    
    if 'Migracion' in df.columns:
        print("\nDistribución por migración:")
        print(df['Migracion'].value_counts())
    
    # Guardar estadísticas en archivo
    stats_dict = {
        'fecha_generacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_registros': len(df),
        'becas_unicas': df['NombreBeca'].nunique(),
        'instituciones_unicas': df['Institucion'].nunique(),
        'departamentos_unicos': df['Departamento'].nunique(),
        'distribucion_becas': df['NombreBeca'].value_counts().to_dict(),
        'distribucion_departamentos': df['Departamento'].value_counts().to_dict(),
        'distribucion_modalidades': df['Modalidad'].value_counts().to_dict() if 'Modalidad' in df.columns else {},
        'distribucion_estrato': df['Estrato_socioeconomico'].value_counts().to_dict() if 'Estrato_socioeconomico' in df.columns else {},
        'distribucion_migracion': df['Migracion'].value_counts().to_dict() if 'Migracion' in df.columns else {}
    }
    
    with open('estadisticas_dashboard_2025.json', 'w', encoding='utf-8') as f:
        json.dump(stats_dict, f, indent=2, ensure_ascii=False)
    
    print("\n✓ Estadísticas guardadas en: estadisticas_dashboard_2025.json")


def main():
    """Función principal"""
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  EXTRACCIÓN DE DATOS PARA DASHBOARD DE BECAS 2025       ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    
    # Verificar archivos disponibles
    archivos_requeridos = [
        'beca18_datos_expandido.csv',
        'instituciones_beca_18.csv',
        'instituciones_beca_tec.csv',
        'instituciones_beca_peru.csv',
        'becas_integrales_completo.csv'
    ]
    
    print("Verificando archivos disponibles...")
    archivos_faltantes = []
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"  ✓ {archivo}")
        else:
            print(f"  ✗ {archivo} (no encontrado)")
            archivos_faltantes.append(archivo)
    
    if archivos_faltantes:
        print(f"\n⚠ Advertencia: {len(archivos_faltantes)} archivo(s) no encontrado(s)")
        print("Se procesarán los archivos disponibles.\n")
    else:
        print("\n✓ Todos los archivos requeridos están disponibles\n")
    
    # Consolidar datos
    df_consolidado = consolidar_datos()
    
    if df_consolidado is not None:
        print("\n" + "="*60)
        print("✓ PROCESO COMPLETADO EXITOSAMENTE")
        print("="*60)
        print(f"\nArchivos generados:")
        print("  • dashboard_becas_2025_consolidado.csv")
        print("  • dashboard_becas_2025_consolidado.json")
        print("  • estadisticas_dashboard_2025.json")
        print("\nLos datos están listos para ser usados en el dashboard.")
    else:
        print("\n" + "="*60)
        print("✗ ERROR: No se pudo consolidar los datos")
        print("="*60)


if __name__ == "__main__":
    main()
