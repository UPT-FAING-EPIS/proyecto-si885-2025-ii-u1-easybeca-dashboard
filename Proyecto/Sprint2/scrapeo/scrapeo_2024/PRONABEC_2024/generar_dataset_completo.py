"""
Script para extraer datos PRONABEC 2024 con campos específicos del dataset
Incluye campos reales e inventados basados en el contexto disponible
"""

import pandas as pd
import json
import random
from datetime import datetime

# Configuración de datos inventados
GENEROS = ['Masculino', 'Femenino']
ESTRATOS = ['Pobre', 'Pobre Extremo', 'No pobre']
MIGRACION = ['Migró', 'No Migró']
CATEGORIAS_BECAS = [
    'Pregrado',
    'Posgrado Maestria',
    'Posgrado Doctorado',
    'Especiales'
]

# Países para becas internacionales (principalmente Posgrado)
PAISES_BECAS = [
    'Estados Unidos',
    'Reino Unido',
    'España',
    'Francia',
    'Alemania',
    'Canadá',
    'Australia',
    'Chile',
    'Argentina',
    'Brasil',
    'México',
    'Colombia'
]

# Carreras más comunes en Perú
CARRERAS_COMUNES = [
    'Administración de Empresas',
    'Ingeniería de Sistemas',
    'Contabilidad',
    'Derecho',
    'Medicina Humana',
    'Enfermería',
    'Ingeniería Civil',
    'Educación',
    'Psicología',
    'Economía',
    'Ingeniería Industrial',
    'Arquitectura',
    'Marketing',
    'Administración de Negocios Internacionales',
    'Ingeniería Electrónica',
    'Trabajo Social',
    'Comunicaciones',
    'Nutrición',
    'Ingeniería Mecánica',
    'Turismo y Hotelería'
]

INSTITUCIONES_PERU = [
    'Universidad Nacional Mayor de San Marcos',
    'Universidad Nacional de Ingeniería',
    'Universidad Nacional Agraria La Molina',
    'Universidad Nacional del Callao',
    'Universidad Nacional Federico Villarreal',
    'Universidad Peruana Cayetano Heredia',
    'Pontificia Universidad Católica del Perú',
    'Universidad del Pacífico',
    'Universidad Nacional San Antonio Abad del Cusco',
    'Universidad Nacional de Trujillo',
    'Universidad Nacional San Agustín de Arequipa',
    'Universidad Nacional del Altiplano',
    'Universidad Nacional de la Amazonía Peruana',
    'Universidad Nacional de Piura',
    'Universidad Nacional de Cajamarca',
    'Universidad Nacional San Cristóbal de Huamanga',
    'Universidad Nacional Hermilio Valdizán',
    'Universidad Nacional de Ucayali',
    'Universidad Nacional Jorge Basadre Grohmann',
    'Universidad Nacional Daniel Alcides Carrión'
]

def cargar_datos_base():
    """Carga los datos extraídos del PDF"""
    print("📂 Cargando datos base del scraping...")
    
    datos = {}
    
    try:
        # Datos principales
        datos['departamentos'] = pd.read_csv('dashboard_departamentos_2024.csv', encoding='utf-8-sig')
        print(f"  ✓ Departamentos: {len(datos['departamentos'])} registros")
    except:
        print("  ⚠ No se encontraron datos de departamentos")
        return None
    
    try:
        datos['becas'] = pd.read_csv('dashboard_becas_2024.csv', encoding='utf-8-sig')
        print(f"  ✓ Becas: {len(datos['becas'])} registros")
    except:
        datos['becas'] = pd.DataFrame()
    
    try:
        datos['instituciones'] = pd.read_csv('dashboard_instituciones_2024.csv', encoding='utf-8-sig')
        print(f"  ✓ Instituciones: {len(datos['instituciones'])} registros")
    except:
        datos['instituciones'] = pd.DataFrame()
    
    return datos

def generar_datos_completos(datos_base):
    """Genera dataset completo con todos los campos solicitados"""
    print("\n🔄 Generando dataset con campos específicos...")
    
    registros = []
    datos_inventados = {
        'Carrera': 0,
        'Institucion': 0,
        'Genero': 0,
        'EstratoSocioeconomico': 0,
        'BecasSegunMigracion': 0,
        'CategoriaDeBecas': 0
    }
    
    # Obtener becas y departamentos
    df_becas = datos_base.get('becas', pd.DataFrame())
    df_dept = datos_base['departamentos']
    df_inst = datos_base.get('instituciones', pd.DataFrame())
    
    # Mapeo de tipos de becas a categorías
    tipo_beca_map = {
        'Pregrado': 'Pregrado',
        'Posgrado': 'Posgrado Maestria',
        'Especiales': 'Especiales'
    }
    
    # Generar registros por departamento
    for idx, row in df_dept.iterrows():
        departamento = row['Departamento']
        cantidad = int(row['CantidadBecarios'])
        
        # Generar registros individuales para cada becario
        for i in range(cantidad):
            
            # Determinar tipo de beca (basado en datos reales si existen)
            if not df_becas.empty and random.random() > 0.3:
                tipo_beca_real = random.choice(df_becas['TipoBeca'].tolist())
                nombre_beca = df_becas[df_becas['TipoBeca'] == tipo_beca_real]['NombreBeca'].iloc[0]
                categoria_beca = tipo_beca_map.get(tipo_beca_real, 'Pregrado')
                beca_inventada = False
            else:
                nombre_beca = random.choice(['Beca 18', 'Beca Permanencia', 'Beca Vocación'])
                categoria_beca = random.choice(CATEGORIAS_BECAS)
                beca_inventada = False  # Nombre está en el documento
                datos_inventados['CategoriaDeBecas'] += 1
            
            # Determinar Lugar (puede ser departamento de Perú o país extranjero)
            # Becas de Posgrado tienen mayor probabilidad de ser en el extranjero
            if 'Posgrado' in categoria_beca and random.random() < 0.25:  # 25% de posgrado en el extranjero
                lugar = random.choice(PAISES_BECAS)
                datos_inventados['Lugar'] = datos_inventados.get('Lugar', 0) + 1
            else:
                lugar = departamento  # Usar departamento del Perú
            
            # Institución (algunas reales, otras inventadas)
            if not df_inst.empty and random.random() > 0.7:
                institucion = random.choice(df_inst['Institucion'].tolist())
            else:
                institucion = random.choice(INSTITUCIONES_PERU)
                datos_inventados['Institucion'] += 1
            
            # Carrera (siempre inventada - no hay en el PDF)
            carrera = random.choice(CARRERAS_COMUNES)
            datos_inventados['Carrera'] += 1
            
            # Género (siempre inventado - no hay en el PDF)
            genero = random.choice(GENEROS)
            datos_inventados['Genero'] += 1
            
            # Estrato socioeconómico (siempre inventado - no hay en el PDF)
            # Distribución más realista: más pobres que no pobres
            if random.random() < 0.45:
                estrato = 'Pobre'
            elif random.random() < 0.75:
                estrato = 'Pobre Extremo'
            else:
                estrato = 'No pobre'
            datos_inventados['EstratoSocioeconomico'] += 1
            
            # Migración (siempre inventado - no hay en el PDF)
            # Si es de Lima, menos probable que migre
            # Si estudia en el extranjero, definitivamente migró
            if lugar not in ['Lima', 'Ica', 'Callao', 'Cusco', 'Piura', 'Arequipa', 'La Libertad', 
                            'Lambayeque', 'Junín', 'Puno', 'Cajamarca', 'Ancash', 'Apurímac', 
                            'Huánuco', 'San Martín', 'Ayacucho', 'Loreto', 'Ucayali', 'Amazonas',
                            'Huancavelica', 'Pasco', 'Tumbes', 'Tacna', 'Madre de Dios', 'Moquegua']:
                # Estudia en el extranjero
                migracion = 'Migró'
            elif departamento == 'Lima':
                migracion = 'No Migró' if random.random() < 0.8 else 'Migró'
            else:
                migracion = 'Migró' if random.random() < 0.4 else 'No Migró'
            datos_inventados['BecasSegunMigracion'] += 1
            
            # Crear registro
            registro = {
                'NombreBeca': nombre_beca,
                'Institucion': institucion,
                'Carrera': carrera,
                'Lugar': lugar,  # Cambiado de Departamento a Lugar
                'CategoriaDeBecas': categoria_beca,
                'Anio_Convocatoria': 2024,
                'Genero': genero,
                'EstratoSocioeconomico': estrato,
                'BecasSegunMigracion': migracion
            }
            
            registros.append(registro)
    
    df_final = pd.DataFrame(registros)
    
    return df_final, datos_inventados

def generar_reporte_datos_inventados(datos_inventados, total_registros):
    """Genera reporte de datos inventados"""
    print("\n" + "="*70)
    print("  ⚠️  REPORTE DE DATOS INVENTADOS")
    print("="*70)
    
    reporte = []
    
    print("\n📊 RESUMEN:")
    print(f"   Total de registros generados: {total_registros}")
    print(f"\n📌 CAMPOS Y SU ORIGEN:\n")
    
    # Datos REALES del PDF
    print("   ✅ DATOS REALES (del PDF oficial):")
    print("      • NombreBeca: Extraído del documento")
    print("      • Lugar: Departamentos extraídos del documento (países inventados)")
    print("      • Anio_Convocatoria: 2024 (del documento)")
    
    reporte.append({
        'Campo': 'NombreBeca',
        'Origen': 'REAL - Extraído del PDF',
        'Cantidad': total_registros,
        'Porcentaje': '100%',
        'Justificacion': 'Datos oficiales del documento PRONABEC 2024'
    })
    
    reporte.append({
        'Campo': 'Lugar',
        'Origen': 'REAL + INVENTADO - Base del PDF',
        'Cantidad': datos_inventados.get('Lugar', 0),
        'Porcentaje': f"{(datos_inventados.get('Lugar', 0)/total_registros*100):.1f}%",
        'Justificacion': 'Departamentos del Perú extraídos del PDF. Países extranjeros inventados para becas de posgrado (~25%)'
    })
    
    reporte.append({
        'Campo': 'Anio_Convocatoria',
        'Origen': 'REAL - Del documento',
        'Cantidad': total_registros,
        'Porcentaje': '100%',
        'Justificacion': 'Año 2024 según Memoria Anual oficial'
    })
    
    # Datos PARCIALMENTE INVENTADOS
    print("\n   ⚠️  DATOS PARCIALMENTE INVENTADOS:")
    print(f"      • Lugar: {datos_inventados.get('Lugar', 0)} lugares inventados (~25% países extranjeros)")
    print("        Razón: Becas de posgrado incluyen estudios en el extranjero")
    print("        Solución: Países principales para becas internacionales")
    
    print(f"\n      • Institucion: {datos_inventados['Institucion']} registros inventados")
    print("        Razón: Solo 4 instituciones mencionadas en el PDF")
    print("        Solución: Universidades públicas reconocidas del Perú")
    
    reporte.append({
        'Campo': 'Institucion',
        'Origen': 'PARCIAL - 4 reales + inventadas',
        'Cantidad': datos_inventados['Institucion'],
        'Porcentaje': f"{(datos_inventados['Institucion']/total_registros*100):.1f}%",
        'Justificacion': 'Solo 4 instituciones en PDF, completado con universidades públicas reales del Perú'
    })
    
    reporte.append({
        'Campo': 'CategoriaDeBecas',
        'Origen': 'INFERIDO - De tipos del PDF',
        'Cantidad': datos_inventados['CategoriaDeBecas'],
        'Porcentaje': f"{(datos_inventados['CategoriaDeBecas']/total_registros*100):.1f}%",
        'Justificacion': 'Categorías: Pregrado, Posgrado Maestria, Posgrado Doctorado, Especiales (basadas en tipos del PDF)'
    })
    
    # Datos COMPLETAMENTE INVENTADOS
    print("\n   ❌ DATOS COMPLETAMENTE INVENTADOS (NO en el PDF):")
    print(f"      • Carrera: {datos_inventados['Carrera']} registros (100%)")
    print("        Razón: El PDF NO incluye información de carreras")
    print("        Solución: Carreras más demandadas en Perú")
    
    print(f"\n      • Genero: {datos_inventados['Genero']} registros (100%)")
    print("        Razón: El PDF NO incluye información de género")
    print("        Solución: Distribución aleatoria Masculino/Femenino")
    
    print(f"\n      • EstratoSocioeconomico: {datos_inventados['EstratoSocioeconomico']} registros (100%)")
    print("        Razón: El PDF NO incluye datos de estratos por becario")
    print("        Solución: Distribución realista (45% Pobre, 30% Pobre Extremo, 25% No pobre)")
    
    print(f"\n      • BecasSegunMigracion: {datos_inventados['BecasSegunMigracion']} registros (100%)")
    print("        Razón: El PDF NO incluye datos de migración por becario")
    print("        Solución: Lógica realista (Lima 80% no migra, otros 40% migra)")
    
    reporte.append({
        'Campo': 'Carrera',
        'Origen': 'INVENTADO - No existe en PDF',
        'Cantidad': datos_inventados['Carrera'],
        'Porcentaje': '100%',
        'Justificacion': 'PDF no incluye carreras. Usadas: las 20 carreras más demandadas en Perú'
    })
    
    reporte.append({
        'Campo': 'Genero',
        'Origen': 'INVENTADO - No existe en PDF',
        'Cantidad': datos_inventados['Genero'],
        'Porcentaje': '100%',
        'Justificacion': 'PDF no incluye género. Distribución aleatoria 50/50'
    })
    
    reporte.append({
        'Campo': 'EstratoSocioeconomico',
        'Origen': 'INVENTADO - No existe en PDF',
        'Cantidad': datos_inventados['EstratoSocioeconomico'],
        'Porcentaje': '100%',
        'Justificacion': 'PDF no incluye estratos. Distribución realista: 45% Pobre, 30% Pobre Extremo, 25% No pobre'
    })
    
    reporte.append({
        'Campo': 'BecasSegunMigracion',
        'Origen': 'INVENTADO - No existe en PDF',
        'Cantidad': datos_inventados['BecasSegunMigracion'],
        'Porcentaje': '100%',
        'Justificacion': 'PDF no incluye migración. Lógica: Lima 20% migra, otros departamentos 40% migra'
    })
    
    print("\n" + "="*70)
    print("  💡 RECOMENDACIÓN PARA TU EXPOSICIÓN")
    print("="*70)
    print("\n   Menciona claramente que:")
    print("   1. ✅ Becas y lugares base son DATOS REALES del PDF oficial")
    print("   2. ⚠️  Lugares en el extranjero (~25%) son para becas de posgrado")
    print("   3. ⚠️  Categorías: Pregrado, Posgrado Maestria, Posgrado Doctorado, Especiales")
    print("   4. ⚠️  Instituciones son mayormente reales (universidades públicas)")
    print("   5. ❌ Carrera, Género, Estrato y Migración son INVENTADOS")
    print("   6. 📋 Estos campos inventados siguen lógica realista del contexto peruano")
    print("   7. 🎯 Son necesarios para demostrar funcionalidad del dashboard")
    print("\n")
    
    return pd.DataFrame(reporte)

def main():
    """Función principal"""
    print("="*70)
    print("  GENERACIÓN DE DATASET CON CAMPOS ESPECÍFICOS")
    print("  PRONABEC 2024")
    print("="*70 + "\n")
    
    try:
        # Cargar datos base
        datos_base = cargar_datos_base()
        
        if datos_base is None:
            print("\n❌ No se pudieron cargar los datos base")
            return
        
        # Generar dataset completo
        df_final, datos_inventados = generar_datos_completos(datos_base)
        
        print(f"\n✅ Dataset generado: {len(df_final)} registros")
        
        # Generar reporte de datos inventados
        df_reporte = generar_reporte_datos_inventados(datos_inventados, len(df_final))
        
        # Guardar archivos
        print("\n💾 Guardando archivos...")
        
        # Dataset principal
        archivo_principal = 'PRONABEC_2024_DATASET_ACTUALIZADO.xlsx'
        
        with pd.ExcelWriter(archivo_principal, engine='openpyxl') as writer:
            # Hoja 1: Datos principales
            df_final.to_excel(writer, sheet_name='Datos_Becarios', index=False)
            
            # Hoja 2: Reporte de datos inventados
            df_reporte.to_excel(writer, sheet_name='Reporte_Datos_Inventados', index=False)
            
            # Hoja 3: Estadísticas del dataset
            stats = {
                'Métrica': [
                    'Total de Becarios',
                    'Lugares Únicos (Perú + Extranjero)',
                    'Lugares en el Perú',
                    'Lugares en el Extranjero',
                    'Instituciones Únicas',
                    'Carreras Únicas',
                    'Categorías de Becas',
                    'Año',
                    'Becarios Masculinos',
                    'Becarios Femeninos',
                    'Estratos Pobre',
                    'Estratos Pobre Extremo',
                    'Estratos No Pobre',
                    'Becarios que Migraron',
                    'Becarios que No Migraron'
                ],
                'Valor': [
                    len(df_final),
                    df_final['Lugar'].nunique(),
                    len(df_final[df_final['Lugar'].isin(['Lima', 'Ica', 'Callao', 'Cusco', 'Piura', 'Arequipa', 'La Libertad', 
                            'Lambayeque', 'Junín', 'Puno', 'Cajamarca', 'Ancash', 'Apurímac', 
                            'Huánuco', 'San Martín', 'Ayacucho', 'Loreto', 'Ucayali', 'Amazonas',
                            'Huancavelica', 'Pasco', 'Tumbes', 'Tacna', 'Madre de Dios', 'Moquegua'])]),
                    len(df_final[~df_final['Lugar'].isin(['Lima', 'Ica', 'Callao', 'Cusco', 'Piura', 'Arequipa', 'La Libertad', 
                            'Lambayeque', 'Junín', 'Puno', 'Cajamarca', 'Ancash', 'Apurímac', 
                            'Huánuco', 'San Martín', 'Ayacucho', 'Loreto', 'Ucayali', 'Amazonas',
                            'Huancavelica', 'Pasco', 'Tumbes', 'Tacna', 'Madre de Dios', 'Moquegua'])]),
                    df_final['Institucion'].nunique(),
                    df_final['Carrera'].nunique(),
                    df_final['CategoriaDeBecas'].nunique(),
                    2024,
                    len(df_final[df_final['Genero'] == 'Masculino']),
                    len(df_final[df_final['Genero'] == 'Femenino']),
                    len(df_final[df_final['EstratoSocioeconomico'] == 'Pobre']),
                    len(df_final[df_final['EstratoSocioeconomico'] == 'Pobre Extremo']),
                    len(df_final[df_final['EstratoSocioeconomico'] == 'No pobre']),
                    len(df_final[df_final['BecasSegunMigracion'] == 'Migró']),
                    len(df_final[df_final['BecasSegunMigracion'] == 'No Migró'])
                ]
            }
            
            df_stats = pd.DataFrame(stats)
            df_stats.to_excel(writer, sheet_name='Estadisticas', index=False)
        
        print(f"  ✓ {archivo_principal}")
        
        # También en CSV para fácil importación
        df_final.to_csv('PRONABEC_2024_DATASET_COMPLETO.csv', index=False, encoding='utf-8-sig')
        print(f"  ✓ PRONABEC_2024_DATASET_COMPLETO.csv")
        
        # Guardar reporte separado
        df_reporte.to_excel('REPORTE_DATOS_INVENTADOS.xlsx', index=False, engine='openpyxl')
        print(f"  ✓ REPORTE_DATOS_INVENTADOS.xlsx")
        
        # Vista previa
        print("\n📄 VISTA PREVIA DE LOS DATOS:\n")
        print(df_final.head(10).to_string(index=False))
        
        print("\n" + "="*70)
        print("  ✅ PROCESO COMPLETADO")
        print("="*70)
        print(f"\n📁 Archivo principal: {archivo_principal}")
        print(f"📊 Total registros: {len(df_final)}")
        print(f"📋 Campos: {len(df_final.columns)}")
        print("\n🎯 IMPORTANTE PARA TU EXPOSICIÓN:")
        print("   Lee el archivo: REPORTE_DATOS_INVENTADOS.xlsx")
        print("   Contiene la justificación detallada de cada campo\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
