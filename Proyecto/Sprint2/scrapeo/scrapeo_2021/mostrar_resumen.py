import pandas as pd

def mostrar_resumen_datasets():
    """
    Muestra un resumen rápido de todos los datasets generados
    """
    print("\n" + "="*80)
    print("RESUMEN DE DATASETS GENERADOS - PRONABEC 2021")
    print("="*80 + "\n")
    
    # Dataset 1: Maestro
    print("📊 DATASET MAESTRO (Consolidado)")
    print("-" * 80)
    df_maestro = pd.read_csv('dataset_maestro_pronabec_2021.csv')
    print(f"Total de registros: {len(df_maestro)}")
    print(f"Columnas: {', '.join(df_maestro.columns)}")
    print("\nPrimeras 5 filas:")
    print(df_maestro.head())
    print("\nResumen por tipo de beneficio:")
    print(df_maestro.groupby('TipoBeneficio')['CantidadBecarios'].sum())
    
    # Dataset 2: Becarios por Región
    print("\n\n" + "="*80)
    print("🗺️ DATASET BECARIOS POR REGIÓN")
    print("-" * 80)
    df_region = pd.read_csv('dataset_becarios_region_2021.csv')
    print(f"Total de registros: {len(df_region)}")
    print(f"\nTop 5 departamentos con más becarios:")
    print(df_region.nlargest(5, 'CantidadBecarios')[['Departamento', 'CantidadBecarios', 'PorcentajeRegional']])
    print(f"\nTotal nacional: {df_region['CantidadBecarios'].sum():,} becarios")
    
    # Dataset 3: Tipo de Gestión
    print("\n\n" + "="*80)
    print("🏫 DATASET TIPO DE GESTIÓN INSTITUCIONAL")
    print("-" * 80)
    df_gestion = pd.read_csv('dataset_tipo_gestion_2021.csv')
    print(f"Total de registros: {len(df_gestion)}")
    print("\nDistribución:")
    for _, row in df_gestion.iterrows():
        porcentaje = (row['CantidadBecarios'] / df_gestion['CantidadBecarios'].sum()) * 100
        print(f"  {row['TipoGestion']:15} : {row['CantidadBecarios']:>5,} ({porcentaje:>5.1f}%)")
    
    # Dataset 4: Becarios por País
    print("\n\n" + "="*80)
    print("🌍 DATASET BECARIOS POR PAÍS (Extranjero)")
    print("-" * 80)
    df_pais = pd.read_csv('dataset_becarios_pais_2021.csv')
    print(f"Total de registros: {len(df_pais)}")
    print(f"\nTop 10 países de destino:")
    print(df_pais.nlargest(10, 'CantidadBecarios')[['Pais', 'CantidadBecarios']])
    print(f"\nTotal becarios en el extranjero: {df_pais['CantidadBecarios'].sum()}")
    
    # Dataset 5: Género
    print("\n\n" + "="*80)
    print("👥 DATASET DISTRIBUCIÓN POR GÉNERO (Créditos)")
    print("-" * 80)
    df_genero = pd.read_csv('dataset_genero_2021.csv')
    print(f"Total de registros: {len(df_genero)}")
    print("\nPor tipo de crédito:")
    print(df_genero.pivot_table(
        index='NombreBeca',
        columns='Genero',
        values='CantidadCreditos',
        aggfunc='sum'
    ))
    print("\nTotal general por género:")
    print(df_genero.groupby('Genero')['CantidadCreditos'].sum())
    
    # Dataset 6: Créditos Educativos por Región
    print("\n\n" + "="*80)
    print("💳 DATASET CRÉDITOS EDUCATIVOS POR REGIÓN")
    print("-" * 80)
    df_creditos = pd.read_csv('dataset_creditos_educativos_2021.csv')
    print(f"Total de registros: {len(df_creditos)}")
    print(f"\nTop 5 departamentos con más créditos:")
    top5_creditos = df_creditos.groupby('Departamento').agg({
        'CantidadCreditos': 'sum',
        'MontoDesembolsado': 'sum'
    }).nlargest(5, 'CantidadCreditos')
    print(top5_creditos)
    print(f"\nTotal créditos: {df_creditos['CantidadCreditos'].sum():,}")
    print(f"Monto total desembolsado: S/ {df_creditos['MontoDesembolsado'].sum():,.2f}")
    
    # Estadísticas finales
    print("\n\n" + "="*80)
    print("📈 RESUMEN ESTADÍSTICO GENERAL")
    print("="*80)
    
    total_becarios = df_region['CantidadBecarios'].sum()
    total_creditos = df_creditos['CantidadCreditos'].sum()
    total_monto = df_creditos['MontoDesembolsado'].sum()
    total_extranjero = df_pais['CantidadBecarios'].sum()
    total_mujeres_credito = df_genero[df_genero['Genero'] == 'Mujeres']['CantidadCreditos'].sum()
    total_hombres_credito = df_genero[df_genero['Genero'] == 'Hombres']['CantidadCreditos'].sum()
    
    print(f"""
    📚 Total Becarios Beca 18 (2021):          {total_becarios:>10,}
    💳 Total Créditos Educativos (2021):       {total_creditos:>10,}
    💰 Monto Total Desembolsado:               S/ {total_monto:>12,.2f}
    🌍 Becarios en el Extranjero:              {total_extranjero:>10}
    🏛️  Departamentos Cubiertos:               {len(df_region):>10}
    🌎 Países de Destino:                      {len(df_pais):>10}
    
    👥 Distribución Créditos por Género:
       • Mujeres:                              {total_mujeres_credito:>10,} ({(total_mujeres_credito/(total_mujeres_credito+total_hombres_credito))*100:.1f}%)
       • Hombres:                              {total_hombres_credito:>10,} ({(total_hombres_credito/(total_mujeres_credito+total_hombres_credito))*100:.1f}%)
    
    🏫 Tipo de Gestión (Beca 18):
       • Asociativa:                           {df_gestion[df_gestion['TipoGestion']=='Asociativa']['CantidadBecarios'].values[0]:>10,}
       • Societaria:                           {df_gestion[df_gestion['TipoGestion']=='Societaria']['CantidadBecarios'].values[0]:>10,}
       • Pública:                              {df_gestion[df_gestion['TipoGestion']=='Pública']['CantidadBecarios'].values[0]:>10,}
    """)
    
    print("\n" + "="*80)
    print("✅ ARCHIVOS DISPONIBLES PARA IMPORTAR EN DASHBOARD")
    print("="*80)
    print("""
    Formatos disponibles:
    • Excel (.xlsx) - Compatible con Power BI, Tableau, Excel
    • CSV (.csv)    - Compatible con cualquier herramienta
    • HTML (.html)  - Reporte interactivo para navegador
    • PNG (.png)    - Gráficos de visualización
    
    Datasets principales:
    1. dataset_maestro_pronabec_2021 - Consolidado completo
    2. dataset_becarios_region_2021 - Becarios por departamento
    3. dataset_tipo_gestion_2021 - Tipo de gestión institucional
    4. dataset_becarios_pais_2021 - Becarios en el extranjero
    5. dataset_genero_2021 - Distribución por género
    6. dataset_creditos_educativos_2021 - Créditos por región
    
    Reportes y visualizaciones:
    • reporte_pronabec_2021.html - Reporte interactivo
    • reporte_visual_pronabec_2021.png - Gráficos consolidados
    • README.md - Documentación completa
    """)
    
    print("="*80)
    print("🎯 LOS DATOS ESTÁN LISTOS PARA TU DASHBOARD")
    print("="*80 + "\n")

if __name__ == "__main__":
    mostrar_resumen_datasets()
