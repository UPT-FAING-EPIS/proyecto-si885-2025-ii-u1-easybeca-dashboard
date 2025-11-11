"""
Script de análisis y resumen de datos de Becas Pronabec 2020
"""

import pandas as pd
import json

def main():
    print("\n" + "=" * 80)
    print(" " * 20 + "RESUMEN DE DATOS - PRONABEC 2020")
    print("=" * 80)
    
    # 1. Beca 18 por departamento
    print("\n📊 BECA 18 - DISTRIBUCIÓN POR DEPARTAMENTO")
    print("-" * 80)
    df1 = pd.read_csv('beca18_por_departamento_2020.csv')
    print(f"Total de departamentos: {len(df1)}")
    print(f"Total de becarios: {df1['TotalBecarios'].sum():,}")
    print(f"Becarios nuevos: {df1['BecariosNuevos'].sum():,}")
    print(f"Becarios continuadores: {df1['BecariosContinuadores'].sum():,}")
    
    print("\n🏆 Top 5 departamentos con más becarios:")
    top5_dept = df1.nlargest(5, 'TotalBecarios')[['Departamento', 'TotalBecarios', 'BecariosNuevos', 'BecariosContinuadores']]
    for idx, row in top5_dept.iterrows():
        print(f"   {row['Departamento']:15} - Total: {row['TotalBecarios']:5,} (Nuevos: {row['BecariosNuevos']:4,}, Continuadores: {row['BecariosContinuadores']:5,})")
    
    # 2. Beca 18 por carrera
    print("\n\n📚 BECA 18 - DISTRIBUCIÓN POR ÁREA DE ESTUDIO")
    print("-" * 80)
    df2 = pd.read_csv('beca18_por_carrera_2020.csv')
    print(f"Total de áreas de estudio: {len(df2)}")
    print(f"Total de becarios: {df2['TotalBecarios'].sum():,}")
    
    print("\n🏆 Áreas de estudio más demandadas:")
    for idx, row in df2.nlargest(5, 'TotalBecarios').iterrows():
        porcentaje = (row['TotalBecarios'] / df2['TotalBecarios'].sum()) * 100
        print(f"   {row['Carrera']:45} - {row['TotalBecarios']:5,} becarios ({porcentaje:.1f}%)")
    
    # 3. Beca 18 por tipo de institución
    print("\n\n🏛️  BECA 18 - DISTRIBUCIÓN POR TIPO DE INSTITUCIÓN")
    print("-" * 80)
    df3 = pd.read_csv('beca18_por_institucion_2020.csv')
    for idx, row in df3.iterrows():
        porcentaje = (row['TotalBecarios'] / df3['TotalBecarios'].sum()) * 100
        print(f"   {row['Institucion']:35} - {row['TotalBecarios']:5,} becarios ({porcentaje:.1f}%)")
    
    # 4. Becas de Posgrado
    print("\n\n🌍 BECAS DE POSGRADO - DISTRIBUCIÓN INTERNACIONAL")
    print("-" * 80)
    df4 = pd.read_csv('beca_posgrado_por_pais_2020.csv')
    print(f"Total de países: {len(df4)}")
    print(f"Total de becarios: {df4['TotalBecarios'].sum():,}")
    print(f"Becarios nuevos: {df4['BecariosNuevos'].sum():,}")
    print(f"Becarios continuadores: {df4['BecariosContinuadores'].sum():,}")
    
    print("\n🏆 Top 10 países destino:")
    top10_paises = df4.nlargest(10, 'TotalBecarios')[['PaisEstudio', 'TotalBecarios', 'BecariosNuevos', 'BecariosContinuadores']]
    for idx, row in top10_paises.iterrows():
        print(f"   {row['PaisEstudio']:20} - Total: {row['TotalBecarios']:3} (Nuevos: {row['BecariosNuevos']:2}, Continuadores: {row['BecariosContinuadores']:3})")
    
    # 5. Tipo de programa de posgrado
    print("\n\n🎓 BECAS DE POSGRADO - POR TIPO DE PROGRAMA")
    print("-" * 80)
    df5 = pd.read_csv('beca_posgrado_por_programa_2020.csv')
    for idx, row in df5.iterrows():
        porcentaje = (row['TotalBecarios'] / df5['TotalBecarios'].sum()) * 100
        print(f"   {row['TipoPrograma']:15} - {row['TotalBecarios']:3} becarios ({porcentaje:.1f}%)")
    
    # 6. Modalidades de becas
    print("\n\n🎯 OTRAS MODALIDADES DE BECAS")
    print("-" * 80)
    df6 = pd.read_csv('becarios_continuadores_por_modalidad_2020.csv')
    # Excluir el registro 'Total'
    df6_filtered = df6[df6['NombreBeca'] != 'Total']
    print(f"Modalidades especiales: {len(df6_filtered)}")
    print(f"Total de becarios continuadores: {df6_filtered['BecariosContinuadores'].sum():,}")
    
    print("\nModalidades:")
    for idx, row in df6_filtered.iterrows():
        print(f"   • {row['NombreBeca']:60} - {row['BecariosContinuadores']:4,} becarios")
    
    # 7. Créditos educativos
    print("\n\n💰 CRÉDITOS EDUCATIVOS")
    print("-" * 80)
    df7 = pd.read_csv('creditos_educativos_2020.csv')
    print(f"Modalidades de crédito: {len(df7)}")
    print(f"Total de créditos otorgados: {df7['CantidadCreditos'].sum():,}")
    print(f"Monto total desembolsado: S/ {df7['MontoDesembolsado'].sum():,.2f}")
    
    print("\nDetalle por modalidad:")
    for idx, row in df7.iterrows():
        porcentaje = (row['CantidadCreditos'] / df7['CantidadCreditos'].sum()) * 100
        print(f"   {row['TipoCredito']:40} - {row['CantidadCreditos']:3,} créditos ({porcentaje:.1f}%) - S/ {row['MontoDesembolsado']:,.2f}")
    
    # RESUMEN GENERAL
    print("\n\n" + "=" * 80)
    print(" " * 25 + "RESUMEN GENERAL 2020")
    print("=" * 80)
    
    total_beca18 = df1['TotalBecarios'].sum()
    total_posgrado = df4['TotalBecarios'].sum()
    total_otras = df6_filtered['BecariosContinuadores'].sum()
    total_creditos = df7['CantidadCreditos'].sum()
    
    print(f"\n📌 BECARIOS TOTALES:")
    print(f"   • Beca 18:                          {total_beca18:6,} becarios")
    print(f"   • Becas de Posgrado Internacional:  {total_posgrado:6,} becarios")
    print(f"   • Otras modalidades:                {total_otras:6,} becarios")
    print(f"   • TOTAL BECARIOS:                   {total_beca18 + total_posgrado + total_otras:6,} becarios")
    
    print(f"\n💳 CRÉDITOS EDUCATIVOS:")
    print(f"   • Total de créditos otorgados:      {total_creditos:6,} créditos")
    print(f"   • Monto total desembolsado:         S/ {df7['MontoDesembolsado'].sum():,.2f}")
    
    print("\n" + "=" * 80)
    print(" " * 15 + "Datos extraídos de: Memoria Anual Pronabec 2020")
    print("=" * 80)
    
    # Guardar resumen en archivo
    with open('resumen_estadistico_2020.txt', 'w', encoding='utf-8') as f:
        f.write("RESUMEN ESTADÍSTICO - PRONABEC 2020\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total Beca 18: {total_beca18:,}\n")
        f.write(f"Total Posgrado: {total_posgrado:,}\n")
        f.write(f"Total Otras Modalidades: {total_otras:,}\n")
        f.write(f"TOTAL BECARIOS: {total_beca18 + total_posgrado + total_otras:,}\n")
        f.write(f"\nTotal Créditos Educativos: {total_creditos:,}\n")
        f.write(f"Monto Desembolsado: S/ {df7['MontoDesembolsado'].sum():,.2f}\n")
    
    print("\n✅ Resumen guardado en: resumen_estadistico_2020.txt")

if __name__ == "__main__":
    main()
