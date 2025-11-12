"""
Script para generar dataset de becarios en formato Excel
con campos específicos según los requisitos del usuario
"""

import pandas as pd
import random
import numpy as np

# Definir los datos base desde los CSVs existentes
carreras_disponibles = [
    "Medicina Humana",
    "Ingeniería Civil",
    "Derecho",
    "Ingeniería Industrial",
    "Arquitectura",
    "Ingeniería de Sistemas",
    "Administración",
    "Contabilidad",
    "Educación",
    "Enfermería",
    "Ingeniería Mecánica",
    "Administración de Negocios Internacionales",
    "Gestión Administrativa",
    "Gestión Logística"
]

instituciones_disponibles = [
    "Universidad Peruana de Ciencias Aplicadas (UPC)",
    "Universidad Científica del Sur",
    "Pontificia Universidad Católica del Perú (PUCP)",
    "Servicio Nacional de Adiestramiento en Trabajo Industrial (SENATI)",
    "Universidad Peruana Cayetano Heredia",
    "Universidad Continental",
    "Universidad Nacional San Antonio Abad del Cusco",
    "EEST Privada ADEX",
    "Universidad Nacional Mayor de San Marcos",
    "Universidad Nacional de Ingeniería"
]

departamentos_peru = [
    "Lima", "Puno", "Cusco", "Junín", "Cajamarca", "Ayacucho", 
    "Arequipa", "La Libertad", "Piura", "Huánuco", "Áncash", 
    "Loreto", "Apurímac", "San Martín", "Huancavelica", "Lambayeque",
    "Ica", "Amazonas", "Ucayali", "Pasco", "Tacna", "Callao", 
    "Tumbes", "Madre de Dios", "Moquegua"
]

# Algunos países para becas internacionales (inventado)
paises_internacionales = [
    "España", "Chile", "Argentina", "Colombia", "México", "Brasil"
]

lugares = departamentos_peru + paises_internacionales

nombres_becas = [
    "Beca 18",
    "Beca Tec",
    "Beca Permanencia",
    "Beca Inclusión",
    "Beca Vocación de Maestro"
]

categorias_becas = [
    "Pregrado",
    "Posgrado Maestria",
    "Posgrado Doctorado",
    "Especiales"
]

generos = ["Masculino", "Femenino"]

estratos_socioeconomicos = ["Pobre", "Pobre Extremo", "No pobre"]

estados_migracion = ["Migro", "No Migro", "No aplica"]

# Años de convocatoria disponibles
anios = [2023, 2024, 2025]

# Generar dataset de 200 becarios
num_becarios = 200
random.seed(42)  # Para reproducibilidad

datos = []

for i in range(num_becarios):
    # Seleccionar tipo de beca
    nombre_beca = random.choice(nombres_becas)
    
    # Asignar categoría según tipo de beca
    if nombre_beca == "Beca 18":
        categoria = "Pregrado"
    elif nombre_beca == "Beca Tec":
        categoria = random.choice(["Pregrado", "Especiales"])
    elif nombre_beca == "Beca Permanencia":
        categoria = "Pregrado"
    elif nombre_beca == "Beca Inclusión":
        categoria = "Especiales"
    elif nombre_beca == "Beca Vocación de Maestro":
        categoria = random.choice(["Pregrado", "Posgrado Maestria"])
    else:
        categoria = random.choice(categorias_becas)
    
    # Asignar año (mayormente 2023, algunos 2024-2025)
    if i < 150:
        anio = 2023
    elif i < 180:
        anio = 2024
    else:
        anio = 2025
    
    # Seleccionar institución
    institucion = random.choice(instituciones_disponibles)
    
    # Seleccionar carrera
    carrera = random.choice(carreras_disponibles)
    
    # Seleccionar lugar (mayormente Perú, algunos internacional)
    if random.random() < 0.95:  # 95% en Perú
        lugar = random.choice(departamentos_peru)
        # Si estudia en su región, menor probabilidad de migración
        migracion = random.choices(
            estados_migracion, 
            weights=[30, 70, 0], 
            k=1
        )[0]
    else:  # 5% internacional
        lugar = random.choice(paises_internacionales)
        migracion = "No aplica"  # Para estudios internacionales
    
    # Género
    genero = random.choice(generos)
    
    # Estrato socioeconómico (mayormente pobres según los datos)
    estrato = random.choices(
        estratos_socioeconomicos,
        weights=[60, 30, 10],  # Mayoría pobre
        k=1
    )[0]
    
    # Crear registro
    registro = {
        "NombreBeca": nombre_beca,
        "Institucion": institucion,
        "Carrera": carrera,
        "Lugar": lugar,
        "CategoriaDeBecas": categoria,
        "Anio_Convocatoria": anio,
        "Genero": genero,
        "EstratoSocieconomico": estrato,
        "BecasSegunMigracion": migracion
    }
    
    datos.append(registro)

# Crear DataFrame
df = pd.DataFrame(datos)

# Ordenar por año y nombre de beca
df = df.sort_values(["Anio_Convocatoria", "NombreBeca"], ascending=[True, True])
df = df.reset_index(drop=True)

# Guardar en Excel
nombre_archivo = "dataset_becarios_completo.xlsx"
df.to_excel(nombre_archivo, index=False, sheet_name="Becarios")

print(f"✅ Archivo Excel generado: {nombre_archivo}")
print(f"📊 Total de registros: {len(df)}")
print("\n" + "="*80)
print("DATOS INVENTADOS/GENERADOS (para tu exposición):")
print("="*80)

print("\n1. CAMPOS COMPLETAMENTE INVENTADOS:")
print("   - Género: Asignado aleatoriamente (50% Masculino, 50% Femenino)")
print("     Los datos originales NO contenían información de género")

print("\n2. CAMPOS PARCIALMENTE INVENTADOS:")
print("   - NombreBeca: Se agregaron becas adicionales:")
print("     * Beca Tec, Beca Permanencia, Beca Inclusión, Beca Vocación de Maestro")
print("     Solo 'Beca 18' estaba documentada en los datos originales de 2023")
print()
print("   - Año_Convocatoria: Se agregaron años 2024 y 2025")
print("     Solo 2023 estaba documentado en los datos originales")
print("     Distribución: 75% año 2023, 15% año 2024, 10% año 2025")
print()
print("   - CategoriaDeBecas: Clasificación según las opciones solicitadas:")
print("     * Pregrado (mayoría)")
print("     * Posgrado Maestria")
print("     * Posgrado Doctorado")
print("     * Especiales")
print("     Los datos originales solo mencionaban 'Pregrado' y 'Especiales'")
print()
print("   - BecasSegunMigracion: Estados generados:")
print("     * 'Migro' (~30% para estudios en Perú)")
print("     * 'No Migro' (~70% para estudios en Perú)")
print("     * 'No aplica' (para estudios internacionales)")
print("     Solo había referencias generales a migración (88.9% migraban a Lima)")

print("\n3. CAMPOS AMPLIADOS:")
print("   - Lugar (antes Departamento): Se agregaron países internacionales:")
print("     * España, Chile, Argentina, Colombia, México, Brasil")
print("     Los datos originales solo contenían departamentos del Perú")
print("     Distribución: 95% en Perú, 5% internacional")
print()
print("   - EstratoSocieconomico: Se agregó categoría 'No pobre' (~10%)")
print("     Los datos originales solo mencionaban 'Pobre' y 'Pobre Extremo'")
print()
print("   - Instituciones: Se agregaron algunas instituciones adicionales")
print("     a las 7 principales documentadas en los datos originales")

print("\n4. DATOS REALES DE LOS ARCHIVOS ORIGINALES:")
print("   - Carreras principales (Top 9 de Beca 18-2023)")
print("   - Instituciones principales (Top 7 de Beca 18-2023)")
print("   - Departamentos del Perú (25 departamentos con sus porcentajes)")
print("   - Estratos: Pobre y Pobre Extremo")
print("   - Total de becarios Beca 18-2023: 4,998")

print("\n" + "="*80)
print("NOTA IMPORTANTE PARA TU EXPOSICIÓN:")
print("="*80)
print("""
Los datos se basaron en la Memoria Anual del PRONABEC 2022 (Beca 18-2023).
El dataset generado combina:
- Datos reales extraídos de los documentos oficiales
- Datos generados algorítmicamente para completar campos faltantes
- Extrapolaciones lógicas basadas en patrones típicos de becas

Este dataset es DEMOSTRATIVO y debe usarse solo con fines educativos.
Para análisis serios, se debe obtener la base de datos oficial del PRONABEC.
""")

print("\n📁 Estadísticas del dataset generado:")
print(df.groupby("NombreBeca").size())
print("\nDistribución por categoría:")
print(df.groupby("CategoriaDeBecas").size())
print("\nDistribución por año:")
print(df.groupby("Anio_Convocatoria").size())
print("\nDistribución por género:")
print(df.groupby("Genero").size())
print("\nDistribución por estrato:")
print(df.groupby("EstratoSocieconomico").size())
