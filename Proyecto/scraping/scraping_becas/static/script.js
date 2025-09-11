// JavaScript principal para la API de Scraping de Becas Perú

// Configuración global
const API_BASE_URL = window.location.origin;
const POLLING_INTERVAL = 2000; // 2 segundos
const MAX_RETRIES = 3;

// Estado global de la aplicación
let currentStatus = {
    isRunning: false,
    currentTask: null,
    progress: 0,
    lastUpdate: null
};

// Elementos del DOM
const elements = {
    statusIndicator: null,
    statusText: null,
    progressBar: null,
    progressText: null,
    scrapingButtons: null,
    comparisonButton: null,
    resultsContainer: null,
    loadingSpinner: null
};

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
    initializeElements();
    initializeEventListeners();
    startStatusPolling();
    loadInitialData();
});

// Inicializar referencias a elementos del DOM
function initializeElements() {
    elements.statusIndicator = document.getElementById('status-indicator');
    elements.statusText = document.getElementById('status-text');
    elements.progressBar = document.getElementById('progress-bar');
    elements.progressText = document.getElementById('progress-text');
    elements.scrapingButtons = document.querySelectorAll('.scraping-btn');
    elements.comparisonButton = document.getElementById('comparison-btn');
    elements.resultsContainer = document.getElementById('results-container');
    elements.loadingSpinner = document.querySelector('.loading-spinner');
}

// Configurar event listeners
function initializeEventListeners() {
    // Botones de scraping
    document.getElementById('scrape-all-btn')?.addEventListener('click', () => startScraping('all'));
    document.getElementById('scrape-pronabec-btn')?.addEventListener('click', () => startScraping('pronabec'));
    document.getElementById('scrape-universities-btn')?.addEventListener('click', () => startScraping('universities'));
    document.getElementById('scrape-bcp-btn')?.addEventListener('click', () => startScraping('bcp'));
    
    // Botón de comparación
    document.getElementById('comparison-btn')?.addEventListener('click', startComparison);
    
    // Botones de exportación
    document.getElementById('export-excel-btn')?.addEventListener('click', exportToExcel);
    document.getElementById('export-json-btn')?.addEventListener('click', exportToJSON);
    
    // Botones de validación
    document.getElementById('validate-data-btn')?.addEventListener('click', validateData);
    
    // Tabs de comparación
    document.querySelectorAll('.comparison-tab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            switchComparisonTab(tab.getAttribute('data-tab'));
        });
    });
    
    // Botones de detalles de fuentes
    document.querySelectorAll('.source-detail-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const source = e.target.getAttribute('data-source');
            showSourceDetails(source);
        });
    });
}

// Funciones de scraping
async function startScraping(source) {
    if (currentStatus.isRunning) {
        showNotification('Ya hay un proceso de scraping en ejecución', 'warning');
        return;
    }
    
    try {
        updateScrapingButtons(true);
        updateStatus('running', `Iniciando scraping de ${source}...`);
        
        const endpoint = source === 'all' ? '/scrape/all' : `/scrape/${source}`;
        const response = await fetchWithRetry(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            showNotification(`Scraping de ${source} iniciado correctamente`, 'success');
            currentStatus.isRunning = true;
            currentStatus.currentTask = source;
        } else {
            throw new Error(`Error al iniciar scraping: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Error en scraping:', error);
        showNotification(`Error al iniciar scraping: ${error.message}`, 'error');
        updateStatus('error', 'Error en el scraping');
        updateScrapingButtons(false);
    }
}

// Función de comparación
async function startComparison() {
    try {
        showLoadingSpinner(true);
        updateStatus('running', 'Comparando datos con Excel...');
        
        const response = await fetchWithRetry('/api/compare', {
            method: 'GET'
        });
        
        if (response.ok) {
            const data = await response.json();
            displayComparisonResults(data);
            showNotification('Comparación completada', 'success');
        } else {
            throw new Error(`Error en comparación: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Error en comparación:', error);
        showNotification(`Error en comparación: ${error.message}`, 'error');
    } finally {
        showLoadingSpinner(false);
        updateStatus('idle', 'Listo');
    }
}

// Función de validación de datos
async function validateData() {
    try {
        showLoadingSpinner(true);
        
        const response = await fetchWithRetry('/validate');
        
        if (response.ok) {
            const data = await response.json();
            displayValidationResults(data);
            showNotification('Validación completada', 'success');
        } else {
            throw new Error(`Error en validación: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Error en validación:', error);
        showNotification(`Error en validación: ${error.message}`, 'error');
    } finally {
        showLoadingSpinner(false);
    }
}

// Funciones de exportación
async function exportToExcel() {
    try {
        const response = await fetchWithRetry('/export/excel');
        
        if (response.ok) {
            const blob = await response.blob();
            downloadFile(blob, 'becas_scrapeadas.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');
            showNotification('Datos exportados a Excel', 'success');
        } else {
            throw new Error(`Error en exportación: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Error en exportación:', error);
        showNotification(`Error en exportación: ${error.message}`, 'error');
    }
}

async function exportToJSON() {
    try {
        const response = await fetchWithRetry('/data');
        
        if (response.ok) {
            const data = await response.json();
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            downloadFile(blob, 'becas_scrapeadas.json', 'application/json');
            showNotification('Datos exportados a JSON', 'success');
        } else {
            throw new Error(`Error en exportación: ${response.statusText}`);
        }
    } catch (error) {
        console.error('Error en exportación:', error);
        showNotification(`Error en exportación: ${error.message}`, 'error');
    }
}

// Función para descargar archivos
function downloadFile(blob, filename, mimeType) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// Polling de estado
function startStatusPolling() {
    setInterval(async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/status`);
            if (response.ok) {
                const status = await response.json();
                updateStatusFromAPI(status);
            }
        } catch (error) {
            console.error('Error al obtener estado:', error);
        }
    }, POLLING_INTERVAL);
}

// Actualizar estado desde la API
function updateStatusFromAPI(status) {
    const wasRunning = currentStatus.isRunning;
    currentStatus = { ...currentStatus, ...status };
    
    // Actualizar UI
    if (status.is_running !== undefined) {
        if (status.is_running) {
            updateStatus('running', status.current_task || 'Procesando...');
        } else {
            updateStatus('idle', 'Listo');
            if (wasRunning) {
                // El proceso acaba de terminar
                updateScrapingButtons(false);
                showNotification('Proceso completado', 'success');
                loadScrapedData();
            }
        }
    }
    
    if (status.progress !== undefined) {
        updateProgress(status.progress);
    }
}

// Actualizar estado visual
function updateStatus(status, message) {
    if (elements.statusIndicator) {
        elements.statusIndicator.className = `status-indicator status-${status}`;
    }
    
    if (elements.statusText) {
        elements.statusText.textContent = message;
    }
    
    currentStatus.lastUpdate = new Date();
}

// Actualizar barra de progreso
function updateProgress(progress) {
    if (elements.progressBar) {
        elements.progressBar.style.width = `${progress}%`;
        elements.progressBar.setAttribute('aria-valuenow', progress);
    }
    
    if (elements.progressText) {
        elements.progressText.textContent = `${Math.round(progress)}%`;
    }
    
    currentStatus.progress = progress;
}

// Habilitar/deshabilitar botones de scraping
function updateScrapingButtons(disabled) {
    elements.scrapingButtons?.forEach(btn => {
        btn.disabled = disabled;
        if (disabled) {
            btn.innerHTML = btn.innerHTML.replace(/Scrapear|Iniciar/, '<span class="loading-spinner"></span> Procesando');
        } else {
            btn.innerHTML = btn.innerHTML.replace(/<span class="loading-spinner"><\/span> Procesando/, 'Scrapear');
        }
    });
}

// Mostrar/ocultar spinner de carga
function showLoadingSpinner(show) {
    if (elements.loadingSpinner) {
        elements.loadingSpinner.style.display = show ? 'inline-block' : 'none';
    }
}

// Cargar datos iniciales
async function loadInitialData() {
    try {
        await loadScrapedData();
        await loadSourcesInfo();
    } catch (error) {
        console.error('Error cargando datos iniciales:', error);
    }
}

// Cargar datos scrapeados
async function loadScrapedData() {
    try {
        const response = await fetchWithRetry('/data');
        if (response.ok) {
            const data = await response.json();
            updateDataStats(data);
            displayRecentData(data);
        }
    } catch (error) {
        console.error('Error cargando datos:', error);
    }
}

// Cargar información de fuentes
async function loadSourcesInfo() {
    try {
        const response = await fetchWithRetry('/sources');
        if (response.ok) {
            const sources = await response.json();
            updateSourcesInfo(sources);
        }
    } catch (error) {
        console.error('Error cargando fuentes:', error);
    }
}

// Actualizar estadísticas de datos
function updateDataStats(data) {
    const totalCount = document.getElementById('total-scholarships');
    const pronabecCount = document.getElementById('pronabec-count');
    const universitiesCount = document.getElementById('universities-count');
    const bcpCount = document.getElementById('bcp-count');
    
    // data es un array directamente, no un objeto con scholarships
    if (data && Array.isArray(data)) {
        const total = data.length;
        const pronabec = data.filter(s => s.source === 'PRONABEC' || s.fuente === 'PRONABEC').length;
        const universities = data.filter(s => s.source === 'Universities' || s.fuente === 'UNIVERSIDADES').length;
        const bcp = data.filter(s => s.source === 'BCP' || s.fuente === 'BCP').length;
        
        if (totalCount) totalCount.textContent = total;
        if (pronabecCount) pronabecCount.textContent = pronabec;
        if (universitiesCount) universitiesCount.textContent = universities;
        if (bcpCount) bcpCount.textContent = bcp;
    }
}

// Mostrar datos recientes
function displayRecentData(data) {
    const container = document.getElementById('recent-data-container');
    if (!container || !data || !Array.isArray(data)) return;
    
    const recentData = data.slice(0, 5); // Últimos 5
    
    container.innerHTML = recentData.map(scholarship => `
        <div class="card mb-2">
            <div class="card-body p-3">
                <h6 class="card-title mb-1">${scholarship.titulo || scholarship.title || 'Sin título'}</h6>
                <p class="card-text small text-muted mb-1">${scholarship.descripcion || scholarship.description ? (scholarship.descripcion || scholarship.description).substring(0, 100) + '...' : 'Sin descripción'}</p>
                <div class="d-flex justify-content-between align-items-center">
                    <span class="badge badge-primary">${scholarship.fuente || scholarship.source || 'Desconocido'}</span>
                    <small class="text-muted">${scholarship.fecha_scraping || scholarship.scraped_at ? new Date(scholarship.fecha_scraping || scholarship.scraped_at).toLocaleDateString() : 'Fecha desconocida'}</small>
                </div>
            </div>
        </div>
    `).join('');
}

// Mostrar resultados de comparación
function displayComparisonResults(data) {
    const container = document.getElementById('comparison-results');
    if (!container) return;
    
    container.innerHTML = `
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h3 class="text-success">${data.exact_matches_count || 0}</h3>
                        <p class="card-text">Coincidencias Exactas</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h3 class="text-warning">${data.partial_matches_count || 0}</h3>
                        <p class="card-text">Coincidencias Parciales</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h3 class="text-info">${data.new_entries ? data.new_entries.length : 0}</h3>
                        <p class="card-text">Nuevas Becas</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card text-center">
                    <div class="card-body">
                        <h3 class="text-danger">${data.missing_entries ? data.missing_entries.length : 0}</h3>
                        <p class="card-text">Becas Faltantes</p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card">
            <div class="card-header">
                <h5>Detalles de Comparación</h5>
            </div>
            <div class="card-body">
                <div class="comparison-details">
                    ${generateComparisonDetails(data)}
                </div>
            </div>
        </div>
    `;
}

// Generar detalles de comparación
function generateComparisonDetails(data) {
    let html = '';
    
    if (data.exact_matches && data.exact_matches.length > 0) {
        html += '<h6>Coincidencias Exactas:</h6>';
        data.exact_matches.forEach(match => {
            html += `
                <div class="match-item">
                    <strong>${match.nombre || match.title}</strong>
                    <p class="mb-1">${match.descripcion ? match.descripcion.substring(0, 150) + '...' : ''}</p>
                    <small class="text-muted">Fuente: ${match.fuente || match.source}</small>
                </div>
            `;
        });
    }
    
    if (data.new_entries && data.new_entries.length > 0) {
        html += '<h6 class="mt-4">Nuevas Becas:</h6>';
        data.new_entries.forEach(entry => {
            html += `
                <div class="new-entry-item">
                    <strong>${entry.nombre}</strong>
                    <p class="mb-1">${entry.descripcion ? entry.descripcion.substring(0, 150) + '...' : ''}</p>
                    <small class="text-muted">Fuente: ${entry.fuente}</small>
                </div>
            `;
        });
    }
    
    if (data.partial_matches && data.partial_matches.length > 0) {
        html += '<h6 class="mt-4">Coincidencias Parciales:</h6>';
        data.partial_matches.forEach(match => {
            html += `
                <div class="partial-match-item">
                    <strong>${match.title}</strong>
                    <p class="mb-1">${match.description ? match.description.substring(0, 150) + '...' : ''}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">Fuente: ${match.source}</small>
                        <span class="similarity-score score-${getSimilarityClass(match.similarity)}">
                            ${Math.round(match.similarity * 100)}% similitud
                        </span>
                    </div>
                </div>
            `;
        });
    }
    
    return html || '<p class="text-muted">No hay detalles de comparación disponibles.</p>';
}

// Obtener clase CSS para puntuación de similitud
function getSimilarityClass(similarity) {
    if (similarity >= 0.8) return 'high';
    if (similarity >= 0.6) return 'medium';
    return 'low';
}

// Mostrar resultados de validación
function displayValidationResults(data) {
    const container = document.getElementById('validation-results');
    if (!container) return;
    
    container.innerHTML = `
        <div class="card">
            <div class="card-header">
                <h5>Resultados de Validación</h5>
            </div>
            <div class="card-body">
                <div class="row mb-3">
                    <div class="col-md-4">
                        <div class="text-center">
                            <h4 class="text-success">${data.valid_count || 0}</h4>
                            <p>Registros Válidos</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="text-center">
                            <h4 class="text-warning">${data.warning_count || 0}</h4>
                            <p>Advertencias</p>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="text-center">
                            <h4 class="text-danger">${data.error_count || 0}</h4>
                            <p>Errores</p>
                        </div>
                    </div>
                </div>
                
                ${generateValidationDetails(data)}
            </div>
        </div>
    `;
}

// Generar detalles de validación
function generateValidationDetails(data) {
    let html = '';
    
    if (data.errors && data.errors.length > 0) {
        html += '<h6>Errores Encontrados:</h6>';
        data.errors.forEach(error => {
            html += `
                <div class="verification-item error">
                    <strong>Error:</strong> ${error.message}
                    <br><small>Registro: ${error.record_id || 'Desconocido'}</small>
                </div>
            `;
        });
    }
    
    if (data.warnings && data.warnings.length > 0) {
        html += '<h6 class="mt-3">Advertencias:</h6>';
        data.warnings.forEach(warning => {
            html += `
                <div class="verification-item warning">
                    <strong>Advertencia:</strong> ${warning.message}
                    <br><small>Registro: ${warning.record_id || 'Desconocido'}</small>
                </div>
            `;
        });
    }
    
    return html || '<p class="text-success">Todos los datos son válidos.</p>';
}

// Cambiar tab de comparación
function switchComparisonTab(tabName) {
    // Actualizar tabs activos
    document.querySelectorAll('.comparison-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Mostrar contenido correspondiente
    document.querySelectorAll('.tab-content').forEach(content => {
        content.style.display = 'none';
    });
    document.getElementById(`${tabName}-content`).style.display = 'block';
}

// Mostrar detalles de fuente
function showSourceDetails(source) {
    // Implementar modal o navegación a página de detalles
    window.location.href = `/sources?source=${source}`;
}

// Actualizar información de fuentes
function updateSourcesInfo(sources) {
    sources.forEach(source => {
        const card = document.querySelector(`[data-source="${source.name}"]`);
        if (card) {
            const statusBadge = card.querySelector('.status-badge');
            const lastUpdate = card.querySelector('.last-update');
            
            if (statusBadge) {
                statusBadge.className = `badge status-badge badge-${source.status === 'active' ? 'success' : 'secondary'}`;
                statusBadge.textContent = source.status === 'active' ? 'Activo' : 'Inactivo';
            }
            
            if (lastUpdate) {
                lastUpdate.textContent = source.last_update ? 
                    `Última actualización: ${new Date(source.last_update).toLocaleDateString()}` : 
                    'Sin actualizaciones';
            }
        }
    });
}

// Función de fetch con reintentos
async function fetchWithRetry(url, options = {}, retries = MAX_RETRIES) {
    for (let i = 0; i < retries; i++) {
        try {
            const response = await fetch(`${API_BASE_URL}${url}`, options);
            return response;
        } catch (error) {
            if (i === retries - 1) throw error;
            await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
        }
    }
}

// Sistema de notificaciones
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show notification`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="close" data-dismiss="alert">
            <span>&times;</span>
        </button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remover después del tiempo especificado
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, duration);
}

// Utilidades adicionales
function formatDate(dateString) {
    if (!dateString) return 'Fecha desconocida';
    return new Date(dateString).toLocaleDateString('es-PE', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatNumber(number) {
    return new Intl.NumberFormat('es-PE').format(number);
}

function truncateText(text, maxLength = 100) {
    if (!text) return '';
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
}

// Exportar funciones para uso global
window.ScrapingAPI = {
    startScraping,
    startComparison,
    validateData,
    exportToExcel,
    exportToJSON,
    showNotification,
    updateStatus,
    updateProgress
};