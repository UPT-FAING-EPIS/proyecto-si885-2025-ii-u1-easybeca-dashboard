"""
EJEMPLOS DE USO - Datos de Beca 18 - 2023

Este archivo contiene ejemplos prácticos de cómo usar los datos extraídos
en diferentes escenarios y con diferentes herramientas.
"""

import pandas as pd
import json

print("="*80)
print("EJEMPLOS DE USO - DATOS BECA 18 - 2023")
print("="*80)
print()

# =============================================================================
# EJEMPLO 1: Cargar y explorar un dataset CSV
# =============================================================================
print("EJEMPLO 1: Cargar y explorar datos de departamentos")
print("-"*80)

df_departamentos = pd.read_csv('beca18_2023_becarios_por_departamento.csv')

print("\n📊 Primeros 5 registros:")
print(df_departamentos.head())

print("\n📊 Información del dataset:")
print(df_departamentos.info())

print("\n📊 Estadísticas descriptivas:")
print(df_departamentos[['CantidadBecarios', 'Porcentaje']].describe())

# =============================================================================
# EJEMPLO 2: Análisis de datos
# =============================================================================
print("\n" + "="*80)
print("EJEMPLO 2: Análisis de datos")
print("-"*80)

# Top 5 departamentos
print("\n🏆 Top 5 departamentos con más becarios:")
top5 = df_departamentos.nlargest(5, 'CantidadBecarios')
for idx, row in top5.iterrows():
    print(f"  {idx+1}. {row['Departamento']}: {row['CantidadBecarios']} becarios ({row['Porcentaje']:.2f}%)")

# Departamentos con menos de 100 becarios
print("\n📉 Departamentos con menos de 100 becarios:")
menos100 = df_departamentos[df_departamentos['CantidadBecarios'] < 100]
print(f"  Total: {len(menos100)} departamentos")
for _, row in menos100.iterrows():
    print(f"  • {row['Departamento']}: {row['CantidadBecarios']} becarios")

# =============================================================================
# EJEMPLO 3: Combinar múltiples datasets
# =============================================================================
print("\n" + "="*80)
print("EJEMPLO 3: Trabajar con múltiples datasets")
print("-"*80)

# Cargar todos los datasets
df_resumen = pd.read_csv('beca18_2023_resumen_general.csv')
df_migracion = pd.read_csv('beca18_2023_migracion.csv')
df_modalidades = pd.read_csv('beca18_2023_modalidades.csv')

print("\n📋 Resumen General:")
for col in df_resumen.columns:
    print(f"  • {col}: {df_resumen[col].iloc[0]}")

print("\n🚶 Migración:")
for _, row in df_migracion.iterrows():
    print(f"  • {row['EstadoMigracion']}: {row['CantidadBecarios']:,} becarios ({row['Porcentaje']}%)")
    print(f"    Destino: {row['DestinoMayoritario']}")

print(f"\n📚 Total de modalidades: {len(df_modalidades)}")
for _, row in df_modalidades.iterrows():
    print(f"  • {row['Modalidad']}")

# =============================================================================
# EJEMPLO 4: Usar el archivo Excel
# =============================================================================
print("\n" + "="*80)
print("EJEMPLO 4: Cargar datos desde Excel")
print("-"*80)

# Cargar todas las hojas del Excel
excel_file = 'beca18_2023_datos_completos.xlsx'
datos_excel = pd.read_excel(excel_file, sheet_name=None)

print(f"\n📊 Archivo Excel: {excel_file}")
print(f"Total de hojas: {len(datos_excel)}")
print("\nHojas disponibles:")
for i, (nombre, df) in enumerate(datos_excel.items(), 1):
    print(f"  {i}. {nombre} ({len(df)} registros)")

# =============================================================================
# EJEMPLO 5: Leer datos JSON
# =============================================================================
print("\n" + "="*80)
print("EJEMPLO 5: Leer resumen JSON")
print("-"*80)

with open('beca18_2023_resumen.json', 'r', encoding='utf-8') as f:
    resumen_json = json.load(f)

print("\n📄 Contenido del JSON:")
print(json.dumps(resumen_json, indent=2, ensure_ascii=False))

# =============================================================================
# EJEMPLO 6: Filtrar y buscar datos
# =============================================================================
print("\n" + "="*80)
print("EJEMPLO 6: Filtrar y buscar datos")
print("-"*80)

# Buscar un departamento específico
departamento_buscar = 'Lima'
lima_data = df_departamentos[df_departamentos['Departamento'] == departamento_buscar]
if not lima_data.empty:
    print(f"\n🔍 Datos de {departamento_buscar}:")
    print(f"  • Becarios: {lima_data['CantidadBecarios'].iloc[0]}")
    print(f"  • Porcentaje: {lima_data['Porcentaje'].iloc[0]}%")
    print(f"  • Ranking: #{df_departamentos['CantidadBecarios'].rank(ascending=False)[lima_data.index[0]].astype(int)}")

# Departamentos de la costa norte
costa_norte = ['Tumbes', 'Piura', 'Lambayeque', 'La Libertad']
df_costa_norte = df_departamentos[df_departamentos['Departamento'].isin(costa_norte)]
print(f"\n🌊 Becarios de la Costa Norte:")
total_costa_norte = df_costa_norte['CantidadBecarios'].sum()
print(f"  Total: {total_costa_norte} becarios")
for _, row in df_costa_norte.iterrows():
    print(f"  • {row['Departamento']}: {row['CantidadBecarios']}")

# =============================================================================
# EJEMPLO 7: Calcular porcentajes y proporciones
# =============================================================================
print("\n" + "="*80)
print("EJEMPLO 7: Calcular porcentajes y proporciones")
print("-"*80)

total_becarios = df_resumen['TotalBecasOtorgadas'].iloc[0]

# Porcentaje de becarios de Lima sobre el total
lima_becarios = df_departamentos[df_departamentos['Departamento'] == 'Lima']['CantidadBecarios'].iloc[0]
print(f"\n📊 Lima representa:")
print(f"  • {lima_becarios:,} becarios de {total_becarios:,} totales")
print(f"  • {(lima_becarios/total_becarios)*100:.2f}% del total nacional")

# Porcentaje de migrantes que fueron a Lima
migrantes = df_migracion[df_migracion['EstadoMigracion'] == 'Migró']['CantidadBecarios'].iloc[0]
lima_destino_pct = 88.9  # Dato del PDF
lima_migrantes = int(migrantes * lima_destino_pct / 100)
print(f"\n🚶 Migración hacia Lima:")
print(f"  • {lima_migrantes:,} becarios migraron a Lima")
print(f"  • Representa el {lima_destino_pct}% de todos los migrantes")
print(f"  • Representa el {(lima_migrantes/total_becarios)*100:.2f}% del total nacional")

# =============================================================================
# EJEMPLO 8: Exportar datos procesados
# =============================================================================
print("\n" + "="*80)
print("EJEMPLO 8: Exportar datos procesados")
print("-"*80)

# Crear un nuevo dataset procesado
df_procesado = df_departamentos.copy()
df_procesado['Ranking'] = df_procesado['CantidadBecarios'].rank(ascending=False).astype(int)
df_procesado['Categoria'] = df_procesado['CantidadBecarios'].apply(
    lambda x: 'Alto' if x > 300 else 'Medio' if x > 150 else 'Bajo'
)

print("\n💾 Guardando nuevo dataset procesado...")
df_procesado.to_csv('departamentos_procesado.csv', index=False, encoding='utf-8-sig')
print("  ✓ Guardado: departamentos_procesado.csv")

print("\n📋 Vista previa del dataset procesado:")
print(df_procesado.head(10))

# =============================================================================
# EJEMPLO 9: Estadísticas avanzadas
# =============================================================================
print("\n" + "="*80)
print("EJEMPLO 9: Estadísticas avanzadas")
print("-"*80)

print("\n📊 Concentración de becarios:")
# Calcular qué porcentaje de becarios está en el top 5 de departamentos
top5_total = df_departamentos.nlargest(5, 'CantidadBecarios')['CantidadBecarios'].sum()
print(f"  • Top 5 departamentos: {top5_total:,} becarios ({(top5_total/total_becarios)*100:.2f}%)")

# Calcular qué porcentaje está en el top 10
top10_total = df_departamentos.nlargest(10, 'CantidadBecarios')['CantidadBecarios'].sum()
print(f"  • Top 10 departamentos: {top10_total:,} becarios ({(top10_total/total_becarios)*100:.2f}%)")

# Índice de concentración (Índice de Herfindahl-Hirschman simplificado)
hhi = ((df_departamentos['Porcentaje'] ** 2).sum())
print(f"  • Índice de concentración (HHI): {hhi:.2f}")
if hhi > 1000:
    print("    → Alta concentración de becarios en pocos departamentos")
else:
    print("    → Baja concentración, distribución más equitativa")

# =============================================================================
# EJEMPLO 10: Preparar datos para dashboard
# =============================================================================
print("\n" + "="*80)
print("EJEMPLO 10: Preparar datos para dashboard")
print("-"*80)

# Crear un dataset simplificado para un dashboard
dashboard_data = {
    'total_becarios': int(total_becarios),
    'total_departamentos': len(df_departamentos),
    'total_modalidades': len(df_modalidades),
    'top_departamento': df_departamentos.nlargest(1, 'CantidadBecarios')['Departamento'].iloc[0],
    'top_departamento_cantidad': int(df_departamentos.nlargest(1, 'CantidadBecarios')['CantidadBecarios'].iloc[0]),
    'porcentaje_migracion': float(df_migracion[df_migracion['EstadoMigracion'] == 'Migró']['Porcentaje'].iloc[0]),
    'promedio_por_departamento': int(df_departamentos['CantidadBecarios'].mean())
}

print("\n📊 KPIs para Dashboard:")
for key, value in dashboard_data.items():
    print(f"  • {key}: {value}")

# Guardar KPIs en JSON
with open('dashboard_kpis.json', 'w', encoding='utf-8') as f:
    json.dump(dashboard_data, f, ensure_ascii=False, indent=2)
print("\n💾 KPIs guardados en: dashboard_kpis.json")

# =============================================================================
# RESUMEN
# =============================================================================
print("\n" + "="*80)
print("RESUMEN DE EJEMPLOS")
print("="*80)
print("""
✅ Ejemplo 1: Cargar y explorar datasets CSV
✅ Ejemplo 2: Análisis básico de datos
✅ Ejemplo 3: Trabajar con múltiples datasets
✅ Ejemplo 4: Cargar datos desde Excel
✅ Ejemplo 5: Leer datos JSON
✅ Ejemplo 6: Filtrar y buscar datos
✅ Ejemplo 7: Calcular porcentajes y proporciones
✅ Ejemplo 8: Exportar datos procesados
✅ Ejemplo 9: Estadísticas avanzadas
✅ Ejemplo 10: Preparar datos para dashboard

Archivos generados:
  • departamentos_procesado.csv
  • dashboard_kpis.json
""")

print("\n🎉 ¡Todos los ejemplos ejecutados exitosamente!")
print("\nPuedes modificar este script para adaptarlo a tus necesidades específicas.")
print("="*80)
