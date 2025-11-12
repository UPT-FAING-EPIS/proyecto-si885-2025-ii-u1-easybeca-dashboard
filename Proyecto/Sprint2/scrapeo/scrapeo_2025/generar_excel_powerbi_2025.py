"""
Script para generar archivo Excel completo con múltiples hojas
para Power BI - Datos de Becas 2025
"""

import pandas as pd
import json
from datetime import datetime
import os

def crear_hoja_principal():
    """Crea la hoja principal con los campos del dataset solicitado"""
    print("Generando Hoja Principal: Becas 2025...")
    
    # Cargar datos consolidados
    df = pd.read_csv('dashboard_becas_2025_consolidado.csv')
    
    # Seleccionar y renombrar campos según especificación
    df_principal = pd.DataFrame({
        'NombreBeca': df['NombreBeca'],
        'Institucion': df['Institucion'],
        'AnioBecariosConfirmados': df['AnioBecariosConfirmados'],
        'Departamento': df['Departamento'],
        'Carrera': df['Carrera'],
        'Modalidad': df['Modalidad'],
        'Estrato_socioeconomico': df['Estrato_socioeconomico'],
        'Becas_segun_migracion': df['Migracion']
    })
    
    print(f"  ✓ {len(df_principal)} registros procesados")
    return df_principal


def crear_hoja_instituciones_2025():
    """Crea hoja con información detallada de instituciones"""
    print("\nGenerando Hoja: Instituciones 2025...")
    
    df = pd.read_csv('dashboard_becas_2025_consolidado.csv')
    
    # Agrupar por institución
    instituciones = df.groupby('Institucion').agg({
        'NombreBeca': lambda x: ', '.join(x.unique()),
        'Departamento': 'first',
        'AnioBecariosConfirmados': 'first'
    }).reset_index()
    
    instituciones.columns = ['Institucion', 'ProgramasBecas', 'Departamento', 'Anio']
    instituciones['TotalRegistros'] = df.groupby('Institucion').size().values
    
    # Agregar información adicional si existe
    if 'TipoInstitucion' in df.columns:
        tipo_inst = df.groupby('Institucion')['TipoInstitucion'].first().reset_index()
        instituciones = instituciones.merge(tipo_inst, on='Institucion', how='left')
    
    print(f"  ✓ {len(instituciones)} instituciones únicas")
    return instituciones


def crear_hoja_departamentos_2025():
    """Crea hoja con análisis por departamento"""
    print("\nGenerando Hoja: Departamentos 2025...")
    
    df = pd.read_csv('dashboard_becas_2025_consolidado.csv')
    
    departamentos = df.groupby('Departamento').agg({
        'NombreBeca': 'count',
        'Institucion': 'nunique',
        'Modalidad': 'nunique'
    }).reset_index()
    
    departamentos.columns = ['Departamento', 'TotalBecas', 'InstitucionesUnicas', 'ModalidadesUnicas']
    departamentos = departamentos.sort_values('TotalBecas', ascending=False)
    
    # Agregar porcentaje
    total = departamentos['TotalBecas'].sum()
    departamentos['Porcentaje'] = (departamentos['TotalBecas'] / total * 100).round(2)
    
    print(f"  ✓ {len(departamentos)} departamentos con cobertura")
    return departamentos


def crear_hoja_modalidades_2025():
    """Crea hoja con análisis por modalidad"""
    print("\nGenerando Hoja: Modalidades 2025...")
    
    df = pd.read_csv('dashboard_becas_2025_consolidado.csv')
    
    modalidades = df.groupby('Modalidad').agg({
        'NombreBeca': 'count',
        'Institucion': 'nunique',
        'Departamento': 'nunique'
    }).reset_index()
    
    modalidades.columns = ['Modalidad', 'TotalBecas', 'Instituciones', 'Departamentos']
    modalidades = modalidades.sort_values('TotalBecas', ascending=False)
    
    # Agregar porcentaje
    total = modalidades['TotalBecas'].sum()
    modalidades['Porcentaje'] = (modalidades['TotalBecas'] / total * 100).round(2)
    
    print(f"  ✓ {len(modalidades)} modalidades diferentes")
    return modalidades


def crear_hoja_estratos_2025():
    """Crea hoja con análisis por estrato socioeconómico"""
    print("\nGenerando Hoja: Estratos Socioeconómicos 2025...")
    
    df = pd.read_csv('dashboard_becas_2025_consolidado.csv')
    
    estratos = df.groupby('Estrato_socioeconomico').agg({
        'NombreBeca': 'count',
        'Institucion': 'nunique',
        'Departamento': 'nunique'
    }).reset_index()
    
    estratos.columns = ['Estrato_Socioeconomico', 'TotalBecas', 'Instituciones', 'Departamentos']
    estratos = estratos.sort_values('TotalBecas', ascending=False)
    
    # Agregar porcentaje
    total = estratos['TotalBecas'].sum()
    estratos['Porcentaje'] = (estratos['TotalBecas'] / total * 100).round(2)
    
    print(f"  ✓ {len(estratos)} estratos socioeconómicos identificados")
    return estratos


def crear_hoja_migracion_2025():
    """Crea hoja con análisis de migración"""
    print("\nGenerando Hoja: Análisis Migración 2025...")
    
    df = pd.read_csv('dashboard_becas_2025_consolidado.csv')
    
    migracion = df.groupby('Migracion').agg({
        'NombreBeca': 'count',
        'Institucion': 'nunique',
        'Departamento': 'nunique'
    }).reset_index()
    
    migracion.columns = ['Tipo_Migracion', 'TotalBecas', 'Instituciones', 'Departamentos']
    
    # Agregar porcentaje
    total = migracion['TotalBecas'].sum()
    migracion['Porcentaje'] = (migracion['TotalBecas'] / total * 100).round(2)
    
    # Clasificar migración
    migracion['Clasificacion'] = migracion['Tipo_Migracion'].apply(lambda x: 
        'No migró' if 'Sin migración' in x or 'Sin especificar' in x 
        else 'Migró' if 'Posible migración' in x or 'Internacional' in x 
        else 'No especificado'
    )
    
    print(f"  ✓ {len(migracion)} tipos de migración")
    return migracion


def crear_hoja_becas_detalle_2025():
    """Crea hoja con detalle de cada programa de becas"""
    print("\nGenerando Hoja: Detalle Programas Becas 2025...")
    
    df = pd.read_csv('dashboard_becas_2025_consolidado.csv')
    
    becas = df.groupby('NombreBeca').agg({
        'Institucion': 'nunique',
        'Departamento': 'nunique',
        'Carrera': 'nunique',
        'Modalidad': 'nunique',
        'AnioBecariosConfirmados': 'count'
    }).reset_index()
    
    becas.columns = ['NombreBeca', 'Instituciones', 'Departamentos', 'Carreras', 'Modalidades', 'TotalRegistros']
    becas = becas.sort_values('TotalRegistros', ascending=False)
    
    # Agregar porcentaje
    total = becas['TotalRegistros'].sum()
    becas['Porcentaje'] = (becas['TotalRegistros'] / total * 100).round(2)
    
    print(f"  ✓ {len(becas)} programas de becas")
    return becas


def crear_hoja_carreras_2025():
    """Crea hoja con análisis por carrera"""
    print("\nGenerando Hoja: Carreras 2025...")
    
    df = pd.read_csv('dashboard_becas_2025_consolidado.csv')
    
    # Filtrar carreras específicas (no genéricas)
    df_carreras = df[~df['Carrera'].str.contains('Todas las carreras|Según modalidad|Variable', case=False, na=False)]
    
    if len(df_carreras) > 0:
        carreras = df_carreras.groupby('Carrera').agg({
            'NombreBeca': lambda x: ', '.join(x.unique()),
            'Institucion': 'nunique',
            'AnioBecariosConfirmados': 'count'
        }).reset_index()
        
        carreras.columns = ['Carrera', 'ProgramasBecas', 'Instituciones', 'TotalBecas']
        carreras = carreras.sort_values('TotalBecas', ascending=False)
        
        print(f"  ✓ {len(carreras)} carreras específicas")
    else:
        carreras = pd.DataFrame(columns=['Carrera', 'ProgramasBecas', 'Instituciones', 'TotalBecas'])
        print("  ⚠ No hay carreras específicas, usando todas las carreras")
        
        carreras = df.groupby('Carrera').agg({
            'NombreBeca': lambda x: ', '.join(x.unique()),
            'Institucion': 'nunique',
            'AnioBecariosConfirmados': 'count'
        }).reset_index()
        
        carreras.columns = ['Carrera', 'ProgramasBecas', 'Instituciones', 'TotalBecas']
        carreras = carreras.sort_values('TotalBecas', ascending=False)
    
    return carreras


def crear_hoja_beca18_detalle_2025():
    """Crea hoja específica para Beca 18 con todas sus modalidades"""
    print("\nGenerando Hoja: Beca 18 Detalle 2025...")
    
    try:
        df = pd.read_csv('beca18_datos_expandido.csv')
        df_2025 = df[df['convocatoria'] == 2025].copy()
        
        # Análisis por modalidad
        beca18_modalidad = df_2025.groupby('modalidad').agg({
            'nombre_universidad': 'nunique',
            'ubicacion': lambda x: x.dropna().nunique(),
            'tipo_universidad': lambda x: ', '.join(x.unique())
        }).reset_index()
        
        beca18_modalidad.columns = ['Modalidad', 'UniversidadesUnicas', 'UbicacionesUnicas', 'TipoUniversidad']
        beca18_modalidad['TotalRegistros'] = df_2025.groupby('modalidad').size().values
        
        print(f"  ✓ {len(beca18_modalidad)} modalidades de Beca 18")
        return beca18_modalidad
    except Exception as e:
        print(f"  ⚠ Error al procesar Beca 18: {e}")
        return pd.DataFrame()


def crear_hoja_beca_tec_detalle_2025():
    """Crea hoja específica para Beca Tec"""
    print("\nGenerando Hoja: Beca Tec Detalle 2025...")
    
    try:
        df = pd.read_csv('instituciones_beca_tec.csv')
        
        beca_tec = df.groupby(['nombre_institucion', 'region']).agg({
            'programa': lambda x: ', '.join(x.unique()[:3]) + ('...' if len(x.unique()) > 3 else ''),
            'tipo_institucion': 'first',
            'modalidad_programa': 'first'
        }).reset_index()
        
        beca_tec.columns = ['Institucion', 'Region', 'ProgramasOfrecidos', 'TipoInstitucion', 'Modalidad']
        beca_tec['TotalProgramas'] = df.groupby(['nombre_institucion', 'region']).size().values
        
        print(f"  ✓ {len(beca_tec)} instituciones de Beca Tec")
        return beca_tec
    except Exception as e:
        print(f"  ⚠ Error al procesar Beca Tec: {e}")
        return pd.DataFrame()


def crear_hoja_resumen_ejecutivo_2025():
    """Crea hoja con resumen ejecutivo y KPIs"""
    print("\nGenerando Hoja: Resumen Ejecutivo 2025...")
    
    df = pd.read_csv('dashboard_becas_2025_consolidado.csv')
    
    # Crear resumen con KPIs
    resumen = pd.DataFrame({
        'Indicador': [
            'Total de Becas (Registros)',
            'Programas de Becas',
            'Instituciones Participantes',
            'Departamentos con Cobertura',
            'Modalidades Diferentes',
            'Carreras Ofrecidas',
            'Beca Más Popular',
            'Departamento con Más Becas',
            'Modalidad Más Común',
            'Estrato Socioeconómico Principal',
            'Porcentaje con Migración',
            'Porcentaje sin Migración',
            'Becas Internacionales',
            'Becas Nacionales',
            'Fecha de Generación'
        ],
        'Valor': [
            len(df),
            df['NombreBeca'].nunique(),
            df['Institucion'].nunique(),
            df['Departamento'].nunique(),
            df['Modalidad'].nunique(),
            df['Carrera'].nunique(),
            df['NombreBeca'].value_counts().index[0],
            df['Departamento'].value_counts().index[0],
            df['Modalidad'].value_counts().index[0],
            df['Estrato_socioeconomico'].value_counts().index[0],
            f"{(df['Migracion'].str.contains('Posible migración|Internacional').sum() / len(df) * 100):.1f}%",
            f"{(df['Migracion'].str.contains('Sin migración|Sin especificar').sum() / len(df) * 100):.1f}%",
            df['Migracion'].str.contains('Internacional').sum(),
            len(df) - df['Migracion'].str.contains('Internacional').sum(),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ]
    })
    
    print(f"  ✓ {len(resumen)} indicadores clave")
    return resumen


def crear_hoja_matriz_beca_departamento_2025():
    """Crea matriz cruzada de Becas vs Departamentos"""
    print("\nGenerando Hoja: Matriz Beca-Departamento 2025...")
    
    df = pd.read_csv('dashboard_becas_2025_consolidado.csv')
    
    # Crear tabla pivote
    matriz = pd.crosstab(df['NombreBeca'], df['Departamento'])
    
    # Ordenar por total
    matriz['Total'] = matriz.sum(axis=1)
    matriz = matriz.sort_values('Total', ascending=False)
    
    # Agregar fila de totales
    matriz.loc['Total'] = matriz.sum()
    
    print(f"  ✓ Matriz de {len(matriz)-1} becas × {len(matriz.columns)-1} departamentos")
    return matriz


def generar_excel_completo():
    """Genera el archivo Excel con todas las hojas"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║     GENERACIÓN DE EXCEL PARA POWER BI - BECAS 2025          ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    archivo_salida = 'Dashboard_Becas_PowerBI_2025.xlsx'
    
    # Crear archivo Excel con múltiples hojas
    with pd.ExcelWriter(archivo_salida, engine='openpyxl') as writer:
        
        # 1. Hoja Principal
        df_principal = crear_hoja_principal()
        df_principal.to_excel(writer, sheet_name='Becas 2025', index=False)
        
        # 2. Resumen Ejecutivo
        df_resumen = crear_hoja_resumen_ejecutivo_2025()
        df_resumen.to_excel(writer, sheet_name='Resumen 2025', index=False)
        
        # 3. Instituciones
        df_instituciones = crear_hoja_instituciones_2025()
        df_instituciones.to_excel(writer, sheet_name='Instituciones 2025', index=False)
        
        # 4. Departamentos
        df_departamentos = crear_hoja_departamentos_2025()
        df_departamentos.to_excel(writer, sheet_name='Departamentos 2025', index=False)
        
        # 5. Modalidades
        df_modalidades = crear_hoja_modalidades_2025()
        df_modalidades.to_excel(writer, sheet_name='Modalidades 2025', index=False)
        
        # 6. Estratos Socioeconómicos
        df_estratos = crear_hoja_estratos_2025()
        df_estratos.to_excel(writer, sheet_name='Estratos 2025', index=False)
        
        # 7. Migración
        df_migracion = crear_hoja_migracion_2025()
        df_migracion.to_excel(writer, sheet_name='Migracion 2025', index=False)
        
        # 8. Detalle de Becas
        df_becas = crear_hoja_becas_detalle_2025()
        df_becas.to_excel(writer, sheet_name='Programas Becas 2025', index=False)
        
        # 9. Carreras
        df_carreras = crear_hoja_carreras_2025()
        df_carreras.to_excel(writer, sheet_name='Carreras 2025', index=False)
        
        # 10. Beca 18 Detalle
        df_beca18 = crear_hoja_beca18_detalle_2025()
        if not df_beca18.empty:
            df_beca18.to_excel(writer, sheet_name='Beca18 Detalle 2025', index=False)
        
        # 11. Beca Tec Detalle
        df_beca_tec = crear_hoja_beca_tec_detalle_2025()
        if not df_beca_tec.empty:
            df_beca_tec.to_excel(writer, sheet_name='BecaTec Detalle 2025', index=False)
        
        # 12. Matriz Beca-Departamento
        df_matriz = crear_hoja_matriz_beca_departamento_2025()
        df_matriz.to_excel(writer, sheet_name='Matriz Beca-Depto 2025')
    
    print("\n" + "="*70)
    print("✓ ARCHIVO EXCEL GENERADO EXITOSAMENTE")
    print("="*70)
    print(f"\nArchivo: {archivo_salida}")
    print("\nHojas creadas:")
    print("  1. Becas 2025 - Dataset principal")
    print("  2. Resumen 2025 - KPIs y resumen ejecutivo")
    print("  3. Instituciones 2025 - Análisis de instituciones")
    print("  4. Departamentos 2025 - Análisis por departamento")
    print("  5. Modalidades 2025 - Análisis por modalidad")
    print("  6. Estratos 2025 - Análisis socioeconómico")
    print("  7. Migracion 2025 - Análisis de migración")
    print("  8. Programas Becas 2025 - Detalle por programa")
    print("  9. Carreras 2025 - Análisis por carrera")
    print(" 10. Beca18 Detalle 2025 - Detalle específico Beca 18")
    print(" 11. BecaTec Detalle 2025 - Detalle específico Beca Tec")
    print(" 12. Matriz Beca-Depto 2025 - Tabla cruzada")
    
    print("\n¡Listo para importar en Power BI!")
    
    return archivo_salida


def verificar_dependencias():
    """Verifica que existan los archivos necesarios"""
    archivos_requeridos = [
        'dashboard_becas_2025_consolidado.csv',
        'beca18_datos_expandido.csv',
        'instituciones_beca_tec.csv'
    ]
    
    faltantes = []
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            faltantes.append(archivo)
    
    if faltantes:
        print("⚠ Advertencia: Algunos archivos no se encontraron:")
        for f in faltantes:
            print(f"  - {f}")
        print("\nEl proceso continuará con los archivos disponibles.\n")
    
    return len(faltantes) == 0


def main():
    """Función principal"""
    print("\n")
    
    # Verificar dependencias
    verificar_dependencias()
    
    # Generar Excel
    archivo = generar_excel_completo()
    
    print("\n" + "="*70)
    print("PROCESO COMPLETADO")
    print("="*70)
    print(f"\nArchivo generado: {archivo}")
    print("Tamaño:", f"{os.path.getsize(archivo) / 1024:.2f} KB")
    
    return archivo


if __name__ == "__main__":
    main()
