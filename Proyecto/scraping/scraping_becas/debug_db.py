from database.hybrid_database_manager import HybridDatabaseManager
import json

# Conectar a la base de datos
db = HybridDatabaseManager()

# Obtener todos los datos
data = db.get_all_scraped_data()

print(f"Total de registros en la base de datos: {len(data)}")
print("\nPrimeros 5 registros:")
for i, item in enumerate(data[:5]):
    print(f"\n{i+1}. {json.dumps(item, indent=2, ensure_ascii=False)}")

# Buscar específicamente becas con 'BCP'
print("\n=== BÚSQUEDA DE BECAS CON 'BCP' ===")
bcp_becas = []
for item in data:
    nombre = item.get('nombre_beca', '').lower()
    if 'bcp' in nombre:
        bcp_becas.append(item)
        print(f"Encontrada: {item.get('nombre_beca', 'N/A')}")

if not bcp_becas:
    print("No se encontraron becas con 'BCP' en la base de datos")
    print("\nTodos los nombres de becas en la DB:")
    for item in data:
        print(f"  - {item.get('nombre_beca', 'N/A')}")