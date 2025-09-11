# API de Scraping de Becas Perú

Sistema de web scraping desarrollado en Python con FastAPI para extraer, validar y comparar información de becas de estudio de fuentes oficiales en Perú.

## 🎯 Características Principales

- **Scraping Automatizado**: Extrae datos de PRONABEC, universidades y BCP
- **API REST**: Endpoints para controlar el scraping y acceder a los datos
- **Interfaz Web**: Dashboard para monitorear el proceso y visualizar resultados
- **Validación de Datos**: Compara datos scrapeados con archivo Excel de referencia
- **Base de Datos**: Almacenamiento persistente con SQLite
- **Exportación**: Datos disponibles en Excel y JSON

## 🏗️ Estructura del Proyecto

```
scraping_becas/
├── main.py                 # Aplicación principal FastAPI
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Documentación
├── scrapers/              # Módulos de scraping
│   ├── __init__.py
│   ├── pronabec_scraper.py
│   ├── universities_scraper.py
│   └── bcp_scraper.py
├── database/              # Gestión de base de datos
│   ├── __init__.py
│   └── database_manager.py
├── utils/                 # Utilidades y helpers
│   ├── __init__.py
│   └── helpers.py
├── templates/             # Plantillas HTML
│   ├── index.html
│   ├── sources.html
│   └── comparison.html
└── static/               # Archivos estáticos
    ├── style.css
    └── script.js
```

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- Google Chrome (para Selenium)
- ChromeDriver

### Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   cd scraping_becas
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # En Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar ChromeDriver**
   - Descargar ChromeDriver desde https://chromedriver.chromium.org/
   - Agregar al PATH del sistema o colocar en el directorio del proyecto

## 🎮 Uso

### Iniciar la Aplicación

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La aplicación estará disponible en: http://localhost:8000

### Endpoints de la API

#### Scraping
- `POST /scrape/all` - Scrapear todas las fuentes
- `POST /scrape/pronabec` - Scrapear solo PRONABEC
- `POST /scrape/universities` - Scrapear solo universidades
- `POST /scrape/bcp` - Scrapear solo BCP

#### Datos
- `GET /data` - Obtener todos los datos scrapeados
- `GET /status` - Estado actual del scraping
- `GET /sources` - Información de las fuentes

#### Comparación y Validación
- `POST /compare` - Comparar con Excel de referencia
- `GET /validate` - Validar datos scrapeados

#### Exportación
- `GET /export/excel` - Exportar a Excel
- `GET /export/json` - Exportar a JSON

### Interfaz Web

1. **Dashboard Principal** (`/`)
   - Monitoreo en tiempo real
   - Controles de scraping
   - Estadísticas rápidas

2. **Fuentes de Datos** (`/sources`)
   - Información detallada de cada fuente
   - Estado de las fuentes
   - Controles específicos

3. **Comparación** (`/comparison`)
   - Resultados de comparación con Excel
   - Análisis de coincidencias
   - Métricas de precisión

## 📊 Fuentes de Datos

### PRONABEC
- **URL**: https://www.pronabec.gob.pe/
- **Datos**: Becas nacionales e internacionales
- **Método**: Requests + BeautifulSoup + Selenium

### Universidades
- **Fuentes**: Múltiples universidades peruanas
- **Datos**: Becas institucionales y convenios
- **Método**: Scraping adaptativo por universidad

### BCP (Banco de Crédito del Perú)
- **URL**: Programas de becas BCP
- **Datos**: Becas de excelencia académica
- **Método**: Selenium para contenido dinámico

## 🔧 Configuración Avanzada

### Variables de Entorno

Crear archivo `.env` (opcional):
```env
DATABASE_URL=sqlite:///./becas.db
CHROME_DRIVER_PATH=/path/to/chromedriver
LOG_LEVEL=INFO
SCRAPING_DELAY=2
MAX_RETRIES=3
```

### Personalización de Scrapers

Cada scraper puede configurarse modificando los archivos en `/scrapers/`:

- **URLs objetivo**: Modificar las listas de URLs
- **Selectores CSS**: Actualizar selectores para cambios en sitios web
- **Filtros**: Ajustar criterios de filtrado de datos
- **Validaciones**: Personalizar reglas de validación

## 📈 Monitoreo y Logs

### Logs del Sistema
- Los logs se guardan en `logs/scraping.log`
- Niveles: DEBUG, INFO, WARNING, ERROR
- Rotación automática de archivos

### Base de Datos
- **Archivo**: `becas.db` (SQLite)
- **Tablas**: scholarships, excel_data, comparisons, scraping_logs
- **Backup**: Automático antes de cada scraping

## 🧪 Testing

### Ejecutar Tests
```bash
python -m pytest tests/ -v
```

### Tests Incluidos
- Tests unitarios para scrapers
- Tests de integración para API
- Tests de validación de datos
- Tests de comparación con Excel

## 🔒 Consideraciones de Seguridad

- **Rate Limiting**: Delays entre requests para evitar bloqueos
- **User Agents**: Rotación de user agents
- **Proxies**: Soporte para proxies (configuración manual)
- **Cookies**: Gestión automática de sesiones

## 🐛 Solución de Problemas

### Errores Comunes

1. **ChromeDriver no encontrado**
   ```
   Solución: Verificar instalación y PATH de ChromeDriver
   ```

2. **Timeout en scraping**
   ```
   Solución: Aumentar delays en configuración
   ```

3. **Datos no encontrados**
   ```
   Solución: Verificar selectores CSS en scrapers
   ```

4. **Error de conexión**
   ```
   Solución: Verificar conectividad y URLs objetivo
   ```

### Logs de Debug

Activar logs detallados:
```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## 📝 Contribución

### Agregar Nueva Fuente

1. Crear nuevo scraper en `/scrapers/`
2. Implementar clase heredando de base scraper
3. Agregar endpoints en `main.py`
4. Actualizar interfaz web
5. Agregar tests correspondientes

### Mejoras Sugeridas

- [ ] Scraping programado (cron jobs)
- [ ] Notificaciones por email
- [ ] Dashboard de métricas avanzadas
- [ ] API de webhooks
- [ ] Soporte para más formatos de exportación

## 📄 Licencia

Este proyecto está desarrollado para fines educativos y de investigación. Respetar los términos de uso de los sitios web scrapeados.

## 🤝 Soporte

Para reportar problemas o solicitar características:
1. Revisar logs del sistema
2. Verificar configuración
3. Consultar documentación de APIs
4. Contactar al equipo de desarrollo

---

**Nota**: Este sistema está diseñado para extraer información pública de becas con fines de investigación y comparación. Asegúrate de cumplir con los términos de uso de cada sitio web.