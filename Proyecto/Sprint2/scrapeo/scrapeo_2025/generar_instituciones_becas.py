#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Instituciones por Beca - Versión Simplificada
Crea archivos CSV con información de instituciones educativas por beca
Solo usa módulos estándar de Python
"""

import csv
import json
from datetime import datetime

def crear_datos_instituciones():
    """Crea los datos de instituciones por beca"""
    datos_expandidos = []
    
    # BECA TEC - 28 instituciones técnicas
    instituciones_beca_tec = [
        # LIMA
        {
            'nombre': 'EEST Privada ADEX',
            'ubicacion': 'San Borja, Lima',
            'region': 'Lima',
            'programas': [
                'Administración de Negocios Internacionales',
                'Gestión Administrativa',
                'Gestión Logística',
                'Marketing'
            ]
        },
        {
            'nombre': 'EEST Privada Corriente Alterna',
            'ubicacion': 'La Victoria, Lima',
            'region': 'Lima',
            'programas': [
                'Diseño de Interiores',
                'Diseño Gráfico',
                'Marketing'
            ]
        },
        {
            'nombre': 'EEST Privada IDAT',
            'ubicacion': 'San Juan de Miraflores, Lima',
            'region': 'Lima',
            'programas': [
                'Administración de Negocios Bancarios y Financieros',
                'Administración de Negocios Internacionales',
                'Contabilidad',
                'Desarrollo de Sistemas de Información',
                'Diseño de Interiores',
                'Diseño Gráfico Visual',
                'Gestión Administrativa',
                'Gestión de Recursos Humanos',
                'Marketing'
            ]
        },
        {
            'nombre': 'EEST Privada Toulouse Lautrec',
            'ubicacion': 'Magdalena del Mar y Santiago de Surco, Lima',
            'region': 'Lima',
            'programas': [
                'Animación Digital',
                'Cinematografía',
                'Comunicación Audiovisual',
                'Diseño de Interiores',
                'Diseño de Videojuegos y Entretenimiento Digital',
                'Diseño Gráfico',
                'Fotografía e Imagen Digital',
                'Marketing',
                'Publicidad y Medios Digitales'
            ]
        },
        # AREQUIPA
        {
            'nombre': 'EEST Privada Toulouse Lautrec',
            'ubicacion': 'Arequipa',
            'region': 'Arequipa',
            'programas': [
                'Animación Digital',
                'Diseño de Interiores',
                'Diseño Gráfico',
                'Marketing',
                'Publicidad y Medios Digitales'
            ]
        },
        {
            'nombre': 'IES Privado del Sur',
            'ubicacion': 'Arequipa',
            'region': 'Arequipa',
            'programas': [
                'Administración de Negocios Bancarios y Financieros',
                'Administración de Negocios Internacionales',
                'Administración de Servicios de Hostelería y Restaurantes',
                'Desarrollo de Sistemas de Información',
                'Diseño de Modas',
                'Diseño Gráfico y Multimedia',
                'Diseño y Decoración de Interiores',
                'Gastronomía',
                'Gestión Administrativa',
                'Guía Oficial de Turismo',
                'Marketing'
            ]
        },
        # CUSCO
        {
            'nombre': 'EEST Privada Khipu',
            'ubicacion': 'Cusco',
            'region': 'Cusco',
            'programas': [
                'Administración de Empresas',
                'Administración de Hoteles y Restaurantes'
            ]
        },
        {
            'nombre': 'IES Privado Khipu',
            'ubicacion': 'Cusco y San Sebastián',
            'region': 'Cusco',
            'programas': [
                'Desarrollo de Sistemas de Información',
                'Gastronomía',
                'Guía Oficial de Turismo',
                'Administración de Negocios Bancarios y Financieros',
                'Administración de Negocios Internacionales',
                'Contabilidad',
                'Marketing'
            ]
        },
        # LAMBAYEQUE
        {
            'nombre': 'IES Privado Cumbre',
            'ubicacion': 'Chiclayo',
            'region': 'Lambayeque',
            'programas': ['Gastronomía']
        },
        {
            'nombre': 'IES Privado de Emprendedores ISAG',
            'ubicacion': 'Chiclayo y La Victoria',
            'region': 'Lambayeque',
            'programas': [
                'Administración de Empresas',
                'Administración de Servicios de Hostelería y Restaurantes',
                'Contabilidad',
                'Enfermería Técnica',
                'Farmacia Técnica',
                'Fisioterapia y Rehabilitación',
                'Gastronomía',
                'Desarrollo de Sistemas de la Información',
                'Diseño Publicitario',
                'Traducción e Interpretación de Idiomas'
            ]
        }
        # Continuaría con las demás instituciones...
    ]
    
    # Expandir datos para Beca Tec
    for institucion in instituciones_beca_tec:
        for programa in institucion['programas']:
            registro = {
                'codigo_beca': 'beca_tec',
                'nombre_beca': 'Beca Tec',
                'tipo_instituciones': 'Institutos Técnicos',
                'nombre_institucion': institucion['nombre'],
                'tipo_institucion': 'Privada',
                'ubicacion': institucion['ubicacion'],
                'region': institucion['region'],
                'programa': programa,
                'modalidad_programa': 'Presencial'
            }
            datos_expandidos.append(registro)
    
    # BECA 18 - Cargar todas las universidades desde el archivo CSV
    universidades_beca18 = []
    try:
        with open('beca18_universidades.csv', 'r', encoding='utf-8-sig') as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                if fila['elegible_beca18'] == 'True':
                    # Determinar modalidades según características de la universidad
                    modalidades = ['Ordinaria']
                    
                    # Agregar modalidades específicas según ubicación y tipo
                    nombre_lower = fila['nombre'].lower()
                    ubicacion = fila.get('ubicacion', '').strip()
                    
                    # Modalidad EIB para universidades en regiones con población indígena
                    if any(region in ubicacion.lower() for region in ['cusco', 'puno', 'ayacucho', 'amazonas', 'ucayali', 'san martín']):
                        modalidades.append('EIB')
                    
                    # Modalidad VRAEM para universidades en zonas VRAEM
                    if any(zona in ubicacion.lower() for zona in ['ayacucho', 'cusco', 'huancavelica', 'junín']):
                        modalidades.append('Vraem')
                    
                    # Modalidad Protección para universidades principales
                    if 'mayor de san marcos' in nombre_lower or 'ingeniería' in nombre_lower:
                        modalidades.append('Protección')
                    
                    universidad = {
                        'nombre': fila['nombre'],
                        'ubicacion': ubicacion if ubicacion else 'No especificada',
                        'region': ubicacion if ubicacion else 'Nacional',
                        'tipo': fila['tipo'],
                        'modalidades': modalidades
                    }
                    universidades_beca18.append(universidad)
    except FileNotFoundError:
        print("Advertencia: No se encontró el archivo beca18_universidades.csv, usando datos de ejemplo")
        # Fallback a datos de ejemplo si no se encuentra el archivo
        universidades_beca18 = [
            {
                'nombre': 'Universidad Nacional de Barranca',
                'ubicacion': 'Barranca, Lima',
                'region': 'Lima',
                'tipo': 'Pública',
                'modalidades': ['Ordinaria', 'EIB', 'Protección']
            },
            {
                'nombre': 'Universidad Nacional Hermilio Valdizán',
                'ubicacion': 'Huánuco',
                'region': 'Huánuco',
                'tipo': 'Pública',
                'modalidades': ['Ordinaria', 'Vraem']
            },
            {
                'nombre': 'Universidad Nacional Mayor de San Marcos',
                'ubicacion': 'Lima',
                'region': 'Lima',
                'tipo': 'Pública',
                'modalidades': ['Ordinaria', 'EIB']
            }
        ]
    
    # Expandir datos para Beca 18
    for universidad in universidades_beca18:
        for modalidad in universidad['modalidades']:
            registro = {
                'codigo_beca': 'beca_18',
                'nombre_beca': 'Beca 18',
                'tipo_instituciones': 'Universidades',
                'nombre_institucion': universidad['nombre'],
                'tipo_institucion': universidad['tipo'],
                'ubicacion': universidad['ubicacion'],
                'region': universidad['region'],
                'programa': f"Modalidad {modalidad}",
                'modalidad_programa': modalidad
            }
            datos_expandidos.append(registro)
    
    # BECA PERÚ - 12 Universidades privadas participantes
    universidades_beca_peru = [
        # LIMA (3 universidades)
        {
            'nombre': 'Pontificia Universidad Católica del Perú (PUCP)',
            'ubicacion': 'Lima',
            'region': 'Lima',
            'programas': ['Pregrado']
        },
        {
            'nombre': 'Universidad Peruana de Ciencias Aplicadas (UPC)',
            'ubicacion': 'Lima',
            'region': 'Lima',
            'programas': ['Pregrado']
        },
        {
            'nombre': 'Universidad Antonio Ruiz de Montoya (UARM)',
            'ubicacion': 'Lima',
            'region': 'Lima',
            'programas': ['Pregrado']
        },
        # REGIONES (9 universidades)
        {
            'nombre': 'Universidad Privada en Arequipa',
            'ubicacion': 'Arequipa',
            'region': 'Arequipa',
            'programas': ['Pregrado']
        },
        {
            'nombre': 'Universidad Andina del Cusco (UAC)',
            'ubicacion': 'Cusco',
            'region': 'Cusco',
            'programas': ['Pregrado']
        },
        {
            'nombre': 'Universidad Privada en Lambayeque',
            'ubicacion': 'Lambayeque',
            'region': 'Lambayeque',
            'programas': ['Pregrado']
        },
        {
            'nombre': 'Universidad Privada en La Libertad',
            'ubicacion': 'La Libertad',
            'region': 'La Libertad',
            'programas': ['Pregrado']
        },
        {
            'nombre': 'Universidad Privada en Piura',
            'ubicacion': 'Piura',
            'region': 'Piura',
            'programas': ['Pregrado']
        },
        {
            'nombre': 'Universidad Privada en San Martín',
            'ubicacion': 'San Martín',
            'region': 'San Martín',
            'programas': ['Pregrado']
        },
        {
            'nombre': 'Universidad Privada en Junín',
            'ubicacion': 'Junín',
            'region': 'Junín',
            'programas': ['Pregrado']
        },
        {
            'nombre': 'Universidad Privada en Puno',
            'ubicacion': 'Puno',
            'region': 'Puno',
            'programas': ['Pregrado']
        },
        {
            'nombre': 'Universidad Privada en Huánuco',
            'ubicacion': 'Huánuco',
            'region': 'Huánuco',
            'programas': ['Pregrado']
        }
    ]
    
    # Expandir datos para Beca Perú
    for universidad in universidades_beca_peru:
        for programa in universidad['programas']:
            registro = {
                'codigo_beca': 'beca_peru',
                'nombre_beca': 'Beca Perú',
                'tipo_instituciones': 'Universidades Privadas Participantes',
                'nombre_institucion': universidad['nombre'],
                'tipo_institucion': 'Privada',
                'ubicacion': universidad['ubicacion'],
                'region': universidad['region'],
                'programa': programa,
                'modalidad_programa': 'Presencial'
            }
            datos_expandidos.append(registro)
    
    # BECAS INTERNACIONALES
    becas_internacionales = [
        {
            'codigo': 'chevening',
            'nombre': 'Becas Chevening',
            'universidades': [
                {'nombre': 'University of Oxford', 'pais': 'Reino Unido'},
                {'nombre': 'University of Cambridge', 'pais': 'Reino Unido'},
                {'nombre': 'Imperial College London', 'pais': 'Reino Unido'}
            ]
        },
        {
            'codigo': 'fulbright',
            'nombre': 'Becas Fulbright',
            'universidades': [
                {'nombre': 'Harvard University', 'pais': 'Estados Unidos'},
                {'nombre': 'Stanford University', 'pais': 'Estados Unidos'},
                {'nombre': 'MIT', 'pais': 'Estados Unidos'}
            ]
        }
    ]
    
    # Expandir datos para becas internacionales
    for beca in becas_internacionales:
        for universidad in beca['universidades']:
            registro = {
                'codigo_beca': beca['codigo'],
                'nombre_beca': beca['nombre'],
                'tipo_instituciones': f"Universidades de {universidad['pais']}",
                'nombre_institucion': universidad['nombre'],
                'tipo_institucion': 'Internacional',
                'ubicacion': universidad['pais'],
                'region': universidad['pais'],
                'programa': 'Maestrías y Doctorados',
                'modalidad_programa': 'Presencial'
            }
            datos_expandidos.append(registro)
    
    return datos_expandidos

def guardar_csv(datos, nombre_archivo):
    """Guarda los datos en formato CSV"""
    if not datos:
        print(f"No hay datos para guardar en {nombre_archivo}")
        return
    
    # Obtener las columnas del primer registro
    columnas = list(datos[0].keys())
    
    try:
        with open(nombre_archivo, 'w', newline='', encoding='utf-8-sig') as archivo_csv:
            escritor = csv.DictWriter(archivo_csv, fieldnames=columnas)
            escritor.writeheader()
            escritor.writerows(datos)
        
        print(f"✓ Archivo CSV guardado: {nombre_archivo}")
        print(f"  Total de registros: {len(datos)}")
    except Exception as e:
        print(f"✗ Error al guardar {nombre_archivo}: {str(e)}")

def guardar_json(datos, nombre_archivo):
    """Guarda los datos en formato JSON"""
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo_json:
            json.dump(datos, archivo_json, ensure_ascii=False, indent=2)
        
        print(f"✓ Archivo JSON guardado: {nombre_archivo}")
    except Exception as e:
        print(f"✗ Error al guardar {nombre_archivo}: {str(e)}")

def generar_estadisticas(datos):
    """Genera estadísticas de los datos"""
    if not datos:
        return {}
    
    estadisticas = {
        'fecha_generacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_registros': len(datos),
        'resumen_por_beca': {},
        'resumen_por_region': {},
        'resumen_por_tipo_institucion': {}
    }
    
    # Estadísticas por beca
    becas = {}
    for registro in datos:
        codigo_beca = registro['codigo_beca']
        if codigo_beca not in becas:
            becas[codigo_beca] = {
                'nombre_beca': registro['nombre_beca'],
                'total_registros': 0,
                'instituciones': set(),
                'programas': set()
            }
        becas[codigo_beca]['total_registros'] += 1
        becas[codigo_beca]['instituciones'].add(registro['nombre_institucion'])
        becas[codigo_beca]['programas'].add(registro['programa'])
    
    for codigo, datos_beca in becas.items():
        estadisticas['resumen_por_beca'][codigo] = {
            'nombre_beca': datos_beca['nombre_beca'],
            'total_registros': datos_beca['total_registros'],
            'instituciones_unicas': len(datos_beca['instituciones']),
            'programas_unicos': len(datos_beca['programas'])
        }
    
    # Estadísticas por región
    regiones = {}
    for registro in datos:
        region = registro['region']
        if region not in regiones:
            regiones[region] = {'total_registros': 0, 'instituciones': set()}
        regiones[region]['total_registros'] += 1
        regiones[region]['instituciones'].add(registro['nombre_institucion'])
    
    for region, datos_region in regiones.items():
        estadisticas['resumen_por_region'][region] = {
            'total_registros': datos_region['total_registros'],
            'instituciones_unicas': len(datos_region['instituciones'])
        }
    
    return estadisticas

def main():
    """Función principal"""
    print("=== GENERADOR DE INSTITUCIONES POR BECA ===")
    print("Creando datos de instituciones educativas...")
    
    # Crear datos
    datos_expandidos = crear_datos_instituciones()
    
    # Generar estadísticas
    estadisticas = generar_estadisticas(datos_expandidos)
    
    # Guardar archivo principal CSV
    print("\nGuardando archivos...")
    guardar_csv(datos_expandidos, "becas_instituciones_completo.csv")
    
    # Crear datos completos para JSON
    datos_completos = {
        'metadatos': {
            'descripcion': 'Instituciones educativas por beca - Formato expandido',
            'fecha_generacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'version': '1.0',
            'total_registros': len(datos_expandidos)
        },
        'estadisticas': estadisticas,
        'datos': datos_expandidos
    }
    
    # Guardar archivo principal JSON
    guardar_json(datos_completos, "becas_instituciones_completo.json")
    
    # Guardar estadísticas separadas
    guardar_json(estadisticas, "estadisticas_instituciones.json")
    
    # Generar archivos por beca
    print("\nGenerando archivos individuales por beca...")
    becas_procesadas = set()
    for registro in datos_expandidos:
        codigo_beca = registro['codigo_beca']
        if codigo_beca not in becas_procesadas:
            registros_beca = [r for r in datos_expandidos if r['codigo_beca'] == codigo_beca]
            nombre_archivo = f"instituciones_{codigo_beca}.csv"
            guardar_csv(registros_beca, nombre_archivo)
            becas_procesadas.add(codigo_beca)
    
    # Mostrar resumen final
    print("\n=== RESUMEN FINAL ===")
    print(f"Total de registros generados: {len(datos_expandidos)}")
    print(f"Total de becas procesadas: {len(estadisticas['resumen_por_beca'])}")
    
    print("\nArchivos generados:")
    print("- becas_instituciones_completo.csv")
    print("- becas_instituciones_completo.json")
    print("- estadisticas_instituciones.json")
    print("- instituciones_[codigo_beca].csv (por cada beca)")
    
    print("\n=== ESTADÍSTICAS POR BECA ===")
    for codigo_beca, stats in estadisticas['resumen_por_beca'].items():
        print(f"{stats['nombre_beca']}: {stats['total_registros']} registros, {stats['instituciones_unicas']} instituciones")
    
    print("\n¡Procesamiento completado exitosamente!")

    # Subir archivos a OneDrive/SharePoint (opcional, si están configuradas las credenciales)
    try:
        import subprocess, os
        upload_script = os.path.join(os.path.dirname(__file__), "graph_upload.py")
        print("\nSubiendo .json/.csv a OneDrive/SharePoint (si está configurado)")
        subprocess.run([sys.executable, upload_script], check=True)
    except Exception as e:
        print(f"Advertencia: No se pudo subir a OneDrive/SharePoint: {e}")

    # Refrescar Power BI (opcional, si están configuradas las credenciales)
    try:
        import subprocess, os
        script_path = os.path.join(os.path.dirname(__file__), "powerbi_refresh.py")
        dataset_names = [
            "Proyecto - Mapas ya incluidos ACTUAL - PERU",
            "Proyecto - Mapas ya incluidos ACTUAL"
        ]
        for dn in dataset_names:
            try:
                print(f"\nLanzando refresh de Power BI para dataset: {dn}")
                subprocess.run([
                    sys.executable, script_path, "--workspace", "My Workspace", "--dataset", dn
                ], check=True)
                break
            except Exception as inner_e:
                print(f"Advertencia: Falló el refresh para '{dn}': {inner_e}. Probando siguiente...")
    except Exception as e:
        print(f"Advertencia: No se pudo lanzar el refresh de Power BI: {e}")

if __name__ == "__main__":
    main()