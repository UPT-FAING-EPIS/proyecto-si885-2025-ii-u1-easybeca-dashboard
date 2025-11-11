"""
Script para extraer datos estructurados de Beca 18 - 2023
del texto extraído del PDF de la Memoria Anual del Pronabec 2023
"""

import pandas as pd
import re
import json

def leer_texto_completo(filename='texto_completo_pronabec_2023.txt'):
    """Lee el archivo de texto completo"""
    print(f"Leyendo archivo: {filename}")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            contenido = f.read()
        print(f"✓ Archivo leído exitosamente")
        return contenido
    except Exception as e:
        print(f"✗ Error al leer archivo: {e}")
        return None

def extraer_datos_beca18_2023():
    """Extrae datos específicos de Beca 18 - 2023"""
    
    texto = leer_texto_completo()
    if not texto:
        return None
    
    # Datos extraídos manualmente del texto
    datos_beca18_2023 = {
        'informacion_general': {
            'nombre_beca': 'Beca 18',
            'anio': 2023,
            'total_becas_otorgadas': 4998,
            'meta_becas': 5000,
            'cobertura_porcentaje': 10.2,
            'becas_universidades': 3991,
            'becas_institutos_escuelas': 1007,
            'postulantes_aptos': 48985,
            'preseleccionados': 14827,
            'seleccionados': 4998
        },
        
        'migracion': {
            'becarios_que_migraron': 2152,
            'becarios_que_no_migraron': 2846,  # 4998 - 2152
            'porcentaje_migracion': 43.1,
            'destino_principal_migracion': 'Lima',
            'porcentaje_lima_de_migrantes': 88.9,
            'porcentaje_lima_del_total': 38.3
        },
        
        'estrato_socioeconomico': {
            'nota': 'Los becarios son pobres o pobres extremos según SISFOH',
            'pobres': 'SI',
            'pobres_extremos': 'SI'
        },
        
        'modalidades': [
            {'nombre': 'Beca 18 Ordinaria', 'descripcion': 'Modalidad principal'},
            {'nombre': 'Beca Huallaga', 'descripcion': 'Para talentos residentes en el Huallaga'},
            {'nombre': 'Beca Vraem', 'descripcion': 'Para talentos del Valle de los ríos Apurímac, Ene y Mantaro'},
            {'nombre': 'Beca CNA y PA', 'descripcion': 'Para talentos de Comunidad Nativa Amazónica o Población Afroperuana'},
            {'nombre': 'Beca Protección', 'descripcion': 'Para adolescentes en situación de abandono y/o tutelados por el Estado'},
            {'nombre': 'Beca EIB', 'descripcion': 'Para talentos que dominen lenguas amazónicas originarias - Educación Intercultural Bilingüe'},
            {'nombre': 'Beca FF.AA.', 'descripcion': 'Para licenciados del Servicio Militar Voluntario'},
            {'nombre': 'Beca Repared', 'descripcion': 'Para víctimas de la violencia ocurrida 1980-2000'}
        ],
        
        'departamentos_procedencia': {
            'Lima': 905,  # Dato aproximado basado en el gráfico
            'Puno': 362,
            'Cusco': 305,
            'Junín': 279,
            'Cajamarca': 261,
            'Ayacucho': 254,
            'Arequipa': 253,
            'La Libertad': 245,
            'Piura': 213,
            'Huánuco': 196,
            'Áncash': 185,
            'Loreto': 183,
            'Apurímac': 174,
            'San Martín': 151,
            'Huancavelica': 133,
            'Lambayeque': 127,
            'Ica': 116,
            'Amazonas': 81,
            'Ucayali': 81,
            'Pasco': 73,
            'Tacna': 68,
            'Callao': 65,
            'Tumbes': 59,
            'Madre de Dios': 43,
            'Moquegua': 36
        },
        
        'instituciones_educativas': {
            'nota': 'El PDF menciona 121 universidades, institutos y escuelas elegibles',
            'tipos': {
                'universidades': 3991,
                'institutos_y_escuelas': 1007
            },
            'principales_universidades': [
                'Universidad Peruana de Ciencias Aplicadas (UPC)',
                'Universidad Científica del Sur',
                'Pontificia Universidad Católica del Perú (PUCP)',
                'Servicio Nacional de Adiestramiento en Trabajo Industrial (SENATI)',
                'Universidad Peruana Cayetano Heredia',
                'Universidad Continental',
                'Universidad Nacional San Antonio Abad del Cusco'
            ]
        },
        
        'carreras': {
            'nota': 'Carreras más elegidas por los becarios en 2023',
            'principales': [
                'Medicina Humana',
                'Ingeniería Civil',
                'Derecho',
                'Ingeniería Industrial',
                'Arquitectura',
                'Ingeniería de Sistemas',
                'Administración',
                'Contabilidad',
                'Educación'
            ]
        }
    }
    
    return datos_beca18_2023

def crear_dataset_para_dashboard(datos):
    """Crea datasets estructurados para el dashboard"""
    
    print("\nCreando datasets para el dashboard...")
    
    datasets = {}
    
    # 1. Dataset resumen general
    datasets['resumen_general'] = pd.DataFrame([{
        'NombreBeca': datos['informacion_general']['nombre_beca'],
        'Anio': datos['informacion_general']['anio'],
        'TotalBecasOtorgadas': datos['informacion_general']['total_becas_otorgadas'],
        'MetaBecas': datos['informacion_general']['meta_becas'],
        'Cobertura%': datos['informacion_general']['cobertura_porcentaje'],
        'BecasUniversidades': datos['informacion_general']['becas_universidades'],
        'BecasInstitutosEscuelas': datos['informacion_general']['becas_institutos_escuelas']
    }])
    
    # 2. Dataset por departamento
    dept_data = []
    for dept, cantidad in datos['departamentos_procedencia'].items():
        dept_data.append({
            'NombreBeca': 'Beca 18',
            'Anio': 2023,
            'Departamento': dept,
            'CantidadBecarios': cantidad,
            'Porcentaje': round((cantidad / datos['informacion_general']['total_becas_otorgadas']) * 100, 2)
        })
    datasets['becarios_por_departamento'] = pd.DataFrame(dept_data)
    
    # 3. Dataset modalidades
    modal_data = []
    for modalidad in datos['modalidades']:
        modal_data.append({
            'NombreBeca': 'Beca 18',
            'Anio': 2023,
            'Modalidad': modalidad['nombre'],
            'Descripcion': modalidad['descripcion']
        })
    datasets['modalidades'] = pd.DataFrame(modal_data)
    
    # 4. Dataset migración
    datasets['migracion'] = pd.DataFrame([
        {
            'NombreBeca': 'Beca 18',
            'Anio': 2023,
            'EstadoMigracion': 'Migró',
            'CantidadBecarios': datos['migracion']['becarios_que_migraron'],
            'Porcentaje': datos['migracion']['porcentaje_migracion'],
            'DestinoMayoritario': datos['migracion']['destino_principal_migracion']
        },
        {
            'NombreBeca': 'Beca 18',
            'Anio': 2023,
            'EstadoMigracion': 'No Migró',
            'CantidadBecarios': datos['migracion']['becarios_que_no_migraron'],
            'Porcentaje': round(100 - datos['migracion']['porcentaje_migracion'], 1),
            'DestinoMayoritario': 'Su mismo departamento'
        }
    ])
    
    # 5. Dataset carreras
    carrera_data = []
    for i, carrera in enumerate(datos['carreras']['principales'], 1):
        carrera_data.append({
            'NombreBeca': 'Beca 18',
            'Anio': 2023,
            'Carrera': carrera,
            'Ranking': i
        })
    datasets['carreras_principales'] = pd.DataFrame(carrera_data)
    
    # 6. Dataset instituciones
    inst_data = []
    for i, institucion in enumerate(datos['instituciones_educativas']['principales_universidades'], 1):
        inst_data.append({
            'NombreBeca': 'Beca 18',
            'Anio': 2023,
            'Institucion': institucion,
            'Ranking': i
        })
    datasets['instituciones_principales'] = pd.DataFrame(inst_data)
    
    # 7. Dataset estrato socioeconómico
    datasets['estrato_socioeconomico'] = pd.DataFrame([
        {
            'NombreBeca': 'Beca 18',
            'Anio': 2023,
            'EstratoSocioeconomico': 'Pobre',
            'Nota': datos['estrato_socioeconomico']['nota']
        },
        {
            'NombreBeca': 'Beca 18',
            'Anio': 2023,
            'EstratoSocioeconomico': 'Pobre Extremo',
            'Nota': datos['estrato_socioeconomico']['nota']
        }
    ])
    
    print("✓ Datasets creados exitosamente")
    return datasets

def guardar_datasets(datasets):
    """Guarda los datasets en diferentes formatos"""
    
    print("\nGuardando datasets...")
    
    # Guardar cada dataset en CSV
    for nombre, df in datasets.items():
        filename_csv = f'beca18_2023_{nombre}.csv'
        df.to_csv(filename_csv, index=False, encoding='utf-8-sig')
        print(f"  ✓ {filename_csv}")
    
    # Guardar todo en un archivo Excel con múltiples hojas
    filename_excel = 'beca18_2023_datos_completos.xlsx'
    with pd.ExcelWriter(filename_excel, engine='openpyxl') as writer:
        for nombre, df in datasets.items():
            df.to_excel(writer, sheet_name=nombre[:31], index=False)  # Excel limita a 31 chars
    print(f"  ✓ {filename_excel}")
    
    # Guardar resumen en JSON
    filename_json = 'beca18_2023_resumen.json'
    resumen = {
        'total_datasets': len(datasets),
        'datasets': {nombre: len(df) for nombre, df in datasets.items()},
        'total_becarios': int(datasets['resumen_general']['TotalBecasOtorgadas'].iloc[0])
    }
    with open(filename_json, 'w', encoding='utf-8') as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {filename_json}")

def mostrar_preview_datos(datasets):
    """Muestra un preview de los datos extraídos"""
    
    print("\n" + "="*80)
    print("PREVIEW DE DATOS EXTRAÍDOS - BECA 18 - 2023")
    print("="*80)
    
    for nombre, df in datasets.items():
        print(f"\n{nombre.upper().replace('_', ' ')}:")
        print(f"Registros: {len(df)}")
        print(df.head(5).to_string())
        print()

def main():
    print("="*80)
    print("EXTRACTOR DE DATOS ESTRUCTURADOS - BECA 18 - 2023")
    print("="*80)
    
    # 1. Extraer datos
    datos = extraer_datos_beca18_2023()
    if not datos:
        print("\n✗ No se pudieron extraer los datos. Abortando.")
        return
    
    # 2. Crear datasets
    datasets = crear_dataset_para_dashboard(datos)
    
    # 3. Mostrar preview
    mostrar_preview_datos(datasets)
    
    # 4. Guardar datasets
    guardar_datasets(datasets)
    
    print("\n" + "="*80)
    print("PROCESO COMPLETADO")
    print("="*80)
    print("\nArchivos generados:")
    print("  • beca18_2023_resumen_general.csv")
    print("  • beca18_2023_becarios_por_departamento.csv")
    print("  • beca18_2023_modalidades.csv")
    print("  • beca18_2023_migracion.csv")
    print("  • beca18_2023_carreras_principales.csv")
    print("  • beca18_2023_instituciones_principales.csv")
    print("  • beca18_2023_estrato_socioeconomico.csv")
    print("  • beca18_2023_datos_completos.xlsx (todos los datasets)")
    print("  • beca18_2023_resumen.json")
    print("\n¡Datos listos para usar en tu dashboard!")

if __name__ == "__main__":
    main()
