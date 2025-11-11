# Diccionario de Datos - Becas Pronabec 2020

Este documento describe los datasets generados a partir de la Memoria Anual del Pronabec 2020.

## Archivos Generados

### 1. beca18_por_departamento_2020.csv / .xlsx
Datos de becarios de Beca 18 distribuidos por departamento.

**Campos:**
- `NombreBeca`: Nombre del programa (Beca 18)
- `AnioBecariosConfirmados`: Año de los datos (2020)
- `Departamento`: Departamento de procedencia u origen del becario
- `BecariosNuevos`: Número de becarios nuevos en 2020
- `BecariosContinuadores`: Número de becarios que continúan sus estudios
- `TotalBecarios`: Total de becarios (nuevos + continuadores)
- `Modalidad`: Categoría de la beca (Beca 18)

**Registros:** 25 (uno por cada departamento del Perú)

---

### 2. beca18_por_carrera_2020.csv / .xlsx
Datos de becarios de Beca 18 distribuidos por área de estudio.

**Campos:**
- `NombreBeca`: Nombre del programa (Beca 18)
- `AnioBecariosConfirmados`: Año de los datos (2020)
- `Carrera`: Área de estudio o carrera profesional
- `BecariosNuevos`: Número de becarios nuevos en 2020
- `BecariosContinuadores`: Número de becarios que continúan sus estudios
- `TotalBecarios`: Total de becarios (nuevos + continuadores)
- `Modalidad`: Categoría de la beca (Beca 18)

**Registros:** 8 áreas de estudio principales
- Educación
- Humanidades y Arte
- Ciencias Sociales, Comerciales y Derecho
- Ciencias Naturales, Exactas y de la Computación
- Ingeniería, Industria y Construcción
- Agropecuaria y Veterinaria
- Ciencias de la Salud
- Servicios

---

### 3. beca18_por_institucion_2020.csv / .xlsx
Datos de becarios de Beca 18 distribuidos por tipo de institución educativa.

**Campos:**
- `NombreBeca`: Nombre del programa (Beca 18)
- `AnioBecariosConfirmados`: Año de los datos (2020)
- `Institucion`: Tipo de institución educativa
- `BecariosNuevos`: Número de becarios nuevos en 2020
- `BecariosContinuadores`: Número de becarios que continúan sus estudios
- `TotalBecarios`: Total de becarios (nuevos + continuadores)
- `Modalidad`: Categoría de la beca (Beca 18)

**Registros:** 3 tipos de instituciones
- Universidad
- Instituto superior tecnológico
- Instituto superior pedagógico

---

### 4. beca_posgrado_por_pais_2020.csv / .xlsx
Datos de becarios de posgrado distribuidos por país de estudio.

**Campos:**
- `NombreBeca`: Nombre del programa (Beca Posgrado)
- `AnioBecariosConfirmados`: Año de los datos (2020)
- `PaisEstudio`: País donde se realizan los estudios de posgrado
- `BecariosNuevos`: Número de becarios nuevos en 2020
- `BecariosContinuadores`: Número de becarios que continúan sus estudios
- `TotalBecarios`: Total de becarios (nuevos + continuadores)
- `Modalidad`: Categoría de la beca (Beca Posgrado Internacional)

**Registros:** 18 países

---

### 5. beca_posgrado_por_programa_2020.csv / .xlsx
Datos de becarios de posgrado distribuidos por tipo de programa.

**Campos:**
- `NombreBeca`: Nombre del programa (Beca Posgrado)
- `AnioBecariosConfirmados`: Año de los datos (2020)
- `TipoPrograma`: Tipo de programa de posgrado (Maestría o Doctorado)
- `BecariosNuevos`: Número de becarios nuevos en 2020
- `BecariosContinuadores`: Número de becarios que continúan sus estudios
- `TotalBecarios`: Total de becarios (nuevos + continuadores)
- `Modalidad`: Categoría de la beca (Beca Posgrado Internacional)

**Registros:** 2 (Maestría y Doctorado)

---

### 6. becarios_continuadores_por_modalidad_2020.csv / .xlsx
Datos de becarios continuadores por diferentes modalidades de becas.

**Campos:**
- `NombreBeca`: Nombre específico de la beca
- `AnioBecariosConfirmados`: Año de los datos (2020)
- `BecariosContinuadores`: Número de becarios que continúan sus estudios
- `Modalidad`: Categoría de la beca

**Registros:** 7 modalidades diferentes incluyendo:
- Beca Complementaria de la Amistad Peruano Ecuatoriana
- Beca de Permanencia de Estudios Nacional Arte
- Beca Excelencia Académica
- Beca Excelencia Internacional Francia
- Vocación de Maestro
- Entre otras

---

### 7. creditos_educativos_2020.csv / .xlsx
Datos de créditos educativos otorgados en 2020.

**Campos:**
- `TipoCredito`: Modalidad del crédito educativo
- `AnioBecariosConfirmados`: Año de los datos (2020)
- `CantidadCreditos`: Número de créditos otorgados
- `MontoDesembolsado`: Monto total desembolsado en soles (S/)
- `Modalidad`: Categoría (Crédito Educativo)

**Registros:** 4 modalidades de créditos

---

### 8. datos_becas_consolidado_2020.csv / .xlsx
Dataset consolidado con información general de becas.

**Campos:**
- `NombreBeca`: Nombre del programa de becas
- `Institucion`: Tipo de institución (cuando aplica)
- `AnioBecariosConfirmados`: Año de los datos (2020)
- `Departamento`: Departamento de procedencia
- `Carrera`: Área de estudio o carrera
- `Modalidad`: Categoría específica de la beca
- `BecariosNuevos`: Número de becarios nuevos
- `BecariosContinuadores`: Número de becarios continuadores
- `TotalBecarios`: Total de becarios

---

## Información Adicional

### Archivos JSON Auxiliares
- `tablas_extraidas.json`: Todas las tablas extraídas del PDF original
- `texto_extraido.json`: Texto completo extraído del PDF

### Notas Importantes

1. **Año de Datos**: Todos los datos corresponden al año 2020
2. **Fuente**: Memoria Anual del Pronabec 2020
3. **Becarios Nuevos**: Estudiantes que inician su beca en 2020
4. **Becarios Continuadores**: Estudiantes que iniciaron su beca en años anteriores y continúan en 2020
5. **Total Becarios**: Suma de becarios nuevos y continuadores

### Campos No Extraídos
Los siguientes campos solicitados no pudieron ser extraídos del PDF con el nivel de detalle requerido:
- **Estrato socioeconómico individual**: El documento contiene información agregada pero no desagregada por becario
- **Migración individual**: El documento menciona migración pero no proporciona datos detallados por becario

Estos datos podrían estar disponibles en otros documentos del Pronabec o bases de datos internas.

---

## Uso para Dashboard

Estos datasets son ideales para crear visualizaciones en dashboards que muestren:

1. **Distribución Geográfica**: Mapa de becarios por departamento
2. **Áreas de Estudio**: Gráficos de distribución por carrera
3. **Tipos de Institución**: Comparación entre universidades e institutos
4. **Tendencias Internacionales**: Becas de posgrado por país
5. **Modalidades de Beca**: Comparación entre diferentes programas
6. **Análisis Financiero**: Montos de créditos educativos

---

## Contacto y Soporte

Para más información sobre los datos o para reportar problemas, consultar la documentación oficial de Pronabec.
