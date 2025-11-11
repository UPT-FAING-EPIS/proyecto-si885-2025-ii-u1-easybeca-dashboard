import pandas as pd
import os

def generar_reporte_excel():
    """
    Lee el archivo CSV consolidado y genera un reporte en formato Excel
    con las columnas solicitadas, guardándolo en la ruta de OneDrive.
    """
    archivo_csv = 'becas_instituciones_completo.csv'
    
    # --- INICIO DE LA MODIFICACIÓN ---
    
    # 1. Definir el directorio de destino de OneDrive
    directorio_destino = r"C:\Users\Andy\OneDrive - UNIVERSIDAD PRIVADA DE TACNA\Datos Power BI"
    
    # 2. Definir el nombre del archivo
    nombre_archivo = 'reporte_becas.xlsx'
    
    # 3. Combinar ambos para crear la ruta completa
    archivo_excel = os.path.join(directorio_destino, nombre_archivo)
    
    # --- FIN DE LA MODIFICACIÓN ---

    if not os.path.exists(archivo_csv):
        print(f"✗ Error: No se encontró el archivo de origen '{archivo_csv}'.")
        print("Por favor, ejecuta primero los scripts de generación de datos.")
        return

    print(f"Leyendo datos desde '{archivo_csv}'...")
    df = pd.read_csv(archivo_csv)

    # Mapeo de columnas existentes y creación de las nuevas
    reporte_df = pd.DataFrame({
        'NombreBeca': df.get('nombre_beca', pd.Series(index=df.index, dtype=str)),
        'Institucion': df.get('nombre_institucion', pd.Series(index=df.index, dtype=str)),
        'Facultad/Escuela': 'No disponible',
        'Carrera': df.get('programa', pd.Series(index=df.index, dtype=str)),
        'Departamento': df.get('region', pd.Series(index=df.index, dtype=str)),
        'Categoria de becas': df.get('tipo_instituciones', pd.Series(index=df.index, dtype=str)),
        'Anio_Convocatoria': 'No disponible'
    })

    # Llenar valores nulos por si alguna columna no existiera en el CSV
    reporte_df.fillna('No disponible', inplace=True)

    # --- INICIO DE LA MODIFICACIÓN (Buena práctica) ---
    # Asegurarse de que el directorio de OneDrive exista antes de guardar
    try:
        os.makedirs(directorio_destino, exist_ok=True)
    except Exception as e:
        print(f"✗ Error al crear el directorio '{directorio_destino}': {e}")
        return
    # --- FIN DE LA MODIFICACIÓN ---

    print(f"Guardando reporte en '{archivo_excel}'...") # Esta línea ahora imprime la ruta completa
    try:
        reporte_df.to_excel(archivo_excel, index=False)
        print(f"✓ Reporte de Excel '{archivo_excel}' generado con éxito.")
        print(f"  Total de registros: {len(reporte_df)}")
    except Exception as e:
        print(f"✗ Error al guardar el archivo de Excel: {e}")
        print("  Asegúrate de no tener el archivo abierto en Excel.")

if __name__ == "__main__":
    generar_reporte_excel()