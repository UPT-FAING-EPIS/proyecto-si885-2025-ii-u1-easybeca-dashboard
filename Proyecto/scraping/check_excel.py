import pandas as pd
import sys

try:
    # Leer el archivo Excel
    df = pd.read_excel('Becas_Peru.xlsx')
    
    print(f'Columnas en Excel: {df.columns.tolist()}')
    print(f'Total filas: {len(df)}')
    print(f'Shape: {df.shape}')
    
    print('\nPrimeras 5 filas:')
    print(df.head())
    
    print('\nÚltimas 5 filas:')
    print(df.tail())
    
    # Verificar si hay datos nulos
    print('\nDatos nulos por columna:')
    print(df.isnull().sum())
    
except Exception as e:
    print(f'Error al leer Excel: {e}')
    sys.exit(1)