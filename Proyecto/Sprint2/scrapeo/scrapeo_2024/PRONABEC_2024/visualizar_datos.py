"""
Visualización de Datos PRONABEC 2024
Genera gráficos para el dashboard
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from pathlib import Path

# Configurar estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def cargar_datos_dashboard():
    """Carga los datasets procesados"""
    print("📂 Cargando datos del dashboard...")
    
    datos = {}
    try:
        datos['departamentos'] = pd.read_csv('dashboard_departamentos_2024.csv', encoding='utf-8-sig')
        datos['becas'] = pd.read_csv('dashboard_becas_2024.csv', encoding='utf-8-sig')
        
        with open('dashboard_estadisticas_2024.json', 'r', encoding='utf-8') as f:
            datos['estadisticas'] = json.load(f)
        
        print("  ✅ Datos cargados exitosamente")
        return datos
    except Exception as e:
        print(f"  ❌ Error cargando datos: {e}")
        return None

def crear_grafico_departamentos(df_dept):
    """Crea gráfico de becarios por departamento"""
    print("\n📊 Generando gráfico de departamentos...")
    
    # Filtrar Total General si existe
    df_dept = df_dept[df_dept['Departamento'] != 'Total General'].copy()
    
    # Crear figura con subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Gráfico 1: Top 15 departamentos (barras horizontales)
    top15 = df_dept.head(15).sort_values('CantidadBecarios', ascending=True)
    colors = plt.cm.viridis(range(len(top15)))
    
    ax1.barh(top15['Departamento'], top15['CantidadBecarios'], color=colors)
    ax1.set_xlabel('Cantidad de Becarios', fontsize=12, fontweight='bold')
    ax1.set_title('Top 15 Departamentos con Más Becarios PRONABEC 2024', 
                  fontsize=14, fontweight='bold', pad=20)
    ax1.grid(axis='x', alpha=0.3)
    
    # Agregar valores en las barras
    for i, (idx, row) in enumerate(top15.iterrows()):
        ax1.text(row['CantidadBecarios'] + 1, i, f"{int(row['CantidadBecarios'])}", 
                va='center', fontweight='bold')
    
    # Gráfico 2: Distribución porcentual (pie chart)
    total_becarios = df_dept['CantidadBecarios'].sum()
    top10_pie = df_dept.head(10).copy()
    otros = df_dept.iloc[10:]['CantidadBecarios'].sum()
    
    if otros > 0:
        otros_row = pd.DataFrame([{'Departamento': 'Otros', 'CantidadBecarios': otros}])
        top10_pie = pd.concat([top10_pie, otros_row], ignore_index=True)
    
    colors_pie = plt.cm.Set3(range(len(top10_pie)))
    wedges, texts, autotexts = ax2.pie(top10_pie['CantidadBecarios'], 
                                         labels=top10_pie['Departamento'],
                                         autopct='%1.1f%%',
                                         startangle=90,
                                         colors=colors_pie)
    
    ax2.set_title('Distribución Porcentual de Becarios por Departamento\nPRONABEC 2024', 
                  fontsize=14, fontweight='bold', pad=20)
    
    # Mejorar texto
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(9)
    
    plt.tight_layout()
    plt.savefig('grafico_departamentos_2024.png', dpi=300, bbox_inches='tight')
    print("  ✅ Guardado: grafico_departamentos_2024.png")
    plt.close()

def crear_grafico_becas(df_becas):
    """Crea gráfico de tipos de becas"""
    print("\n📊 Generando gráfico de tipos de becas...")
    
    if df_becas.empty:
        print("  ⚠ No hay datos de becas para graficar")
        return
    
    # Limpiar datos numéricos
    df_becas['BecasOtorgadas_Clean'] = df_becas['BecasOtorgadas'].astype(str).str.replace(' ', '').str.replace(',', '').astype(float)
    df_becas['Meta_Clean'] = df_becas['Meta'].astype(str).str.replace(' ', '').str.replace(',', '').astype(float)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfico 1: Becas otorgadas por tipo
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    
    bars = ax1.bar(df_becas['TipoBeca'], df_becas['BecasOtorgadas_Clean'], 
                   color=colors, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Becas Otorgadas', fontsize=12, fontweight='bold')
    ax1.set_title('Becas Otorgadas por Tipo - PRONABEC 2024', 
                  fontsize=14, fontweight='bold', pad=20)
    ax1.grid(axis='y', alpha=0.3)
    
    # Agregar valores en las barras
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    # Rotar etiquetas del eje x
    ax1.set_xticklabels(df_becas['TipoBeca'], rotation=15, ha='right')
    
    # Gráfico 2: Comparación Meta vs Otorgadas
    x = range(len(df_becas))
    width = 0.35
    
    ax2.bar([i - width/2 for i in x], df_becas['Meta_Clean'], 
            width, label='Meta', color='#95E1D3', edgecolor='black')
    ax2.bar([i + width/2 for i in x], df_becas['BecasOtorgadas_Clean'], 
            width, label='Otorgadas', color='#F38181', edgecolor='black')
    
    ax2.set_ylabel('Cantidad de Becas', fontsize=12, fontweight='bold')
    ax2.set_title('Meta vs Becas Otorgadas - PRONABEC 2024', 
                  fontsize=14, fontweight='bold', pad=20)
    ax2.set_xticks(x)
    ax2.set_xticklabels(df_becas['TipoBeca'], rotation=15, ha='right')
    ax2.legend(fontsize=11)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('grafico_becas_2024.png', dpi=300, bbox_inches='tight')
    print("  ✅ Guardado: grafico_becas_2024.png")
    plt.close()

def crear_grafico_resumen(estadisticas):
    """Crea gráfico de resumen general"""
    print("\n📊 Generando gráfico de resumen...")
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Resumen General PRONABEC 2024', fontsize=18, fontweight='bold', y=0.995)
    
    # Gráfico 1: Indicadores principales
    ax1.axis('off')
    info_text = f"""
    📊 ESTADÍSTICAS GENERALES PRONABEC 2024
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    👥 Total de Becarios:        {estadisticas['total_becarios']:,}
    
    📍 Departamentos Atendidos:  {estadisticas['total_departamentos']}
    
    🎓 Tipos de Becas:           {estadisticas['tipos_becas']}
    
    🏫 Instituciones:            {estadisticas['instituciones']}
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """
    ax1.text(0.1, 0.5, info_text, fontsize=14, family='monospace',
             verticalalignment='center', bbox=dict(boxstyle='round', 
             facecolor='wheat', alpha=0.5))
    
    # Gráfico 2: Top 5 departamentos
    if 'top_5_departamentos' in estadisticas:
        top5 = estadisticas['top_5_departamentos']
        departamentos = [d['Departamento'] for d in top5]
        cantidades = [d['CantidadBecarios'] for d in top5]
        
        colors = plt.cm.plasma(range(len(departamentos)))
        bars = ax2.barh(departamentos, cantidades, color=colors, edgecolor='black')
        ax2.set_xlabel('Cantidad de Becarios', fontsize=11, fontweight='bold')
        ax2.set_title('Top 5 Departamentos con Más Becarios', 
                      fontsize=13, fontweight='bold', pad=15)
        ax2.grid(axis='x', alpha=0.3)
        
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax2.text(width + 1, bar.get_y() + bar.get_height()/2,
                    f'{int(width)}',
                    ha='left', va='center', fontweight='bold')
    
    # Gráfico 3: Distribución regional (agrupada)
    ax3.axis('off')
    regiones_info = """
    🗺️ COBERTURA NACIONAL
    
    El programa PRONABEC 2024 tiene presencia
    en los 26 departamentos del Perú.
    
    📈 Concentración:
    • Lima: Mayor concentración de becarios
    • Costa: Alto porcentaje de participación
    • Sierra y Selva: Cobertura equilibrada
    
    🎯 Objetivo:
    Garantizar acceso equitativo a educación
    superior de calidad en todo el país.
    """
    ax3.text(0.1, 0.5, regiones_info, fontsize=12,
             verticalalignment='center', bbox=dict(boxstyle='round',
             facecolor='lightblue', alpha=0.5))
    
    # Gráfico 4: Información del documento
    ax4.axis('off')
    fuente_info = """
    📄 FUENTE DE DATOS
    
    Documento:
    Memoria Anual PRONABEC 2024
    
    Entidad:
    Programa Nacional de Becas y Crédito
    Educativo (PRONABEC)
    
    Ministerio de Educación del Perú
    
    🔗 Datos extraídos mediante web scraping
    automático del documento oficial PDF.
    """
    ax4.text(0.1, 0.5, fuente_info, fontsize=11,
             verticalalignment='center', bbox=dict(boxstyle='round',
             facecolor='lightgreen', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('grafico_resumen_2024.png', dpi=300, bbox_inches='tight')
    print("  ✅ Guardado: grafico_resumen_2024.png")
    plt.close()

def main():
    """Función principal"""
    print("="*70)
    print("  GENERACIÓN DE VISUALIZACIONES - PRONABEC 2024")
    print("="*70)
    
    try:
        # Cargar datos
        datos = cargar_datos_dashboard()
        
        if datos:
            # Crear gráficos
            crear_grafico_departamentos(datos['departamentos'])
            crear_grafico_becas(datos['becas'])
            crear_grafico_resumen(datos['estadisticas'])
            
            print("\n" + "="*70)
            print("  ✅ VISUALIZACIONES GENERADAS EXITOSAMENTE")
            print("="*70)
            print("\n📊 Gráficos generados:")
            print("   • grafico_departamentos_2024.png")
            print("   • grafico_becas_2024.png")
            print("   • grafico_resumen_2024.png")
            print("\n💡 Usa estos gráficos en tu dashboard o presentaciones\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
