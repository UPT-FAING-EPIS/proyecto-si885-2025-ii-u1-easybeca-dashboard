import pandas as pd
import numpy as np
import os
from datetime import datetime

def analizar_excel_becas():
    """
    Analiza el archivo Excel de Becas Perú y prepara los datos para Power BI
    """
    try:
        # Leer el archivo Excel
        archivo_excel = 'Becas_Perú.xlsx'
        
        print(f"Analizando archivo: {archivo_excel}")
        print("=" * 50)
        
        # Leer todas las hojas del Excel
        excel_file = pd.ExcelFile(archivo_excel)
        print(f"Hojas encontradas: {excel_file.sheet_names}")
        print()
        
        # Diccionario para almacenar los DataFrames
        dataframes = {}
        
        # Analizar cada hoja
        for sheet_name in excel_file.sheet_names:
            print(f"Analizando hoja: {sheet_name}")
            print("-" * 30)
            
            # Leer la hoja
            df = pd.read_excel(archivo_excel, sheet_name=sheet_name)
            dataframes[sheet_name] = df
            
            # Información básica
            print(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
            print(f"Columnas: {list(df.columns)}")
            print()
            
            # Mostrar primeras filas
            print("Primeras 5 filas:")
            print(df.head())
            print()
            
            # Información de tipos de datos
            print("Tipos de datos:")
            print(df.dtypes)
            print()
            
            # Valores nulos
            print("Valores nulos por columna:")
            print(df.isnull().sum())
            print()
            
            # Estadísticas descriptivas para columnas numéricas
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                print("Estadísticas descriptivas (columnas numéricas):")
                print(df[numeric_cols].describe())
                print()
            
            # Valores únicos para columnas categóricas
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                unique_count = df[col].nunique()
                print(f"Columna '{col}': {unique_count} valores únicos")
                if unique_count <= 20:  # Mostrar valores únicos si son pocos
                    print(f"Valores: {df[col].unique().tolist()}")
                print()
            
            print("=" * 50)
            print()
        
        # Preparar archivos para Power BI
        preparar_para_powerbi(dataframes)
        
        return dataframes
        
    except Exception as e:
        print(f"Error al analizar el archivo: {str(e)}")
        return None

def preparar_para_powerbi(dataframes):
    """
    Prepara los datos para Power BI
    """
    print("PREPARANDO DATOS PARA POWER BI")
    print("=" * 50)
    
    # Crear carpeta para archivos de Power BI
    carpeta_powerbi = 'datos_powerbi'
    if not os.path.exists(carpeta_powerbi):
        os.makedirs(carpeta_powerbi)
    
    for sheet_name, df in dataframes.items():
        # Limpiar nombre de archivo
        nombre_archivo = sheet_name.replace(' ', '_').replace('/', '_')
        
        # Guardar como CSV (formato recomendado para Power BI)
        csv_path = os.path.join(carpeta_powerbi, f'{nombre_archivo}.csv')
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"✓ Guardado: {csv_path}")
        
        # Guardar como Excel limpio
        excel_path = os.path.join(carpeta_powerbi, f'{nombre_archivo}_limpio.xlsx')
        df.to_excel(excel_path, index=False)
        print(f"✓ Guardado: {excel_path}")
    
    # Crear archivo de metadatos
    crear_metadatos(dataframes, carpeta_powerbi)
    
    # Crear script de conexión para Power BI
    crear_script_powerbi(dataframes, carpeta_powerbi)
    
    print(f"\n✓ Todos los archivos preparados en la carpeta: {carpeta_powerbi}")

def crear_metadatos(dataframes, carpeta):
    """
    Crea un archivo de metadatos con información sobre las tablas
    """
    metadatos = []
    
    for sheet_name, df in dataframes.items():
        for col in df.columns:
            metadatos.append({
                'Tabla': sheet_name,
                'Columna': col,
                'Tipo_Datos': str(df[col].dtype),
                'Valores_Nulos': df[col].isnull().sum(),
                'Valores_Unicos': df[col].nunique(),
                'Porcentaje_Nulos': round((df[col].isnull().sum() / len(df)) * 100, 2)
            })
    
    df_metadatos = pd.DataFrame(metadatos)
    metadatos_path = os.path.join(carpeta, 'metadatos_tablas.xlsx')
    df_metadatos.to_excel(metadatos_path, index=False)
    print(f"✓ Metadatos guardados: {metadatos_path}")

def crear_script_powerbi(dataframes, carpeta):
    """
    Crea un script con instrucciones para Power BI
    """
    script_content = f"""
# INSTRUCCIONES PARA POWER BI - BECAS PERÚ
# Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## ARCHIVOS PREPARADOS:
"""
    
    for sheet_name in dataframes.keys():
        nombre_archivo = sheet_name.replace(' ', '_').replace('/', '_')
        script_content += f"""
### Tabla: {sheet_name}
- Archivo CSV: {nombre_archivo}.csv
- Archivo Excel: {nombre_archivo}_limpio.xlsx
- Filas: {dataframes[sheet_name].shape[0]}
- Columnas: {dataframes[sheet_name].shape[1]}
"""
    
    script_content += """

## PASOS PARA IMPORTAR EN POWER BI:

1. Abrir Power BI Desktop
2. Hacer clic en "Obtener datos" > "Texto/CSV" o "Excel"
3. Seleccionar los archivos CSV o Excel de la carpeta 'datos_powerbi'
4. Revisar y transformar los datos si es necesario
5. Cargar los datos al modelo

## RECOMENDACIONES:

- Usar archivos CSV para mejor rendimiento
- Revisar los tipos de datos en Power Query
- Crear relaciones entre tablas si es necesario
- Verificar la calidad de los datos usando el archivo de metadatos

## ARCHIVOS ADICIONALES:

- metadatos_tablas.xlsx: Información detallada sobre cada columna
- Este archivo: Instrucciones y documentación
"""
    
    script_path = os.path.join(carpeta, 'INSTRUCCIONES_POWERBI.txt')
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"✓ Instrucciones guardadas: {script_path}")

if __name__ == "__main__":
    # Ejecutar análisis
    dataframes = analizar_excel_becas()
    
    if dataframes:
        print("\n" + "=" * 50)
        print("ANÁLISIS COMPLETADO EXITOSAMENTE")
        print("=" * 50)
        print("\nArchivos preparados para Power BI en la carpeta 'datos_powerbi'")
        print("Revisa el archivo 'INSTRUCCIONES_POWERBI.txt' para más detalles")
    else:
        print("\nError en el análisis. Revisa el archivo Excel.")