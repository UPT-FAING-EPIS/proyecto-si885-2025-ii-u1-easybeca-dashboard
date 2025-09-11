import pandas as pd
import os
from utils.helpers import ExcelComparator
from database.hybrid_database_manager import HybridDatabaseManager

# Probar cargar Excel directamente
excel_path = "../Becas_Peru.xlsx"
print(f"Ruta del Excel: {excel_path}")
print(f"Ruta absoluta: {os.path.abspath(excel_path)}")
print(f"Archivo existe: {os.path.exists(excel_path)}")

try:
    # Intentar cargar con pandas
    df = pd.read_excel(excel_path)
    print(f"\nExcel cargado exitosamente")
    print(f"Filas: {len(df)}")
    print(f"Columnas: {list(df.columns)}")
    print(f"Primeras 3 filas:")
    for i in range(min(3, len(df))):
        row = df.iloc[i]
        print(f"  {i+1}. {row.get('Nombre Beca', 'N/A')}")
    
    # Convertir a dict
    excel_data = df.to_dict('records')
    print(f"\nConvertido a dict: {len(excel_data)} registros")
    
except Exception as e:
    print(f"Error cargando Excel: {e}")

# Probar obtener datos scrapeados
print("\n=== DATOS SCRAPEADOS ===")
try:
    db = HybridDatabaseManager()
    scraped_data = db.get_all_scraped_data()
    print(f"Total scrapeados: {len(scraped_data)}")
    print("Primeros 3:")
    for i, item in enumerate(scraped_data[:3]):
        print(f"  {i+1}. {item.get('nombre_beca', 'N/A')}")
except Exception as e:
    print(f"Error obteniendo datos scrapeados: {e}")

# Probar comparador
print("\n=== PRUEBA DE COMPARADOR ===")
try:
    comparator = ExcelComparator()
    result = comparator.compare_with_excel(scraped_data, excel_path)
    print(f"Resultado de comparación: {result}")
except Exception as e:
    print(f"Error en comparador: {e}")