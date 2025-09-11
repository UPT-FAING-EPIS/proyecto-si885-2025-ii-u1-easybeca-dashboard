# Sistema de Scraping de Becas Perú - Integración Power BI

## Descripción del Proyecto

**Nombre del Proyecto:** BecasPerú Analytics Dashboard

Sistema integral de scraping y análisis de becas educativas en Perú con visualización en Power BI.

## Características Principales

### 🔍 Scraping Automatizado
- **BCP Becas**: Extracción de becas del Banco de Crédito del Perú
- **PRONABEC**: Scraping de becas del Programa Nacional de Becas
- **Universidades**: Recopilación de becas universitarias

### 📊 Análisis y Comparación
- Comparación automática con base de datos Excel existente
- Detección de coincidencias exactas y parciales
- Identificación de nuevas becas y becas faltantes
- Métricas de precisión y validación de datos

### 🗄️ Base de Datos
- **MySQL**: Almacenamiento principal de datos scrapeados
- **Backup SQLite**: Sistema de respaldo local
- Gestión híbrida de bases de datos

### 📈 Visualización Power BI
- Dashboard interactivo de becas
- KPIs de rendimiento del scraping
- Análisis temporal de disponibilidad de becas
- Comparativas por fuente y tipo de beca

## Estructura del Proyecto

```
BecasPerú Analytics Dashboard/
├── scraping_becas/          # Sistema principal de scraping
├── datos_powerbi/           # Archivos para Power BI
├── .venv/                   # Entorno virtual Python
└── Becas_Peru.xlsx         # Base de datos Excel de referencia
```

## Tecnologías Utilizadas

- **Backend**: Python, FastAPI, Uvicorn
- **Base de Datos**: MySQL, SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Scraping**: BeautifulSoup, Requests
- **Visualización**: Power BI Desktop
- **Análisis**: Pandas, NumPy

## Casos de Uso

1. **Monitoreo Continuo**: Seguimiento automático de nuevas becas
2. **Análisis Comparativo**: Evaluación de cobertura de becas
3. **Reportes Ejecutivos**: Dashboards para toma de decisiones
4. **Validación de Datos**: Verificación de calidad de información

## Estado del Proyecto

✅ **Completado:**
- Sistema de scraping funcional
- Integración con MySQL
- Interface web de comparación
- Exportación para Power BI

🔄 **En Desarrollo:**
- Optimización de scrapers
- Mejoras en dashboard Power BI
- Automatización de reportes

---

**Proyecto desarrollado para análisis de becas educativas en Perú**
*Integración completa con Power BI para visualización avanzada*