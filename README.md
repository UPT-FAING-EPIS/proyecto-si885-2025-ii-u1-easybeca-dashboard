[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/VMb-1xPS)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=20268708)
# 🎓 Proyecto de Inteligencia de Negocios  
**Análisis de Requisitos y Nivel de Dificultad en Becas Universitarias del Perú**  

📍 **Universidad Privada de Tacna**  
**Facultad de Ingeniería – Escuela Profesional de Ingeniería de Sistemas**  

---

## 👥 Integrantes del Equipo  
- Calizaya Ladera, Andy Michael
- Vargas Gutierrez, Angel Jose
- Colque Ponce, Sergio Alberto
- Castillo Mamani, Diego Fernadinho

---

## ❗ Problemática  
Las becas universitarias en el Perú representan una oportunidad crucial para jóvenes con talento académico y limitaciones económicas. Sin embargo, la información sobre **requisitos, procesos de postulación y beneficios** suele estar dispersa en múltiples documentos (PDFs, convocatorias web, APIs de PRONABEC), lo que dificulta evaluar:  

- ¿Qué beca es más accesible según el perfil del estudiante?  
- ¿Qué nivel de dificultad implica postular a cada una?  
- ¿Cuáles son las principales variables (académicas, socioeconómicas, cobertura) que influyen en la obtención de la beca?  

---

## 🎯 Objetivo General  
Analizar y medir el **nivel de dificultad de postulación (IDB)** en becas universitarias del Perú, integrando requisitos académicos, socioeconómicos y cobertura, mediante un enfoque de Inteligencia de Negocios.  

---

## ✅ Objetivos Específicos  
- Recolectar información real de becas (ej. **Beca BCP, PRONABEC, Beca Presidente de la República**).  
- Clasificar los requisitos en dimensiones (académicos, socioeconómicos, documentos, idioma, etc.).  
- Calcular un **Índice de Dificultad de Beca (IDB)** basado en KPIs predefinidos.  
- Diseñar dashboards interactivos que permitan comparar becas según nivel de dificultad, cobertura y beneficios.  
- Proveer un sistema de apoyo para que los estudiantes identifiquen qué becas son más accesibles a su perfil.  

---

## 🛠️ Tecnologías Utilizadas  
- **Lakehouse (Delta Lake / Databricks / Apache Iceberg)** → Integración de datos crudos (PDFs, CSV, APIs) y estructurados.  
- **Python 🐍** → Procesamiento y análisis de datos (pandas, numpy, PyPDF, requests).  
- **PostgreSQL 🐘** → Almacenamiento estructurado de la información de becas.  
- **Power BI 📊** → Dashboards interactivos para visualización de métricas.  

---

## 📡 Metodología  

### 1. Extracción de datos  
- Recolección de convocatorias en **PDFs y sitios web** oficiales.  
- Obtención de datos de **APIs de PRONABEC y universidades**.  

### 2. Procesamiento y limpieza  
- Conversión de requisitos a tablas normalizadas.  
- Clasificación en categorías:  
  - Requisitos académicos  
  - Socioeconómicos  
  - Documentos obligatorios  
  - Idiomas  
  - Beneficios y cobertura  

### 3. Cálculo de KPIs  
- **Promedio mínimo exigido**  
- **Condición socioeconómica**  
- **Documentación requerida**  
- **Cobertura de beneficios**  
- **Duración y etapas del proceso**  

### 4. Índice de Dificultad de Beca (IDB)  
Se construye a partir de ponderaciones de cada KPI.  
Ejemplo:  
IDB = (0.3 * Académicos) + (0.3 * Socioeconómicos) + (0.2 * Documentos) + (0.2 * Otros)

### 5. Visualización en Power BI  
- Comparación entre becas (IDB).  
- Ranking de becas según accesibilidad.  
- Mapas de cobertura geográfica.  
- Evolución histórica de convocatorias.  

---

## 📊 Ejemplo de Visualizaciones  
- 📈 **Gráfico comparativo**: Becas ordenadas por índice de dificultad (IDB).  
- 📊 **Radar chart**: Requisitos académicos vs. socioeconómicos por beca.  
- 🗺️ **Mapa**: Cobertura de manutención por región.  
- 📋 **Tabla dinámica**: Fechas de convocatoria y duración del proceso.

  <img width="1331" height="786" alt="image" src="https://github.com/user-attachments/assets/e9454cbe-6593-4300-b663-dff812f56b97" />
  <img width="1365" height="756" alt="image" src="https://github.com/user-attachments/assets/bd684f9e-ceb7-4c44-a6eb-f5b2c12a75c6" />


---

## 🚀 Resultados Esperados  
- Identificación de **qué becas son más accesibles** según perfil del estudiante.  
- Cálculo del **índice de dificultad estandarizado (IDB)**.  
- Dashboards que permiten explorar y comparar becas en tiempo real.  
- Herramienta de apoyo para la toma de decisiones de estudiantes, familias y orientadores académicos.  

---

## 📦 Inventario de Artefactos del Proyecto  
| Código | Nombre del Documento | Tipo | Enlace |  
|--------|----------------------|------|--------|  
| FD01   | Informe de Factibilidad | PDF / DOCX | Ver |  
| FD02   | Informe de Visión | PDF / DOCX | Ver |  
| FD03   | Especificación de Requerimientos | PDF / DOCX | Ver |  
| FD04   | Arquitectura de Software | PDF / DOCX | Ver |  
| FD05   | Proyecto Final | PDF / DOCX | Ver |  
| DASHBOARD | Dashboard Power BI | PBIX / Enlace | Ver |  
| DATA  | Diccionario de Datos | MD / DOCX | Ver |  

---

## 📌 Roadmap Futuro  
- Integrar más convocatorias y becas en la base de datos.  
- Automatizar el cálculo del índice de dificultad con **actualización en tiempo real**.  
- Incluir análisis predictivo: **probabilidad de éxito de postulación**.  
- Ampliar el sistema a becas internacionales.  

---

📎 **Video Explicativo del Proyecto (YouTube)**  
🔗 *(Se añadirá una vez grabado)*  

📊 **Dashboard en Power BI**  
🔗 *(Se añadirá el enlace cuando esté publicado)*  

