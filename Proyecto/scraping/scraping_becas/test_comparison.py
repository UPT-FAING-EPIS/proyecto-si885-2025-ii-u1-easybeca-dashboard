import requests

# Probar la comparación
response = requests.get('http://localhost:8000/api/compare')
data = response.json()

print('=== RESULTADOS DE COMPARACIÓN ===')
print(f'Total scrapeados: {data.get("total_scraped")}')
print(f'Total Excel: {data.get("total_excel")}')
print(f'Coincidencias exactas: {len(data.get("exact_matches", []))}')
print(f'Nuevas entradas: {len(data.get("new_entries", []))}')

print('\n=== COINCIDENCIAS ENCONTRADAS ===')
for match in data.get('exact_matches', []):
    scraped_name = match['scraped']['nombre_beca']
    excel_name = match['excel']['Nombre Beca']
    print(f'  ✓ {scraped_name} <-> {excel_name}')

if not data.get('exact_matches', []):
    print('  No se encontraron coincidencias exactas')
    print('\n=== ANÁLISIS DETALLADO ===')
    print('Primeras 5 becas scrapeadas:')
    for i, item in enumerate(data.get('new_entries', [])[:5]):
        print(f'  {i+1}. "{item.get("nombre_beca", "N/A")}"')