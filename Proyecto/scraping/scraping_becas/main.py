from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
import uvicorn
from datetime import datetime
import json
import os
from typing import List, Dict, Optional

# Importar módulos locales
from scrapers.pronabec_scraper import PronabecScraper
from scrapers.universities_scraper import UniversitiesScraper
from scrapers.bcp_scraper import BCPScraper
from database.hybrid_database_manager import HybridDatabaseManager
from utils.helpers import DataValidator, ExcelComparator
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = FastAPI(
    title="API de Scraping de Becas Perú",
    description="API para extraer y validar información de becas desde fuentes oficiales",
    version="1.0.0"
)

# Configurar archivos estáticos y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Inicializar componentes
db_manager = HybridDatabaseManager()
pronabec_scraper = PronabecScraper()
universities_scraper = UniversitiesScraper()
bcp_scraper = BCPScraper()
data_validator = DataValidator()
excel_comparator = ExcelComparator()

# Variables globales para almacenar estado
scraping_status = {
    "last_update": None,
    "total_becas_found": 0,
    "sources_scraped": [],
    "errors": []
}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal con dashboard de scraping"""
    return templates.TemplateResponse("index.html", {
        "request": request,
        "status": scraping_status,
        "last_update": scraping_status.get("last_update", "Nunca")
    })

@app.post("/api/scrape/all")
async def scrape_all_sources(background_tasks: BackgroundTasks):
    """Ejecutar scraping de todas las fuentes"""
    try:
        background_tasks.add_task(run_full_scraping)
        return {
            "message": "Scraping iniciado en segundo plano",
            "status": "started",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al iniciar scraping: {str(e)}")

@app.post("/api/scrape/pronabec")
async def scrape_pronabec():
    """Scraping específico de PRONABEC"""
    try:
        becas = await pronabec_scraper.scrape_becas()
        db_manager.save_scraped_data("PRONABEC", becas)
        
        return {
            "source": "PRONABEC",
            "becas_found": len(becas),
            "data": becas,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping PRONABEC: {str(e)}")

@app.post("/api/scrape/universities")
async def scrape_universities():
    """Scraping de universidades"""
    try:
        becas = await universities_scraper.scrape_all_universities()
        db_manager.save_scraped_data("UNIVERSIDADES", becas)
        
        return {
            "source": "UNIVERSIDADES",
            "becas_found": len(becas),
            "data": becas,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping universidades: {str(e)}")

@app.post("/api/scrape/bcp")
async def scrape_bcp():
    """Scraping específico de Banco BCP"""
    try:
        becas = await bcp_scraper.scrape_becas()
        db_manager.save_scraped_data("BCP", becas)
        
        return {
            "source": "BCP",
            "becas_found": len(becas),
            "data": becas,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping BCP: {str(e)}")

@app.get("/api/data/all")
async def get_all_data():
    """Obtener todos los datos (scrapeados y Excel)"""
    try:
        scraped_data = db_manager.get_all_scraped_data()
        excel_data = db_manager.get_excel_becas()
        
        return {
            "scraped_data": scraped_data,
            "excel_data": excel_data,
            "total_scraped": len(scraped_data),
            "total_excel": len(excel_data),
            "sources": list(set([item.get('fuente', item.get('source', '')) for item in scraped_data]))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo datos: {str(e)}")

@app.get("/api/data/excel")
async def get_excel_data():
    """Obtener datos del Excel"""
    try:
        excel_data = db_manager.get_excel_becas()
        return {
            "total_records": len(excel_data),
            "data": excel_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo datos de Excel: {str(e)}")

@app.get("/api/data")
async def get_scraped_data(source: Optional[str] = None):
    """Obtener datos scrapeados (con filtro opcional por fuente)"""
    try:
        if source:
            data = db_manager.get_scraped_data_by_source(source)
        else:
            data = db_manager.get_all_scraped_data()
        
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo datos: {str(e)}")

@app.get("/api/compare/excel")
async def compare_with_excel():
    """Comparar datos scrapeados con Excel original"""
    try:
        excel_path = "../Becas_Peru.xlsx"
        scraped_data = db_manager.get_all_scraped_data()
        
        if not scraped_data:
            return {
                "message": "No hay datos scrapeados para comparar",
                "comparison_result": None,
                "timestamp": datetime.now().isoformat()
            }
        
        comparison = excel_comparator.compare_with_excel(scraped_data, excel_path)
        
        return {
            "comparison_result": comparison,
            "total_scraped": len(scraped_data),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparando con Excel: {str(e)}")

@app.get("/api/compare")
async def compare_data():
    """Comparar datos scrapeados con Excel (endpoint simplificado)"""
    try:
        excel_path = "../Becas_Peru.xlsx"
        scraped_data = db_manager.get_all_scraped_data()
        
        if not scraped_data:
            return {
                "message": "No hay datos scrapeados para comparar",
                "comparison_result": None,
                "timestamp": datetime.now().isoformat()
            }
        
        comparison = excel_comparator.compare_with_excel(scraped_data, excel_path)
        
        return {
            "comparison_result": comparison,
            "total_scraped": len(scraped_data),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparando datos: {str(e)}")

@app.get("/api/validate/data")
async def validate_scraped_data():
    """Validar calidad de datos scrapeados"""
    try:
        data = db_manager.get_all_data()
        validation_result = data_validator.validate_data(data)
        
        return {
            "validation_result": validation_result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validando datos: {str(e)}")

@app.get("/api/status")
async def get_scraping_status():
    """Obtener estado actual del scraping"""
    return scraping_status

@app.post("/api/load-excel")
async def load_excel_data():
    """Cargar datos del archivo Excel a la base de datos"""
    try:
        excel_path = "../Becas_Peru.xlsx"
        if not os.path.exists(excel_path):
            raise HTTPException(status_code=404, detail="Archivo Excel no encontrado")
        
        inserted_count = db_manager.load_excel_data(excel_path)
        
        return {
            "message": "Datos del Excel cargados exitosamente",
            "records_inserted": inserted_count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cargando Excel: {str(e)}")

@app.get("/sources", response_class=HTMLResponse)
async def sources_page(request: Request):
    """Página de fuentes de datos"""
    sources_info = [
        {
            "name": "PRONABEC",
            "url": "https://www.pronabec.gob.pe",
            "description": "Programa Nacional de Becas y Crédito Educativo",
            "status": "active"
        },
        {
            "name": "Universidad César Vallejo",
            "url": "https://www.ucv.edu.pe",
            "description": "Becas institucionales UCV",
            "status": "active"
        },
        {
            "name": "PUCP",
            "url": "https://www.pucp.edu.pe",
            "description": "Becas Pontificia Universidad Católica del Perú",
            "status": "active"
        },
        {
            "name": "Banco BCP",
            "url": "https://www.viabcp.com",
            "description": "Programa de Becas BCP",
            "status": "active"
        }
    ]
    
    return templates.TemplateResponse("sources.html", {
        "request": request,
        "sources": sources_info
    })

@app.get("/comparison", response_class=HTMLResponse)
async def comparison_page(request: Request):
    """Página de comparación con Excel"""
    return templates.TemplateResponse("comparison.html", {
        "request": request
    })

async def run_full_scraping():
    """Ejecutar scraping completo de todas las fuentes"""
    global scraping_status
    
    try:
        scraping_status["errors"] = []
        scraping_status["sources_scraped"] = []
        total_becas = 0
        
        # Scraping PRONABEC
        try:
            becas_pronabec = await pronabec_scraper.scrape_becas()
            db_manager.save_scraped_data("PRONABEC", becas_pronabec)
            scraping_status["sources_scraped"].append("PRONABEC")
            total_becas += len(becas_pronabec)
        except Exception as e:
            scraping_status["errors"].append(f"PRONABEC: {str(e)}")
        
        # Scraping Universidades
        try:
            becas_unis = await universities_scraper.scrape_all_universities()
            db_manager.save_scraped_data("UNIVERSIDADES", becas_unis)
            scraping_status["sources_scraped"].append("UNIVERSIDADES")
            total_becas += len(becas_unis)
        except Exception as e:
            scraping_status["errors"].append(f"UNIVERSIDADES: {str(e)}")
        
        # Scraping BCP
        try:
            becas_bcp = await bcp_scraper.scrape_becas()
            db_manager.save_scraped_data("BCP", becas_bcp)
            scraping_status["sources_scraped"].append("BCP")
            total_becas += len(becas_bcp)
        except Exception as e:
            scraping_status["errors"].append(f"BCP: {str(e)}")
        
        scraping_status["last_update"] = datetime.now().isoformat()
        scraping_status["total_becas_found"] = total_becas
        
    except Exception as e:
        scraping_status["errors"].append(f"Error general: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)