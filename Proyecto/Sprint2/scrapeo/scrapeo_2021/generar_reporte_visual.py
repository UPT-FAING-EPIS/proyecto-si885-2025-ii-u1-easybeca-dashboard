import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def generar_reporte_visual():
    """
    Genera visualizaciones y un reporte HTML de los datos extraídos
    """
    print("="*80)
    print("GENERANDO REPORTE VISUAL - PRONABEC 2021")
    print("="*80)
    
    # Cargar datasets
    df_region = pd.read_excel('dataset_becarios_region_2021.xlsx')
    df_genero = pd.read_excel('dataset_genero_2021.xlsx')
    df_gestion = pd.read_excel('dataset_tipo_gestion_2021.xlsx')
    df_pais = pd.read_excel('dataset_becarios_pais_2021.xlsx')
    df_maestro = pd.read_excel('dataset_maestro_pronabec_2021.xlsx')
    
    # Crear figura con subplots
    fig = plt.figure(figsize=(16, 12))
    
    # 1. Top 10 Departamentos con más becarios
    ax1 = plt.subplot(2, 3, 1)
    top10_region = df_region.nlargest(10, 'CantidadBecarios')
    ax1.barh(top10_region['Departamento'], top10_region['CantidadBecarios'], color='steelblue')
    ax1.set_xlabel('Cantidad de Becarios')
    ax1.set_title('Top 10 Departamentos con Más Becarios (Beca 18 - 2021)', fontweight='bold')
    ax1.invert_yaxis()
    for i, v in enumerate(top10_region['CantidadBecarios']):
        ax1.text(v + 50, i, str(int(v)), va='center')
    
    # 2. Distribución por Tipo de Gestión
    ax2 = plt.subplot(2, 3, 2)
    colors = ['#ff9999', '#66b3ff', '#99ff99']
    wedges, texts, autotexts = ax2.pie(
        df_gestion['CantidadBecarios'],
        labels=df_gestion['TipoGestion'],
        autopct='%1.1f%%',
        colors=colors,
        startangle=90
    )
    ax2.set_title('Distribución por Tipo de Gestión Institucional (2021)', fontweight='bold')
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    # 3. Créditos por Género
    ax3 = plt.subplot(2, 3, 3)
    df_genero_sum = df_genero.groupby('Genero')['CantidadCreditos'].sum().reset_index()
    ax3.bar(df_genero_sum['Genero'], df_genero_sum['CantidadCreditos'], color=['#ff6b6b', '#4ecdc4'])
    ax3.set_ylabel('Cantidad de Créditos')
    ax3.set_title('Total de Créditos Educativos por Género (2021)', fontweight='bold')
    for i, v in enumerate(df_genero_sum['CantidadCreditos']):
        ax3.text(i, v + 50, str(int(v)), ha='center', fontweight='bold')
    
    # 4. Top 10 Países con Becarios en el Extranjero
    ax4 = plt.subplot(2, 3, 4)
    top10_pais = df_pais[df_pais['Pais'] != 'Total'].nlargest(10, 'CantidadBecarios')
    ax4.barh(top10_pais['Pais'], top10_pais['CantidadBecarios'], color='coral')
    ax4.set_xlabel('Cantidad de Becarios')
    ax4.set_title('Top 10 Países con Becarios Peruanos (2021)', fontweight='bold')
    ax4.invert_yaxis()
    for i, v in enumerate(top10_pais['CantidadBecarios']):
        ax4.text(v + 0.5, i, str(int(v)), va='center')
    
    # 5. Distribución Becas vs Créditos
    ax5 = plt.subplot(2, 3, 5)
    tipo_beneficio = df_maestro.groupby('TipoBeneficio')['CantidadBecarios'].sum().reset_index()
    colors_beneficio = ['#95e1d3', '#f38181']
    wedges, texts, autotexts = ax5.pie(
        tipo_beneficio['CantidadBecarios'],
        labels=tipo_beneficio['TipoBeneficio'],
        autopct='%1.1f%%',
        colors=colors_beneficio,
        startangle=45
    )
    ax5.set_title('Becas vs Créditos Educativos (2021)', fontweight='bold')
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    # 6. Estadísticas Clave (Texto)
    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')
    
    total_becarios = df_region['CantidadBecarios'].sum()
    total_creditos = df_maestro[df_maestro['TipoBeneficio'] == 'Crédito']['CantidadBecarios'].sum()
    total_extranjero = df_pais[df_pais['Pais'] != 'Total']['CantidadBecarios'].sum()
    
    stats_text = f"""
    📊 ESTADÍSTICAS CLAVE PRONABEC 2021
    
    ═══════════════════════════════════════
    
    📚 Total Becarios (Beca 18)
       {total_becarios:,}
    
    💳 Total Créditos Educativos
       {int(total_creditos):,}
    
    🌍 Becarios en el Extranjero
       {total_extranjero}
    
    🏛️ Departamentos Cubiertos
       26 (Todo el Perú)
    
    🌎 Países de Destino
       {len(df_pais)-1} países
    
    ═══════════════════════════════════════
    
    Fuente: Memoria Anual PRONABEC 2021
    """
    
    ax6.text(0.1, 0.5, stats_text, fontsize=11, verticalalignment='center',
             fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('reporte_visual_pronabec_2021.png', dpi=300, bbox_inches='tight')
    print("\n✅ Gráfico guardado: reporte_visual_pronabec_2021.png")
    
    # Generar reporte HTML
    generar_reporte_html(df_region, df_genero, df_gestion, df_pais, df_maestro)
    
    print("\n" + "="*80)
    print("REPORTE VISUAL COMPLETADO")
    print("="*80)

def generar_reporte_html(df_region, df_genero, df_gestion, df_pais, df_maestro):
    """
    Genera un reporte HTML interactivo
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reporte PRONABEC 2021</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            h1 {
                color: #667eea;
                text-align: center;
                margin-bottom: 10px;
            }
            h2 {
                color: #764ba2;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
                margin-top: 30px;
            }
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            .stat-value {
                font-size: 2.5em;
                font-weight: bold;
                margin: 10px 0;
            }
            .stat-label {
                font-size: 1em;
                opacity: 0.9;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            th {
                background: #667eea;
                color: white;
                padding: 12px;
                text-align: left;
            }
            td {
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }
            tr:hover {
                background: #f5f5f5;
            }
            .footer {
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 2px solid #ddd;
                color: #666;
            }
            .image-container {
                text-align: center;
                margin: 30px 0;
            }
            .image-container img {
                max-width: 100%;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📊 REPORTE PRONABEC 2021</h1>
            <p style="text-align: center; color: #666;">
                Análisis de Becas y Créditos Educativos en Perú
            </p>
    """
    
    # Estadísticas clave
    total_becarios = df_region['CantidadBecarios'].sum()
    total_creditos = df_maestro[df_maestro['TipoBeneficio'] == 'Crédito']['CantidadBecarios'].sum()
    total_extranjero = df_pais[df_pais['Pais'] != 'Total']['CantidadBecarios'].sum()
    
    html_content += f"""
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">📚 Becarios Beca 18</div>
                    <div class="stat-value">{total_becarios:,}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">💳 Créditos Educativos</div>
                    <div class="stat-value">{int(total_creditos):,}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">🌍 Becarios al Extranjero</div>
                    <div class="stat-value">{total_extranjero}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">🏛️ Departamentos</div>
                    <div class="stat-value">26</div>
                </div>
            </div>
            
            <h2>🗺️ Top 10 Departamentos con Más Becarios</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Departamento</th>
                        <th>Cantidad de Becarios</th>
                        <th>Porcentaje</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    top10_region = df_region.nlargest(10, 'CantidadBecarios')
    for idx, row in top10_region.iterrows():
        html_content += f"""
                    <tr>
                        <td>{idx + 1}</td>
                        <td><strong>{row['Departamento']}</strong></td>
                        <td>{row['CantidadBecarios']:,}</td>
                        <td>{row['PorcentajeRegional']}%</td>
                    </tr>
        """
    
    html_content += """
                </tbody>
            </table>
            
            <h2>🏫 Distribución por Tipo de Gestión</h2>
            <table>
                <thead>
                    <tr>
                        <th>Tipo de Gestión</th>
                        <th>Cantidad de Becarios</th>
                        <th>Porcentaje</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    total_gestion = df_gestion['CantidadBecarios'].sum()
    for _, row in df_gestion.iterrows():
        porcentaje = (row['CantidadBecarios'] / total_gestion) * 100
        html_content += f"""
                    <tr>
                        <td><strong>{row['TipoGestion']}</strong></td>
                        <td>{row['CantidadBecarios']:,}</td>
                        <td>{porcentaje:.1f}%</td>
                    </tr>
        """
    
    html_content += """
                </tbody>
            </table>
            
            <h2>🌎 Top 10 Países de Destino</h2>
            <table>
                <thead>
                    <tr>
                        <th>#</th>
                        <th>País</th>
                        <th>Cantidad de Becarios</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    top10_pais = df_pais[df_pais['Pais'] != 'Total'].nlargest(10, 'CantidadBecarios')
    for idx, row in enumerate(top10_pais.itertuples(), 1):
        html_content += f"""
                    <tr>
                        <td>{idx}</td>
                        <td><strong>{row.Pais}</strong></td>
                        <td>{row.CantidadBecarios}</td>
                    </tr>
        """
    
    html_content += """
                </tbody>
            </table>
            
            <h2>👥 Distribución por Género (Créditos Educativos)</h2>
            <table>
                <thead>
                    <tr>
                        <th>Género</th>
                        <th>Cantidad de Créditos</th>
                        <th>Porcentaje</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    df_genero_sum = df_genero.groupby('Genero')['CantidadCreditos'].sum().reset_index()
    total_genero = df_genero_sum['CantidadCreditos'].sum()
    for _, row in df_genero_sum.iterrows():
        porcentaje = (row['CantidadCreditos'] / total_genero) * 100
        html_content += f"""
                    <tr>
                        <td><strong>{row['Genero']}</strong></td>
                        <td>{row['CantidadCreditos']:,}</td>
                        <td>{porcentaje:.1f}%</td>
                    </tr>
        """
    
    html_content += """
                </tbody>
            </table>
            
            <div class="image-container">
                <h2>📈 Visualización General</h2>
                <img src="reporte_visual_pronabec_2021.png" alt="Reporte Visual PRONABEC 2021">
            </div>
            
            <div class="footer">
                <p><strong>Fuente:</strong> Memoria Anual del Pronabec 2021</p>
                <p><strong>Año de datos:</strong> 2021</p>
                <p><strong>Generado:</strong> Noviembre 2025</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open('reporte_pronabec_2021.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Reporte HTML guardado: reporte_pronabec_2021.html")

if __name__ == "__main__":
    generar_reporte_visual()
