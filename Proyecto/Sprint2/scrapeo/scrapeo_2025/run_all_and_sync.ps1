Param(
    [string]$Repo = "C:\Users\Angel\Desktop\scrapeo_universidad"
)

$ErrorActionPreference = "Stop"
Set-Location $Repo

# Ejecutar scrapers (ajusta si alguno no aplica)
python beca18_scraper.py
python becas_integrales_scraper.py
python becas_instituciones_scraper.py
python generar_instituciones_becas.py

# Copiar resultados a OneDrive/SharePoint
python sync_to_onedrive.py

# Refrescar datasets en Power BI (My Workspace)
python powerbi_refresh.py --workspace "My Workspace" --dataset "scraping"

# Intentar refrescar el dataset de Mapas (renombrado o anterior)
$datasetsToTry = @("Proyecto - Mapas ya incluidos ACTUAL - PERU", "Proyecto - Mapas ya incluidos ACTUAL")
foreach ($dn in $datasetsToTry) {
  Write-Host "Intentando refrescar dataset: $dn"
  python powerbi_refresh.py --workspace "My Workspace" --dataset "$dn"
  if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Refresh lanzado con '$dn'"
    break
  } else {
    Write-Warning "Falló el refresh para '$dn' (exit $LASTEXITCODE). Probando siguiente..."
  }
}