# Web Scraping - Memoria Anual PRONABEC 2021

## 📋 Descripción

Este proyecto extrae datos de la **Memoria Anual del Pronabec 2021** para crear datasets estructurados que permitan construir un dashboard analítico sobre becas y créditos educativos en Perú.

**Fuente:** [Memoria Anual del Pronabec 2021 (PDF)](https://cdn.www.gob.pe/uploads/document/file/3157095/Memoria%20Anual%20del%20Pronabec%202021.pdf?v=1653683954)

**Año de datos:** 2021

---

## 🎯 Datos Extraídos

### Campos del Dataset Principal

El dataset maestro (`dataset_maestro_pronabec_2021.xlsx`) contiene los siguientes campos:

| Campo | Descripción | Tipo | Ejemplo |
|-------|-------------|------|---------|
| **NombreBeca** | Nombre del programa de beca o crédito | Texto | "Beca 18", "Crédito General" |
| **Institucion** | Institución donde el becario estudia/estudió | Texto | "Varias", "Diversas", "Internacional" |
| **AnioBecariosConfirmados** | Año de becarios confirmados | Número | 2021 |
| **Departamento** | Departamento donde está ubicada la institución o región de origen | Texto | "Lima", "Cusco", "Arequipa" |
| **Carrera** | Carrera financiada por la beca | Texto | "Varias", "Diversas" |
| **Modalidad** | Categoría específica de la beca | Texto | "General", "Crédito Educativo" |
| **EstratoSocioeconomico** | Clasificación social (pobre, pobre extrema, no pobre) | Texto | "No especificado" |
| **Migracion** | Becarios que migraron o no para estudiar | Texto | "No especificado" |
| **CantidadBecarios** | Cantidad de becarios o créditos | Número | 457, 1536 |
| **TipoBeneficio** | Tipo de beneficio otorgado | Texto | "Beca", "Crédito" |
| **MontoDesembolsado** | Monto desembolsado en soles (solo para créditos) | Número | 14473084.0 |

---

## 📊 Datasets Generados

### 1. Dataset Maestro
**Archivo:** `dataset_maestro_pronabec_2021.xlsx` / `dataset_maestro_pronabec_2021.csv`

Dataset consolidado con 123 registros que combina información de becas y créditos educativos.

### 2. Becarios por Región
**Archivo:** `dataset_becarios_region_2021.xlsx` / `dataset_becarios_region_2021.csv`

- **Registros:** 26 (uno por departamento)
- **Programa:** Beca 18
- **Total becarios:** 37,380
- **Incluye:** Distribución geográfica y porcentajes regionales

**Departamentos con más becarios (2021):**
1. Lima: 5,417 becarios (28.98%)
2. Junín: 1,463 becarios (7.83%)
3. Cusco: 1,042 becarios (5.58%)
4. Piura: 1,060 becarios (5.67%)
5. Ayacucho: 921 becarios (4.93%)

### 3. Tipo de Gestión Institucional
**Archivo:** `dataset_tipo_gestion_2021.xlsx` / `dataset_tipo_gestion_2021.csv`

- **Registros:** 3
- **Total:** 4,996 becarios (Convocatoria 2021)

**Distribución:**
- Asociativa: 3,034 becarios (61%)
- Societaria: 1,644 becarios (33%)
- Pública: 318 becarios (6%)

### 4. Becarios por País (Becas en el Extranjero)
**Archivo:** `dataset_becarios_pais_2021.xlsx` / `dataset_becarios_pais_2021.csv`

- **Registros:** 14 países
- **Total becarios en el extranjero:** 302

**Top 5 países:**
1. España: 44 becarios
2. Estados Unidos: 27 becarios
3. Argentina: 21 becarios
4. Reino Unido: 20 becarios
5. Australia: 15 becarios

### 5. Distribución por Género
**Archivo:** `dataset_genero_2021.xlsx` / `dataset_genero_2021.csv`

- **Registros:** 8 (por tipo de crédito y género)

**Créditos por tipo y género:**
- **Crédito General:** 1,603 mujeres (58%) | 1,184 hombres (42%)
- **Crédito Talento:** 128 mujeres (67%) | 63 hombres (33%)
- **Crédito 18:** 127 mujeres (56%) | 100 hombres (44%)
- **Crédito Continuidad:** 1,348 mujeres (57%) | 1,021 hombres (43%)

### 6. Créditos Educativos por Región
**Archivo:** `dataset_creditos_educativos_2021.xlsx` / `dataset_creditos_educativos_2021.csv`

- **Registros:** 97
- **Total créditos:** 11,148
- **Monto total desembolsado:** S/ 87,650,340.00

**Top 5 departamentos (Crédito General):**
1. Lima: 1,536 créditos - S/ 14,473,084
2. Arequipa: 159 créditos - S/ 956,535
3. Cusco: 147 créditos - S/ 891,392
4. Junín: 108 créditos - S/ 748,397
5. Callao: 99 créditos - S/ 995,624

---

## 📈 Resumen Estadístico 2021

### Totales Generales
- 📚 **Becarios Beca 18:** 37,380
- 💳 **Créditos Educativos:** 11,148
- 💰 **Monto Total Desembolsado:** S/ 87,650,340.00
- 🌍 **Becarios en el Extranjero:** 302
- 🏛️ **Departamentos Cubiertos:** 26 (todo el Perú)
- 🌎 **Países de Destino:** 14

### Distribución Geográfica
- **Lima:** 28.98% de becarios
- **Otras regiones:** 71.02% de becarios

### Migración Estudiantil (Convocatoria 2021)
- **Región Lima de origen:** 1,305 becarios (26%)
- **Otras regiones de origen:** 3,691 becarios (74%)
- **Estudian en Lima:** 3,710 becarios (74%)
- **Estudian en otras regiones:** 1,286 becarios (26%)

---

## 🛠️ Scripts de Extracción

### 1. `scrape_pronabec_2021.py`
Script principal que descarga el PDF y extrae:
- Texto completo de todas las páginas
- 70 tablas identificadas
- Palabras clave relevantes

**Salidas:**
- `Memoria_Pronabec_2021.pdf` - PDF descargado
- `texto_completo_2021.txt` - Texto extraído
- `palabras_clave_encontradas_2021.xlsx` - Menciones de términos clave
- `tablas_relevantes_2021.xlsx` - Tablas con datos útiles
- `todas_las_tablas_2021.xlsx` - Todas las tablas extraídas

### 2. `procesar_datos_dashboard_2021.py`
Script que procesa y estructura los datos extraídos para el dashboard.

**Funciones principales:**
- Limpieza y normalización de datos
- Creación de datasets temáticos
- Generación de dataset maestro consolidado
- Cálculo de estadísticas descriptivas

---

## 🚀 Cómo Usar

### Requisitos
```bash
pip install requests pypdf2 pdfplumber pandas tabula-py camelot-py[cv] openpyxl
```

### Ejecución

1. **Extraer datos del PDF:**
```bash
python scrape_pronabec_2021.py
```

2. **Procesar datos para dashboard:**
```bash
python procesar_datos_dashboard_2021.py
```

3. **Archivos generados:**
Los datasets estarán en formato `.xlsx` y `.csv` listos para importar en herramientas de visualización (Power BI, Tableau, Excel, etc.)

---

## 📊 Uso para Dashboard

### Visualizaciones Recomendadas

1. **Mapa de Calor:** Distribución de becarios por departamento
2. **Gráfico de Barras:** Top 10 regiones con más becarios
3. **Gráfico de Torta:** Distribución por tipo de gestión institucional
4. **Gráfico de Barras Apiladas:** Género por tipo de crédito
5. **Mapa Mundial:** Becarios en el extranjero
6. **Gráfico de Flujo (Sankey):** Migración estudiantil (origen → destino)
7. **KPIs Principales:**
   - Total de becarios
   - Total de créditos
   - Monto desembolsado
   - Cobertura geográfica

### Filtros Sugeridos
- Año (2021 fijo para este dataset)
- Departamento
- Tipo de beca/crédito
- Género
- Tipo de gestión institucional

---

## 📝 Notas Importantes

### Limitaciones de los Datos

1. **Estrato Socioeconómico:** No se encontró información detallada por registro individual en las tablas del PDF
2. **Carreras Específicas:** No están desagregadas por becario en las tablas disponibles
3. **Migración:** Los datos de migración están agregados por convocatoria, no por becario individual
4. **Instituciones:** No se especifican nombres de instituciones educativas por becario

### Datos Disponibles vs. Solicitados

| Campo Solicitado | Estado | Fuente/Alternativa |
|------------------|--------|-------------------|
| ✅ NombreBeca | Disponible | Beca 18, Crédito General, Crédito Talento, etc. |
| ⚠️ Institucion | Parcial | Datos agregados, no por becario |
| ✅ AnioBecariosConfirmados | Disponible | 2021 |
| ✅ Departamento | Disponible | 26 departamentos |
| ⚠️ Carrera | No disponible | Información no desagregada |
| ✅ Modalidad | Disponible | Por tipo de beca/crédito |
| ⚠️ EstratoSocioeconomico | No disponible | No hay datos desagregados |
| ⚠️ Migracion | Parcial | Datos agregados por convocatoria |

### Datos Adicionales Extraídos

Aunque no estaban en el listado original, se extrajeron:
- ✅ Distribución por género
- ✅ Tipo de gestión institucional (Asociativa, Societaria, Pública)
- ✅ Becarios en el extranjero por país
- ✅ Montos desembolsados por región
- ✅ Migración agregada (origen y destino)

---

## 🔧 Mejoras Futuras

1. Integrar datos de otros años (2020, 2022, etc.)
2. Buscar fuentes complementarias con datos más granulares
3. Agregar scraping de carreras desde otra fuente
4. Incorporar datos de estratos socioeconómicos
5. Agregar información de empleabilidad post-beca

---

## 📧 Contacto y Soporte

Para dudas sobre los datos o el proceso de extracción, revisar:
- El código fuente de los scripts
- Los archivos de salida intermedios (tablas extraídas)
- La memoria original del Pronabec 2021

---

**Última actualización:** Noviembre 2025  
**Fuente de datos:** PRONABEC - Gobierno del Perú  
**Año de datos:** 2021
