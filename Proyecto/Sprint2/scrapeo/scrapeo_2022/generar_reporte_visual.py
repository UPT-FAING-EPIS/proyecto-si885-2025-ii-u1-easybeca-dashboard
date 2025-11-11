import pandas as pd
from pathlib import Path

# Crear HTML
html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte de Datos PRONABEC 2022</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
        }
        
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        .stat-card .number {
            font-size: 3em;
            font-weight: bold;
            color: #667eea;
            margin: 10px 0;
        }
        
        .stat-card .label {
            font-size: 1.1em;
            color: #666;
            font-weight: 500;
        }
        
        .section {
            padding: 40px;
        }
        
        .section h2 {
            color: #1e3c72;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            font-size: 2em;
        }
        
        .dataset-card {
            background: #f8f9fa;
            border-left: 5px solid #667eea;
            padding: 25px;
            margin-bottom: 25px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        
        .dataset-card:hover {
            background: #e9ecef;
            border-left-width: 8px;
        }
        
        .dataset-card h3 {
            color: #2a5298;
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        
        .dataset-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }
        
        .info-item {
            background: white;
            padding: 12px;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        .info-item strong {
            color: #667eea;
            display: block;
            margin-bottom: 5px;
        }
        
        .table-container {
            overflow-x: auto;
            margin-top: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }
        
        th {
            background: #1e3c72;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
            font-size: 0.95em;
        }
        
        td {
            padding: 12px 15px;
            border-bottom: 1px solid #dee2e6;
        }
        
        tr:hover {
            background: #f8f9fa;
        }
        
        .badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            background: #667eea;
            color: white;
        }
        
        .footer {
            background: #1e3c72;
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .footer a {
            color: #a5b4fc;
            text-decoration: none;
            font-weight: 600;
        }
        
        .footer a:hover {
            color: white;
            text-decoration: underline;
        }
        
        @media (max-width: 768px) {
            .header h1 {
                font-size: 1.8em;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
            
            .section {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Reporte de Datos PRONABEC 2022</h1>
            <p>Web Scraping - Memoria Anual del Programa Nacional de Becas y Crédito Educativo</p>
            <p style="font-size: 0.9em; margin-top: 10px;">Fuente: Gobierno del Perú</p>
        </div>
"""

# Leer archivos
output_dir = Path("datos_extraidos")

# Estadísticas generales
stats = {
    'departamentos': 0,
    'becas': 0,
    'programas': 0,
    'paises': 0,
    'creditos': 0
}

# Leer cada archivo
datasets = {}

files = [
    ('becarios_por_departamento_2022.csv', 'departamentos'),
    ('becas_por_tipo_modalidad_2022.csv', 'becas'),
    ('metas_otorgamiento_becas_2022.csv', 'programas'),
    ('becas_internacionales_pais_2022.csv', 'paises'),
    ('creditos_educativos_2022.csv', 'creditos')
]

for filename, key in files:
    filepath = output_dir / filename
    if filepath.exists():
        df = pd.read_csv(filepath)
        datasets[key] = df
        stats[key] = len(df) - 1 if 'total' in df.iloc[-1].to_string().lower() else len(df)

# Agregar estadísticas
html_content += """
        <div class="stats-grid">
            <div class="stat-card">
                <div class="number">{departamentos}</div>
                <div class="label">Departamentos</div>
            </div>
            <div class="stat-card">
                <div class="number">{becas}</div>
                <div class="label">Modalidades de Becas</div>
            </div>
            <div class="stat-card">
                <div class="number">{programas}</div>
                <div class="label">Programas</div>
            </div>
            <div class="stat-card">
                <div class="number">{paises}</div>
                <div class="label">Países (Int.)</div>
            </div>
        </div>
""".format(**stats)

# Sección de datasets
html_content += """
        <div class="section">
            <h2>📁 Datasets Extraídos</h2>
"""

# Dataset 1: Departamentos
if 'departamentos' in datasets:
    df = datasets['departamentos']
    html_content += f"""
            <div class="dataset-card">
                <h3>1. Becarios por Departamento</h3>
                <p>Distribución de becarios aptos, asistentes e inasistentes por departamento del Perú.</p>
                <div class="dataset-info">
                    <div class="info-item">
                        <strong>Registros:</strong>
                        {len(df)}
                    </div>
                    <div class="info-item">
                        <strong>Archivo:</strong>
                        becarios_por_departamento_2022.csv
                    </div>
                    <div class="info-item">
                        <strong>Campos:</strong>
                        {len(df.columns)} columnas
                    </div>
                    <div class="info-item">
                        <strong>Año:</strong>
                        <span class="badge">2022</span>
                    </div>
                </div>
                <div class="table-container">
                    {df.head(10).to_html(index=False, classes='data-table')}
                </div>
            </div>
"""

# Dataset 2: Becas
if 'becas' in datasets:
    df = datasets['becas']
    html_content += f"""
            <div class="dataset-card">
                <h3>2. Becas por Tipo y Modalidad</h3>
                <p>Tipos de becas ofrecidas con información de becarios continuadores y nuevas becas otorgadas.</p>
                <div class="dataset-info">
                    <div class="info-item">
                        <strong>Registros:</strong>
                        {len(df)}
                    </div>
                    <div class="info-item">
                        <strong>Archivo:</strong>
                        becas_por_tipo_modalidad_2022.csv
                    </div>
                    <div class="info-item">
                        <strong>Campos:</strong>
                        {len(df.columns)} columnas
                    </div>
                    <div class="info-item">
                        <strong>Año:</strong>
                        <span class="badge">2022</span>
                    </div>
                </div>
                <div class="table-container">
                    {df.head(10).to_html(index=False, classes='data-table')}
                </div>
            </div>
"""

# Dataset 3: Metas
if 'programas' in datasets:
    df = datasets['programas']
    html_content += f"""
            <div class="dataset-card">
                <h3>3. Metas y Otorgamiento de Becas</h3>
                <p>Comparación entre metas planteadas y becas efectivamente otorgadas por programa.</p>
                <div class="dataset-info">
                    <div class="info-item">
                        <strong>Registros:</strong>
                        {len(df)}
                    </div>
                    <div class="info-item">
                        <strong>Archivo:</strong>
                        metas_otorgamiento_becas_2022.csv
                    </div>
                    <div class="info-item">
                        <strong>Campos:</strong>
                        {len(df.columns)} columnas
                    </div>
                    <div class="info-item">
                        <strong>Año:</strong>
                        <span class="badge">2022</span>
                    </div>
                </div>
                <div class="table-container">
                    {df.head(10).to_html(index=False, classes='data-table')}
                </div>
            </div>
"""

# Dataset 4: Internacional
if 'paises' in datasets:
    df = datasets['paises']
    html_content += f"""
            <div class="dataset-card">
                <h3>4. Becas Internacionales por País</h3>
                <p>Distribución de becas de maestría y doctorado por país de destino.</p>
                <div class="dataset-info">
                    <div class="info-item">
                        <strong>Registros:</strong>
                        {len(df)}
                    </div>
                    <div class="info-item">
                        <strong>Archivo:</strong>
                        becas_internacionales_pais_2022.csv
                    </div>
                    <div class="info-item">
                        <strong>Campos:</strong>
                        {len(df.columns)} columnas
                    </div>
                    <div class="info-item">
                        <strong>Modalidad:</strong>
                        <span class="badge">Internacional</span>
                    </div>
                </div>
                <div class="table-container">
                    {df.to_html(index=False, classes='data-table')}
                </div>
            </div>
"""

# Dataset 5: Créditos
if 'creditos' in datasets:
    df = datasets['creditos']
    html_content += f"""
            <div class="dataset-card">
                <h3>5. Créditos Educativos</h3>
                <p>Modalidades de crédito educativo con beneficiarios y montos desembolsados.</p>
                <div class="dataset-info">
                    <div class="info-item">
                        <strong>Registros:</strong>
                        {len(df)}
                    </div>
                    <div class="info-item">
                        <strong>Archivo:</strong>
                        creditos_educativos_2022.csv
                    </div>
                    <div class="info-item">
                        <strong>Campos:</strong>
                        {len(df.columns)} columnas
                    </div>
                    <div class="info-item">
                        <strong>Año:</strong>
                        <span class="badge">2022</span>
                    </div>
                </div>
                <div class="table-container">
                    {df.to_html(index=False, classes='data-table')}
                </div>
            </div>
"""

html_content += """
        </div>
        
        <div class="footer">
            <p><strong>Proyecto:</strong> EasyBeca Dashboard - Sprint 2</p>
            <p style="margin-top: 10px;">Datos extraídos mediante Web Scraping del PDF oficial</p>
            <p style="margin-top: 10px;">
                <a href="https://cdn.www.gob.pe/uploads/document/file/4498935/Memoria%20Anual%20del%20Pronabec%202022.pdf?v=1683306322" target="_blank">
                    📄 Ver documento original
                </a>
            </p>
            <p style="margin-top: 20px; font-size: 0.9em; opacity: 0.8;">
                © 2025 - Datos del Gobierno del Perú - PRONABEC
            </p>
        </div>
    </div>
</body>
</html>
"""

# Guardar HTML
html_path = output_dir / "REPORTE_VISUAL_2022.html"
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("="*70)
print("✓ REPORTE VISUAL GENERADO")
print("="*70)
print(f"\nArchivo: {html_path}")
print("\nAbre este archivo en tu navegador para ver el reporte interactivo.")
print("\nEl reporte incluye:")
print("  • Estadísticas generales")
print("  • Visualización de todos los datasets")
print("  • Tablas con primeras filas de cada dataset")
print("  • Información detallada de cada archivo")
