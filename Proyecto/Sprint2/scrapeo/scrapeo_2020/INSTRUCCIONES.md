# Proyecto de Web Scraping - Pronabec 2020

## 📋 Resumen Ejecutivo

Se ha realizado con éxito el web scraping del documento PDF "Memoria Anual del Pronabec 2020", extrayendo datos estructurados sobre becas y créditos educativos del año 2020.

## ✅ Datos Extraídos

### Campos Principales Obtenidos:
- ✅ **NombreBeca**: Nombre del programa de becas
- ✅ **Institucion**: Tipo de institución educativa (Universidad, IST, ISP)
- ✅ **AnioBecariosConfirmados**: Año 2020
- ✅ **Departamento**: Departamento de origen/ubicación
- ✅ **Carrera**: Área de estudio o carrera profesional
- ✅ **Modalidad**: Categoría específica de la beca
- ⚠️ **Estrato socioeconómico**: No disponible a nivel individual en el documento
- ⚠️ **Becas según migración**: No disponible a nivel individual en el documento

### Datos Adicionales Extraídos:
- Becarios nuevos vs continuadores
- Becas de posgrado por país de destino
- Tipo de programa (Maestría, Doctorado)
- Créditos educativos con montos desembolsados

## 📊 Estadísticas Generales 2020

### Becarios Totales: **22,667**
- **Beca 18**: 20,846 becarios (91.9%)
- **Becas de Posgrado Internacional**: 457 becarios (2.0%)
- **Otras modalidades**: 1,364 becarios (6.0%)

### Top 5 Departamentos (Beca 18):
1. Lima: 5,199 becarios (24.9%)
2. Junín: 1,652 becarios (7.9%)
3. Piura: 1,239 becarios (5.9%)
4. Cusco: 1,093 becarios (5.2%)
5. Huancavelica: 1,056 becarios (5.1%)

### Top 3 Áreas de Estudio:
1. Ingeniería, Industria y Construcción: 11,126 becarios (53.4%)
2. Ciencias Sociales, Comerciales y Derecho: 5,484 becarios (26.3%)
3. Ciencias de la Salud: 1,487 becarios (7.1%)

### Créditos Educativos:
- **Total de créditos otorgados**: 5,444
- **Monto total desembolsado**: S/ 11,990,218.00

## 📁 Archivos Generados

### Datasets CSV y Excel (14 archivos):
1. `beca18_por_departamento_2020.csv/.xlsx` - 25 registros
2. `beca18_por_carrera_2020.csv/.xlsx` - 8 registros
3. `beca18_por_institucion_2020.csv/.xlsx` - 3 registros
4. `beca_posgrado_por_pais_2020.csv/.xlsx` - 18 registros
5. `beca_posgrado_por_programa_2020.csv/.xlsx` - 2 registros
6. `becarios_continuadores_por_modalidad_2020.csv/.xlsx` - 7 registros
7. `creditos_educativos_2020.csv/.xlsx` - 4 registros
8. `datos_becas_consolidado_2020.csv/.xlsx` - 25 registros

### Archivos de Soporte:
- `tablas_extraidas.json` - 118 tablas extraídas del PDF
- `texto_extraido.json` - Texto completo de 115 páginas
- `resumen_estadistico_2020.txt` - Resumen estadístico

### Scripts Python:
- `scraper_pronabec_2020.py` - Script principal de scraping
- `parser_datos_becas.py` - Parser de datos estructurados
- `analisis_datos.py` - Análisis y estadísticas

### Documentación:
- `README.md` - Instrucciones de uso
- `DICCIONARIO_DATOS.md` - Diccionario de datos completo
- `INSTRUCCIONES.md` - Este archivo
- `requirements.txt` - Dependencias del proyecto

## 🚀 Uso de los Datos

### Para Dashboard:
Los archivos CSV/Excel están listos para ser importados en herramientas de visualización:
- Power BI
- Tableau
- Python (Matplotlib, Plotly, Streamlit)
- Excel Dashboards

### Visualizaciones Recomendadas:
1. **Mapa de calor**: Distribución geográfica de becarios por departamento
2. **Gráfico de barras**: Top áreas de estudio
3. **Gráfico circular**: Distribución por tipo de institución
4. **Mapa mundial**: Becas de posgrado por país
5. **Gráfico de líneas**: Tendencias de becarios nuevos vs continuadores
6. **Tabla dinámica**: Créditos educativos por modalidad

## 🔧 Instalación y Ejecución

### Requisitos:
```bash
pip install -r requirements.txt
```

### Ejecutar scraping completo:
```bash
python scraper_pronabec_2020.py
python parser_datos_becas.py
python analisis_datos.py
```

## ⚠️ Limitaciones

### Datos No Disponibles:
1. **Estrato socioeconómico individual**: El documento solo contiene datos agregados
2. **Migración individual**: El documento menciona migración pero sin datos desagregados
3. **Nombres de becarios**: Por privacidad, no están disponibles
4. **Instituciones específicas**: Solo se menciona el tipo (Universidad, IST, ISP)

### Recomendaciones:
- Para datos de estrato socioeconómico y migración individual, consultar bases de datos internas del Pronabec
- El documento contiene referencias a estos datos pero no los desglosa por becario

## 📈 Insights Principales

1. **Lima concentra el 25% de los becarios** de Beca 18
2. **Ingeniería es la carrera más demandada** (53% de becarios)
3. **79% de becarios estudian en universidades**
4. **España es el destino preferido** para posgrados (35% del total)
5. **81.8% de becas de posgrado son maestrías**

## 🎯 Conclusiones

El proyecto ha extraído exitosamente datos estructurados y listos para análisis de dashboard sobre:
- 22,667 becarios en diferentes modalidades
- 25 departamentos del Perú
- 8 áreas de estudio principales
- 18 países de destino para posgrados
- S/ 11.9 millones en créditos educativos

Los datos están organizados en múltiples archivos CSV/Excel para facilitar su uso en diferentes contextos de análisis y visualización.

---

**Fuente**: Memoria Anual del Pronabec 2020  
**Fecha de extracción**: Noviembre 2025  
**Año de datos**: 2020
