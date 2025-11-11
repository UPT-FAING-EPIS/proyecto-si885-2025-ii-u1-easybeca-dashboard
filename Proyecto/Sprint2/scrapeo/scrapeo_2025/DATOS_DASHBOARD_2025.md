# Datos Extraídos para Dashboard de Becas 2025

## 📊 Resumen de Extracción de Datos

Este documento describe los archivos generados con datos del **año 2025** para el dashboard de becas.

**Fecha de generación:** 11 de noviembre de 2025  
**Total de registros procesados:** 962  
**Programas de becas:** 20  
**Instituciones participantes:** 137  
**Departamentos con cobertura:** 39

---

## 📁 Archivos Generados

### 1. Archivos Principales de Datos

#### `dashboard_becas_2025_consolidado.csv`
**Descripción:** Dataset principal consolidado con todos los datos del año 2025.

**Campos incluidos:**
- `NombreBeca`: Nombre del programa de beca
- `Institucion`: Institución donde el becario estudiará o estudió
- `AnioBecariosConfirmados`: Año de becarios confirmados (2025)
- `Departamento`: Departamento donde está ubicada la institución educativa
- `Carrera`: Carrera financiada por la beca
- `Modalidad`: Categoría específica de la beca
- `Estrato_socioeconomico`: Clasificación social (pobre, pobre extrema, no pobre, etc.)
- `Migracion`: Clasificación de migración (Nacional - Sin especificar, Lima - Sin migración, Posible migración, Internacional)
- Campos adicionales: TipoUniversidad, Estado, Quintil, NotaMinima, Fuente, etc.

**Registros:** 962

---

#### `dashboard_becas_2025_consolidado.json`
**Descripción:** Versión JSON del dataset consolidado, útil para APIs y aplicaciones web.

**Formato:** Array de objetos JSON con los mismos campos que el CSV.

---

#### `dashboard_becas_2025_simplificado.csv`
**Descripción:** Versión simplificada del dataset con solo los 8 campos principales del dashboard.

**Campos incluidos:**
1. NombreBeca
2. Institucion
3. AnioBecariosConfirmados
4. Departamento
5. Carrera
6. Modalidad
7. Estrato Socioeconómico
8. Migracion

**Uso recomendado:** Ideal para dashboards que necesitan solo los campos esenciales.

---

### 2. Archivos de Estadísticas y Reportes

#### `estadisticas_dashboard_2025.json`
**Descripción:** Estadísticas generales del dataset consolidado.

**Contenido:**
- Total de registros
- Becas únicas
- Instituciones únicas
- Departamentos únicos
- Distribución por becas
- Distribución por departamentos
- Distribución por modalidades
- Distribución por estrato socioeconómico
- Distribución por migración

---

#### `reporte_detallado_por_beca.json`
**Descripción:** Análisis detallado de cada programa de becas.

**Para cada beca incluye:**
- Nombre de la beca
- Total de registros
- Instituciones únicas
- Departamentos
- Top 5 instituciones
- Top 5 departamentos
- Distribución de modalidades
- Distribución de estratos
- Distribución de migración

---

#### `reporte_por_departamento.json`
**Descripción:** Análisis por departamento (Top 10).

**Para cada departamento incluye:**
- Total de becas
- Tipos de becas disponibles
- Instituciones únicas
- Modalidades

---

#### `resumen_ejecutivo_2025.txt`
**Descripción:** Resumen ejecutivo en formato de texto legible.

**Contenido:**
- Datos generales
- Programas de becas más importantes
- Cobertura geográfica
- Modalidades principales
- Enfoque socioeconómico
- Análisis de migración
- Observaciones

---

## 📈 Estadísticas Clave

### Distribución por Programa de Becas

| Programa de Beca | Registros | Porcentaje |
|-----------------|-----------|------------|
| Beca 18 | 864 | 89.8% |
| Beca Tec | 62 | 6.4% |
| Beca Perú | 13 | 1.4% |
| Becas Chevening | 4 | 0.4% |
| Becas Fulbright | 4 | 0.4% |
| Otros (15 programas) | 15 | 1.6% |

### Top 10 Departamentos con Mayor Cobertura

| Departamento | Becas | Porcentaje |
|--------------|-------|------------|
| Lima | 301 | 31.3% |
| No especificado | 296 | 30.8% |
| Nacional | 49 | 5.1% |
| Arequipa | 44 | 4.6% |
| Huancayo | 27 | 2.8% |
| Lambayeque | 21 | 2.2% |
| Chiclayo | 18 | 1.9% |
| Trujillo | 18 | 1.9% |
| Ayacucho | 11 | 1.1% |
| Puno | 11 | 1.1% |

### Modalidades Principales

| Modalidad | Registros | Porcentaje |
|-----------|-----------|------------|
| Ordinaria | 190 | 19.8% |
| EIB (Educación Intercultural Bilingüe) | 98 | 10.2% |
| Protección | 98 | 10.2% |
| Vraem | 97 | 10.1% |
| Huallaga | 95 | 9.9% |
| CNA y PA | 95 | 9.9% |
| FF.AA. | 95 | 9.9% |
| Repared | 95 | 9.9% |

### Estratos Socioeconómicos

| Estrato | Registros | Porcentaje |
|---------|-----------|------------|
| Variable | 381 | 39.6% |
| Pobre o Pobre Extrema | 286 | 29.7% |
| Variable según modalidad | 103 | 10.7% |
| Víctimas de violencia | 95 | 9.9% |
| Estudiantes de institutos técnicos | 61 | 6.3% |
| Otros | 36 | 3.8% |

### Análisis de Migración

| Tipo de Migración | Registros | Porcentaje |
|-------------------|-----------|------------|
| Nacional - Sin especificar | 345 | 35.9% |
| Lima - Sin migración | 301 | 31.3% |
| Posible migración | 236 | 24.5% |
| Internacional | 80 | 8.3% |

---

## 🔍 Fuentes de Datos Procesadas

Los datos fueron extraídos y consolidados de los siguientes archivos CSV y JSON:

1. ✅ `beca18_datos_expandido.csv` - 760 registros de Beca 18
2. ✅ `instituciones_beca_18.csv` - 103 registros de instituciones Beca 18
3. ✅ `instituciones_beca_tec.csv` - 61 registros de Beca Tec
4. ✅ `instituciones_beca_peru.csv` - 12 registros de Beca Perú
5. ✅ `instituciones_chevening.csv` - 3 registros de Becas Chevening
6. ✅ `instituciones_fulbright.csv` - 3 registros de Becas Fulbright
7. ✅ `becas_integrales_completo.csv` - 20 registros de becas integrales

**Criterio de filtrado:** Solo se incluyeron datos con convocatoria 2025 o estado "Activa" para 2025.

---

## 🛠️ Scripts de Procesamiento

### `extraer_datos_dashboard_2025.py`
Script principal que extrae y consolida todos los datos del año 2025.

**Funciones principales:**
- `extraer_datos_beca18_expandido()` - Extrae datos de Beca 18
- `extraer_datos_instituciones_beca18()` - Extrae instituciones de Beca 18
- `extraer_datos_beca_tec()` - Extrae datos de Beca Tec
- `extraer_datos_beca_peru()` - Extrae datos de Beca Perú
- `extraer_datos_becas_internacionales()` - Extrae becas Chevening y Fulbright
- `extraer_datos_becas_integrales()` - Extrae datos integrales
- `generar_campo_migracion()` - Genera clasificación de migración
- `consolidar_datos()` - Consolida todos los datos

**Ejecutar:**
```bash
python extraer_datos_dashboard_2025.py
```

---

### `analizar_datos_dashboard.py`
Script de análisis que genera reportes detallados y estadísticas.

**Funciones principales:**
- `generar_reporte_por_beca()` - Análisis por cada beca
- `generar_reporte_por_departamento()` - Análisis por departamento
- `generar_reporte_migracion()` - Análisis de migración
- `generar_reporte_estratos()` - Análisis de estratos socioeconómicos
- `generar_reporte_modalidades()` - Análisis de modalidades
- `generar_resumen_ejecutivo()` - Resumen ejecutivo
- `generar_csv_simplificado()` - CSV simplificado para dashboard

**Ejecutar:**
```bash
python analizar_datos_dashboard.py
```

---

## 📊 Uso en Dashboard

### Campos Recomendados para Visualizaciones

#### Para gráficos de distribución:
- **Por Beca:** `NombreBeca`
- **Por Departamento:** `Departamento`
- **Por Modalidad:** `Modalidad`
- **Por Estrato:** `Estrato_socioeconomico`

#### Para análisis de migración:
- **Campo:** `Migracion`
- **Categorías:**
  - Nacional - Sin especificar
  - Lima - Sin migración
  - Posible migración
  - Internacional

#### Para análisis temporal:
- **Campo:** `AnioBecariosConfirmados` (siempre 2025)

#### Para análisis de instituciones:
- **Campo:** `Institucion`
- **Instituciones únicas:** 137

---

## 🎯 Casos de Uso del Dashboard

### 1. Dashboard General de Becas
**Archivo recomendado:** `dashboard_becas_2025_simplificado.csv`

**Visualizaciones sugeridas:**
- Gráfico de barras: Becas por programa
- Mapa de calor: Distribución geográfica
- Gráfico de torta: Estratos socioeconómicos
- Tabla: Top 10 instituciones

---

### 2. Dashboard de Beca 18
**Filtrar por:** `NombreBeca = "Beca 18"`

**Visualizaciones sugeridas:**
- Distribución por modalidad (Ordinaria, EIB, Protección, etc.)
- Mapa de universidades públicas vs privadas
- Análisis por quintil
- Cobertura geográfica

---

### 3. Dashboard de Migración Educativa
**Campo principal:** `Migracion`

**Visualizaciones sugeridas:**
- Flujo de migración por departamento
- Becas internacionales vs nacionales
- Análisis de movilidad estudiantil

---

### 4. Dashboard de Equidad Socioeconómica
**Campo principal:** `Estrato_socioeconomico`

**Visualizaciones sugeridas:**
- Distribución de becas por estrato
- Comparación entre programas
- Análisis de inclusión

---

## 📌 Notas Importantes

### Limitaciones
1. **Datos de migración:** Son estimaciones basadas en la ubicación de la institución vs departamento de origen (no disponible en los datos fuente).
2. **Carreras:** Para Beca 18, no hay especificación de carreras individuales en la fuente original.
3. **Departamento "No especificado":** 296 registros (30.8%) no tienen departamento específico en los datos originales.

### Datos Faltantes
- **Becarios confirmados individuales:** No hay conteo de becarios individuales, solo registros de instituciones y modalidades.
- **Departamento de origen:** No está disponible en los datos fuente.
- **Carreras específicas:** Solo disponible para Beca Tec, Beca Perú y becas internacionales.

### Calidad de Datos
- ✅ Todos los datos son del año 2025
- ✅ Se han consolidado múltiples fuentes
- ✅ Se han eliminado duplicados
- ✅ Se han normalizado los nombres de campos

---

## 🚀 Próximos Pasos

1. **Importar datos al dashboard:**
   - Usar `dashboard_becas_2025_simplificado.csv` para Power BI, Tableau, etc.
   - Usar `dashboard_becas_2025_consolidado.json` para aplicaciones web

2. **Crear visualizaciones:**
   - Seguir las recomendaciones de casos de uso

3. **Actualizar datos:**
   - Ejecutar `extraer_datos_dashboard_2025.py` cuando haya nuevos datos

4. **Análisis adicional:**
   - Ejecutar `analizar_datos_dashboard.py` para reportes actualizados

---

## 📞 Contacto y Soporte

Para más información o consultas sobre los datos:
- Revisar los archivos JSON de reportes para análisis detallados
- Consultar `resumen_ejecutivo_2025.txt` para un overview completo
- Los scripts son modulares y pueden ser adaptados según necesidades específicas

---

**Última actualización:** 11 de noviembre de 2025  
**Versión:** 1.0  
**Estado:** Datos listos para uso en dashboard
