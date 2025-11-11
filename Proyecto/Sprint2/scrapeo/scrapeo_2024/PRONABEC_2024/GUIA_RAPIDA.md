# 🚀 Guía Rápida de Uso - Web Scraping PRONABEC 2024

## ⚡ Inicio Rápido

### 1️⃣ Ejecutar el Scraping Completo

```bash
# Activar entorno virtual (si es necesario)
.venv\Scripts\activate

# Ejecutar scraping mejorado
python scrape_pronabec_2024_mejorado.py

# Analizar y consolidar datos
python analizar_datos.py

# Generar visualizaciones
python visualizar_datos.py
```

---

## 📂 Archivos Principales para tu Dashboard

### 🎯 Archivos Recomendados

**Para usar en dashboards**:
- `dashboard_departamentos_2024.xlsx` - Datos por departamento
- `dashboard_becas_2024.xlsx` - Tipos de becas
- `dashboard_estadisticas_2024.json` - Estadísticas generales

**Para presentaciones**:
- `grafico_departamentos_2024.png`
- `grafico_becas_2024.png`
- `grafico_resumen_2024.png`

---

## 🔥 Casos de Uso Rápidos

### Dashboard en Power BI

1. **Importar datos**:
   - Datos > Obtener datos > Excel
   - Seleccionar: `dashboard_departamentos_2024.xlsx`

2. **Crear visualización**:
   - Mapa de relleno → Ubicación: Departamento, Valores: CantidadBecarios
   - Gráfico de barras → Eje X: Departamento, Eje Y: CantidadBecarios

### Dashboard en Python

```python
import pandas as pd
import plotly.express as px

# Cargar datos
df = pd.read_csv('dashboard_departamentos_2024.csv')

# Crear mapa
fig = px.choropleth(df, 
                    locations='Departamento',
                    locationmode='country names',
                    color='CantidadBecarios',
                    title='Distribución de Becarios PRONABEC 2024')
fig.show()
```

### Análisis en Excel

1. Abrir `dashboard_departamentos_2024.xlsx`
2. Seleccionar datos → Insertar → Gráfico recomendado
3. Elegir "Mapa de árbol" o "Gráfico de barras"

---

## 📊 Estructura de Datos

### dashboard_departamentos_2024.csv

```csv
Departamento,CantidadBecarios,AnioBecariosConfirmados
Lima,151,2024
Ica,93,2024
Callao,49,2024
```

**Campos**:
- `Departamento`: Nombre del departamento (string)
- `CantidadBecarios`: Número de becarios (int)
- `AnioBecariosConfirmados`: Año (int, siempre 2024)

### dashboard_becas_2024.csv

```csv
TipoBeca,NombreBeca,Meta,BecasOtorgadas,PorcentajeOtorgamiento
Pregrado,Beca 18,10000,10004,100.0
```

**Campos**:
- `TipoBeca`: Tipo de beca (string)
- `NombreBeca`: Nombre específico (string)
- `Meta`: Meta planificada (int)
- `BecasOtorgadas`: Becas realmente otorgadas (int)
- `PorcentajeOtorgamiento`: % de cumplimiento (float)

---

## 🎨 Visualizaciones Disponibles

### grafico_departamentos_2024.png
- **Izquierda**: Top 15 departamentos (barras horizontales)
- **Derecha**: Distribución porcentual (pie chart)
- **Uso**: Presentaciones, informes, dashboards estáticos

### grafico_becas_2024.png
- **Izquierda**: Becas otorgadas por tipo
- **Derecha**: Meta vs Otorgadas (comparación)
- **Uso**: Análisis de cumplimiento de metas

### grafico_resumen_2024.png
- Panel completo con estadísticas generales
- Top 5 departamentos
- Información de cobertura
- **Uso**: Resumen ejecutivo, presentaciones a directivos

---

## 🔧 Personalización Rápida

### Cambiar Colores en visualizar_datos.py

```python
# Línea ~96
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']  # Cambia estos códigos

# Para más colores usar paletas
colors = plt.cm.viridis(range(n))  # viridis, plasma, inferno, magma
```

### Filtrar Departamentos Específicos

```python
import pandas as pd

df = pd.read_csv('dashboard_departamentos_2024.csv')

# Top 10
df_top10 = df.head(10)

# Departamentos específicos
costa = ['Lima', 'Callao', 'Piura', 'La Libertad', 'Ica']
df_costa = df[df['Departamento'].isin(costa)]

# Guardar filtrado
df_costa.to_csv('becarios_costa_2024.csv', index=False)
```

### Agregar Campos Calculados

```python
import pandas as pd

df = pd.read_csv('dashboard_departamentos_2024.csv')

# Calcular porcentaje
total = df['CantidadBecarios'].sum()
df['PorcentajeTotal'] = (df['CantidadBecarios'] / total * 100).round(2)

# Categorizar
def categorizar(cantidad):
    if cantidad > 100: return 'Alto'
    elif cantidad > 50: return 'Medio'
    else: return 'Bajo'

df['Categoria'] = df['CantidadBecarios'].apply(categorizar)

df.to_csv('dashboard_departamentos_enriquecido.csv', index=False)
```

---

## 📈 Métricas Clave para Dashboard

### KPIs Principales

```python
import pandas as pd
import json

# Cargar estadísticas
with open('dashboard_estadisticas_2024.json', 'r', encoding='utf-8') as f:
    stats = json.load(f)

print(f"📊 Total Becarios: {stats['total_becarios']:,}")
print(f"📍 Departamentos: {stats['total_departamentos']}")
print(f"🎓 Tipos de Becas: {stats['tipos_becas']}")
```

### Indicadores de Concentración

```python
df = pd.read_csv('dashboard_departamentos_2024.csv')

top5 = df.head(5)['CantidadBecarios'].sum()
total = df['CantidadBecarios'].sum()
concentracion = (top5 / total * 100)

print(f"Top 5 concentra: {concentracion:.1f}% del total")
```

---

## 🛠️ Solución de Problemas

### Error: "File not found"
```bash
# Asegúrate de estar en el directorio correcto
cd PRONABEC_2024
python analizar_datos.py
```

### Error: "Module not found"
```bash
# Instalar dependencias
pip install pandas openpyxl matplotlib seaborn
```

### Datos Vacíos o Incompletos
```python
# Verificar datos
import pandas as pd

df = pd.read_csv('dashboard_departamentos_2024.csv')
print(df.info())
print(df.isnull().sum())

# Llenar valores nulos
df.fillna(0, inplace=True)
```

---

## 📞 Checklist de Entrega

- [ ] Datos extraídos (`dashboard_*.csv` y `.xlsx`)
- [ ] Visualizaciones generadas (`grafico_*.png`)
- [ ] Estadísticas en JSON (`dashboard_estadisticas_2024.json`)
- [ ] Documentación (`README_DASHBOARD.md`, `RESUMEN_PROYECTO.md`)
- [ ] Scripts funcionando (`scrape_*.py`, `analizar_datos.py`, `visualizar_datos.py`)

---

## 🎯 Tips para un Dashboard Efectivo

1. **Usa KPIs Grandes**: Total de becarios, departamentos, etc.
2. **Mapas Geográficos**: Visualiza distribución por departamento
3. **Gráficos de Tendencia**: Compara metas vs resultados
4. **Filtros Interactivos**: Permite filtrar por departamento o tipo de beca
5. **Top N**: Muestra top 5 o top 10 departamentos
6. **Porcentajes**: Agrega visualizaciones de distribución porcentual

---

## ✨ Mejoras Futuras Sugeridas

1. **Scraping Periódico**: Automatizar extracción mensual
2. **Datos Históricos**: Comparar 2024 vs años anteriores
3. **Geolocalización**: Agregar coordenadas GPS de instituciones
4. **API REST**: Crear servicio web para acceso a datos
5. **Dashboard Web**: Desarrollar interfaz web interactiva (Streamlit/Dash)

---

## 📚 Recursos Adicionales

### Tutoriales Recomendados
- [Power BI Dashboard](https://learn.microsoft.com/es-es/power-bi/)
- [Plotly Dash en Python](https://dash.plotly.com/)
- [Pandas para Análisis](https://pandas.pydata.org/docs/)

### Herramientas Sugeridas
- **Visualización**: Power BI, Tableau, Looker Studio
- **Python**: Jupyter Notebook, Streamlit, Dash
- **Excel**: Tablas dinámicas, gráficos dinámicos

---

**¡Listo para crear tu dashboard! 🚀**

Si necesitas ayuda adicional, revisa `RESUMEN_PROYECTO.md` o `README_DASHBOARD.md`
