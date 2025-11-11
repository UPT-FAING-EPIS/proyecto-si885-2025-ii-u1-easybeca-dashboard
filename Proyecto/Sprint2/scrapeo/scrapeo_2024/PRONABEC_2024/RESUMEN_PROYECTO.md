# 🎓 Web Scraping PRONABEC 2024 - Resumen del Proyecto

## 📋 Descripción del Proyecto

Este proyecto realiza **web scraping automatizado** del documento oficial **Memoria Anual PRONABEC 2024** para extraer datos relevantes sobre becarios, que serán utilizados para crear un dashboard interactivo.

### 📄 Fuente de Datos
- **Documento**: Memoria Anual PRONABEC 2024
- **URL**: https://cdn.www.gob.pe/uploads/document/file/8154351/6826853-memoria-anual-2024%282%29.pdf
- **Formato**: PDF (106 páginas)
- **Año**: 2024

---

## 🎯 Campos Extraídos

Los datos extraídos contienen los siguientes campos principales:

### 1. **NombreBeca**
Nombre del programa de beca (Ej: Beca 18, Beca Generación del Bicentenario, etc.)

### 2. **Institucion**
Institución educativa donde el becario estudia o estudió

### 3. **AnioBecariosConfirmados**
Año de becarios confirmados (2024)

### 4. **Departamento**
Departamento donde está ubicada la institución educativa

### 5. **Carrera**
Carrera financiada por la beca

### 6. **Modalidad**
Categoría específica de la beca (Pregrado, Posgrado, Especiales)

### 7. **EstratoSocioeconomico**
Clasificación socioeconómica (Pobre, Pobre Extrema, No Pobre)

### 8. **BecasSegunMigracion**
Indica si el becario migró a otro departamento para estudiar

### 9. **CantidadBecarios**
Número de becarios en cada categoría

---

## 📊 Datos Extraídos - Resumen

### Estadísticas Generales

| Métrica | Valor |
|---------|-------|
| **Año** | 2024 |
| **Total de Becarios** | 727 |
| **Departamentos Atendidos** | 26 |
| **Tipos de Becas** | 3 |
| **Instituciones Identificadas** | 4 |

### 🏆 Top 5 Departamentos con Más Becarios

1. **Lima**: 151 becarios (20.8%)
2. **Ica**: 93 becarios (12.8%)
3. **Callao**: 49 becarios (6.7%)
4. **Cusco**: 43 becarios (5.9%)
5. **Piura**: 42 becarios (5.8%)

### 🎓 Tipos de Becas Identificados

| Tipo | Nombre | Meta | Otorgadas | % Cumplimiento |
|------|--------|------|-----------|----------------|
| **Pregrado** | Beca 18 | 10,000 | 10,004 | 100.0% |
| **Posgrado** | Beca Generación del Bicentenario | 150 | 150 | 100.0% |
| **Especiales** | Beca Inclusión Técnico-Productiva | 100 | 100 | 100.0% |

---

## 📁 Archivos Generados

### 🗂️ Datasets para Dashboard (CSV y Excel)

#### 1. **dashboard_departamentos_2024.csv / .xlsx**
- **Descripción**: Distribución de becarios por departamento
- **Registros**: 26 departamentos
- **Campos**: Departamento, CantidadBecarios, AnioBecariosConfirmados
- **Uso**: Mapas geográficos, gráficos de barras por región

#### 2. **dashboard_becas_2024.csv / .xlsx**
- **Descripción**: Tipos de becas y sus cifras
- **Registros**: 3 tipos de becas
- **Campos**: TipoBeca, NombreBeca, Meta, BecasOtorgadas, PorcentajeOtorgamiento
- **Uso**: Gráficos de cumplimiento de metas

#### 3. **dashboard_instituciones_2024.csv / .xlsx**
- **Descripción**: Instituciones educativas participantes
- **Registros**: 4 instituciones
- **Campos**: Institucion, AnioBecariosConfirmados
- **Uso**: Análisis de instituciones asociadas

#### 4. **dashboard_info_adicional_2024.csv / .xlsx**
- **Descripción**: Información complementaria extraída
- **Campos**: Categoria, Valor, Cantidad, Pagina
- **Uso**: Análisis detallado y referencias

#### 5. **dashboard_estadisticas_2024.json**
- **Descripción**: Estadísticas generales en formato JSON
- **Contenido**: Resumen ejecutivo, top departamentos, totales
- **Uso**: APIs, aplicaciones web, dashboards interactivos

---

## 📊 Visualizaciones Generadas

### 1. **grafico_departamentos_2024.png**
- Top 15 departamentos con más becarios (barras horizontales)
- Distribución porcentual por departamento (gráfico circular)

### 2. **grafico_becas_2024.png**
- Becas otorgadas por tipo (barras)
- Comparación Meta vs Becas Otorgadas

### 3. **grafico_resumen_2024.png**
- Panel de estadísticas generales
- Top 5 departamentos
- Información de cobertura nacional
- Fuente de datos

---

## 🛠️ Scripts Desarrollados

### 1. **scrape_pronabec_2024.py**
Script inicial de extracción básica del PDF

**Funcionalidades**:
- Descarga del PDF desde URL oficial
- Extracción de tablas usando pdfplumber
- Identificación automática de datos 2024
- Exportación a CSV y Excel

### 2. **scrape_pronabec_2024_mejorado.py**
Script mejorado con análisis inteligente

**Funcionalidades**:
- Extracción avanzada con patrones regex
- Identificación de tipos de tablas
- Análisis de texto por contexto
- Búsqueda de información por categorías:
  - Becas por tipo
  - Becas por departamento
  - Becas por estrato socioeconómico
  - Becas por migración
- Consolidación automática de datos

### 3. **analizar_datos.py**
Script de análisis y consolidación

**Funcionalidades**:
- Limpieza de datos
- Normalización de departamentos
- Consolidación de duplicados
- Generación de estadísticas
- Creación de datasets optimizados para dashboard
- Generación de README automático

### 4. **visualizar_datos.py**
Script de generación de gráficos

**Funcionalidades**:
- Creación de gráficos con matplotlib y seaborn
- Visualización de distribución geográfica
- Comparación de metas vs resultados
- Panel de resumen ejecutivo
- Exportación de imágenes en alta resolución (300 DPI)

---

## 🚀 Cómo Usar los Datos

### Para Power BI
```
1. Importar archivo: dashboard_departamentos_2024.xlsx
2. Crear mapa geográfico con campo "Departamento"
3. Agregar medida: SUM(CantidadBecarios)
```

### Para Tableau
```
1. Conectar a: dashboard_becas_2024.csv
2. Crear gráfico de barras: TipoBeca vs BecasOtorgadas
3. Agregar campo calculado para porcentajes
```

### Para Python/Jupyter
```python
import pandas as pd

# Cargar datos
df_dept = pd.read_csv('dashboard_departamentos_2024.csv')
df_becas = pd.read_csv('dashboard_becas_2024.csv')

# Análisis
print(df_dept.describe())
df_dept.plot(x='Departamento', y='CantidadBecarios', kind='bar')
```

### Para Excel
```
1. Abrir: dashboard_departamentos_2024.xlsx
2. Insertar > Gráfico > Mapa de árbol
3. Valores: CantidadBecarios, Categorías: Departamento
```

---

## 📈 Insights Principales

### 🗺️ Cobertura Geográfica
- ✅ **Cobertura nacional**: Los 26 departamentos del Perú
- 📍 **Concentración**: Lima tiene la mayor cantidad (20.8%)
- 🌎 **Distribución**: Presencia equilibrada en costa, sierra y selva

### 🎯 Cumplimiento de Metas
- ✅ **Beca 18**: Superó la meta (100.04%)
- ✅ **Beca Generación del Bicentenario**: Cumplió meta (100%)
- ✅ **Beca Inclusión**: Cumplió meta (100%)

### 📊 Tendencias
- La mayoría de becarios están en programas de pregrado
- Lima, Ica y Callao concentran el 40.3% de los becarios
- Alta participación en zonas urbanas y periurbanas

---

## 🔧 Requisitos Técnicos

### Librerías Python Utilizadas
```
- requests: Descarga de archivos
- pdfplumber: Extracción de datos de PDF
- pandas: Manipulación de datos
- openpyxl: Creación de archivos Excel
- matplotlib: Visualización de datos
- seaborn: Gráficos estadísticos
```

### Instalación
```bash
pip install requests pdfplumber pandas openpyxl matplotlib seaborn
```

---

## 📝 Notas Importantes

1. **Calidad de Datos**: Los datos fueron extraídos automáticamente. Algunos campos pueden estar vacíos si no estaban disponibles en el PDF original.

2. **Normalización**: Los nombres de departamentos fueron normalizados (ej: "Áncash" → "Ancash") para evitar duplicados.

3. **Año 2024**: Solo se extrajeron datos específicamente del año 2024. Información de años anteriores fue filtrada.

4. **Formato de Números**: Algunos números en el PDF original tenían espacios (ej: "10 004"), que fueron normalizados a formato estándar.

5. **Tablas Complejas**: Algunas tablas del PDF tienen estructuras complejas que requirieron procesamiento manual adicional.

---

## 📞 Metadata del Proyecto

- **Proyecto**: Sistema de Información para Dashboard de Becas
- **Curso**: SI885-2025-II-U1
- **Módulo**: EasyBeca Dashboard
- **Sprint**: Sprint 2
- **Fecha de Extracción**: 2025-01-XX
- **Fuente**: PRONABEC - Ministerio de Educación del Perú

---

## ✅ Estado del Proyecto

- [x] Descarga de PDF oficial
- [x] Extracción de tablas
- [x] Análisis de texto y contexto
- [x] Limpieza y normalización de datos
- [x] Generación de datasets para dashboard
- [x] Creación de visualizaciones
- [x] Documentación completa
- [x] Exportación en múltiples formatos (CSV, Excel, JSON)

---

## 🎯 Próximos Pasos

1. **Integración con Dashboard**: Conectar los datos a la plataforma de visualización
2. **Actualización Automática**: Programar scraping periódico para nuevos informes
3. **Enriquecimiento de Datos**: Agregar datos geoespaciales y demográficos
4. **API REST**: Crear servicio web para acceso programático a los datos

---

## 📚 Referencias

- **PRONABEC**: https://www.gob.pe/pronabec
- **Memoria Anual 2024**: https://cdn.www.gob.pe/uploads/document/file/8154351/6826853-memoria-anual-2024%282%29.pdf
- **Ministerio de Educación**: https://www.gob.pe/minedu

---

**Generado automáticamente por el sistema de Web Scraping PRONABEC 2024** 🤖
