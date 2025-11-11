# 🚀 GUÍA RÁPIDA DE USO - WEB SCRAPING PRONABEC 2021

## ✅ ¿Qué se ha realizado?

Se ha extraído exitosamente la información de la **Memoria Anual del Pronabec 2021** y se han creado datasets estructurados listos para usar en un dashboard de visualización.

---

## 📦 Archivos Generados

### 🎯 Datasets para Dashboard (Formato Excel y CSV)

1. **`dataset_maestro_pronabec_2021`** (123 registros)
   - Dataset consolidado con todos los datos
   - Incluye becas y créditos educativos
   - Listo para importar directamente

2. **`dataset_becarios_region_2021`** (26 registros)
   - Becarios Beca 18 por departamento
   - Total: 37,380 becarios
   - Con porcentajes regionales

3. **`dataset_tipo_gestion_2021`** (3 registros)
   - Distribución por tipo de gestión institucional
   - Asociativa, Societaria, Pública

4. **`dataset_becarios_pais_2021`** (14 registros)
   - Becarios en el extranjero por país
   - Total: 302 becarios internacionales

5. **`dataset_genero_2021`** (8 registros)
   - Distribución de créditos por género
   - Por tipo de crédito educativo

6. **`dataset_creditos_educativos_2021`** (97 registros)
   - Créditos educativos por región
   - Incluye montos desembolsados

### 📊 Reportes y Visualizaciones

- **`reporte_pronabec_2021.html`** - Reporte interactivo HTML
- **`reporte_visual_pronabec_2021.png`** - Gráficos consolidados
- **`README.md`** - Documentación completa
- **`GUIA_RAPIDA.md`** - Esta guía

### 🔧 Scripts de Procesamiento

- **`scrape_pronabec_2021.py`** - Extracción del PDF
- **`procesar_datos_dashboard_2021.py`** - Procesamiento de datos
- **`generar_reporte_visual.py`** - Generación de visualizaciones
- **`mostrar_resumen.py`** - Resumen de datasets

---

## 📊 Datos Extraídos - Resumen

| Indicador | Valor |
|-----------|-------|
| 📚 Becarios Beca 18 | 37,380 |
| 💳 Créditos Educativos | 11,148 |
| 💰 Monto Desembolsado | S/ 87,650,340 |
| 🌍 Becarios al Extranjero | 302 |
| 🏛️ Departamentos | 26 (Todo Perú) |
| 🌎 Países Destino | 14 |

---

## 🎨 Cómo Usar en tu Dashboard

### Opción 1: Power BI

1. Abrir Power BI Desktop
2. **Obtener datos** → **Excel** o **Texto/CSV**
3. Seleccionar el archivo que necesites (ej: `dataset_maestro_pronabec_2021.xlsx`)
4. Cargar los datos
5. Crear visualizaciones usando los campos:
   - `Departamento` → Mapa geográfico
   - `CantidadBecarios` → KPI y gráficos de barras
   - `TipoBeneficio` → Filtro (Beca/Crédito)
   - `NombreBeca` → Leyenda y filtro

### Opción 2: Tableau

1. Abrir Tableau Desktop
2. **Conectar** → **Archivo de Excel** o **Archivo de texto**
3. Seleccionar `dataset_maestro_pronabec_2021.xlsx`
4. Arrastrar campos a la vista:
   - Filas: `Departamento`
   - Columnas: `CantidadBecarios`
   - Color: `TipoBeneficio`
   - Filtros: `NombreBeca`, año

### Opción 3: Excel

1. Abrir `dataset_maestro_pronabec_2021.xlsx`
2. Usar **Insertar** → **Tablas dinámicas**
3. Crear gráficos desde los datos
4. Usar **Insertar** → **Mapas** para visualización geográfica

### Opción 4: Python (Plotly, Matplotlib, Seaborn)

```python
import pandas as pd
import plotly.express as px

# Cargar datos
df = pd.read_csv('dataset_maestro_pronabec_2021.csv')

# Crear mapa de calor por región
fig = px.choropleth(
    df[df['TipoBeneficio'] == 'Beca'],
    locations='Departamento',
    locationmode='country names',
    color='CantidadBecarios',
    title='Distribución de Becarios por Región - 2021'
)
fig.show()
```

---

## 📈 Visualizaciones Recomendadas

### 1. **Mapa de Calor Geográfico**
- **Dataset:** `dataset_becarios_region_2021`
- **Campo clave:** `Departamento`, `CantidadBecarios`
- **Tipo:** Mapa coroplético de Perú

### 2. **Top 10 Departamentos**
- **Dataset:** `dataset_becarios_region_2021`
- **Tipo:** Gráfico de barras horizontal
- **Ordenar por:** `CantidadBecarios` descendente

### 3. **Distribución por Tipo de Gestión**
- **Dataset:** `dataset_tipo_gestion_2021`
- **Tipo:** Gráfico de dona o torta
- **Mostrar:** Porcentajes

### 4. **Género en Créditos**
- **Dataset:** `dataset_genero_2021`
- **Tipo:** Gráfico de barras apiladas
- **Eje X:** Tipo de crédito
- **Eje Y:** Cantidad
- **Segmentar por:** Género

### 5. **Becarios Internacionales**
- **Dataset:** `dataset_becarios_pais_2021`
- **Tipo:** Gráfico de barras horizontal o mapa mundial
- **Top 10 países**

### 6. **Créditos y Montos por Región**
- **Dataset:** `dataset_creditos_educativos_2021`
- **Tipo:** Gráfico de dispersión o burbujas
- **Eje X:** `CantidadCreditos`
- **Eje Y:** `MontoDesembolsado`
- **Tamaño burbuja:** Monto

### 7. **KPIs Principales** (Tarjetas)
- Total Becarios
- Total Créditos
- Monto Desembolsado
- Cobertura Departamental

### 8. **Filtros Recomendados**
- Año (2021 fijo)
- Departamento (multi-selección)
- Tipo de Beca/Crédito
- Tipo de Beneficio (Beca/Crédito)

---

## 🗂️ Estructura de los Campos

### Campos Principales del Dataset Maestro

| Campo | Tipo | Descripción | Ejemplo |
|-------|------|-------------|---------|
| **NombreBeca** | Texto | Nombre del programa | "Beca 18", "Crédito General" |
| **Institucion** | Texto | Institución educativa | "Varias", "Diversas" |
| **AnioBecariosConfirmados** | Número | Año | 2021 |
| **Departamento** | Texto | Región del Perú | "Lima", "Cusco", "Arequipa" |
| **Carrera** | Texto | Carrera de estudio | "Varias", "Diversas" |
| **Modalidad** | Texto | Tipo de modalidad | "General", "Crédito Educativo" |
| **EstratoSocioeconomico** | Texto | Nivel socioeconómico | "No especificado" |
| **Migracion** | Texto | Migración estudiantil | "No especificado" |
| **CantidadBecarios** | Número | Cantidad de beneficiarios | 457, 1536, etc. |
| **TipoBeneficio** | Texto | Beca o Crédito | "Beca", "Crédito" |
| **MontoDesembolsado** | Número | Monto en soles | 14473084.0 |

---

## ⚠️ Limitaciones Conocidas

### Datos NO Disponibles en el PDF Original:

1. **Carreras específicas por becario** - Solo datos agregados
2. **Instituciones educativas individuales** - No desagregado
3. **Estrato socioeconómico por becario** - No disponible
4. **Migración detallada individual** - Solo datos agregados por convocatoria

### Datos Disponibles y Validados:

✅ Becarios por departamento (26 regiones)
✅ Tipo de gestión institucional
✅ Género en créditos educativos
✅ Becarios en el extranjero por país
✅ Créditos educativos por región con montos
✅ Distribución geográfica nacional

---

## 🔄 Actualización de Datos

Si necesitas datos de otros años, debes:

1. Obtener la URL del PDF de la memoria anual correspondiente
2. Modificar la variable `PDF_URL` en `scrape_pronabec_2021.py`
3. Ejecutar nuevamente los scripts
4. Ajustar el procesamiento según la estructura del nuevo PDF

---

## 💡 Tips y Mejores Prácticas

### Para Dashboard Efectivo:

1. **Usa el dataset maestro** como fuente principal
2. **Filtra por TipoBeneficio** para separar Becas de Créditos
3. **Crea relaciones** entre departamentos para análisis comparativos
4. **Agrega cálculos personalizados:**
   - Tasa de crecimiento anual (si tienes otros años)
   - Porcentaje por región
   - Promedio de monto por crédito

### Para Mejor Visualización:

1. **Colores sugeridos:**
   - Becas: Azul/Verde
   - Créditos: Naranja/Rojo
   - Mujeres: Rosa/Morado
   - Hombres: Azul/Celeste

2. **Tipografía:**
   - Títulos: 16-20pt, negrita
   - Datos: 12-14pt
   - Anotaciones: 10pt

3. **Layout:**
   - KPIs principales arriba
   - Mapa geográfico central
   - Gráficos complementarios en los lados
   - Filtros en panel lateral o arriba

---

## 📞 Soporte

### Archivos de Referencia:
- `README.md` - Documentación técnica completa
- `reporte_pronabec_2021.html` - Vista previa de datos
- Scripts `.py` - Código fuente para modificaciones

### Verificación de Datos:
- Ejecutar `mostrar_resumen.py` para ver estadísticas actuales
- Revisar `texto_completo_2021.txt` para información textual del PDF
- Consultar `todas_las_tablas_2021.xlsx` para todas las tablas extraídas

---

## ✅ Checklist de Uso

- [ ] He revisado el `reporte_pronabec_2021.html` en mi navegador
- [ ] He abierto el `dataset_maestro_pronabec_2021.xlsx` en Excel
- [ ] He identificado qué visualizaciones necesito
- [ ] He importado los datos en mi herramienta de dashboard
- [ ] He creado al menos 3 visualizaciones básicas
- [ ] He agregado filtros interactivos
- [ ] He validado que los totales coinciden con el resumen

---

## 🎯 Próximos Pasos

1. **Importar datos** en tu herramienta preferida
2. **Crear visualizaciones** según las recomendaciones
3. **Publicar dashboard** para stakeholders
4. **Documentar insights** encontrados en los datos

---

**¡Éxito con tu Dashboard! 🚀**

*Última actualización: Noviembre 2025*
*Fuente: PRONABEC - Gobierno del Perú*
