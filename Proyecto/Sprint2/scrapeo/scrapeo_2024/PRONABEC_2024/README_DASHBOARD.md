# Datos PRONABEC 2024 - Dashboard

## 📊 Resumen de Datos

- **Año**: 2024
- **Total de Becarios**: 727
- **Departamentos**: 26
- **Tipos de Becas**: 3
- **Instituciones**: 4

## 📁 Archivos Generados

### Datasets Principales

1. **dashboard_departamentos_2024.csv/xlsx**
   - Contiene: Distribución de becarios por departamento
   - Campos: Departamento, CantidadBecarios, AnioBecariosConfirmados

2. **dashboard_becas_2024.csv/xlsx**
   - Contiene: Tipos de becas y sus cifras
   - Campos: TipoBeca, NombreBeca, Meta, BecasOtorgadas, PorcentajeOtorgamiento

3. **dashboard_instituciones_2024.csv/xlsx**
   - Contiene: Instituciones educativas participantes
   - Campos: Institucion, AnioBecariosConfirmados

4. **dashboard_info_adicional_2024.csv/xlsx**
   - Contiene: Información adicional extraída del texto
   - Campos: Categoria, Valor, Cantidad, Pagina

5. **dashboard_estadisticas_2024.json**
   - Contiene: Estadísticas generales y top departamentos

## 🎯 Campos del Dataset

### NombreBeca
Nombre del programa de beca (Beca 18, Beca Permanencia, etc.)

### Institucion
Institución educativa donde el becario estudia o estudió

### AnioBecariosConfirmados
Año de becarios confirmados (2024)

### Departamento
Departamento donde está ubicada la institución educativa

### Carrera
Carrera financiada por la beca

### Modalidad
Categoría específica de la beca (Pregrado, Posgrado, Especiales)

### EstratoSocioeconomico
Clasificación socioeconómica (Pobre, Pobre Extrema, No Pobre)

### BecasSegunMigracion
Indica si el becario migró a otro departamento para estudiar

### CantidadBecarios
Número de becarios en la categoría

## 📈 Top 5 Departamentos con Más Becarios

1. **Lima**: 151 becarios
2. **Ica**: 93 becarios
3. **Callao**: 49 becarios
4. **Cusco**: 43 becarios
5. **Piura**: 42 becarios


## 🔍 Fuente de Datos

- **Documento**: Memoria Anual PRONABEC 2024
- **URL**: https://cdn.www.gob.pe/uploads/document/file/8154351/6826853-memoria-anual-2024%282%29.pdf
- **Fecha de extracción**: 2025-11-11

## 📝 Notas

- Los datos fueron extraídos automáticamente del PDF oficial
- Algunos campos pueden contener valores N/A si no estaban disponibles en el documento
- Los departamentos fueron normalizados para evitar duplicados
- Las cifras representan becarios del año 2024

## 🚀 Uso para Dashboard

Estos archivos están listos para ser importados en herramientas de visualización como:
- Power BI
- Tableau
- Python (Plotly, Matplotlib, Seaborn)
- R (ggplot2)
- Excel

