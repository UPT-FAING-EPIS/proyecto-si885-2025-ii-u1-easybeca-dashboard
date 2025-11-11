"""
Script de ejemplo para visualizar los datos extraídos de Beca 18 - 2023
Genera gráficos básicos para entender la distribución de los datos
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def cargar_datos():
    """Carga todos los datasets"""
    print("Cargando datos...")
    datos = {
        'resumen': pd.read_csv('beca18_2023_resumen_general.csv'),
        'departamentos': pd.read_csv('beca18_2023_becarios_por_departamento.csv'),
        'modalidades': pd.read_csv('beca18_2023_modalidades.csv'),
        'migracion': pd.read_csv('beca18_2023_migracion.csv'),
        'carreras': pd.read_csv('beca18_2023_carreras_principales.csv'),
        'instituciones': pd.read_csv('beca18_2023_instituciones_principales.csv')
    }
    print("✓ Datos cargados exitosamente\n")
    return datos

def visualizar_resumen(datos):
    """Muestra el resumen general"""
    print("="*80)
    print("RESUMEN GENERAL - BECA 18 - 2023")
    print("="*80)
    resumen = datos['resumen'].iloc[0]
    print(f"Total de becas otorgadas: {resumen['TotalBecasOtorgadas']:,}")
    print(f"Meta establecida: {resumen['MetaBecas']:,}")
    print(f"Cobertura: {resumen['Cobertura%']}%")
    print(f"Becas para universidades: {resumen['BecasUniversidades']:,}")
    print(f"Becas para institutos/escuelas: {resumen['BecasInstitutosEscuelas']:,}")
    print()

def grafico_departamentos(df_departamentos):
    """Genera gráfico de becarios por departamento"""
    print("Generando gráfico: Becarios por Departamento...")
    
    # Top 10 departamentos
    top10 = df_departamentos.nlargest(10, 'CantidadBecarios')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(top10['Departamento'], top10['CantidadBecarios'], 
                   color='steelblue', alpha=0.8)
    
    # Añadir valores en las barras
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
                f'{int(width)} ({top10.iloc[i]["Porcentaje"]:.1f}%)',
                ha='left', va='center', fontsize=9)
    
    ax.set_xlabel('Cantidad de Becarios', fontsize=12, fontweight='bold')
    ax.set_title('Top 10 Departamentos con más Becarios - Beca 18 - 2023', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig('grafico_departamentos.png', dpi=300, bbox_inches='tight')
    print("  ✓ Guardado: grafico_departamentos.png\n")
    plt.close()

def grafico_migracion(df_migracion):
    """Genera gráfico de migración"""
    print("Generando gráfico: Migración de Becarios...")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Gráfico de pastel
    colors = ['#ff9999', '#66b3ff']
    explode = (0.05, 0)
    
    wedges, texts, autotexts = ax.pie(
        df_migracion['CantidadBecarios'],
        labels=df_migracion['EstadoMigracion'],
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        explode=explode,
        shadow=True
    )
    
    # Mejorar texto
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')
    
    ax.set_title('Migración de Becarios - Beca 18 - 2023', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Añadir leyenda con cantidades
    legend_labels = [f'{row["EstadoMigracion"]}: {row["CantidadBecarios"]:,} becarios' 
                    for _, row in df_migracion.iterrows()]
    ax.legend(legend_labels, loc='best', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('grafico_migracion.png', dpi=300, bbox_inches='tight')
    print("  ✓ Guardado: grafico_migracion.png\n")
    plt.close()

def grafico_carreras(df_carreras):
    """Genera gráfico de carreras principales"""
    print("Generando gráfico: Carreras Principales...")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.barh(df_carreras['Carrera'], df_carreras['Ranking'], 
                   color='forestgreen', alpha=0.7)
    
    ax.set_xlabel('Ranking (menor = más elegida)', fontsize=12, fontweight='bold')
    ax.set_title('Carreras Más Elegidas - Beca 18 - 2023', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.invert_yaxis()
    ax.invert_xaxis()  # Invertir para que 1 esté a la derecha
    
    plt.tight_layout()
    plt.savefig('grafico_carreras.png', dpi=300, bbox_inches='tight')
    print("  ✓ Guardado: grafico_carreras.png\n")
    plt.close()

def grafico_instituciones(df_instituciones):
    """Genera gráfico de instituciones principales"""
    print("Generando gráfico: Instituciones Principales...")
    
    # Acortar nombres largos
    df_inst = df_instituciones.copy()
    df_inst['InstitucionCorta'] = df_inst['Institucion'].apply(
        lambda x: x[:40] + '...' if len(x) > 40 else x
    )
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    bars = ax.barh(df_inst['InstitucionCorta'], df_inst['Ranking'], 
                   color='coral', alpha=0.7)
    
    ax.set_xlabel('Ranking (menor = más becarios)', fontsize=12, fontweight='bold')
    ax.set_title('Instituciones Educativas con Más Becarios - Beca 18 - 2023', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.invert_yaxis()
    ax.invert_xaxis()
    
    plt.tight_layout()
    plt.savefig('grafico_instituciones.png', dpi=300, bbox_inches='tight')
    print("  ✓ Guardado: grafico_instituciones.png\n")
    plt.close()

def mostrar_estadisticas(datos):
    """Muestra estadísticas descriptivas"""
    print("="*80)
    print("ESTADÍSTICAS DESCRIPTIVAS")
    print("="*80)
    
    df_dept = datos['departamentos']
    
    print(f"\nDistribución de Becarios por Departamento:")
    print(f"  • Total de departamentos: {len(df_dept)}")
    print(f"  • Promedio por departamento: {df_dept['CantidadBecarios'].mean():.0f} becarios")
    print(f"  • Mediana: {df_dept['CantidadBecarios'].median():.0f} becarios")
    print(f"  • Desviación estándar: {df_dept['CantidadBecarios'].std():.0f} becarios")
    print(f"  • Máximo: {df_dept['CantidadBecarios'].max()} becarios ({df_dept.loc[df_dept['CantidadBecarios'].idxmax(), 'Departamento']})")
    print(f"  • Mínimo: {df_dept['CantidadBecarios'].min()} becarios ({df_dept.loc[df_dept['CantidadBecarios'].idxmin(), 'Departamento']})")
    
    print(f"\nModalidades de Beca:")
    print(f"  • Total de modalidades: {len(datos['modalidades'])}")
    for _, row in datos['modalidades'].iterrows():
        print(f"    - {row['Modalidad']}")
    
    print(f"\nMigración:")
    for _, row in datos['migracion'].iterrows():
        print(f"  • {row['EstadoMigracion']}: {row['CantidadBecarios']:,} becarios ({row['Porcentaje']}%)")
        print(f"    Destino: {row['DestinoMayoritario']}")
    print()

def main():
    print("="*80)
    print("VISUALIZACIÓN DE DATOS - BECA 18 - 2023")
    print("="*80)
    print()
    
    # Cargar datos
    datos = cargar_datos()
    
    # Mostrar resumen
    visualizar_resumen(datos)
    
    # Mostrar estadísticas
    mostrar_estadisticas(datos)
    
    # Generar gráficos
    print("="*80)
    print("GENERANDO GRÁFICOS")
    print("="*80)
    print()
    
    grafico_departamentos(datos['departamentos'])
    grafico_migracion(datos['migracion'])
    grafico_carreras(datos['carreras'])
    grafico_instituciones(datos['instituciones'])
    
    print("="*80)
    print("PROCESO COMPLETADO")
    print("="*80)
    print("\nGráficos generados:")
    print("  • grafico_departamentos.png")
    print("  • grafico_migracion.png")
    print("  • grafico_carreras.png")
    print("  • grafico_instituciones.png")
    print("\n¡Visualizaciones listas para tu dashboard!")

if __name__ == "__main__":
    main()
