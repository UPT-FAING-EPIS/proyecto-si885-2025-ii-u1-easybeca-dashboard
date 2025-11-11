# Scraper de Beca 18

Este proyecto permite extraer información sobre las universidades elegibles para la Beca 18 y los promedios mínimos requeridos para acceder a cada una.

## Características

- Extrae lista de universidades elegibles para Beca 18
- Obtiene promedios mínimos por modalidad (EBR, EBA, EBE)
- Guarda los datos en formato CSV y JSON
- Manejo de errores y rate limiting
- Interfaz simple de línea de comandos

## Instalación

1. Clona o descarga este repositorio
2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Uso

### Uso básico

```python
from beca18_scraper import Beca18Scraper

# Crear instancia del scraper
scraper = Beca18Scraper()

# Ejecutar scraping completo
scraper.run_scraping()
```

### Ejecutar desde línea de comandos

```bash
python beca18_scraper.py
```

### Métodos disponibles

- `get_eligible_universities()`: Obtiene lista de universidades elegibles
- `get_minimum_grades()`: Obtiene promedios mínimos por modalidad
- `save_to_csv(data, filename)`: Guarda datos en formato CSV
- `save_to_json(data, filename)`: Guarda datos en formato JSON
- `run_scraping()`: Ejecuta el proceso completo de scraping

## Archivos de salida

El scraper genera los siguientes archivos:

- `universidades_beca18.csv`: Lista de universidades en formato CSV
- `universidades_beca18.json`: Lista de universidades en formato JSON
- `promedios_minimos.csv`: Promedios mínimos por modalidad en CSV
- `promedios_minimos.json`: Promedios mínimos por modalidad en JSON

## Estructura de datos

### Universidades
```json
{
  "nombre": "Universidad Nacional Mayor de San Marcos",
  "tipo": "Pública",
  "ubicacion": "Lima",
  "estado": "Licenciada"
}
```

### Promedios mínimos
```json
{
  "modalidad": "EBR",
  "requisito": "Tercio superior",
  "promedio_minimo": "14.0",
  "descripcion": "Estudiantes del tercio superior de su promoción"
}
```

## Modalidades de Beca 18

- **EBR (Educación Básica Regular)**: Tercio superior o medio superior
- **EBA (Educación Básica Alternativa)**: Promedio mínimo de 14
- **EBE (Educación Básica Especial)**: Promedio mínimo de 12

## Requisitos del sistema

- Python 3.7 o superior
- Conexión a internet
- Librerías especificadas en requirements.txt

## Limitaciones Actuales

### Datos de Universidades
- **Lista Parcial**: El scraper incluye solo una muestra de universidades conocidas
- **Lista Completa Oficial**: Se encuentra en la Resolución Jefatural N° 1393-2024 de PRONABEC
- **Criterio de Elegibilidad**: Son elegibles todas las instituciones de educación superior licenciadas por SUNEDU o MINEDU hasta el 13 de septiembre de 2024
- **Actualización Manual**: La lista de universidades requiere actualización manual basada en documentos oficiales

### Promedios por Universidad
- **No Disponibles**: Los promedios mínimos específicos por universidad no están públicamente disponibles
- **Solo por Modalidad**: El sistema actual proporciona promedios por modalidad de beca, no por institución
- **Variabilidad**: Los promedios pueden variar según la demanda y disponibilidad de cupos por universidad

### Fuentes de Información
- **PRONABEC**: Fuente oficial para bases, requisitos y listas de instituciones
- **SUNEDU**: Licenciamiento de universidades
- **MINEDU**: Licenciamiento de institutos y escuelas superiores
- **Limitación de Scraping**: Algunos datos requieren acceso a sistemas internos de PRONABEC

## Notas importantes

- El scraper incluye delays entre requests para evitar sobrecargar los servidores
- Los datos se basan en información oficial de PRONABEC
- La información puede cambiar según las convocatorias anuales
- **IMPORTANTE**: Siempre verificar la información en fuentes oficiales de PRONABEC
- Para la lista completa de universidades, consultar la RJ 1393-2024
- Los promedios específicos por universidad no son públicos y pueden variar por convocatoria

## Soporte

Para reportar problemas o sugerencias, por favor revisa la documentación oficial de Beca 18 en:
- https://www.pronabec.gob.pe/
- https://www.gob.pe/pronabec

## Licencia

Este proyecto es de uso educativo y personal. Respeta los términos de uso de los sitios web consultados.