# 📊 DATASET PRONABEC 2021 - FORMATO FINAL PARA DASHBOARD

## ✅ ARCHIVO GENERADO

**Nombre:** `dataset_pronabec_2021_formato_final.xlsx` / `.csv`

**Total de registros:** 4,578

**Año:** 2021

---

## 📋 ESTRUCTURA DEL DATASET

### Campos Incluidos (9 columnas):

| # | Campo | Tipo | Ejemplo | Fuente |
|---|-------|------|---------|--------|
| 1 | **NombreBeca** | Texto | "Beca 18", "Crédito General" | ✅ REAL |
| 2 | **Institucion** | Texto | "Universidad Nacional Mayor de San Marcos" | ⚠️ INVENTADO |
| 3 | **Carrera** | Texto | "Ingeniería de Sistemas", "Medicina" | ⚠️ INVENTADO |
| 4 | **Lugar** | Texto | "Lima", "España", "Cusco" | ✅ REAL |
| 5 | **CategoriaDeBecas** | Texto | "Pregrado", "Posgrado Maestria" | ✅ REAL |
| 6 | **Anio_Convocatoria** | Número | 2021 | ✅ REAL |
| 7 | **Genero** | Texto | "Masculino", "Femenino" | ✅ PARCIAL |
| 8 | **EstratoSocieconomico** | Texto | "Pobre", "Pobre Extremo", "No Pobre" | ⚠️ INVENTADO |
| 9 | **BecasSegunMigracion** | Texto | "Migró", "No Migró" | ⚠️ INVENTADO |

---

## 📊 ESTADÍSTICAS DEL DATASET

### Por Categoría de Becas:
- **Pregrado:** 4,266 registros (93.2%)
- **Especiales:** 161 registros (3.5%)
- **Posgrado Doctorado:** 78 registros (1.7%)
- **Posgrado Maestría:** 73 registros (1.6%)

### Por Género:
- **Femenino:** 2,603 registros (56.9%)
- **Masculino:** 1,975 registros (43.1%)

### Por Estrato Socioeconómico:
- **Pobre:** 2,433 registros (53.2%)
- **Pobre Extremo:** 1,667 registros (36.4%)
- **No Pobre:** 478 registros (10.4%)

### Por Migración:
- **Migró:** 2,526 registros (55.2%)
- **No Migró:** 2,052 registros (44.8%)

### Top 10 Lugares de Estudio:
1. Lima: 2,636 becarios
2. Piura: 107 becarios
3. Puno: 99 becarios
4. Tacna: 98 becarios
5. Áncash: 98 becarios
6. Junín: 96 becarios
7. Callao: 93 becarios
8. Cusco: 86 becarios
9. Lambayeque: 86 becarios
10. Cajamarca: 85 becarios

---

## ⚠️ DATOS INVENTADOS - IMPORTANTE PARA TU EXPOSICIÓN

### ❌ CAMPOS 100% INVENTADOS:

#### 1. 📚 **CARRERA** (100% Inventado)
- **Razón:** El PDF NO desagrega carreras por becario individual
- **Método:** Asignación aleatoria de 28 carreras típicas
- **Carreras Pregrado:** 
  - Ingeniería de Sistemas, Administración, Contabilidad, Derecho
  - Medicina Humana, Enfermería, Educación, Ingeniería Civil
  - Ingeniería Industrial, Psicología, Arquitectura, Economía
  - Y 16 carreras más...
- **Carreras Posgrado:**
  - MBA, Ingeniería de Software, Ciencias de Datos
  - Biotecnología, Gestión Pública, Economía Aplicada
  - Física, Química, Ciencias Políticas, y más...

#### 2. 🏛️ **INSTITUCIÓN** (100% Inventado)
- **Razón:** El PDF NO especifica instituciones por becario
- **Método:** Asignación aleatoria de 25 instituciones
- **Para Perú:**
  - Universidad Nacional Mayor de San Marcos
  - Universidad Nacional de Ingeniería
  - Pontificia Universidad Católica del Perú
  - Universidad de Lima
  - Y 21 universidades más (públicas y privadas)
- **Para Extranjero:**
  - España: Universidad Complutense de Madrid, Universidad de Barcelona
  - EE.UU.: MIT, Stanford, Harvard, Yale
  - Reino Unido: Oxford, Cambridge, Imperial College
  - Y más según el país

#### 3. 💰 **ESTRATO SOCIOECONÓMICO** (100% Inventado)
- **Razón:** El PDF NO desagrega estratos por becario
- **Método:** Distribución probabilística estimada
- **Distribución aplicada:**
  - **Pobre Extremo:** 40% (mayor peso en regiones rurales)
  - **Pobre:** 50% (mayoría de becarios Pronabec)
  - **No Pobre:** 10% (casos excepcionales)
- **Excepción para becas extranjero:**
  - **Pobre:** 60%
  - **No Pobre:** 40%
  - No hay "Pobre Extremo" (requisitos más altos)

#### 4. 🚗 **BECAS SEGÚN MIGRACIÓN** (80% Inventado)
- **Razón:** El PDF solo tiene datos agregados, NO individuales
- **Método:** Lógica probabilística basada en región de origen
- **Reglas aplicadas:**
  - **Si origen es Lima:**
    - 20% Migró (a otras regiones)
    - 80% No Migró (estudia en Lima)
  - **Si origen NO es Lima:**
    - 60% Migró (principalmente a Lima)
    - 40% No Migró (estudia en su región)
  - **Becas extranjero:**
    - 100% Migró (obvio, al extranjero)

---

## ✅ DATOS REALES DEL PDF

### Campos con información real:

1. ✅ **NombreBeca** - Totalmente real
   - Beca 18
   - Crédito General
   - Crédito Continuidad
   - Crédito Talento
   - Crédito 18
   - Beca Posgrado en el Extranjero

2. ✅ **Lugar** - Totalmente real
   - 26 departamentos de Perú (del PDF)
   - 14 países para becas extranjero (del PDF)

3. ✅ **Anio_Convocatoria** - Totalmente real
   - 2021 (todos los datos son de este año)

4. ✅ **CategoriaDeBecas** - Parcialmente real
   - Pregrado: Real (Beca 18)
   - Especiales: Real (Crédito Talento)
   - Posgrado: Inferido de becas extranjero

5. ✅ **Genero** - Parcialmente real
   - Distribución real para créditos educativos
   - Estimado para Beca 18 (57% F, 43% M según datos agregados)

6. ✅ **Cantidades totales por región** - Reales
   - Los totales se mantienen fieles al PDF

---

## 🎤 PARA TU EXPOSICIÓN - TEXTO SUGERIDO

### Slide de Limitaciones de Datos:

> **"Metodología de Completado de Datos"**
> 
> Debido a que la Memoria Anual del Pronabec 2021 presenta información agregada 
> y no individual por becario, se aplicó la siguiente metodología:
> 
> **Datos Reales (del PDF):**
> - Programas de becas
> - Cantidad de becarios por región
> - Países y regiones de destino
> - Año de convocatoria (2021)
> - Distribución de género (parcial)
> 
> **Datos Generados (mediante algoritmos):**
> - Carreras específicas (28 opciones típicas)
> - Instituciones educativas (25 universidades reconocidas)
> - Estrato socioeconómico (40% Pobre Extremo, 50% Pobre, 10% No Pobre)
> - Migración individual (60% migró desde regiones, 20% desde Lima)
> 
> **Nota:** Los datos generados mantienen coherencia con las estadísticas 
> agregadas del Pronabec y representan patrones típicos del programa, pero 
> NO corresponden a becarios individuales reales.

### Slide de Disclaimer:

> **"Disclaimer Importante"**
> 
> Este dataset fue construido a partir de:
> - ✅ Datos oficiales agregados de la Memoria Anual Pronabec 2021
> - ⚠️ Modelado probabilístico para datos no disponibles
> 
> Los campos de Carrera, Institución, Estrato Socioeconómico y Migración 
> individual fueron generados mediante distribuciones probabilísticas basadas 
> en criterios típicos del programa y mantienen consistencia con los totales 
> reales por región.
> 
> **El propósito es didáctico y de visualización, no representa registros 
> administrativos reales del Pronabec.**

---

## 📈 CÓMO USAR ESTE DATASET

### 1. Para Análisis Geográfico:
- Usar campo **"Lugar"** (100% real)
- Filtrar por categoría de beca
- Crear mapas de calor

### 2. Para Análisis Demográfico:
- **Género:** Usar con precaución (parcialmente real)
- **Estrato:** Solo para tendencias generales (inventado)
- **Migración:** Solo para tendencias (inventado)

### 3. Para Análisis de Programas:
- **NombreBeca:** 100% confiable
- **CategoriaDeBecas:** Confiable
- **Anio_Convocatoria:** 100% real

### 4. Para Dashboard:
- **KPIs confiables:** Total becarios por región, por programa, por año
- **KPIs con precaución:** Distribución por carrera, por institución
- **Tendencias válidas:** Migración (Lima como polo de atracción)

---

## 🎯 VALIDACIONES REALIZADAS

### ✅ Validación de Totales:
- Total becarios Beca 18 por región: ✅ Coincide con PDF
- Total créditos educativos: ✅ Coincide con PDF
- Total becarios extranjero por país: ✅ Coincide con PDF
- Distribución de género en créditos: ✅ Similar al PDF

### ✅ Validación de Coherencia:
- Becas extranjero = 100% migración: ✅ Lógico
- Lima mayoría del destino: ✅ Coherente
- Pobre Extremo mayor en regiones: ✅ Realista
- Género 57% F / 43% M: ✅ Según datos agregados

---

## 📁 ARCHIVOS GENERADOS

1. **dataset_pronabec_2021_formato_final.xlsx** - Dataset principal (Excel)
2. **dataset_pronabec_2021_formato_final.csv** - Dataset principal (CSV)
3. **REPORTE_DATOS_INVENTADOS_2021.txt** - Documentación de datos inventados
4. **DATASET_FINAL_EXPLICACION.md** - Este documento

---

## ⚡ QUICK START

### Importar en Excel:
```
1. Abrir dataset_pronabec_2021_formato_final.xlsx
2. Insertar → Tabla dinámica
3. Crear gráficos según necesidades
```

### Importar en Power BI:
```
1. Obtener datos → Excel
2. Seleccionar dataset_pronabec_2021_formato_final.xlsx
3. Cargar datos
4. Crear relaciones si es necesario
```

### Importar en Python:
```python
import pandas as pd
df = pd.read_excel('dataset_pronabec_2021_formato_final.xlsx')
print(df.head())
print(df.describe())
```

---

## 📞 PREGUNTAS FRECUENTES

**Q: ¿Por qué algunos datos están inventados?**
A: El PDF oficial solo proporciona estadísticas agregadas, no registros individuales de becarios.

**Q: ¿Puedo usar este dataset para investigación académica?**
A: Solo para propósitos didácticos y de visualización. Para investigación formal, solicitar datos al Pronabec.

**Q: ¿Los totales son correctos?**
A: Sí, los totales por región, programa y año coinciden 100% con el PDF oficial.

**Q: ¿Cómo menciono las limitaciones en mi exposición?**
A: Usa el texto sugerido en la sección "Para tu Exposición" de este documento.

---

## 🎓 CONCLUSIÓN

Este dataset combina:
- ✅ **Datos oficiales reales** del Pronabec 2021
- ⚠️ **Modelado probabilístico** para completar información faltante
- 🎯 **Coherencia estadística** con los totales oficiales

Es ideal para:
- Dashboards de visualización
- Prácticas de análisis de datos
- Presentaciones educativas
- Aprendizaje de herramientas BI

**NO es ideal para:**
- Investigación académica formal
- Toma de decisiones administrativas
- Análisis de becarios específicos

---

**Fecha de generación:** Noviembre 2025  
**Fuente:** Memoria Anual del Pronabec 2021  
**Metodología:** Web scraping + modelado probabilístico  
**Total registros:** 4,578
