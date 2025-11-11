# Web Scraping - Memoria Anual PRONABEC 2022

## 📋 Descripción del Proyecto

Este proyecto realiza web scraping del documento PDF "Memoria Anual del Pronabec 2022" para extraer datos estructurados sobre becas educativas otorgadas en Perú durante el año 2022. Los datos extraídos están preparados para ser utilizados en la creación de un dashboard analítico.

**Fuente:** [Memoria Anual del Pronabec 2022](https://cdn.www.gob.pe/uploads/document/file/4498935/Memoria%20Anual%20del%20Pronabec%202022.pdf?v=1683306322)

**Año de los datos:** 2022

---

## 📊 Datasets Extraídos

### 1. **becarios_por_departamento_2022.csv**
**Descripción:** Distribución de becarios aptos, asistentes e inasistentes por departamento del Perú.

**Campos:**
- `Departamento`: Departamento del Perú
- `Aptos_N`: Número de becarios aptos
- `Aptos_Pct`: Porcentaje de becarios aptos
- `Asistentes_N`: Número de becarios que asistieron al examen
- `Asistentes_Pct`: Porcentaje de asistencia
- `Inasistentes_N`: Número de becarios inasistentes
- `Inasistentes_Pct`: Porcentaje de inasistencia
- `Pagina`: Página del PDF original
- `Anio`: Año del registro (2022)

**Registros:** 25 departamentos + total general

**Utilidad para Dashboard:**
- Mapas de calor geográficos
- Gráficos de distribución regional
- Análisis de migración interna (becarios que estudian en su departamento vs. migran)
- Comparación de tasas de asistencia por región

---

### 2. **becas_por_tipo_modalidad_2022.csv**
**Descripción:** Tipos de becas ofrecidas por PRONABEC con información de becarios continuadores y nuevas becas otorgadas.

**Campos:**
- `TipoBeca`: Tipo de beca (Pregrado, Posgrado, Especiales)
- `NombreBeca`: Nombre específico del programa de beca
- `BecariosContinuadores`: Número de becarios que continúan estudios
- `CantidadBecasOtorgadas2022`: Nuevas becas otorgadas en 2022
- `TotalBecariosActivos`: Total de becarios activos en el programa
- `Pagina`: Página del PDF original
- `Anio`: Año del registro (2022)

**Registros:** 20 modalidades de becas

**Programas incluidos:**
- **Pregrado:** Beca 18, Excelencia Académica, Vocación de Maestro, Mujeres en Ciencias, etc.
- **Posgrado:** Beca Generación del Bicentenario, Beca Aleprona, Docente Universitario
- **Especiales:** Beca Permanencia, Continuidad, Inclusión, etc.

**Utilidad para Dashboard:**
- Gráficos de barras por tipo de beca
- Distribución por modalidad
- Análisis de continuidad vs. nuevas becas
- Comparación de programas más populares

---

### 3. **metas_otorgamiento_becas_2022.csv**
**Descripción:** Metas planteadas vs. becas efectivamente otorgadas por programa.

**Campos:**
- `TipoBeca`: Tipo de beca (Pregrado, Posgrado, Especiales)
- `NombreBeca`: Nombre del programa
- `Meta`: Meta de becas planteada
- `BecasOtorgadas`: Número de becas realmente otorgadas
- `PorcentajeOtorgamiento`: Porcentaje de cumplimiento de la meta
- `Pagina`: Página del PDF original
- `Anio`: Año del registro (2022)

**Registros:** 14 programas

**Utilidad para Dashboard:**
- KPIs de cumplimiento de metas
- Indicadores de eficiencia por programa
- Gráficos de progreso (meta vs. real)
- Análisis de sobrecumplimiento o déficit

---

### 4. **becas_internacionales_pais_2022.csv**
**Descripción:** Distribución de becas de posgrado (maestría y doctorado) por país de destino.

**Campos:**
- `PaisEstudios`: País donde se realizan los estudios
- `Maestria`: Número de becas de maestría
- `Doctorado`: Número de becas de doctorado
- `Total`: Total de becas por país
- `Pagina`: Página del PDF original
- `Anio`: Año del registro (2022)
- `Modalidad`: Tipo de modalidad (Internacional)

**Registros:** 15 países

**Países principales:**
- Estados Unidos (34 becas)
- España (30 becas)
- Argentina (24 becas)
- Reino Unido (22 becas)
- Australia (12 becas)

**Utilidad para Dashboard:**
- Mapas de migración internacional
- Distribución por país de destino
- Comparación maestría vs. doctorado
- Análisis de preferencias geográficas

---

### 5. **creditos_educativos_2022.csv**
**Descripción:** Información sobre modalidades de crédito educativo otorgadas por PRONABEC.

**Campos:**
- `ModalidadCredito`: Tipo de crédito educativo
- `BeneficiariosDesembolsos`: Número de beneficiarios con desembolsos
- `MontoDesembolsado`: Monto total desembolsado (en soles)
- `ParticipacionPct`: Porcentaje de participación del crédito
- `Pagina`: Página del PDF original
- `Anio`: Año del registro (2022)

**Registros:** 4 modalidades (3 + total)

**Modalidades:**
- **Crédito Talento:** 174 beneficiarios, 63% de participación
- **Crédito 18:** 150 beneficiarios, 22% de participación
- **Crédito Continuidad:** 189 beneficiarios, 14% de participación

**Utilidad para Dashboard:**
- Análisis financiero de recursos
- Distribución de montos por modalidad
- Comparación de beneficiarios
- Gráficos de participación presupuestaria

---

## 🔧 Scripts Desarrollados

### 1. `scraper_pronabec_2022.py`
**Función:** Script principal de web scraping que descarga y extrae tablas del PDF.

**Características:**
- Descarga automática del PDF desde la URL oficial
- Extracción de todas las tablas usando `pdfplumber`
- Identificación inteligente de datasets relevantes basada en palabras clave
- Generación de archivo Excel consolidado con múltiples hojas
- Exportación de CSVs individuales

**Uso:**
```bash
python scraper_pronabec_2022.py
```

**Output:**
- `datos_extraidos/pronabec_2022_datos.xlsx` (archivo Excel con todas las hojas)
- CSVs individuales por cada tabla extraída
- Resumen de datasets encontrados

---

### 2. `procesar_datos_dashboard.py`
**Función:** Procesa y limpia los datos extraídos para uso en dashboards.

**Características:**
- Limpieza de datos (eliminación de encabezados duplicados, valores nulos)
- Renombrado de columnas a nombres descriptivos
- Filtrado de filas válidas
- Adición de campos calculados (Año, Modalidad)
- Generación de reporte consolidado

**Uso:**
```bash
python procesar_datos_dashboard.py
```

**Output:**
- 5 archivos CSV limpios y listos para dashboard
- `REPORTE_CONSOLIDADO_2022.csv` con resumen de todos los datasets

---

## 📁 Estructura de Archivos

```
scrapeo_2022/
│
├── scraper_pronabec_2022.py          # Script principal de scraping
├── procesar_datos_dashboard.py       # Script de procesamiento
├── README_DATOS_EXTRAIDOS.md         # Esta documentación
│
└── datos_extraidos/
    ├── pronabec_2022_datos.xlsx      # Excel con todos los datos
    ├── becarios_por_departamento_2022.csv
    ├── becas_por_tipo_modalidad_2022.csv
    ├── metas_otorgamiento_becas_2022.csv
    ├── becas_internacionales_pais_2022.csv
    ├── creditos_educativos_2022.csv
    ├── REPORTE_CONSOLIDADO_2022.csv
    └── [otros CSVs de tablas extraídas]
```

---

## 🎯 Campos del Dashboard Solicitados

Comparación con los campos requeridos:

| Campo Requerido | Dataset que lo contiene | Observaciones |
|----------------|------------------------|---------------|
| **NombreBeca** | `becas_por_tipo_modalidad_2022.csv`, `metas_otorgamiento_becas_2022.csv` | ✅ Disponible |
| **Institucion** | ❌ No encontrado en el PDF | El PDF no contiene información detallada por institución |
| **AnioBecariosConfirmados** | Todos los datasets (campo `Anio` = 2022) | ✅ Disponible |
| **Departamento** | `becarios_por_departamento_2022.csv` | ✅ Disponible |
| **Carrera** | ❌ No encontrado en el PDF | El PDF no desglosa por carrera específica |
| **Modalidad** | `becas_por_tipo_modalidad_2022.csv` (TipoBeca, NombreBeca) | ✅ Parcialmente disponible |
| **Estrato socioeconómico** | ❌ No encontrado en el PDF | El PDF no incluye esta información por becario |
| **Migración** | `becarios_por_departamento_2022.csv`, `becas_internacionales_pais_2022.csv` | ✅ Datos de distribución geográfica disponibles |

---

## 📈 Casos de Uso para Dashboard

### 1. **Análisis Geográfico**
- Mapa de calor de becarios por departamento
- Tasa de asistencia a exámenes por región
- Migración interna (departamentos con más migración)
- Migración internacional (países destino)

### 2. **Análisis de Programas**
- Comparación de becas por tipo (Pregrado, Posgrado, Especiales)
- Programas más populares
- Tendencias de continuidad vs. nuevos becarios
- Cumplimiento de metas por programa

### 3. **Análisis Financiero**
- Distribución de créditos educativos
- Montos desembolsados por modalidad
- Participación presupuestaria
- Beneficiarios por tipo de crédito

### 4. **KPIs Principales**
- Total de becas otorgadas en 2022
- Porcentaje de cumplimiento de metas
- Tasa de asistencia a exámenes
- Distribución por tipo de beca
- Becas internacionales por continente

---

## ⚠️ Limitaciones y Consideraciones

1. **Datos faltantes:**
   - El PDF no contiene información detallada por institución educativa
   - No hay desglose por carrera específica
   - No incluye información de estrato socioeconómico por becario individual
   - Datos de migración son inferidos a partir de distribución geográfica

2. **Calidad de los datos:**
   - Algunas tablas del PDF tienen formato complejo
   - Valores con formato de miles (espacios) que pueden requerir limpieza adicional
   - Algunas columnas pueden contener valores NaN en modalidades específicas

3. **Recomendaciones:**
   - Para información más detallada (institución, carrera), considerar buscar anexos del documento o datos complementarios
   - Los datos de migración son aproximados; para análisis preciso de migración, se requeriría datos de origen y destino por becario
   - Para estrato socioeconómico, buscar fuentes adicionales del PRONABEC

---

## 🚀 Próximos Pasos

1. **Enriquecimiento de datos:**
   - Buscar fuentes complementarias para campos faltantes
   - Cruzar con datos de años anteriores para análisis temporal
   - Agregar coordenadas geográficas para mapas

2. **Visualización:**
   - Crear dashboard interactivo con Power BI, Tableau o Python (Plotly/Dash)
   - Implementar filtros por tipo de beca, departamento, modalidad
   - Crear storytelling con los datos

3. **Análisis adicional:**
   - Análisis de tendencias comparando con años anteriores
   - Predicción de demanda de becas por región
   - Análisis de eficiencia en cumplimiento de metas

---

## 📦 Dependencias

```python
requests==2.31.0
pdfplumber==0.10.3
pandas==2.1.4
openpyxl==3.1.2
```

**Instalación:**
```bash
pip install requests pdfplumber pandas openpyxl
```

---

## 👥 Autor

Proyecto desarrollado para: **EasyBeca Dashboard - Sprint 2**

**Fecha de extracción:** Noviembre 2025

**Fuente oficial:** Gobierno del Perú - PRONABEC

---

## 📝 Notas Finales

Este dataset es ideal para:
- ✅ Análisis de distribución geográfica de becas
- ✅ Evaluación de cumplimiento de metas
- ✅ Análisis de tipos y modalidades de becas
- ✅ Visualización de migración educativa
- ✅ Análisis financiero de créditos educativos

Para análisis más granulares (por institución, carrera, estrato socioeconómico individual), se recomienda complementar con fuentes de datos adicionales del PRONABEC o MINEDU.
