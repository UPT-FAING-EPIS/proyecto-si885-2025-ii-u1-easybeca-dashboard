# 📊 REPORTE PARA EXPOSICIÓN - Datos Inventados

## 🎯 Dataset Generado: PRONABEC_2024_DATASET_COMPLETO.xlsx

**Total de registros**: 727 becarios (datos reales del PDF oficial)

---

## ✅ CAMPOS CON DATOS REALES (Del PDF Oficial)

### 1. **NombreBeca** ✅
- **Origen**: Extraído directamente del PDF
- **Ejemplos**: Beca 18, Beca Permanencia, Beca Vocación
- **Cantidad**: 727 registros (100% reales)
- **Fuente**: Memoria Anual PRONABEC 2024

### 2. **Departamento** ✅
- **Origen**: Extraído directamente del PDF
- **Cantidad**: 26 departamentos del Perú
- **Registros**: 727 (100% reales)
- **Distribución**: Lima (151), Ica (93), Callao (49), etc.
- **Fuente**: Tabla de distribución geográfica del documento oficial

### 3. **Anio_Convocatoria** ✅
- **Origen**: Del documento oficial
- **Valor**: 2024
- **Cantidad**: 727 registros (100% reales)
- **Fuente**: Memoria Anual PRONABEC 2024

---

## ⚠️ CAMPOS PARCIALMENTE INVENTADOS

### 4. **Institucion** ⚠️
- **Origen**: MIXTO (4 reales + 20 inventadas)
- **Instituciones REALES del PDF**: 
  - Universidad Privada del Norte S.A.C.
  - Universidad San Ignacio de Loyola S.R.L.
  - Universidad Científica del Sur S.A.C.
  - Universidad Peruana de Ciencias Aplicadas S.A.C.
- **Instituciones INVENTADAS**: 519 registros (71.4%)
- **Justificación**: 
  - El PDF solo menciona 4 instituciones específicas
  - Se completó con las 20 universidades públicas más importantes del Perú
  - Todas son instituciones REALES y reconocidas oficialmente
- **Para tu exposición**: 
  > "Las instituciones son reales y reconocidas por SUNEDU. Solo 4 fueron mencionadas en el PDF, las demás son las universidades públicas más importantes del país, donde PRONABEC típicamente otorga becas."

### 5. **CategoriaDeBecas** ⚠️
- **Origen**: INFERIDO de los tipos de becas del PDF
- **Categorías basadas en**: 
  - Pregrado - Beca 18 (del tipo "Pregrado" en el PDF)
  - Posgrado - Maestría (del tipo "Posgrado" en el PDF)
  - Especiales - Inclusión (del tipo "Especiales" en el PDF)
- **Registros inferidos**: 515 (70.8%)
- **Justificación**: El PDF menciona 3 tipos generales (Pregrado, Posgrado, Especiales) pero no especifica las subcategorías
- **Para tu exposición**:
  > "Las categorías fueron inferidas de los 3 tipos de becas mencionados en el documento: Pregrado, Posgrado y Especiales. Cada categoría refleja las modalidades típicas de cada programa."

---

## ❌ CAMPOS COMPLETAMENTE INVENTADOS (NO en el PDF)

### 6. **Carrera** ❌
- **Origen**: INVENTADO (0% del PDF)
- **Cantidad inventada**: 727 registros (100%)
- **Método**: Lista de las 20 carreras más demandadas en Perú
- **Carreras incluidas**:
  - Administración de Empresas
  - Ingeniería de Sistemas
  - Contabilidad
  - Derecho
  - Medicina Humana
  - Enfermería
  - Ingeniería Civil
  - (y 13 más)
- **Justificación**: 
  - El PDF NO incluye información de carreras por becario
  - Se usaron las carreras más populares según estadísticas del INEI
- **Para tu exposición**:
  > "⚠️ IMPORTANTE: El campo 'Carrera' fue completamente inventado ya que el documento oficial no incluye esta información desagregada. Se utilizaron las 20 carreras universitarias más demandadas en Perú según el INEI para demostrar la funcionalidad del dashboard."

### 7. **Genero** ❌
- **Origen**: INVENTADO (0% del PDF)
- **Cantidad inventada**: 727 registros (100%)
- **Distribución**: Aproximadamente 50% Masculino, 50% Femenino (aleatorio)
- **Método**: Asignación aleatoria
- **Justificación**: El PDF NO incluye datos de género por becario
- **Para tu exposición**:
  > "⚠️ El campo 'Género' fue inventado mediante distribución aleatoria 50/50, ya que el documento no contiene esta información. Es usado únicamente para demostrar análisis de género en el dashboard."

### 8. **EstratoSocioeconomico** ❌
- **Origen**: INVENTADO (0% del PDF)
- **Cantidad inventada**: 727 registros (100%)
- **Distribución aplicada**:
  - 45% Pobre (≈327 becarios)
  - 30% Pobre Extremo (≈218 becarios)
  - 25% No pobre (≈182 becarios)
- **Método**: Distribución ponderada realista
- **Justificación**: 
  - El PDF NO incluye estratos por becario individual
  - La distribución refleja el enfoque de PRONABEC en población vulnerable
  - Basado en estadísticas generales de beneficiarios de programas sociales
- **Para tu exposición**:
  > "⚠️ El 'Estrato Socioeconómico' fue inventado siguiendo una distribución realista (45% Pobre, 30% Pobre Extremo, 25% No pobre) que refleja el público objetivo de PRONABEC según sus lineamientos institucionales. El documento oficial no contiene esta información desagregada."

### 9. **BecasSegunMigracion** ❌
- **Origen**: INVENTADO (0% del PDF)
- **Cantidad inventada**: 727 registros (100%)
- **Lógica aplicada**:
  - Lima: 80% "No Migró" (estudian en su mismo departamento)
  - Otros departamentos: 40% "Migró" (se trasladan a estudiar)
- **Método**: Lógica basada en patrones de migración estudiantil
- **Justificación**: 
  - El PDF NO incluye datos de migración por becario
  - La lógica refleja que Lima tiene más oferta educativa (menos migración)
  - Departamentos pequeños tienen menos oferta (más migración)
- **Para tu exposición**:
  > "⚠️ El campo 'BecasSegunMigracion' fue generado con lógica realista: becarios de Lima tienen 80% probabilidad de no migrar (por mayor oferta educativa local), mientras que becarios de otros departamentos tienen 40% probabilidad de migrar hacia centros urbanos. El documento oficial no contiene esta información."

---

## 📊 RESUMEN PARA TU EXPOSICIÓN

### Datos Reales (100% confiables)
```
✅ NombreBeca          → 727 registros (100% del PDF)
✅ Departamento        → 727 registros (100% del PDF)
✅ Anio_Convocatoria   → 727 registros (100% del PDF)
```

### Datos Parcialmente Inventados
```
⚠️ Institucion         → 71.4% inventado (pero instituciones REALES)
⚠️ CategoriaDeBecas    → 70.8% inferido (basado en tipos del PDF)
```

### Datos Completamente Inventados
```
❌ Carrera              → 100% inventado (carreras comunes en Perú)
❌ Genero               → 100% inventado (distribución aleatoria)
❌ EstratoSocioeconomico → 100% inventado (distribución realista)
❌ BecasSegunMigracion  → 100% inventado (lógica geográfica)
```

---

## 🎤 TEXTO SUGERIDO PARA TU EXPOSICIÓN

### Introducción de los Datos

> "Para el desarrollo de este dashboard, utilizamos datos oficiales de la Memoria Anual PRONABEC 2024. Es importante aclarar el origen de cada campo:"

### Sobre los Datos Reales

> "Los campos **NombreBeca**, **Departamento** y **Año** fueron extraídos directamente del documento oficial mediante web scraping, representando información 100% real de los 727 becarios distribuidos en los 26 departamentos del Perú."

### Sobre los Datos Parcialmente Inventados

> "El campo **Institución** contiene 4 instituciones mencionadas explícitamente en el PDF, y fue completado con las 20 universidades públicas más importantes del país, todas reconocidas oficialmente por SUNEDU, ya que PRONABEC trabaja con múltiples instituciones educativas."

> "Las **Categorías de Becas** fueron inferidas de los 3 tipos principales mencionados en el documento: Pregrado, Posgrado y Especiales, asignando subcategorías lógicas a cada una."

### Sobre los Datos Inventados (CLAVE)

> "⚠️ **IMPORTANTE**: Los campos **Carrera**, **Género**, **Estrato Socioeconómico** y **Migración** fueron generados sintéticamente para demostrar la funcionalidad completa del dashboard, ya que el documento oficial no incluye esta información desagregada por becario individual."

> "Para estos campos inventados, aplicamos:"
> - **Carreras**: Las 20 más demandadas según estadísticas del INEI
> - **Género**: Distribución aleatoria 50/50
> - **Estrato**: Distribución ponderada (45% Pobre, 30% Pobre Extremo, 25% No pobre) según el perfil típico de beneficiarios
> - **Migración**: Lógica geográfica realista (Lima 80% no migra, provincias 40% migra)

### Conclusión

> "Si bien algunos campos fueron generados sintéticamente, esto no invalida el valor del proyecto. Los datos reales del PDF (727 becarios en 26 departamentos) son el núcleo del análisis, y los campos inventados nos permitieron desarrollar un dashboard completo y funcional que puede ser replicado cuando estos datos estén disponibles oficialmente."

---

## 📋 TABLA RESUMEN PARA DIAPOSITIVA

| Campo | Origen | % Real | Justificación |
|-------|--------|--------|---------------|
| NombreBeca | PDF Oficial | 100% | Extraído directamente |
| Departamento | PDF Oficial | 100% | Distribución oficial |
| Anio_Convocatoria | PDF Oficial | 100% | Año del documento |
| Institucion | Mixto | 28.6% | Solo 4 en PDF, resto son universidades reales |
| CategoriaDeBecas | Inferido | 29.2% | Basado en 3 tipos del PDF |
| **Carrera** | **Inventado** | **0%** | **No existe en PDF** |
| **Genero** | **Inventado** | **0%** | **No existe en PDF** |
| **EstratoSocioeconomico** | **Inventado** | **0%** | **No existe en PDF** |
| **BecasSegunMigracion** | **Inventado** | **0%** | **No existe en PDF** |

---

## 💡 CONSEJOS PARA TU EXPOSICIÓN

### ✅ Sé transparente
- Menciona claramente qué es real y qué es inventado
- Explica por qué fue necesario inventar algunos campos
- Demuestra que usaste lógica realista

### ✅ Enfatiza el valor
- Los 727 becarios en 26 departamentos SON REALES
- El dashboard demuestra capacidad técnica
- La metodología es replicable con datos completos

### ✅ Justifica profesionalmente
- "Datos sintéticos para demostración funcional"
- "Basados en estadísticas y patrones reales"
- "Metodología aplicable a datos reales futuros"

### ❌ Evita
- No digas "son todos reales" sin aclarar
- No ocultes que algunos datos son inventados
- No minimices la importancia de los datos reales que SÍ tienes

---

## 📁 ARCHIVOS GENERADOS

1. **PRONABEC_2024_DATASET_COMPLETO.xlsx** (3 hojas)
   - Hoja 1: Datos_Becarios (727 registros con 9 campos)
   - Hoja 2: Reporte_Datos_Inventados (tabla detallada)
   - Hoja 3: Estadisticas (métricas del dataset)

2. **PRONABEC_2024_DATASET_COMPLETO.csv**
   - Formato CSV para importar fácilmente

3. **REPORTE_DATOS_INVENTADOS.xlsx**
   - Tabla detallada de justificaciones por campo

---

## ✨ ¡Éxito en tu exposición!

Recuerda: La transparencia y honestidad académica son más importantes que pretender tener datos que no existen. Tu proyecto demuestra habilidades técnicas reales de web scraping, procesamiento de datos y desarrollo de dashboards.
