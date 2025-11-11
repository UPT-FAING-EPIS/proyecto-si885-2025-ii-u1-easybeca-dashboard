"""
Script para analizar y generar reportes adicionales de los datos del dashboard 2025
"""

import pandas as pd
import json
from datetime import datetime

def cargar_datos():
    """Carga el dataset consolidado"""
    print("Cargando datos consolidados...")
    df = pd.read_csv('dashboard_becas_2025_consolidado.csv')
    print(f"✓ {len(df)} registros cargados\n")
    return df

def generar_reporte_por_beca(df):
    """Genera un reporte detallado por cada beca"""
    print("="*80)
    print("REPORTE DETALLADO POR TIPO DE BECA")
    print("="*80)
    
    becas = df['NombreBeca'].unique()
    
    reportes = {}
    
    for beca in sorted(becas):
        df_beca = df[df['NombreBeca'] == beca]
        
        reporte = {
            'nombre': beca,
            'total_registros': len(df_beca),
            'instituciones_unicas': df_beca['Institucion'].nunique(),
            'departamentos': df_beca['Departamento'].nunique(),
            'modalidades': df_beca['Modalidad'].nunique() if 'Modalidad' in df_beca.columns else 0,
            'instituciones_top_5': df_beca['Institucion'].value_counts().head(5).to_dict(),
            'departamentos_top_5': df_beca['Departamento'].value_counts().head(5).to_dict(),
            'modalidades_distribucion': df_beca['Modalidad'].value_counts().to_dict() if 'Modalidad' in df_beca.columns else {},
            'estrato_distribucion': df_beca['Estrato_socioeconomico'].value_counts().to_dict() if 'Estrato_socioeconomico' in df_beca.columns else {},
            'migracion_distribucion': df_beca['Migracion'].value_counts().to_dict() if 'Migracion' in df_beca.columns else {}
        }
        
        reportes[beca] = reporte
        
        print(f"\n{beca}")
        print("-" * 80)
        print(f"Total de registros: {reporte['total_registros']}")
        print(f"Instituciones únicas: {reporte['instituciones_unicas']}")
        print(f"Departamentos: {reporte['departamentos']}")
        
        if reporte['instituciones_top_5']:
            print("\nTop 5 Instituciones:")
            for inst, count in list(reporte['instituciones_top_5'].items())[:5]:
                print(f"  • {inst}: {count}")
        
        if reporte['departamentos_top_5']:
            print("\nTop 5 Departamentos:")
            for dept, count in list(reporte['departamentos_top_5'].items())[:5]:
                print(f"  • {dept}: {count}")
    
    # Guardar reportes en JSON
    with open('reporte_detallado_por_beca.json', 'w', encoding='utf-8') as f:
        json.dump(reportes, f, indent=2, ensure_ascii=False)
    
    print("\n✓ Reporte detallado guardado en: reporte_detallado_por_beca.json")
    return reportes

def generar_reporte_por_departamento(df):
    """Genera un reporte por departamento"""
    print("\n" + "="*80)
    print("REPORTE POR DEPARTAMENTO")
    print("="*80)
    
    departamentos = df['Departamento'].value_counts().head(20)
    
    print(f"\nTop 20 Departamentos con más becas:")
    for i, (dept, count) in enumerate(departamentos.items(), 1):
        print(f"{i:2d}. {dept:30s} - {count:4d} becas")
    
    # Análisis por departamento
    reporte_dept = {}
    for dept in departamentos.index[:10]:  # Top 10
        df_dept = df[df['Departamento'] == dept]
        reporte_dept[dept] = {
            'total_becas': len(df_dept),
            'becas_tipos': df_dept['NombreBeca'].value_counts().to_dict(),
            'instituciones_unicas': df_dept['Institucion'].nunique(),
            'modalidades': df_dept['Modalidad'].value_counts().to_dict() if 'Modalidad' in df_dept.columns else {}
        }
    
    with open('reporte_por_departamento.json', 'w', encoding='utf-8') as f:
        json.dump(reporte_dept, f, indent=2, ensure_ascii=False)
    
    print("\n✓ Reporte por departamento guardado en: reporte_por_departamento.json")

def generar_reporte_migracion(df):
    """Analiza los patrones de migración"""
    print("\n" + "="*80)
    print("ANÁLISIS DE MIGRACIÓN")
    print("="*80)
    
    if 'Migracion' not in df.columns:
        print("No hay datos de migración disponibles")
        return
    
    migracion = df['Migracion'].value_counts()
    
    print("\nDistribución de migración:")
    for tipo, count in migracion.items():
        porcentaje = (count / len(df)) * 100
        print(f"  • {tipo}: {count} ({porcentaje:.1f}%)")
    
    # Análisis por beca
    print("\nMigración por tipo de beca:")
    for beca in df['NombreBeca'].unique()[:10]:  # Top 10 becas
        df_beca = df[df['NombreBeca'] == beca]
        if 'Migracion' in df_beca.columns:
            mig = df_beca['Migracion'].value_counts()
            print(f"\n  {beca}:")
            for tipo, count in mig.items():
                print(f"    - {tipo}: {count}")

def generar_reporte_estratos(df):
    """Analiza los estratos socioeconómicos"""
    print("\n" + "="*80)
    print("ANÁLISIS DE ESTRATOS SOCIOECONÓMICOS")
    print("="*80)
    
    if 'Estrato_socioeconomico' not in df.columns:
        print("No hay datos de estrato socioeconómico disponibles")
        return
    
    estratos = df['Estrato_socioeconomico'].value_counts()
    
    print("\nDistribución de estratos socioeconómicos:")
    total = len(df)
    for estrato, count in estratos.items():
        porcentaje = (count / total) * 100
        print(f"  • {estrato}: {count} ({porcentaje:.1f}%)")
    
    # Por beca
    print("\nEstrato socioeconómico por tipo de beca:")
    for beca in ['Beca 18', 'Beca Tec', 'Beca Perú']:
        df_beca = df[df['NombreBeca'] == beca]
        if not df_beca.empty and 'Estrato_socioeconomico' in df_beca.columns:
            print(f"\n  {beca}:")
            estratos_beca = df_beca['Estrato_socioeconomico'].value_counts()
            for estrato, count in estratos_beca.items():
                porcentaje = (count / len(df_beca)) * 100
                print(f"    - {estrato}: {count} ({porcentaje:.1f}%)")

def generar_reporte_modalidades(df):
    """Analiza las modalidades de becas"""
    print("\n" + "="*80)
    print("ANÁLISIS DE MODALIDADES")
    print("="*80)
    
    if 'Modalidad' not in df.columns:
        print("No hay datos de modalidad disponibles")
        return
    
    modalidades = df['Modalidad'].value_counts().head(15)
    
    print("\nTop 15 Modalidades más comunes:")
    for i, (mod, count) in enumerate(modalidades.items(), 1):
        porcentaje = (count / len(df)) * 100
        print(f"{i:2d}. {mod:40s} - {count:4d} ({porcentaje:5.1f}%)")

def generar_resumen_ejecutivo(df):
    """Genera un resumen ejecutivo en formato de texto"""
    print("\n" + "="*80)
    print("RESUMEN EJECUTIVO - BECAS 2025")
    print("="*80)
    
    resumen = f"""
RESUMEN EJECUTIVO DE BECAS - AÑO 2025
Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

1. DATOS GENERALES
   • Total de registros procesados: {len(df):,}
   • Programas de becas diferentes: {df['NombreBeca'].nunique()}
   • Instituciones educativas participantes: {df['Institucion'].nunique()}
   • Departamentos con cobertura: {df['Departamento'].nunique()}

2. PROGRAMAS DE BECAS MÁS IMPORTANTES
"""
    
    for beca, count in df['NombreBeca'].value_counts().head(5).items():
        porcentaje = (count / len(df)) * 100
        resumen += f"   • {beca}: {count:,} registros ({porcentaje:.1f}%)\n"
    
    resumen += "\n3. COBERTURA GEOGRÁFICA (Top 10 Departamentos)\n"
    for dept, count in df['Departamento'].value_counts().head(10).items():
        porcentaje = (count / len(df)) * 100
        resumen += f"   • {dept}: {count:,} becas ({porcentaje:.1f}%)\n"
    
    if 'Modalidad' in df.columns:
        resumen += "\n4. MODALIDADES PRINCIPALES\n"
        for mod, count in df['Modalidad'].value_counts().head(5).items():
            porcentaje = (count / len(df)) * 100
            resumen += f"   • {mod}: {count:,} ({porcentaje:.1f}%)\n"
    
    if 'Estrato_socioeconomico' in df.columns:
        resumen += "\n5. ENFOQUE SOCIOECONÓMICO\n"
        for estrato, count in df['Estrato_socioeconomico'].value_counts().head(5).items():
            porcentaje = (count / len(df)) * 100
            resumen += f"   • {estrato}: {count:,} ({porcentaje:.1f}%)\n"
    
    if 'Migracion' in df.columns:
        resumen += "\n6. ANÁLISIS DE MIGRACIÓN\n"
        for mig, count in df['Migracion'].value_counts().items():
            porcentaje = (count / len(df)) * 100
            resumen += f"   • {mig}: {count:,} ({porcentaje:.1f}%)\n"
    
    resumen += """
7. OBSERVACIONES
   • Los datos corresponden al año 2025
   • Incluyen becas nacionales e internacionales
   • Se han consolidado múltiples fuentes de información
   • Los datos están listos para su uso en dashboards y análisis

8. ARCHIVOS GENERADOS
   • dashboard_becas_2025_consolidado.csv (Dataset principal)
   • dashboard_becas_2025_consolidado.json (Formato JSON)
   • estadisticas_dashboard_2025.json (Estadísticas generales)
   • reporte_detallado_por_beca.json (Análisis por beca)
   • reporte_por_departamento.json (Análisis por departamento)
   • resumen_ejecutivo_2025.txt (Este documento)
"""
    
    print(resumen)
    
    # Guardar resumen
    with open('resumen_ejecutivo_2025.txt', 'w', encoding='utf-8') as f:
        f.write(resumen)
    
    print("\n✓ Resumen ejecutivo guardado en: resumen_ejecutivo_2025.txt")

def generar_csv_simplificado(df):
    """Genera una versión simplificada del CSV con solo los campos principales del dashboard"""
    print("\n" + "="*80)
    print("GENERANDO CSV SIMPLIFICADO PARA DASHBOARD")
    print("="*80)
    
    # Campos principales del dashboard
    campos_principales = [
        'NombreBeca',
        'Institucion',
        'AnioBecariosConfirmados',
        'Departamento',
        'Carrera',
        'Modalidad',
        'Estrato_socioeconomico',
        'Migracion'
    ]
    
    # Verificar qué campos existen
    campos_disponibles = [campo for campo in campos_principales if campo in df.columns]
    
    # Crear dataset simplificado
    df_simplificado = df[campos_disponibles].copy()
    
    # Renombrar columnas para mejor legibilidad
    df_simplificado.columns = df_simplificado.columns.str.replace('_', ' ').str.title()
    
    # Guardar
    archivo_salida = 'dashboard_becas_2025_simplificado.csv'
    df_simplificado.to_csv(archivo_salida, index=False, encoding='utf-8-sig')
    
    print(f"\n✓ CSV simplificado generado: {archivo_salida}")
    print(f"  Campos incluidos: {', '.join(df_simplificado.columns.tolist())}")
    print(f"  Total de registros: {len(df_simplificado):,}")
    
    return df_simplificado

def main():
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║  ANÁLISIS DETALLADO DE DATOS PARA DASHBOARD DE BECAS 2025   ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    # Cargar datos
    df = cargar_datos()
    
    # Generar reportes
    generar_reporte_por_beca(df)
    generar_reporte_por_departamento(df)
    generar_reporte_migracion(df)
    generar_reporte_estratos(df)
    generar_reporte_modalidades(df)
    generar_resumen_ejecutivo(df)
    generar_csv_simplificado(df)
    
    print("\n" + "="*80)
    print("✓ ANÁLISIS COMPLETADO EXITOSAMENTE")
    print("="*80)
    print("\nArchivos generados:")
    print("  1. reporte_detallado_por_beca.json")
    print("  2. reporte_por_departamento.json")
    print("  3. resumen_ejecutivo_2025.txt")
    print("  4. dashboard_becas_2025_simplificado.csv")
    print("\n¡Todos los datos están listos para usar en tu dashboard!")

if __name__ == "__main__":
    main()
