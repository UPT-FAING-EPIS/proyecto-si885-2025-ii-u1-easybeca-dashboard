# Scraper Pronabec 2020

Este proyecto extrae datos de becas del documento "Memoria Anual del Pronabec 2020".

## Campos Extraídos

- **NombreBeca**: Nombre del programa de becas
- **Institucion**: Institución donde el becario estudió o estudia
- **AnioBecariosConfirmados**: Año de becarios confirmados (2020)
- **Departamento**: Departamento donde está ubicada la institución educativa
- **Carrera**: Carrera financiada por la beca
- **Modalidad**: Categoría específica de la beca
- **Estrato socioeconómico**: Clasificación social (pobre, pobre extrema, no pobre)
- **Becas según migración**: Becarios que migraron o no migraron a otro departamento

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python scraper_pronabec_2020.py
```

## Archivos Generados

- `texto_extraido.json`: Texto completo extraído del PDF
- `tablas_extraidas.json`: Todas las tablas encontradas en el PDF
- `becas_pronabec_2020.csv`: Datos estructurados de becas (si se encuentran)
- `becas_pronabec_2020.json`: Datos en formato JSON

## Notas

El script primero extrae todo el contenido del PDF y lo guarda en archivos JSON para su análisis. Luego, puedes ajustar el parser según la estructura específica de las tablas encontradas.
