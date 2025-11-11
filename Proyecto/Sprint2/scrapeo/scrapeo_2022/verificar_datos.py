"""
Script de verificación de integridad de datos extraídos
Verifica que todos los archivos estén presentes y contengan datos válidos
"""

import pandas as pd
from pathlib import Path
import sys

def verificar_archivos():
    """Verifica que todos los archivos esperados existan"""
    print("="*80)
    print("VERIFICACIÓN DE INTEGRIDAD DE DATOS - PRONABEC 2022")
    print("="*80)
    print()
    
    output_dir = Path("datos_extraidos")
    
    # Archivos esperados
    archivos_esperados = {
        'CSV Principales': [
            'becarios_por_departamento_2022.csv',
            'becas_por_tipo_modalidad_2022.csv',
            'metas_otorgamiento_becas_2022.csv',
            'becas_internacionales_pais_2022.csv',
            'creditos_educativos_2022.csv'
        ],
        'Archivos Consolidados': [
            'pronabec_2022_datos.xlsx',
            'REPORTE_CONSOLIDADO_2022.csv',
            'REPORTE_VISUAL_2022.html'
        ]
    }
    
    archivos_faltantes = []
    archivos_encontrados = []
    
    for categoria, archivos in archivos_esperados.items():
        print(f"\n📁 {categoria}:")
        print("-" * 80)
        
        for archivo in archivos:
            filepath = output_dir / archivo
            if filepath.exists():
                size = filepath.stat().st_size
                size_kb = size / 1024
                print(f"  ✓ {archivo:<50} ({size_kb:.1f} KB)")
                archivos_encontrados.append(archivo)
            else:
                print(f"  ✗ {archivo:<50} [FALTANTE]")
                archivos_faltantes.append(archivo)
    
    return archivos_faltantes, archivos_encontrados

def verificar_contenido():
    """Verifica el contenido de los archivos CSV principales"""
    print("\n" + "="*80)
    print("VERIFICACIÓN DE CONTENIDO DE DATOS")
    print("="*80)
    
    output_dir = Path("datos_extraidos")
    
    datasets = {
        'becarios_por_departamento_2022.csv': {
            'min_rows': 20,
            'expected_cols': ['Departamento', 'Aptos_N', 'Asistentes_N', 'Anio']
        },
        'becas_por_tipo_modalidad_2022.csv': {
            'min_rows': 15,
            'expected_cols': ['TipoBeca', 'NombreBeca', 'Anio']
        },
        'metas_otorgamiento_becas_2022.csv': {
            'min_rows': 10,
            'expected_cols': ['NombreBeca', 'Meta', 'BecasOtorgadas', 'Anio']
        },
        'becas_internacionales_pais_2022.csv': {
            'min_rows': 10,
            'expected_cols': ['PaisEstudios', 'Maestria', 'Doctorado', 'Anio']
        },
        'creditos_educativos_2022.csv': {
            'min_rows': 3,
            'expected_cols': ['ModalidadCredito', 'BeneficiariosDesembolsos', 'Anio']
        }
    }
    
    problemas = []
    
    for archivo, specs in datasets.items():
        print(f"\n📊 Verificando: {archivo}")
        print("-" * 80)
        
        filepath = output_dir / archivo
        
        if not filepath.exists():
            print(f"  ✗ Archivo no encontrado")
            problemas.append(f"{archivo}: Archivo no existe")
            continue
        
        try:
            df = pd.read_csv(filepath)
            
            # Verificar número de filas
            if len(df) >= specs['min_rows']:
                print(f"  ✓ Filas: {len(df)} (mínimo esperado: {specs['min_rows']})")
            else:
                print(f"  ✗ Filas: {len(df)} (esperado al menos {specs['min_rows']})")
                problemas.append(f"{archivo}: Muy pocas filas ({len(df)})")
            
            # Verificar columnas esperadas
            columnas_faltantes = [col for col in specs['expected_cols'] if col not in df.columns]
            if not columnas_faltantes:
                print(f"  ✓ Columnas esperadas presentes: {', '.join(specs['expected_cols'])}")
            else:
                print(f"  ✗ Columnas faltantes: {', '.join(columnas_faltantes)}")
                problemas.append(f"{archivo}: Columnas faltantes {columnas_faltantes}")
            
            # Verificar que el año sea 2022
            if 'Anio' in df.columns:
                anios = df['Anio'].unique()
                if all(anio == 2022 for anio in anios):
                    print(f"  ✓ Todos los registros son del año 2022")
                else:
                    print(f"  ⚠ Advertencia: Se encontraron años diferentes a 2022: {anios}")
            
            # Verificar valores nulos
            null_counts = df.isnull().sum()
            cols_con_nulos = null_counts[null_counts > 0]
            if len(cols_con_nulos) == 0:
                print(f"  ✓ Sin valores nulos")
            else:
                print(f"  ⚠ Columnas con valores nulos:")
                for col, count in cols_con_nulos.items():
                    print(f"    - {col}: {count} nulos")
            
            # Mostrar primeras filas
            print(f"\n  📝 Primeras 3 filas:")
            print("  " + "\n  ".join(df.head(3).to_string(index=False).split('\n')))
            
        except Exception as e:
            print(f"  ✗ Error al leer el archivo: {e}")
            problemas.append(f"{archivo}: Error de lectura - {str(e)}")
    
    return problemas

def generar_estadisticas():
    """Genera estadísticas generales de los datos"""
    print("\n" + "="*80)
    print("ESTADÍSTICAS GENERALES")
    print("="*80)
    
    output_dir = Path("datos_extraidos")
    
    stats = {}
    
    # Becarios por departamento
    try:
        df = pd.read_csv(output_dir / 'becarios_por_departamento_2022.csv')
        stats['departamentos'] = len(df) - 1  # Excluyendo total
        stats['total_aptos'] = df[df['Departamento'] == 'Total general']['Aptos_N'].values[0] if 'Total general' in df['Departamento'].values else df['Aptos_N'].sum()
    except:
        stats['departamentos'] = 'N/A'
        stats['total_aptos'] = 'N/A'
    
    # Tipos de becas
    try:
        df = pd.read_csv(output_dir / 'becas_por_tipo_modalidad_2022.csv')
        stats['tipos_becas'] = len(df)
        stats['becarios_activos'] = df['TotalBecariosActivos'].sum() if 'TotalBecariosActivos' in df.columns else 'N/A'
    except:
        stats['tipos_becas'] = 'N/A'
        stats['becarios_activos'] = 'N/A'
    
    # Becas internacionales
    try:
        df = pd.read_csv(output_dir / 'becas_internacionales_pais_2022.csv')
        stats['paises'] = len(df) - 1  # Excluyendo total
        stats['becarios_internacional'] = df['Total'].sum()
    except:
        stats['paises'] = 'N/A'
        stats['becarios_internacional'] = 'N/A'
    
    # Créditos educativos
    try:
        df = pd.read_csv(output_dir / 'creditos_educativos_2022.csv')
        # Filtrar la fila de total
        df_sin_total = df[df['ModalidadCredito'] != 'Total']
        stats['modalidades_credito'] = len(df_sin_total)
        stats['beneficiarios_credito'] = df_sin_total['BeneficiariosDesembolsos'].sum()
    except:
        stats['modalidades_credito'] = 'N/A'
        stats['beneficiarios_credito'] = 'N/A'
    
    print(f"""
╔═══════════════════════════════════════════════════════════════════════════╗
║  RESUMEN DE DATOS EXTRAÍDOS - PRONABEC 2022                              ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  📍 Cobertura Geográfica:                                                 ║
║     • Departamentos: {str(stats['departamentos']).rjust(45)} ║
║     • Total Becarios Aptos: {str(stats['total_aptos']).rjust(38)} ║
║                                                                           ║
║  🎓 Programas de Becas:                                                   ║
║     • Modalidades de Becas: {str(stats['tipos_becas']).rjust(38)} ║
║     • Becarios Activos: {str(stats['becarios_activos']).rjust(42)} ║
║                                                                           ║
║  🌍 Becas Internacionales:                                                ║
║     • Países Destino: {str(stats['paises']).rjust(44)} ║
║     • Becarios Internacional: {str(stats['becarios_internacional']).rjust(36)} ║
║                                                                           ║
║  💰 Créditos Educativos:                                                  ║
║     • Modalidades de Crédito: {str(stats['modalidades_credito']).rjust(38)} ║
║     • Beneficiarios: {str(stats['beneficiarios_credito']).rjust(45)} ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
    """)
    
    return stats

def main():
    """Función principal"""
    print()
    
    # Verificar archivos
    faltantes, encontrados = verificar_archivos()
    
    # Verificar contenido
    if encontrados:
        problemas = verificar_contenido()
    else:
        problemas = ["No se encontraron archivos para verificar"]
    
    # Generar estadísticas
    stats = generar_estadisticas()
    
    # Resumen final
    print("\n" + "="*80)
    print("RESUMEN DE VERIFICACIÓN")
    print("="*80)
    
    print(f"\n✓ Archivos encontrados: {len(encontrados)}")
    if faltantes:
        print(f"✗ Archivos faltantes: {len(faltantes)}")
        for archivo in faltantes:
            print(f"  - {archivo}")
    
    if problemas:
        print(f"\n⚠ Problemas detectados: {len(problemas)}")
        for problema in problemas:
            print(f"  - {problema}")
    else:
        print(f"\n✓ No se detectaron problemas")
    
    # Conclusión
    print("\n" + "="*80)
    if not faltantes and not problemas:
        print("✅ VERIFICACIÓN EXITOSA - Todos los datos están completos y válidos")
        print("="*80)
        print("\n📊 Los datos están listos para ser utilizados en el dashboard")
        print("📄 Revisa INSTRUCCIONES_USO.md para comenzar")
        return 0
    else:
        print("⚠️  VERIFICACIÓN COMPLETADA CON ADVERTENCIAS")
        print("="*80)
        print("\n🔧 Revisa los problemas detectados antes de usar los datos")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
