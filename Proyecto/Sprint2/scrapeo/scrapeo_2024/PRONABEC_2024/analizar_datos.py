"""
Análisis y Consolidación de Datos PRONABEC 2024
Genera datasets limpios y listos para dashboard
"""

import pandas as pd
import json
from pathlib import Path

def cargar_datos():
    """Carga todos los archivos generados"""
    print("📂 Cargando datos...")
    
    datos = {}
    archivos = {
        'completo': 'pronabec_becarios_2024_completo.csv',
        'departamentos': 'pronabec_2024_departamentos.csv',
        'becas': 'pronabec_2024_becas.csv',
        'instituciones': 'pronabec_2024_instituciones.csv'
    }
    
    for key, archivo in archivos.items():
        try:
            df = pd.read_csv(archivo, encoding='utf-8-sig')
            datos[key] = df
            print(f"  ✓ {archivo}: {len(df)} registros")
        except Exception as e:
            print(f"  ⚠ Error cargando {archivo}: {e}")
            datos[key] = pd.DataFrame()
    
    # Cargar JSON
    try:
        with open('pronabec_2024_info_adicional.json', 'r', encoding='utf-8') as f:
            datos['info_json'] = json.load(f)
        print(f"  ✓ pronabec_2024_info_adicional.json")
    except:
        datos['info_json'] = {}
    
    return datos

def limpiar_departamentos(df_completo, df_departamentos):
    """Limpia y consolida datos de departamentos"""
    print("\n🧹 Limpiando datos de departamentos...")
    
    # Extraer datos de departamentos del dataset completo
    df_dept = df_completo[df_completo['Departamento'].notna()].copy()
    
    # Normalizar nombres de departamentos
    df_dept['Departamento'] = df_dept['Departamento'].str.strip()
    df_dept['Departamento'] = df_dept['Departamento'].str.title()
    
    # Consolidar departamentos duplicados (ej: Ancash, Áncash)
    normalizaciones = {
        'Áncash': 'Ancash',
        'Apurimac': 'Apurímac',
        'Junin': 'Junín',
        'San Martin': 'San Martín',
        'Madre De Dios': 'Madre de Dios'
    }
    
    df_dept['Departamento'] = df_dept['Departamento'].replace(normalizaciones)
    
    # Agrupar por departamento
    df_consolidado = df_dept.groupby('Departamento').agg({
        'CantidadBecarios': 'sum',
        'AnioBecariosConfirmados': 'first'
    }).reset_index()
    
    df_consolidado = df_consolidado.sort_values('CantidadBecarios', ascending=False)
    
    print(f"  ✓ {len(df_consolidado)} departamentos consolidados")
    return df_consolidado

def analizar_becas(df_becas):
    """Analiza y estructura datos de becas"""
    print("\n📊 Analizando tipos de becas...")
    
    # Buscar columnas relevantes
    becas_info = []
    
    if 'Tipo de Beca' in df_becas.columns and 'Nombre de la beca' in df_becas.columns:
        df_clean = df_becas[['Tipo de Beca', 'Nombre de la beca', 'Meta', 'Becas otorgadas', 'Otorgamiento (%)']].copy()
        df_clean = df_clean.dropna(subset=['Tipo de Beca', 'Nombre de la beca'])
        
        for _, row in df_clean.iterrows():
            becas_info.append({
                'TipoBeca': row['Tipo de Beca'],
                'NombreBeca': row['Nombre de la beca'],
                'Meta': row.get('Meta', 'N/A'),
                'BecasOtorgadas': row.get('Becas otorgadas', 'N/A'),
                'PorcentajeOtorgamiento': row.get('Otorgamiento (%)', 'N/A'),
                'AnioBecariosConfirmados': 2024
            })
    
    if becas_info:
        df_becas_consolidado = pd.DataFrame(becas_info)
        print(f"  ✓ {len(df_becas_consolidado)} tipos de becas identificados")
        return df_becas_consolidado
    else:
        return pd.DataFrame()

def analizar_instituciones(df_inst):
    """Analiza datos de instituciones"""
    print("\n🏫 Analizando instituciones educativas...")
    
    if df_inst.empty:
        return pd.DataFrame()
    
    # Buscar columna de instituciones
    col_inst = None
    for col in df_inst.columns:
        if 'institución' in str(col).lower() or 'ies' in str(col).lower():
            col_inst = col
            break
    
    if col_inst:
        df_clean = df_inst[[col_inst]].copy()
        df_clean = df_clean[df_clean[col_inst].notna()]
        df_clean.columns = ['Institucion']
        df_clean['AnioBecariosConfirmados'] = 2024
        
        print(f"  ✓ {len(df_clean)} instituciones identificadas")
        return df_clean
    
    return pd.DataFrame()

def crear_dataset_dashboard(datos):
    """Crea dataset optimizado para dashboard"""
    print("\n📋 Creando dataset para dashboard...")
    
    # Dataset 1: Becas por Departamento
    df_departamentos = limpiar_departamentos(datos['completo'], datos['departamentos'])
    
    # Dataset 2: Tipos de Becas
    df_becas = analizar_becas(datos['becas'])
    
    # Dataset 3: Instituciones
    df_instituciones = analizar_instituciones(datos['instituciones'])
    
    # Dataset 4: Información extraída del texto
    info_adicional = []
    if datos['info_json']:
        # Becas por tipo
        if 'becas_por_tipo' in datos['info_json']:
            for item in datos['info_json']['becas_por_tipo']:
                info_adicional.append({
                    'Categoria': 'Tipo de Beca',
                    'Valor': item.get('NombreBeca', 'N/A'),
                    'Cantidad': item.get('Cantidad', 0),
                    'Pagina': item.get('Pagina', 0)
                })
        
        # Becas por departamento
        if 'becas_por_departamento' in datos['info_json']:
            for item in datos['info_json']['becas_por_departamento']:
                info_adicional.append({
                    'Categoria': 'Departamento',
                    'Valor': item.get('Departamento', 'N/A'),
                    'Cantidad': item.get('Cantidad', 0),
                    'Pagina': item.get('Pagina', 0)
                })
    
    if info_adicional:
        df_info = pd.DataFrame(info_adicional)
    else:
        df_info = pd.DataFrame()
    
    return {
        'departamentos': df_departamentos,
        'becas': df_becas,
        'instituciones': df_instituciones,
        'info_adicional': df_info
    }

def generar_estadisticas(datasets):
    """Genera estadísticas resumidas"""
    print("\n📈 Generando estadísticas...")
    
    estadisticas = {
        'año': 2024,
        'total_departamentos': len(datasets['departamentos']) if not datasets['departamentos'].empty else 0,
        'total_becarios': int(datasets['departamentos']['CantidadBecarios'].sum()) if not datasets['departamentos'].empty else 0,
        'tipos_becas': len(datasets['becas']) if not datasets['becas'].empty else 0,
        'instituciones': len(datasets['instituciones']) if not datasets['instituciones'].empty else 0
    }
    
    # Top 5 departamentos
    if not datasets['departamentos'].empty:
        top5 = datasets['departamentos'].head(5)
        estadisticas['top_5_departamentos'] = top5[['Departamento', 'CantidadBecarios']].to_dict('records')
    
    print(f"\n  📊 Resumen General:")
    print(f"     • Año: {estadisticas['año']}")
    print(f"     • Total de becarios: {estadisticas['total_becarios']:,}")
    print(f"     • Departamentos: {estadisticas['total_departamentos']}")
    print(f"     • Tipos de becas: {estadisticas['tipos_becas']}")
    print(f"     • Instituciones: {estadisticas['instituciones']}")
    
    if 'top_5_departamentos' in estadisticas:
        print(f"\n  🏆 Top 5 Departamentos:")
        for i, dept in enumerate(estadisticas['top_5_departamentos'], 1):
            print(f"     {i}. {dept['Departamento']}: {dept['CantidadBecarios']} becarios")
    
    return estadisticas

def guardar_datasets(datasets, estadisticas):
    """Guarda todos los datasets procesados"""
    print("\n💾 Guardando datasets procesados...")
    
    archivos_guardados = []
    
    # Guardar datasets individuales
    for nombre, df in datasets.items():
        if not df.empty:
            # CSV
            archivo_csv = f"dashboard_{nombre}_2024.csv"
            df.to_csv(archivo_csv, index=False, encoding='utf-8-sig')
            print(f"  ✓ {archivo_csv}")
            archivos_guardados.append(archivo_csv)
            
            # Excel
            archivo_excel = f"dashboard_{nombre}_2024.xlsx"
            df.to_excel(archivo_excel, index=False, engine='openpyxl')
            print(f"  ✓ {archivo_excel}")
            archivos_guardados.append(archivo_excel)
    
    # Guardar estadísticas
    with open('dashboard_estadisticas_2024.json', 'w', encoding='utf-8') as f:
        json.dump(estadisticas, f, indent=2, ensure_ascii=False)
    print(f"  ✓ dashboard_estadisticas_2024.json")
    archivos_guardados.append('dashboard_estadisticas_2024.json')
    
    # Crear archivo README con la documentación
    readme_content = f"""# Datos PRONABEC 2024 - Dashboard

## 📊 Resumen de Datos

- **Año**: {estadisticas['año']}
- **Total de Becarios**: {estadisticas['total_becarios']:,}
- **Departamentos**: {estadisticas['total_departamentos']}
- **Tipos de Becas**: {estadisticas['tipos_becas']}
- **Instituciones**: {estadisticas['instituciones']}

## 📁 Archivos Generados

### Datasets Principales

1. **dashboard_departamentos_2024.csv/xlsx**
   - Contiene: Distribución de becarios por departamento
   - Campos: Departamento, CantidadBecarios, AnioBecariosConfirmados

2. **dashboard_becas_2024.csv/xlsx**
   - Contiene: Tipos de becas y sus cifras
   - Campos: TipoBeca, NombreBeca, Meta, BecasOtorgadas, PorcentajeOtorgamiento

3. **dashboard_instituciones_2024.csv/xlsx**
   - Contiene: Instituciones educativas participantes
   - Campos: Institucion, AnioBecariosConfirmados

4. **dashboard_info_adicional_2024.csv/xlsx**
   - Contiene: Información adicional extraída del texto
   - Campos: Categoria, Valor, Cantidad, Pagina

5. **dashboard_estadisticas_2024.json**
   - Contiene: Estadísticas generales y top departamentos

## 🎯 Campos del Dataset

### NombreBeca
Nombre del programa de beca (Beca 18, Beca Permanencia, etc.)

### Institucion
Institución educativa donde el becario estudia o estudió

### AnioBecariosConfirmados
Año de becarios confirmados (2024)

### Departamento
Departamento donde está ubicada la institución educativa

### Carrera
Carrera financiada por la beca

### Modalidad
Categoría específica de la beca (Pregrado, Posgrado, Especiales)

### EstratoSocioeconomico
Clasificación socioeconómica (Pobre, Pobre Extrema, No Pobre)

### BecasSegunMigracion
Indica si el becario migró a otro departamento para estudiar

### CantidadBecarios
Número de becarios en la categoría

## 📈 Top 5 Departamentos con Más Becarios

"""
    
    if 'top_5_departamentos' in estadisticas:
        for i, dept in enumerate(estadisticas['top_5_departamentos'], 1):
            readme_content += f"{i}. **{dept['Departamento']}**: {dept['CantidadBecarios']} becarios\n"
    
    readme_content += f"""

## 🔍 Fuente de Datos

- **Documento**: Memoria Anual PRONABEC 2024
- **URL**: https://cdn.www.gob.pe/uploads/document/file/8154351/6826853-memoria-anual-2024%282%29.pdf
- **Fecha de extracción**: {pd.Timestamp.now().strftime('%Y-%m-%d')}

## 📝 Notas

- Los datos fueron extraídos automáticamente del PDF oficial
- Algunos campos pueden contener valores N/A si no estaban disponibles en el documento
- Los departamentos fueron normalizados para evitar duplicados
- Las cifras representan becarios del año 2024

## 🚀 Uso para Dashboard

Estos archivos están listos para ser importados en herramientas de visualización como:
- Power BI
- Tableau
- Python (Plotly, Matplotlib, Seaborn)
- R (ggplot2)
- Excel

"""
    
    with open('README_DASHBOARD.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print(f"  ✓ README_DASHBOARD.md")
    archivos_guardados.append('README_DASHBOARD.md')
    
    return archivos_guardados

def main():
    """Función principal"""
    print("="*70)
    print("  ANÁLISIS Y CONSOLIDACIÓN DE DATOS PRONABEC 2024")
    print("="*70 + "\n")
    
    try:
        # Cargar datos
        datos = cargar_datos()
        
        # Crear datasets para dashboard
        datasets = crear_dataset_dashboard(datos)
        
        # Generar estadísticas
        estadisticas = generar_estadisticas(datasets)
        
        # Guardar todo
        archivos = guardar_datasets(datasets, estadisticas)
        
        print("\n" + "="*70)
        print(f"  ✅ PROCESO COMPLETADO - {len(archivos)} archivos generados")
        print("="*70 + "\n")
        
        print("📁 Archivos listos para dashboard:")
        for archivo in archivos:
            print(f"   • {archivo}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
