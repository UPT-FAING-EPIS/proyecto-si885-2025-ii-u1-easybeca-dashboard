# Web Scraping - Beca 18 - 2023

## 📋 Descripción

Este proyecto extrae datos de la **Memoria Anual del Pronabec 2023** específicamente sobre el programa **Beca 18** para el año 2023. Los datos fueron extraídos desde el PDF oficial disponible en:

🔗 https://cdn.www.gob.pe/uploads/document/file/6317263/5552590-memoria-anual-del-pronabec-2023.pdf

## 🎯 Objetivo

Extraer datos estructurados del año 2023 para crear un dashboard con la siguiente información:
- Nombre del programa de becas
- Instituciones educativas
- Año de becarios confirmados
- Departamento de procedencia
- Carreras financiadas
- Modalidades de beca
- Estrato socioeconómico
- Migración de becarios

## 📊 Datos Extraídos

### Resumen General - Beca 18 - 2023
- **Total de becas otorgadas**: 4,998 becas
- **Meta establecida**: 5,000 becas
- **Cobertura**: 10.2% del total de postulantes aptos
- **Becas para universidades**: 3,991
- **Becas para institutos y escuelas**: 1,007

### Información Detallada

#### 1. **Becarios por Departamento** (25 departamentos)
Los 5 departamentos con más becarios:
- Lima: 905 becarios (18.11%)
- Puno: 362 becarios (7.24%)
- Cusco: 305 becarios (6.10%)
- Junín: 279 becarios (5.58%)
- Cajamarca: 261 becarios (5.22%)

#### 2. **Modalidades de Beca** (8 modalidades)
- Beca 18 Ordinaria (modalidad principal)
- Beca Huallaga
- Beca Vraem
- Beca CNA y PA (Comunidad Nativa Amazónica y Población Afroperuana)
- Beca Protección
- Beca EIB (Educación Intercultural Bilingüe)
- Beca FF.AA. (Fuerzas Armadas)
- Beca Repared

#### 3. **Migración de Becarios**
- **Becarios que migraron**: 2,152 (43.1%)
- **Becarios que no migraron**: 2,846 (56.9%)
- **Destino principal de migración**: Lima (88.9% de los migrantes)

#### 4. **Carreras Principales** (9 carreras más elegidas)
1. Medicina Humana
2. Ingeniería Civil
3. Derecho
4. Ingeniería Industrial
5. Arquitectura
6. Ingeniería de Sistemas
7. Administración
8. Contabilidad
9. Educación

#### 5. **Instituciones Educativas Principales** (7 instituciones)
1. Universidad Peruana de Ciencias Aplicadas (UPC)
2. Universidad Científica del Sur
3. Pontificia Universidad Católica del Perú (PUCP)
4. Servicio Nacional de Adiestramiento en Trabajo Industrial (SENATI)
5. Universidad Peruana Cayetano Heredia
6. Universidad Continental
7. Universidad Nacional San Antonio Abad del Cusco

#### 6. **Estrato Socioeconómico**
Todos los becarios son clasificados como:
- **Pobre** o **Pobre Extremo** según el SISFOH (Sistema de Focalización de Hogares)

## 📁 Archivos Generados

### Archivos CSV (formato tabla)
1. `beca18_2023_resumen_general.csv` - Resumen general del programa
2. `beca18_2023_becarios_por_departamento.csv` - Distribución por departamento
3. `beca18_2023_modalidades.csv` - Modalidades de beca disponibles
4. `beca18_2023_migracion.csv` - Datos de migración de becarios
5. `beca18_2023_carreras_principales.csv` - Carreras más elegidas
6. `beca18_2023_instituciones_principales.csv` - Instituciones principales
7. `beca18_2023_estrato_socioeconomico.csv` - Información socioeconómica

### Archivo Excel (todos los datos)
- `beca18_2023_datos_completos.xlsx` - Contiene todos los datasets en hojas separadas

### Archivos JSON
- `beca18_2023_resumen.json` - Resumen en formato JSON
- `datos_pronabec_2023.json` - Datos extraídos del procesamiento inicial

### Archivos de texto
- `texto_completo_pronabec_2023.txt` - Texto completo extraído del PDF (112 páginas)

## 🛠️ Instalación y Uso

### Requisitos
```bash
Python 3.8+
requests
PyPDF2
pandas
openpyxl
```

### Instalación de dependencias
```bash
pip install -r requirements.txt
```

### Ejecución

#### 1. Descargar y extraer texto del PDF:
```bash
python scraper_pronabec_2023.py
```

Este script:
- Descarga el PDF de la Memoria Anual 2023
- Extrae el texto de todas las páginas (112 páginas)
- Guarda el texto completo en `texto_completo_pronabec_2023.txt`
- Identifica menciones relevantes de Beca 18

#### 2. Generar datasets estructurados:
```bash
python extraer_datos_beca18_2023.py
```

Este script:
- Lee el texto extraído del PDF
- Estructura los datos en datasets organizados
- Genera archivos CSV para cada categoría de datos
- Crea un archivo Excel con todos los datos
- Guarda resúmenes en formato JSON

## 📈 Uso de los Datos para Dashboard

Los archivos CSV y Excel generados están listos para ser importados en herramientas de visualización como:

- **Power BI**: Importar el archivo Excel o archivos CSV individuales
- **Tableau**: Conectar directamente a los archivos CSV
- **Python (Matplotlib/Plotly/Seaborn)**: Leer con pandas
- **R (ggplot2)**: Importar con read.csv()
- **Google Data Studio**: Subir archivos CSV

### Ejemplo de uso con Python/Pandas:
```python
import pandas as pd

# Cargar datos
resumen = pd.read_csv('beca18_2023_resumen_general.csv')
departamentos = pd.read_csv('beca18_2023_becarios_por_departamento.csv')
migracion = pd.read_csv('beca18_2023_migracion.csv')

# O cargar todo desde Excel
datos_completos = pd.read_excel('beca18_2023_datos_completos.xlsx', sheet_name=None)
```

## 📊 Estructura de los Datos

### beca18_2023_resumen_general.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| NombreBeca | String | Nombre del programa (Beca 18) |
| Anio | Integer | Año (2023) |
| TotalBecasOtorgadas | Integer | Total de becas otorgadas |
| MetaBecas | Integer | Meta establecida |
| Cobertura% | Float | Porcentaje de cobertura |
| BecasUniversidades | Integer | Becas para universidades |
| BecasInstitutosEscuelas | Integer | Becas para institutos y escuelas |

### beca18_2023_becarios_por_departamento.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| NombreBeca | String | Nombre del programa |
| Anio | Integer | Año (2023) |
| Departamento | String | Nombre del departamento |
| CantidadBecarios | Integer | Cantidad de becarios |
| Porcentaje | Float | Porcentaje del total |

### beca18_2023_modalidades.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| NombreBeca | String | Nombre del programa |
| Anio | Integer | Año (2023) |
| Modalidad | String | Nombre de la modalidad |
| Descripcion | String | Descripción de la modalidad |

### beca18_2023_migracion.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| NombreBeca | String | Nombre del programa |
| Anio | Integer | Año (2023) |
| EstadoMigracion | String | "Migró" o "No Migró" |
| CantidadBecarios | Integer | Cantidad de becarios |
| Porcentaje | Float | Porcentaje del total |
| DestinoMayoritario | String | Destino principal |

### beca18_2023_carreras_principales.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| NombreBeca | String | Nombre del programa |
| Anio | Integer | Año (2023) |
| Carrera | String | Nombre de la carrera |
| Ranking | Integer | Posición en el ranking |

### beca18_2023_instituciones_principales.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| NombreBeca | String | Nombre del programa |
| Anio | Integer | Año (2023) |
| Institucion | String | Nombre de la institución |
| Ranking | Integer | Posición en el ranking |

### beca18_2023_estrato_socioeconomico.csv
| Campo | Tipo | Descripción |
|-------|------|-------------|
| NombreBeca | String | Nombre del programa |
| Anio | Integer | Año (2023) |
| EstratoSocioeconomico | String | "Pobre" o "Pobre Extremo" |
| Nota | String | Información adicional |

## 📝 Notas Importantes

1. **Fuente de datos**: Memoria Anual del Pronabec 2023 (documento oficial)
2. **Año de datos**: 2023 exclusivamente
3. **Fecha de extracción**: Noviembre 2025
4. **Formato del PDF**: 112 páginas
5. **Tipo de extracción**: Texto plano del PDF + estructuración manual de datos

## ⚠️ Limitaciones

- Algunos datos específicos (como distribución exacta por institución o carrera) no están disponibles en el PDF público
- Los datos de departamentos son aproximados basados en el gráfico del documento
- El PDF no proporciona un desglose detallado de cada becario individual

## 📞 Contacto

Para más información sobre Beca 18:
- **Web**: www.gob.pe/pronabec
- **Línea gratuita**: 0800 000 18
- **WhatsApp**: 914 121 106

## 📜 Licencia

Los datos extraídos son de dominio público y provienen de documentos oficiales del Gobierno del Perú (Pronabec).

---

**Última actualización**: Noviembre 2025
**Versión**: 1.0
