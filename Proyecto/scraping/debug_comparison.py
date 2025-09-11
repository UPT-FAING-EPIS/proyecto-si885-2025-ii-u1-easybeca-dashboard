import requests
import pandas as pd
import json

# Obtener datos scrapeados
response = requests.get('http://localhost:8000/api/compare')
data = response.json()

print("=== DATOS SCRAPEADOS ===")
print(f"Total scrapeados: {data.get('total_scraped', 0)}")
print("\nPrimeros 3 elementos scrapeados:")
for i, item in enumerate(data.get('new_entries', [])[:3]):
    print(f"{i+1}. Nombre: {item.get('nombre_beca', 'N/A')}")
    print(f"   Institución: {item.get('institucion', 'N/A')}")
    print(f"   Fuente: {item.get('fuente', 'N/A')}")
    print()

# Cargar datos del Excel
df = pd.read_excel('Becas_Peru.xlsx')
print("=== DATOS EXCEL ===")
print(f"Total en Excel: {len(df)}")
print("\nPrimeros 3 elementos del Excel:")
for i in range(min(3, len(df))):
    row = df.iloc[i]
    print(f"{i+1}. Nombre: {row.get('Nombre Beca', 'N/A')}")
    print(f"   Institución: {row.get('Institución o Programa', 'N/A')}")
    print()

# Buscar coincidencias específicas
print("=== BÚSQUEDA DE 'BCP' ===")
print("En datos scrapeados:")
for item in data.get('new_entries', []):
    nombre = item.get('nombre_beca', '').lower()
    if 'bcp' in nombre:
        print(f"  - {item.get('nombre_beca', 'N/A')}")

print("\nEn Excel:")
for i, row in df.iterrows():
    nombre = str(row.get('Nombre Beca', '')).lower()
    if 'bcp' in nombre:
        print(f"  - {row.get('Nombre Beca', 'N/A')}")