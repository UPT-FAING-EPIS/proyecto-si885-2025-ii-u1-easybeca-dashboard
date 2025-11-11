import pandas as pd
from pathlib import Path
import re

# Leer el archivo Excel con todas las hojas
excel_path = Path("datos_extraidos/pronabec_2022_datos.xlsx")
xls = pd.ExcelFile(excel_path)

print("=" * 70)
print("ANÁLISIS DE DATOS EXTRAÍDOS DE PRONABEC 2022")
print("=" * 70)
print()

# Diccionario para almacenar los datasets procesados
datasets_procesados = {}

# Analizar cada hoja
for sheet_name in xls.sheet_names:
    print(f"\n{'='*70}")
    print(f"HOJA: {sheet_name}")
    print(f"{'='*70}")
    
    df = pd.read_excel(excel_path, sheet_name=sheet_name)
    print(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
    print(f"\nColumnas: {list(df.columns)}")
    print(f"\nPrimeras 5 filas:")
    print(df.head())
    print(f"\nÚltimas 3 filas:")
    print(df.tail(3))
    
    datasets_procesados[sheet_name] = df

# DATASET 1: Becarios por Departamento (Página 30)
print("\n" + "="*70)
print("PROCESANDO: BECARIOS POR DEPARTAMENTO")
print("="*70)

df_departamentos = datasets_procesados.get('Pagina_30_Tabla_1')
if df_departamentos is not None:
    # Limpiar y procesar
    df_dept_limpio = df_departamentos.copy()
    
    # Renombrar columnas
    cols_nuevas = ['Departamento', 'Aptos_N', 'Aptos_Pct', 'Asistentes_N', 
                   'Asistentes_Pct', 'Inasistentes_N', 'Inasistentes_Pct', 'Pagina']
    df_dept_limpio.columns = cols_nuevas
    
    # Filtrar filas válidas (eliminar encabezados repetidos)
    df_dept_limpio = df_dept_limpio[df_dept_limpio['Departamento'] != 'Departamento']
    df_dept_limpio = df_dept_limpio[df_dept_limpio['Departamento'].notna()]
    df_dept_limpio = df_dept_limpio[df_dept_limpio['Departamento'] != '']
    
    # Agregar año
    df_dept_limpio['Anio'] = 2022
    
    print(df_dept_limpio)
    
    # Guardar
    df_dept_limpio.to_csv('datos_extraidos/becarios_por_departamento_2022.csv', 
                          index=False, encoding='utf-8-sig')
    print("\n✓ Guardado: becarios_por_departamento_2022.csv")

# DATASET 2: Becas por Tipo y Modalidad (Página 55)
print("\n" + "="*70)
print("PROCESANDO: BECAS POR TIPO Y MODALIDAD")
print("="*70)

df_becas = datasets_procesados.get('Pagina_55_Tabla_3')
if df_becas is not None:
    df_becas_limpio = df_becas.copy()
    
    # Limpiar columnas
    df_becas_limpio.columns = ['TipoBeca', 'NombreBeca', 'BecariosContinuadores', 
                               'CantidadBecasOtorgadas2022', 'TotalBecariosActivos', 'Pagina']
    
    # Filtrar filas válidas
    df_becas_limpio = df_becas_limpio[df_becas_limpio['TipoBeca'].notna()]
    df_becas_limpio = df_becas_limpio[df_becas_limpio['TipoBeca'] != '']
    
    # Agregar año
    df_becas_limpio['Anio'] = 2022
    
    print(df_becas_limpio)
    
    # Guardar
    df_becas_limpio.to_csv('datos_extraidos/becas_por_tipo_modalidad_2022.csv', 
                           index=False, encoding='utf-8-sig')
    print("\n✓ Guardado: becas_por_tipo_modalidad_2022.csv")

# DATASET 3: Metas y Otorgamiento de Becas (Página 18)
print("\n" + "="*70)
print("PROCESANDO: METAS Y OTORGAMIENTO DE BECAS")
print("="*70)

df_metas = datasets_procesados.get('Pagina_18_Tabla_5')
if df_metas is not None:
    df_metas_limpio = df_metas.copy()
    
    # Renombrar columnas
    df_metas_limpio.columns = ['TipoBeca', 'NombreBeca', 'Meta', 'BecasOtorgadas', 
                               'PorcentajeOtorgamiento', 'Pagina']
    
    # Filtrar filas válidas
    df_metas_limpio = df_metas_limpio[df_metas_limpio['NombreBeca'].notna()]
    df_metas_limpio = df_metas_limpio[df_metas_limpio['NombreBeca'] != '']
    
    # Agregar año
    df_metas_limpio['Anio'] = 2022
    
    print(df_metas_limpio)
    
    # Guardar
    df_metas_limpio.to_csv('datos_extraidos/metas_otorgamiento_becas_2022.csv', 
                           index=False, encoding='utf-8-sig')
    print("\n✓ Guardado: metas_otorgamiento_becas_2022.csv")

# DATASET 4: Becas Internacionales por País (Página 28)
print("\n" + "="*70)
print("PROCESANDO: BECAS INTERNACIONALES POR PAÍS")
print("="*70)

df_internacional = datasets_procesados.get('Pagina_28_Tabla_6')
if df_internacional is not None:
    df_internacional_limpio = df_internacional.copy()
    
    # Renombrar columnas
    df_internacional_limpio.columns = ['PaisEstudios', 'Maestria', 'Doctorado', 'Total', 'Pagina']
    
    # Filtrar filas válidas
    df_internacional_limpio = df_internacional_limpio[df_internacional_limpio['PaisEstudios'].notna()]
    df_internacional_limpio = df_internacional_limpio[df_internacional_limpio['PaisEstudios'] != '']
    
    # Agregar año y modalidad
    df_internacional_limpio['Anio'] = 2022
    df_internacional_limpio['Modalidad'] = 'Internacional'
    
    print(df_internacional_limpio)
    
    # Guardar
    df_internacional_limpio.to_csv('datos_extraidos/becas_internacionales_pais_2022.csv', 
                                   index=False, encoding='utf-8-sig')
    print("\n✓ Guardado: becas_internacionales_pais_2022.csv")

# DATASET 5: Créditos Educativos (Página 35)
print("\n" + "="*70)
print("PROCESANDO: CRÉDITOS EDUCATIVOS")
print("="*70)

df_creditos = datasets_procesados.get('Pagina_35_Tabla_7')
if df_creditos is not None:
    df_creditos_limpio = df_creditos.copy()
    
    # Renombrar columnas
    df_creditos_limpio.columns = ['ModalidadCredito', 'BeneficiariosDesembolsos', 
                                  'MontoDesembolsado', 'ParticipacionPct', 'Pagina']
    
    # Filtrar filas válidas
    df_creditos_limpio = df_creditos_limpio[df_creditos_limpio['ModalidadCredito'].notna()]
    df_creditos_limpio = df_creditos_limpio[df_creditos_limpio['ModalidadCredito'] != '']
    
    # Agregar año
    df_creditos_limpio['Anio'] = 2022
    
    print(df_creditos_limpio)
    
    # Guardar
    df_creditos_limpio.to_csv('datos_extraidos/creditos_educativos_2022.csv', 
                              index=False, encoding='utf-8-sig')
    print("\n✓ Guardado: creditos_educativos_2022.csv")

# Crear un reporte consolidado
print("\n" + "="*70)
print("CREANDO REPORTE CONSOLIDADO")
print("="*70)

reporte = []

# Resumen de becarios por departamento
if df_departamentos is not None:
    reporte.append({
        'Dataset': 'Becarios por Departamento',
        'Año': 2022,
        'Registros': len(df_dept_limpio),
        'Descripción': 'Distribución de becarios aptos, asistentes e inasistentes por departamento',
        'Archivo': 'becarios_por_departamento_2022.csv',
        'Utilidad_Dashboard': 'Mapa de calor, gráficos geográficos, distribución regional'
    })

# Resumen de becas por tipo
if df_becas is not None:
    reporte.append({
        'Dataset': 'Becas por Tipo y Modalidad',
        'Año': 2022,
        'Registros': len(df_becas_limpio),
        'Descripción': 'Tipos de becas, becarios continuadores y becas otorgadas en 2022',
        'Archivo': 'becas_por_tipo_modalidad_2022.csv',
        'Utilidad_Dashboard': 'Gráficos de barras, distribución por programa'
    })

# Resumen de metas
if df_metas is not None:
    reporte.append({
        'Dataset': 'Metas y Otorgamiento',
        'Año': 2022,
        'Registros': len(df_metas_limpio),
        'Descripción': 'Metas planteadas vs becas otorgadas por programa',
        'Archivo': 'metas_otorgamiento_becas_2022.csv',
        'Utilidad_Dashboard': 'KPIs, indicadores de cumplimiento, gráficos de progreso'
    })

# Resumen internacional
if df_internacional is not None:
    reporte.append({
        'Dataset': 'Becas Internacionales',
        'Año': 2022,
        'Registros': len(df_internacional_limpio),
        'Descripción': 'Becas de maestría y doctorado por país de destino',
        'Archivo': 'becas_internacionales_pais_2022.csv',
        'Utilidad_Dashboard': 'Migración internacional, distribución por país'
    })

# Resumen créditos
if df_creditos is not None:
    reporte.append({
        'Dataset': 'Créditos Educativos',
        'Año': 2022,
        'Registros': len(df_creditos_limpio),
        'Descripción': 'Modalidades de crédito educativo con beneficiarios y montos',
        'Archivo': 'creditos_educativos_2022.csv',
        'Utilidad_Dashboard': 'Análisis financiero, distribución de recursos'
    })

df_reporte = pd.DataFrame(reporte)
df_reporte.to_csv('datos_extraidos/REPORTE_CONSOLIDADO_2022.csv', 
                  index=False, encoding='utf-8-sig')

print(df_reporte.to_string(index=False))
print("\n✓ Guardado: REPORTE_CONSOLIDADO_2022.csv")

print("\n" + "="*70)
print("PROCESO COMPLETADO")
print("="*70)
print("\nArchivos generados en la carpeta 'datos_extraidos/':")
print("  1. becarios_por_departamento_2022.csv")
print("  2. becas_por_tipo_modalidad_2022.csv")
print("  3. metas_otorgamiento_becas_2022.csv")
print("  4. becas_internacionales_pais_2022.csv")
print("  5. creditos_educativos_2022.csv")
print("  6. REPORTE_CONSOLIDADO_2022.csv")
print("  7. pronabec_2022_datos.xlsx (todos los datasets)")
