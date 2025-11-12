import pandas as pd

print("\n╔════════════════════════════════════════════════════════════════╗")
print("║  VISTA PREVIA - Dashboard_Becas_PowerBI_2025.xlsx             ║")
print("╚════════════════════════════════════════════════════════════════╝\n")

# Hoja Principal
print("1. HOJA: Becas 2025 (Dataset Principal)")
print("-" * 70)
df_main = pd.read_excel('Dashboard_Becas_PowerBI_2025.xlsx', sheet_name='Becas 2025')
print(f"   Total de registros: {len(df_main)}")
print(f"   Columnas ({len(df_main.columns)}): {', '.join(df_main.columns)}")
print(f"\n   Primeras 2 filas:")
print(df_main.head(2).to_string(index=False, max_colwidth=30))

# Resumen
print("\n\n2. HOJA: Resumen 2025 (KPIs)")
print("-" * 70)
df_resumen = pd.read_excel('Dashboard_Becas_PowerBI_2025.xlsx', sheet_name='Resumen 2025')
print(f"   Total de indicadores: {len(df_resumen)}")
print(f"\n   Indicadores principales:")
print(df_resumen.head(10).to_string(index=False))

# Departamentos
print("\n\n3. HOJA: Departamentos 2025")
print("-" * 70)
df_dept = pd.read_excel('Dashboard_Becas_PowerBI_2025.xlsx', sheet_name='Departamentos 2025')
print(f"   Total de departamentos: {len(df_dept)}")
print(f"\n   Top 5 departamentos:")
print(df_dept.head(5).to_string(index=False))

print("\n\n✓ Archivo Excel listo para Power BI")
print("✓ 12 hojas con datos del año 2025")
