# Guía de Uso: Dashboard_Becas_PowerBI_2025.xlsx

## 📊 Descripción General

Archivo Excel completo con **12 hojas** de datos del año **2025** listo para importar en Power BI.

**Archivo:** `Dashboard_Becas_PowerBI_2025.xlsx`  
**Tamaño:** 58.05 KB  
**Total de registros:** 962 becas del año 2025  
**Fecha de generación:** 11 de noviembre de 2025

---

## 📑 Estructura del Archivo (12 Hojas)

### 1️⃣ **Becas 2025** (Hoja Principal) ⭐
**Descripción:** Dataset principal con todos los campos requeridos para el dashboard.

**Campos (8 columnas):**
- `NombreBeca` - Nombre del programa de beca
- `Institucion` - Institución donde el becario estudiará o estudió
- `AnioBecariosConfirmados` - Año 2025
- `Departamento` - Departamento donde está ubicada la institución
- `Carrera` - Carrera financiada por la beca
- `Modalidad` - Categoría específica de la beca
- `Estrato_socioeconomico` - Clasificación social (pobre, pobre extrema, no pobre)
- `Becas_segun_migracion` - Migró o no migró a otro departamento

**Registros:** 962  
**Uso en Power BI:** Tabla principal para visualizaciones

---

### 2️⃣ **Resumen 2025** (KPIs)
**Descripción:** Resumen ejecutivo con 15 indicadores clave.

**Indicadores incluidos:**
- Total de Becas (Registros): 962
- Programas de Becas: 20
- Instituciones Participantes: 137
- Departamentos con Cobertura: 39
- Modalidades Diferentes: 26
- Carreras Ofrecidas: 53
- Beca Más Popular: Beca 18
- Departamento con Más Becas: Lima
- Modalidad Más Común: Ordinaria
- Y más...

**Uso en Power BI:** Tarjetas KPI, medidas rápidas

---

### 3️⃣ **Instituciones 2025**
**Descripción:** Análisis detallado de instituciones educativas.

**Campos:**
- Institucion
- ProgramasBecas
- Departamento
- Anio
- TotalRegistros
- TipoInstitucion

**Registros:** 137 instituciones únicas  
**Uso en Power BI:** Análisis por institución, rankings

---

### 4️⃣ **Departamentos 2025**
**Descripción:** Análisis de cobertura geográfica.

**Campos:**
- Departamento
- TotalBecas
- InstitucionesUnicas
- ModalidadesUnicas
- Porcentaje

**Top 5 Departamentos:**
1. Lima - 301 becas (31.29%)
2. No especificado - 296 becas (30.77%)
3. Nacional - 49 becas (5.09%)
4. Arequipa - 44 becas (4.57%)
5. Huancayo - 27 becas (2.81%)

**Registros:** 39 departamentos  
**Uso en Power BI:** Mapas, gráficos geográficos

---

### 5️⃣ **Modalidades 2025**
**Descripción:** Análisis por modalidad de beca.

**Campos:**
- Modalidad
- TotalBecas
- Instituciones
- Departamentos
- Porcentaje

**Registros:** 26 modalidades  
**Modalidades principales:**
- Ordinaria: 190 (19.8%)
- EIB: 98 (10.2%)
- Protección: 98 (10.2%)
- Vraem: 97 (10.1%)

**Uso en Power BI:** Análisis de tipos de beca, filtros

---

### 6️⃣ **Estratos 2025**
**Descripción:** Análisis socioeconómico de becarios.

**Campos:**
- Estrato_Socioeconomico
- TotalBecas
- Instituciones
- Departamentos
- Porcentaje

**Distribución:**
- Variable: 381 (39.6%)
- Pobre o Pobre Extrema: 286 (29.7%)
- Variable según modalidad: 103 (10.7%)
- Víctimas de violencia: 95 (9.9%)

**Registros:** 9 estratos  
**Uso en Power BI:** Análisis de equidad, inclusión social

---

### 7️⃣ **Migracion 2025**
**Descripción:** Análisis de movilidad estudiantil.

**Campos:**
- Tipo_Migracion
- TotalBecas
- Instituciones
- Departamentos
- Porcentaje
- Clasificacion

**Distribución:**
- Nacional - Sin especificar: 345 (35.9%)
- Lima - Sin migración: 301 (31.3%)
- Posible migración: 236 (24.5%)
- Internacional: 80 (8.3%)

**Registros:** 4 tipos de migración  
**Uso en Power BI:** Flujos de migración, movilidad

---

### 8️⃣ **Programas Becas 2025**
**Descripción:** Detalle de cada programa de becas.

**Campos:**
- NombreBeca
- Instituciones
- Departamentos
- Carreras
- Modalidades
- TotalRegistros
- Porcentaje

**Registros:** 20 programas  
**Top 3:**
1. Beca 18: 864 registros (89.8%)
2. Beca Tec: 62 registros (6.4%)
3. Beca Perú: 13 registros (1.4%)

**Uso en Power BI:** Comparación entre programas

---

### 9️⃣ **Carreras 2025**
**Descripción:** Análisis por carrera profesional.

**Campos:**
- Carrera
- ProgramasBecas
- Instituciones
- TotalBecas

**Registros:** 51 carreras específicas  
**Uso en Power BI:** Análisis de demanda por carrera

---

### 🔟 **Beca18 Detalle 2025**
**Descripción:** Análisis específico del programa Beca 18.

**Campos:**
- Modalidad
- UniversidadesUnicas
- UbicacionesUnicas
- TipoUniversidad
- TotalRegistros

**Registros:** 8 modalidades de Beca 18  
**Modalidades:**
- Ordinaria
- EIB
- Protección
- Vraem
- Huallaga
- CNA y PA
- FF.AA.
- Repared

**Uso en Power BI:** Dashboard específico Beca 18

---

### 1️⃣1️⃣ **BecaTec Detalle 2025**
**Descripción:** Análisis específico del programa Beca Tec.

**Campos:**
- Institucion
- Region
- ProgramasOfrecidos
- TipoInstitucion
- Modalidad
- TotalProgramas

**Registros:** 10 instituciones técnicas  
**Uso en Power BI:** Dashboard específico Beca Tec

---

### 1️⃣2️⃣ **Matriz Beca-Depto 2025**
**Descripción:** Tabla cruzada de Becas vs Departamentos.

**Estructura:** Matriz de 20 becas × 39 departamentos  
**Uso en Power BI:** Heat maps, análisis cruzado

---

## 🚀 Cómo Importar en Power BI

### Método 1: Importar Todo el Archivo

```
1. Abrir Power BI Desktop
2. Inicio → Obtener datos → Excel
3. Seleccionar: Dashboard_Becas_PowerBI_2025.xlsx
4. Marcar las hojas que desees importar (recomendado: todas)
5. Clic en "Cargar"
```

### Método 2: Importar Hoja Específica

```
1. Obtener datos → Excel
2. Seleccionar archivo
3. Marcar solo la hoja deseada (ej: "Becas 2025")
4. Clic en "Cargar"
```

---

## 📊 Visualizaciones Recomendadas en Power BI

### Dashboard Principal
**Usar hoja:** `Becas 2025`

1. **Tarjeta KPI:** Total de Becas
   - Campo: COUNT(NombreBeca)

2. **Gráfico de Barras:** Becas por Programa
   - Eje: NombreBeca
   - Valores: COUNT(*)

3. **Mapa:** Distribución Geográfica
   - Ubicación: Departamento
   - Tamaño: COUNT(NombreBeca)

4. **Gráfico Circular:** Estratos Socioeconómicos
   - Leyenda: Estrato_socioeconomico
   - Valores: COUNT(*)

5. **Gráfico de Barras Apiladas:** Migración
   - Eje: Becas_segun_migracion
   - Valores: COUNT(*)

### Dashboard de Instituciones
**Usar hoja:** `Instituciones 2025`

1. **Tabla:** Top Instituciones
   - Columnas: Institucion, TotalRegistros, Departamento

2. **Treemap:** Instituciones por Tamaño
   - Grupo: Institucion
   - Valores: TotalRegistros

### Dashboard Geográfico
**Usar hojas:** `Departamentos 2025` + `Becas 2025`

1. **Mapa de Calor:** Cobertura por Departamento
2. **Gráfico de Barras:** Top 10 Departamentos
3. **Tabla:** Detalle por Departamento

### Dashboard de Modalidades
**Usar hoja:** `Modalidades 2025`

1. **Gráfico de Dona:** Distribución de Modalidades
2. **Gráfico de Barras:** Modalidades por Total de Becas

---

## 🔗 Relaciones entre Hojas en Power BI

### Relaciones Recomendadas:

```
Becas 2025[NombreBeca] → Programas Becas 2025[NombreBeca]
Becas 2025[Departamento] → Departamentos 2025[Departamento]
Becas 2025[Modalidad] → Modalidades 2025[Modalidad]
Becas 2025[Institucion] → Instituciones 2025[Institucion]
```

**Tipo de relación:** Muchos a Uno (N:1)  
**Cardinalidad:** Muchos a Uno  
**Dirección del filtro cruzado:** Ambas o De tabla de dimensión a tabla de hechos

---

## 📈 Medidas DAX Sugeridas

### Medidas Básicas

```dax
Total Becas = COUNT('Becas 2025'[NombreBeca])

Total Instituciones = DISTINCTCOUNT('Becas 2025'[Institucion])

Total Departamentos = DISTINCTCOUNT('Becas 2025'[Departamento])

% con Migración = 
DIVIDE(
    COUNTROWS(FILTER('Becas 2025', 
        'Becas 2025'[Becas_segun_migracion] = "Posible migración" || 
        'Becas 2025'[Becas_segun_migracion] = "Internacional"
    )),
    COUNTROWS('Becas 2025')
)

Beca Más Popular = 
FIRSTNONBLANK(
    TOPN(1, 
        SUMMARIZE('Becas 2025', 'Becas 2025'[NombreBeca]), 
        COUNTROWS('Becas 2025')
    ),
    1
)
```

---

## 🎨 Filtros Recomendados

### Segmentadores (Slicers) Principales:

1. **Por Programa de Beca**
   - Campo: NombreBeca
   - Tipo: Lista

2. **Por Departamento**
   - Campo: Departamento
   - Tipo: Dropdown o Lista

3. **Por Modalidad**
   - Campo: Modalidad
   - Tipo: Lista

4. **Por Estrato Socioeconómico**
   - Campo: Estrato_socioeconomico
   - Tipo: Lista

5. **Por Migración**
   - Campo: Becas_segun_migracion
   - Tipo: Botones

---

## 🔍 Análisis Específicos Sugeridos

### 1. Análisis de Equidad Social
**Hojas:** `Becas 2025` + `Estratos 2025`
- Distribución por estrato socioeconómico
- Comparación entre programas de becas
- Tendencias de inclusión

### 2. Análisis de Movilidad Estudiantil
**Hojas:** `Migracion 2025` + `Becas 2025`
- Flujos de migración entre departamentos
- Becas internacionales vs nacionales
- Instituciones que atraen más migración

### 3. Análisis por Programa
**Hojas:** `Programas Becas 2025` + Dashboard específicos
- Comparación entre Beca 18, Beca Tec, Beca Perú
- Cobertura geográfica por programa
- Modalidades por programa

### 4. Análisis Institucional
**Hojas:** `Instituciones 2025`
- Ranking de instituciones
- Tipo de instituciones (públicas vs privadas)
- Programas de becas por institución

---

## ✅ Checklist de Validación en Power BI

Antes de publicar tu dashboard, verifica:

- [ ] Todas las hojas se importaron correctamente
- [ ] Las relaciones entre tablas están configuradas
- [ ] Los tipos de datos son correctos
- [ ] Las medidas DAX funcionan
- [ ] Los filtros interactúan correctamente
- [ ] Los totales suman correctamente
- [ ] No hay valores nulos inesperados
- [ ] Los gráficos son legibles
- [ ] Los colores siguen una paleta consistente
- [ ] El rendimiento es aceptable

---

## 📝 Notas Importantes

1. **Datos del Año 2025:** Todos los registros corresponden al año 2025.

2. **Campo Migración:** Es una clasificación basada en la ubicación de la institución. Las categorías son:
   - "Nacional - Sin especificar": No se puede determinar migración
   - "Lima - Sin migración": Estudiantes en Lima
   - "Posible migración": Instituciones fuera de Lima (implica movilidad)
   - "Internacional": Becas en el extranjero

3. **Carreras:** Para Beca 18, la mayoría indica "Todas las carreras elegibles" ya que no hay especificación en los datos fuente.

4. **Departamento "No especificado":** Representa instituciones sin ubicación específica en los datos originales.

---

## 🆘 Soporte y Actualizaciones

Para actualizar los datos:
1. Ejecutar: `python generar_excel_powerbi_2025.py`
2. En Power BI: Inicio → Actualizar

Para regenerar con nuevos datos:
1. Actualizar archivos CSV/JSON fuente
2. Ejecutar: `python extraer_datos_dashboard_2025.py`
3. Ejecutar: `python generar_excel_powerbi_2025.py`
4. Actualizar en Power BI

---

## 📊 Estructura de Archivos

```
Dashboard_Becas_PowerBI_2025.xlsx  (58 KB)
├── Becas 2025 (962 registros) ⭐ PRINCIPAL
├── Resumen 2025 (15 KPIs)
├── Instituciones 2025 (137 registros)
├── Departamentos 2025 (39 registros)
├── Modalidades 2025 (26 registros)
├── Estratos 2025 (9 registros)
├── Migracion 2025 (4 registros)
├── Programas Becas 2025 (20 registros)
├── Carreras 2025 (51 registros)
├── Beca18 Detalle 2025 (8 registros)
├── BecaTec Detalle 2025 (10 registros)
└── Matriz Beca-Depto 2025 (20×39 matriz)
```

---

**¡Tu archivo Excel está listo para crear un dashboard profesional en Power BI! 🚀**
