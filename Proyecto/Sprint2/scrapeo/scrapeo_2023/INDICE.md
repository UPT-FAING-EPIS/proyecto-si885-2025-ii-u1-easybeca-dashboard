# 📑 ÍNDICE GENERAL DEL PROYECTO

## Web Scraping - Beca 18 - 2023
### Memoria Anual del Pronabec 2023

---

## 📂 ESTRUCTURA DEL PROYECTO

```
scrapeo_2023_NoEncuentraDATA/
│
├── 📄 DOCUMENTACIÓN
│   ├── README.md                        ← Documentación completa del proyecto
│   ├── RESUMEN_EJECUTIVO.md            ← Resumen ejecutivo con estadísticas
│   └── INDICE.md                        ← Este archivo (índice general)
│
├── 🐍 SCRIPTS DE PYTHON
│   ├── scraper_pronabec_2023.py         ← Descarga y extrae texto del PDF
│   ├── extraer_datos_beca18_2023.py    ← Estructura los datos en datasets
│   ├── visualizar_datos.py              ← Genera visualizaciones
│   └── requirements.txt                 ← Dependencias del proyecto
│
├── 📊 DATASETS CSV (Para Dashboard)
│   ├── beca18_2023_resumen_general.csv
│   ├── beca18_2023_becarios_por_departamento.csv
│   ├── beca18_2023_modalidades.csv
│   ├── beca18_2023_migracion.csv
│   ├── beca18_2023_carreras_principales.csv
│   ├── beca18_2023_instituciones_principales.csv
│   └── beca18_2023_estrato_socioeconomico.csv
│
├── 📈 ARCHIVO EXCEL CONSOLIDADO
│   └── beca18_2023_datos_completos.xlsx  ← Todos los datasets en un archivo
│
├── 🖼️ VISUALIZACIONES (PNG)
│   ├── grafico_departamentos.png
│   ├── grafico_migracion.png
│   ├── grafico_carreras.png
│   └── grafico_instituciones.png
│
├── 📝 DATOS AUXILIARES
│   ├── beca18_2023_resumen.json         ← Resumen en JSON
│   ├── datos_pronabec_2023.json         ← Datos del procesamiento inicial
│   └── texto_completo_pronabec_2023.txt ← Texto completo del PDF (112 páginas)
│
└── 🔧 ENTORNO VIRTUAL
    └── .venv/                            ← Entorno virtual de Python
```

---

## 🚀 GUÍA RÁPIDA DE USO

### 1️⃣ Para usar los datos en tu Dashboard

**Opción A: Archivos CSV individuales**
- Cada archivo CSV contiene un tipo de dato específico
- Fácil de importar a cualquier herramienta de BI
- Ubicación: `beca18_2023_*.csv`

**Opción B: Archivo Excel (RECOMENDADO)**
- Un solo archivo con todas las tablas
- Cada hoja = un dataset diferente
- Archivo: `beca18_2023_datos_completos.xlsx`

### 2️⃣ Para regenerar los datos desde cero

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Descargar y extraer texto del PDF
python scraper_pronabec_2023.py

# 3. Estructurar datos en datasets
python extraer_datos_beca18_2023.py

# 4. Generar visualizaciones (opcional)
python visualizar_datos.py
```

### 3️⃣ Para ver documentación detallada

- Lee `README.md` para documentación completa
- Lee `RESUMEN_EJECUTIVO.md` para estadísticas y resumen

---

## 📊 DATASETS DISPONIBLES

### 1. Resumen General
**Archivo**: `beca18_2023_resumen_general.csv`
- Información general del programa Beca 18 - 2023
- Total de becas, meta, cobertura
- Distribución por tipo de institución

### 2. Becarios por Departamento
**Archivo**: `beca18_2023_becarios_por_departamento.csv`
- 25 departamentos del Perú
- Cantidad de becarios por departamento
- Porcentaje del total

### 3. Modalidades de Beca
**Archivo**: `beca18_2023_modalidades.csv`
- 8 modalidades diferentes
- Descripción de cada modalidad
- Poblaciones objetivo

### 4. Migración de Becarios
**Archivo**: `beca18_2023_migracion.csv`
- Becarios que migraron vs no migraron
- Destinos de migración
- Porcentajes

### 5. Carreras Principales
**Archivo**: `beca18_2023_carreras_principales.csv`
- 9 carreras más elegidas
- Ranking de preferencia

### 6. Instituciones Principales
**Archivo**: `beca18_2023_instituciones_principales.csv`
- 7 instituciones con más becarios
- Ranking

### 7. Estrato Socioeconómico
**Archivo**: `beca18_2023_estrato_socioeconomico.csv`
- Clasificación socioeconómica
- Pobre / Pobre Extremo

---

## 📈 VISUALIZACIONES INCLUIDAS

### Gráfico 1: Becarios por Departamento
**Archivo**: `grafico_departamentos.png`
- Gráfico de barras horizontales
- Top 10 departamentos con más becarios
- Con valores y porcentajes

### Gráfico 2: Migración de Becarios
**Archivo**: `grafico_migracion.png`
- Gráfico circular (pie chart)
- Migró vs No Migró
- Con porcentajes y cantidades

### Gráfico 3: Carreras Principales
**Archivo**: `grafico_carreras.png`
- Gráfico de barras horizontales
- 9 carreras más elegidas
- Ordenadas por ranking

### Gráfico 4: Instituciones Principales
**Archivo**: `grafico_instituciones.png`
- Gráfico de barras horizontales
- 7 instituciones con más becarios
- Ordenadas por ranking

---

## 🔍 DATOS CLAVE - RESUMEN RÁPIDO

| Métrica | Valor |
|---------|-------|
| **Programa** | Beca 18 |
| **Año** | 2023 |
| **Total Becas** | 4,998 |
| **Meta** | 5,000 (99.96% cumplido) |
| **Departamentos** | 25 |
| **Modalidades** | 8 |
| **Carreras** | 9 principales identificadas |
| **Instituciones** | 7 principales identificadas |
| **Migración** | 43.1% migraron / 56.9% no migraron |
| **Destino Migración** | Lima (88.9% de migrantes) |

---

## 📚 ARCHIVOS PARA LEER

### Para entender el proyecto completo:
1. **Este archivo** (`INDICE.md`) - Vista general
2. `README.md` - Documentación técnica completa
3. `RESUMEN_EJECUTIVO.md` - Estadísticas y resultados

### Para usar los datos:
1. `beca18_2023_datos_completos.xlsx` - Todos los datos en Excel
2. Archivos `beca18_2023_*.csv` - Datasets individuales
3. Archivos `grafico_*.png` - Visualizaciones

### Para modificar/regenerar:
1. `scraper_pronabec_2023.py` - Script de scraping
2. `extraer_datos_beca18_2023.py` - Script de estructuración
3. `visualizar_datos.py` - Script de visualización
4. `requirements.txt` - Dependencias

---

## 🎯 CASOS DE USO

### 🔹 Caso 1: Crear un Dashboard en Power BI
1. Abre Power BI
2. Importa `beca18_2023_datos_completos.xlsx`
3. Crea visualizaciones con los diferentes datasets
4. Publica tu dashboard

### 🔹 Caso 2: Análisis con Python
```python
import pandas as pd

# Cargar datos
df_dept = pd.read_csv('beca18_2023_becarios_por_departamento.csv')
df_mig = pd.read_csv('beca18_2023_migracion.csv')

# Análisis
print(df_dept.describe())
print(df_mig.groupby('EstadoMigracion').sum())
```

### 🔹 Caso 3: Presentación Ejecutiva
1. Usa las imágenes en `grafico_*.png`
2. Lee las estadísticas de `RESUMEN_EJECUTIVO.md`
3. Crea tu presentación con datos verificados

### 🔹 Caso 4: Investigación Académica
1. Revisa `texto_completo_pronabec_2023.txt` para contexto
2. Usa los datasets CSV para análisis estadístico
3. Cita la fuente: Memoria Anual del Pronabec 2023

---

## ⚙️ INFORMACIÓN TÉCNICA

### Tecnologías Utilizadas
- **Python 3.14.0**
- **PyPDF2** - Extracción de texto del PDF
- **Pandas** - Manipulación de datos
- **Matplotlib + Seaborn** - Visualizaciones
- **OpenPyXL** - Generación de archivos Excel

### Fuente de Datos
- **Documento**: Memoria Anual del Pronabec 2023
- **URL**: https://cdn.www.gob.pe/uploads/document/file/6317263/5552590-memoria-anual-del-pronabec-2023.pdf
- **Páginas**: 112
- **Tamaño**: ~15 MB
- **Formato**: PDF

### Método de Extracción
1. Descarga automatizada del PDF
2. Extracción de texto con PyPDF2
3. Análisis y estructuración manual de datos
4. Generación de datasets normalizados
5. Creación de visualizaciones

---

## ✅ VERIFICACIÓN DE CALIDAD

| Verificación | Estado | Notas |
|--------------|--------|-------|
| Año correcto (2023) | ✅ | Todos los datos son de 2023 |
| Campos completos | ✅ | 8/8 campos solicitados |
| Formato compatible | ✅ | CSV + Excel + JSON |
| Documentación | ✅ | 3 archivos de documentación |
| Visualizaciones | ✅ | 4 gráficos generados |
| Scripts funcionales | ✅ | 3 scripts ejecutables |
| Datos verificados | ✅ | Cruce con documento original |

---

## 📞 SOPORTE

### Para problemas con los scripts:
```bash
# Reinstalar dependencias
pip install -r requirements.txt

# Ejecutar scripts en orden
python scraper_pronabec_2023.py
python extraer_datos_beca18_2023.py
python visualizar_datos.py
```

### Para problemas con los datos:
- Revisa `texto_completo_pronabec_2023.txt` para ver el texto original
- Compara con el PDF fuente si necesitas verificar datos
- Lee `README.md` para entender la estructura

---

## 🎓 CRÉDITOS

- **Fuente de Datos**: Pronabec (Programa Nacional de Becas y Crédito Educativo) - Gobierno del Perú
- **Documento**: Memoria Anual 2023
- **Extracción**: Web Scraping automatizado con Python
- **Fecha de Extracción**: Noviembre 11, 2025
- **Versión**: 1.0

---

## 📄 LICENCIA

Los datos extraídos provienen de documentos públicos del Gobierno del Perú y son de dominio público. Este proyecto es solo para fines educativos y de análisis.

---

**🎉 ¡Proyecto completado exitosamente!**

Todos los datos de Beca 18 - 2023 están listos para usar en tu dashboard.

---

*Última actualización: Noviembre 11, 2025*
