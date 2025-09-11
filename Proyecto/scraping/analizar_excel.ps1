# Script para analizar Excel de Becas Peru y preparar datos para Power BI

# Importar el modulo ImportExcel
try {
    Import-Module ImportExcel -ErrorAction Stop
    Write-Host "Modulo ImportExcel cargado correctamente" -ForegroundColor Green
} catch {
    Write-Host "Error: No se pudo cargar el modulo ImportExcel" -ForegroundColor Red
    Write-Host "Ejecuta: Install-Module -Name ImportExcel -Force -Scope CurrentUser" -ForegroundColor Yellow
    exit 1
}

# Variables
$ArchivoExcel = "Becas_Peru.xlsx"
$CarpetaPowerBI = "datos_powerbi"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "ANALISIS DEL ARCHIVO EXCEL: $ArchivoExcel" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Verificar si el archivo existe
if (-not (Test-Path $ArchivoExcel)) {
    Write-Host "Error: El archivo $ArchivoExcel no existe" -ForegroundColor Red
    exit 1
}

try {
    # Obtener informacion de las hojas
    $hojas = Get-ExcelSheetInfo -Path $ArchivoExcel
    Write-Host "\nHOJAS ENCONTRADAS:" -ForegroundColor Yellow
    Write-Host "------------------------------" -ForegroundColor Yellow
    
    foreach ($hoja in $hojas) {
        Write-Host "• $($hoja.Name) - $($hoja.Rows) filas" -ForegroundColor White
    }
    
    # Crear carpeta para datos de Power BI
    if (-not (Test-Path $CarpetaPowerBI)) {
        New-Item -ItemType Directory -Path $CarpetaPowerBI | Out-Null
        Write-Host "\nCarpeta '$CarpetaPowerBI' creada" -ForegroundColor Green
    }
    
    # Analizar cada hoja
    $metadatos = @()
    
    foreach ($hoja in $hojas) {
        Write-Host "\n==================================================" -ForegroundColor Magenta
        Write-Host "ANALIZANDO HOJA: $($hoja.Name)" -ForegroundColor Magenta
        Write-Host "==================================================" -ForegroundColor Magenta
        
        # Leer datos de la hoja
        $datos = Import-Excel -Path $ArchivoExcel -WorksheetName $hoja.Name
        
        if ($datos.Count -eq 0) {
            Write-Host "La hoja '$($hoja.Name)' esta vacia" -ForegroundColor Yellow
            continue
        }
        
        # Informacion basica
        $filas = $datos.Count
        $propiedades = $datos[0].PSObject.Properties | Where-Object {$_.Name -notlike "*RowError*" -and $_.Name -notlike "*ItemArray*" -and $_.Name -notlike "*Table*" -and $_.Name -notlike "*HasErrors*"}
        $columnas = $propiedades.Count
        
        Write-Host "Dimensiones: $filas filas x $columnas columnas" -ForegroundColor White
        
        # Obtener nombres de columnas
        $nombresColumnas = $propiedades | Select-Object -ExpandProperty Name
        
        Write-Host "\nCOLUMNAS ENCONTRADAS:" -ForegroundColor Yellow
        Write-Host "-------------------------" -ForegroundColor Yellow
        
        foreach ($col in $nombresColumnas) {
            # Contar valores no nulos
            $valoresNoNulos = ($datos | Where-Object {$_.$col -ne $null -and $_.$col -ne ""}).Count
            $valoresNulos = $filas - $valoresNoNulos
            $porcentajeNulos = if ($filas -gt 0) { [math]::Round(($valoresNulos / $filas) * 100, 2) } else { 0 }
            
            # Contar valores unicos
            $valoresUnicos = ($datos | Select-Object -Property $col -Unique | Where-Object {$_.$col -ne $null -and $_.$col -ne ""}).Count
            
            Write-Host "  • $col" -ForegroundColor White
            Write-Host "    - Valores nulos: $valoresNulos ($porcentajeNulos por ciento)" -ForegroundColor Gray
            Write-Host "    - Valores unicos: $valoresUnicos" -ForegroundColor Gray
            
            # Agregar a metadatos
            $metadatos += [PSCustomObject]@{
                Tabla = $hoja.Name
                Columna = $col
                Total_Filas = $filas
                Valores_Nulos = $valoresNulos
                Porcentaje_Nulos = $porcentajeNulos
                Valores_Unicos = $valoresUnicos
            }
            
            # Mostrar algunos valores unicos si son pocos
            if ($valoresUnicos -le 10 -and $valoresUnicos -gt 0) {
                $ejemplos = $datos | Select-Object -Property $col -Unique | Where-Object {$_.$col -ne $null -and $_.$col -ne ""} | Select-Object -First 5 -ExpandProperty $col
                Write-Host "    - Ejemplos: $($ejemplos -join ', ')" -ForegroundColor Cyan
            }
        }
        
        # Mostrar primeras filas
        Write-Host "\nPRIMERAS 3 FILAS:" -ForegroundColor Yellow
        Write-Host "--------------------" -ForegroundColor Yellow
        $datos | Select-Object -First 3 | Format-Table -AutoSize
        
        # Guardar como CSV para Power BI
        $nombreArchivo = $hoja.Name -replace '[^a-zA-Z0-9_]', '_'
        $rutaCSV = Join-Path $CarpetaPowerBI "$nombreArchivo.csv"
        $datos | Export-Csv -Path $rutaCSV -NoTypeInformation -Encoding UTF8
        Write-Host "Guardado CSV: $rutaCSV" -ForegroundColor Green
        
        # Guardar como Excel limpio
        $rutaExcel = Join-Path $CarpetaPowerBI "$nombreArchivo`_limpio.xlsx"
        $datos | Export-Excel -Path $rutaExcel -AutoSize -TableStyle Medium2
        Write-Host "Guardado Excel: $rutaExcel" -ForegroundColor Green
    }
    
    # Guardar metadatos
    $rutaMetadatos = Join-Path $CarpetaPowerBI "metadatos_tablas.xlsx"
    $metadatos | Export-Excel -Path $rutaMetadatos -AutoSize -TableStyle Medium6 -Title "Metadatos de Tablas - Becas Peru"
    Write-Host "\nMetadatos guardados: $rutaMetadatos" -ForegroundColor Green
    
    # Crear archivo de instrucciones
    $fecha = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    $instrucciones = @"
# INSTRUCCIONES PARA POWER BI - BECAS PERU
# Generado el: $fecha

## ARCHIVOS PREPARADOS:

"@
    
    foreach ($hoja in $hojas) {
        $nombreArchivo = $hoja.Name -replace '[^a-zA-Z0-9_]', '_'
        $instrucciones += @"

### Tabla: $($hoja.Name)
- Archivo CSV: $nombreArchivo.csv
- Archivo Excel: $nombreArchivo`_limpio.xlsx
- Filas: $($hoja.Rows)
"@
    }
    
    $instrucciones += @"


## PASOS PARA IMPORTAR EN POWER BI:

1. Abrir Power BI Desktop
2. Hacer clic en "Obtener datos" > "Texto/CSV" o "Excel"
3. Navegar a la carpeta '$CarpetaPowerBI'
4. Seleccionar los archivos CSV o Excel que necesites
5. Revisar y transformar los datos en Power Query si es necesario
6. Cargar los datos al modelo de Power BI

## RECOMENDACIONES:

- Usar archivos CSV para mejor rendimiento
- Revisar los tipos de datos en Power Query Editor
- Crear relaciones entre tablas si es necesario
- Verificar la calidad de los datos usando el archivo de metadatos
- Configurar actualizaciones automaticas si los datos cambian frecuentemente

## ARCHIVOS INCLUIDOS:

- metadatos_tablas.xlsx: Informacion detallada sobre cada columna
- INSTRUCCIONES_POWERBI.txt: Este archivo con instrucciones
- *.csv: Archivos de datos en formato CSV
- *_limpio.xlsx: Archivos de datos en formato Excel

## TIPS ADICIONALES:

- Si tienes problemas con caracteres especiales, usa los archivos CSV
- Para mejor rendimiento, importa solo las columnas que necesites
- Considera crear medidas DAX para calculos complejos
- Usa filtros para mejorar el rendimiento de los reportes
"@
    
    $rutaInstrucciones = Join-Path $CarpetaPowerBI "INSTRUCCIONES_POWERBI.txt"
    $instrucciones | Out-File -FilePath $rutaInstrucciones -Encoding UTF8
    Write-Host "Instrucciones guardadas: $rutaInstrucciones" -ForegroundColor Green
    
    Write-Host "\n============================================================" -ForegroundColor Green
    Write-Host "ANALISIS COMPLETADO EXITOSAMENTE" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "\nTodos los archivos estan en la carpeta: $CarpetaPowerBI" -ForegroundColor Cyan
    Write-Host "Revisa 'INSTRUCCIONES_POWERBI.txt' para mas detalles" -ForegroundColor Cyan
    
} catch {
    Write-Host "Error durante el analisis: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "\nProceso completado!" -ForegroundColor Green