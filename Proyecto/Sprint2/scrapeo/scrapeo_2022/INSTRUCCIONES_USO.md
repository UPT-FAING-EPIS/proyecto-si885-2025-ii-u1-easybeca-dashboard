# 🚀 GUÍA DE USO - Web Scraping PRONABEC 2022

## 📁 Estructura del Proyecto

```
scrapeo_2022/
│
├── 📄 scraper_pronabec_2022.py          # Script principal de web scraping
├── 📄 procesar_datos_dashboard.py       # Script de procesamiento de datos
├── 📄 generar_reporte_visual.py         # Generador de reporte HTML
├── 📄 RESUMEN_EJECUTIVO.py              # Resumen del proyecto
├── 📄 README_DATOS_EXTRAIDOS.md         # Documentación técnica completa
├── 📄 INSTRUCCIONES_USO.md              # Este archivo
│
└── 📁 datos_extraidos/
    ├── 📊 pronabec_2022_datos.xlsx      # Excel consolidado
    ├── 📊 REPORTE_VISUAL_2022.html      # Visualización interactiva
    ├── 📊 REPORTE_CONSOLIDADO_2022.csv  # Resumen de datasets
    │
    ├── 📈 becarios_por_departamento_2022.csv
    ├── 📈 becas_por_tipo_modalidad_2022.csv
    ├── 📈 metas_otorgamiento_becas_2022.csv
    ├── 📈 becas_internacionales_pais_2022.csv
    ├── 📈 creditos_educativos_2022.csv
    │
    └── 📂 [10 tablas adicionales extraídas]
```

---

## 🎯 Inicio Rápido

### Opción 1: Ver los Datos Ya Extraídos (RECOMENDADO)

Los datos ya han sido extraídos y procesados. Puedes acceder directamente a:

1. **Reporte Visual Interactivo**
   ```
   Abrir: datos_extraidos/REPORTE_VISUAL_2022.html
   ```
   - Abre este archivo en tu navegador
   - Contiene todas las tablas visualizadas
   - Estadísticas principales
   - Navegación fácil

2. **Excel Consolidado**
   ```
   Abrir: datos_extraidos/pronabec_2022_datos.xlsx
   ```
   - Múltiples hojas con diferentes datasets
   - Listo para análisis en Excel

3. **CSVs Individuales**
   ```
   Ubicación: datos_extraidos/*.csv
   ```
   - Listos para importar a Power BI, Tableau, Python, R, etc.

---

## 🔄 Volver a Ejecutar el Scraping (Si es necesario)

### Paso 1: Preparar el Entorno

```powershell
# Activar el entorno virtual (si no está activo)
.\.venv\Scripts\Activate.ps1

# Verificar que las dependencias estén instaladas
pip list | Select-String "pdfplumber|pandas|requests|openpyxl"
```

### Paso 2: Ejecutar el Scraper

```powershell
# Ejecutar el script de scraping
python scraper_pronabec_2022.py
```

**Tiempo estimado:** 1-2 minutos
**Salida:** Carpeta `datos_extraidos/` con tablas extraídas

### Paso 3: Procesar los Datos

```powershell
# Procesar y limpiar los datos
python procesar_datos_dashboard.py
```

**Salida:** 5 CSVs limpios listos para dashboard

### Paso 4: Generar Reporte Visual

```powershell
# Generar reporte HTML interactivo
python generar_reporte_visual.py
```

**Salida:** `REPORTE_VISUAL_2022.html`

### Paso 5: Ver Resumen

```powershell
# Ver resumen ejecutivo
python RESUMEN_EJECUTIVO.py
```

---

## 📊 Usar los Datos en tu Dashboard

### Power BI

1. Abrir Power BI Desktop
2. **Obtener datos** → **Texto/CSV**
3. Seleccionar uno de los CSVs:
   - `becarios_por_departamento_2022.csv`
   - `becas_por_tipo_modalidad_2022.csv`
   - etc.
4. Importar y comenzar a crear visualizaciones

**Visualizaciones sugeridas:**
- Mapa: Becarios por departamento
- Gráfico de barras: Tipos de becas
- KPI: Cumplimiento de metas
- Mapa mundial: Becas internacionales

### Tableau

1. Abrir Tableau Desktop
2. **Conectar** → **Archivo de texto**
3. Seleccionar los CSVs
4. Unir tablas si es necesario
5. Crear dashboard

### Python (Pandas, Plotly, Dash)

```python
import pandas as pd
import plotly.express as px

# Leer datos
df_dept = pd.read_csv('datos_extraidos/becarios_por_departamento_2022.csv')
df_becas = pd.read_csv('datos_extraidos/becas_por_tipo_modalidad_2022.csv')

# Crear visualización
fig = px.bar(df_becas, x='NombreBeca', y='TotalBecariosActivos',
             color='TipoBeca', title='Becarios Activos por Programa')
fig.show()
```

### Excel

1. Abrir Excel
2. **Datos** → **Obtener datos** → **Desde archivo** → **Desde CSV**
3. Seleccionar CSV
4. Importar y analizar con tablas dinámicas

---

## 📈 Análisis Sugeridos

### 1. Análisis Geográfico

**Dataset:** `becarios_por_departamento_2022.csv`

**Preguntas a responder:**
- ¿Qué departamentos tienen más becarios?
- ¿Dónde hay mayor tasa de asistencia?
- ¿Qué regiones tienen más inasistencias?

**Visualizaciones:**
- Mapa de calor del Perú
- Gráfico de barras por departamento
- Tabla comparativa

### 2. Análisis de Programas

**Dataset:** `becas_por_tipo_modalidad_2022.csv`

**Preguntas a responder:**
- ¿Cuáles son los programas más populares?
- ¿Cuántos becarios son continuadores vs. nuevos?
- ¿Qué tipo de beca tiene más becarios activos?

**Visualizaciones:**
- Gráfico de barras apiladas
- Gráfico de pastel (distribución por tipo)
- Tabla de ranking

### 3. Cumplimiento de Metas

**Dataset:** `metas_otorgamiento_becas_2022.csv`

**Preguntas a responder:**
- ¿Qué programas cumplieron sus metas?
- ¿Cuál fue el porcentaje promedio de cumplimiento?
- ¿Qué programa tuvo mejor desempeño?

**Visualizaciones:**
- Indicadores KPI
- Gráfico de progreso (gauge chart)
- Tabla comparativa meta vs. real

### 4. Análisis Internacional

**Dataset:** `becas_internacionales_pais_2022.csv`

**Preguntas a responder:**
- ¿Cuáles son los países destino preferidos?
- ¿Hay más becas de maestría o doctorado?
- ¿Qué continente recibe más becarios?

**Visualizaciones:**
- Mapa mundial
- Gráfico de barras por país
- Distribución maestría vs. doctorado

### 5. Análisis Financiero

**Dataset:** `creditos_educativos_2022.csv`

**Preguntas a responder:**
- ¿Qué modalidad de crédito tiene más beneficiarios?
- ¿Cómo se distribuye el presupuesto?
- ¿Cuál es el monto promedio por beneficiario?

**Visualizaciones:**
- Gráfico de dona (participación %)
- Gráfico de barras (montos)
- Tabla financiera

---

## 🔧 Solución de Problemas

### Problema: "ModuleNotFoundError: No module named 'pdfplumber'"

**Solución:**
```powershell
pip install pdfplumber pandas requests openpyxl
```

### Problema: "PermissionError" al guardar archivos

**Solución:**
- Cerrar Excel si tiene abierto el archivo
- Verificar permisos de escritura en la carpeta
- Ejecutar con privilegios de administrador

### Problema: PDF no se descarga

**Solución:**
- Verificar conexión a internet
- Intentar descargar manualmente desde el navegador
- Verificar que la URL sea correcta

### Problema: Datos con caracteres extraños (Ã, Ñ)

**Solución:**
- Los CSVs están guardados con encoding UTF-8-SIG
- Al abrir en Excel, usar "Importar desde CSV" y seleccionar UTF-8
- En Python: `pd.read_csv('archivo.csv', encoding='utf-8-sig')`

---

## 📖 Documentación Adicional

### Archivos de Referencia

1. **README_DATOS_EXTRAIDOS.md**
   - Descripción detallada de cada dataset
   - Campos y significado
   - Casos de uso

2. **REPORTE_CONSOLIDADO_2022.csv**
   - Resumen de todos los datasets
   - Número de registros
   - Utilidad para dashboard

3. **REPORTE_VISUAL_2022.html**
   - Visualización interactiva
   - Todas las tablas en un solo lugar

---

## 💡 Tips y Mejores Prácticas

### Para Dashboard

1. **Usa filtros interactivos**
   - Por departamento
   - Por tipo de beca
   - Por año (si agregas más años)

2. **Crea KPIs destacados**
   - Total de becarios
   - % Cumplimiento de metas
   - Tasa de asistencia
   - Becarios internacionales

3. **Agrupa visualizaciones**
   - Página 1: Resumen ejecutivo
   - Página 2: Análisis geográfico
   - Página 3: Análisis de programas
   - Página 4: Análisis financiero

### Para Análisis

1. **Cruza datos entre datasets**
   - Relaciona departamentos con tipos de beca
   - Compara metas vs. distribución geográfica

2. **Calcula métricas adicionales**
   - Tasa de inasistencia
   - Promedio de becarios por departamento
   - Crecimiento vs. años anteriores (si tienes datos)

3. **Identifica insights**
   - Departamentos con baja asistencia
   - Programas sub-ejecutados
   - Tendencias de migración

---

## 🎨 Paleta de Colores Sugerida (para Dashboard)

```
Primarios:
- Azul Principal: #1e3c72
- Azul Acento: #2a5298
- Morado: #667eea

Secundarios:
- Verde (éxito): #10b981
- Amarillo (advertencia): #f59e0b
- Rojo (alerta): #ef4444

Grises:
- Fondo: #f8f9fa
- Texto: #333333
- Bordes: #dee2e6
```

---

## 📞 Soporte

Si encuentras problemas o tienes preguntas:

1. Revisa la documentación en `README_DATOS_EXTRAIDOS.md`
2. Verifica los logs de errores en la terminal
3. Asegúrate de tener todas las dependencias instaladas
4. Revisa que los archivos CSV estén en la carpeta correcta

---

## ✅ Checklist de Implementación

### Antes de crear el dashboard:

- [ ] He revisado todos los CSVs generados
- [ ] He abierto el reporte HTML para entender los datos
- [ ] He leído la documentación técnica
- [ ] Entiendo qué campos están disponibles y cuáles no
- [ ] He identificado las visualizaciones que necesito

### Durante la creación:

- [ ] He importado los datos correctamente
- [ ] He verificado que no haya errores de encoding
- [ ] He creado las relaciones entre tablas (si aplica)
- [ ] He agregado filtros interactivos
- [ ] He validado que los números sean correctos

### Antes de publicar:

- [ ] He probado todas las funcionalidades
- [ ] He verificado que las visualizaciones sean claras
- [ ] He agregado títulos y descripciones
- [ ] He documentado las fuentes de datos
- [ ] He incluido fecha de actualización

---

## 🎯 Próximos Pasos Recomendados

1. **Explorar los datos**
   - Abrir `REPORTE_VISUAL_2022.html`
   - Revisar todos los CSVs
   - Identificar insights interesantes

2. **Diseñar el dashboard**
   - Bosquejar layout
   - Definir visualizaciones
   - Seleccionar colores y estilo

3. **Implementar**
   - Importar datos a tu herramienta
   - Crear visualizaciones
   - Agregar interactividad

4. **Iterar**
   - Probar con usuarios
   - Ajustar según feedback
   - Agregar más análisis si es necesario

---

¡Éxito con tu dashboard! 🚀📊

---

**Última actualización:** Noviembre 2025  
**Versión:** 1.0  
**Proyecto:** EasyBeca Dashboard - Sprint 2
