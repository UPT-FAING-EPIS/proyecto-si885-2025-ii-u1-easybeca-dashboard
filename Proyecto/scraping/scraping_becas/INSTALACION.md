# Guía de Instalación - API de Scraping de Becas Perú

## ⚠️ Requisitos Previos

Antes de ejecutar este proyecto, necesitas tener instalado:

### 1. Python 3.8 o superior

**Opción A: Descargar desde el sitio oficial**
- Ir a https://www.python.org/downloads/
- Descargar Python 3.8+ para Windows
- Durante la instalación, **MARCAR** "Add Python to PATH"
- Verificar instalación: `python --version`

**Opción B: Instalar desde Microsoft Store**
- Abrir Microsoft Store
- Buscar "Python 3.11" o "Python 3.10"
- Instalar la versión más reciente

### 2. Google Chrome
- Descargar e instalar desde https://www.google.com/chrome/
- Necesario para el scraping con Selenium

### 3. ChromeDriver
- Ir a https://chromedriver.chromium.org/
- Descargar la versión compatible con tu Chrome
- Extraer y colocar en una carpeta del PATH o en el directorio del proyecto

## 🚀 Pasos de Instalación

### Paso 1: Verificar Python
```bash
python --version
# Debería mostrar: Python 3.8.x o superior
```

### Paso 2: Crear entorno virtual (recomendado)
```bash
cd scraping_becas
python -m venv venv
venv\Scripts\activate
```

### Paso 3: Instalar dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Verificar instalación
```bash
python -c "import fastapi, requests, selenium; print('Dependencias instaladas correctamente')"
```

### Paso 5: Ejecutar la aplicación
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Solución de Problemas

### Error: "python no se reconoce"
**Solución:**
1. Reinstalar Python marcando "Add to PATH"
2. O agregar manualmente Python al PATH del sistema
3. Reiniciar la terminal/PowerShell

### Error: "pip no se reconoce"
**Solución:**
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### Error: "ChromeDriver not found"
**Solución:**
1. Descargar ChromeDriver
2. Colocar en `C:\Windows\System32` o en el directorio del proyecto
3. O agregar la ruta al PATH del sistema

### Error de permisos
**Solución:**
- Ejecutar PowerShell como Administrador
- O usar `--user` en pip: `pip install --user -r requirements.txt`

## 📋 Lista de Verificación

- [ ] Python 3.8+ instalado y en PATH
- [ ] pip funcionando correctamente
- [ ] Google Chrome instalado
- [ ] ChromeDriver descargado y accesible
- [ ] Dependencias instaladas sin errores
- [ ] Aplicación ejecutándose en http://localhost:8000

## 🆘 Si Nada Funciona

### Opción 1: Usar Python desde Microsoft Store
1. Abrir Microsoft Store
2. Instalar "Python 3.11"
3. Reiniciar terminal
4. Intentar nuevamente

### Opción 2: Instalación manual de dependencias
```bash
python -m pip install fastapi uvicorn requests beautifulsoup4 selenium pandas sqlalchemy jinja2 python-multipart aiofiles openpyxl
```

### Opción 3: Usar conda (si está disponible)
```bash
conda create -n becas python=3.9
conda activate becas
pip install -r requirements.txt
```

## 📞 Contacto

Si sigues teniendo problemas:
1. Verificar que todos los requisitos estén instalados
2. Revisar los logs de error completos
3. Consultar la documentación oficial de Python
4. Contactar al equipo de desarrollo

---

**Nota**: Este proyecto requiere conexión a internet para el scraping y acceso a los sitios web objetivo.