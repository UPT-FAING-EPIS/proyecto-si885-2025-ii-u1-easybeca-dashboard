import pandas as pd

# Leer el dataset
df = pd.read_excel('PRONABEC_2024_DATASET_ACTUALIZADO.xlsx', sheet_name='Datos_Becarios')

print('='*80)
print('📊 RESUMEN DEL DATASET ACTUALIZADO')
print('='*80)

print(f'\n✅ Total de registros: {len(df)}')

print(f'\n📌 CAMPOS DEL DATASET:')
for i, col in enumerate(df.columns, 1):
    print(f'   {i}. {col}')

print(f'\n🌍 LUGARES (TOP 10):')
print(df['Lugar'].value_counts().head(10).to_string())

print(f'\n📚 CATEGORÍAS DE BECAS:')
print(df['CategoriaDeBecas'].value_counts().to_string())

print(f'\n🏛️ INSTITUCIONES (TOP 5):')
print(df['Institucion'].value_counts().head(5).to_string())

print(f'\n🎓 CARRERAS (TOP 5):')
print(df['Carrera'].value_counts().head(5).to_string())

print(f'\n👥 GÉNERO:')
print(df['Genero'].value_counts().to_string())

print(f'\n💰 ESTRATO SOCIOECONÓMICO:')
print(df['EstratoSocioeconomico'].value_counts().to_string())

print(f'\n✈️ MIGRACIÓN:')
print(df['BecasSegunMigracion'].value_counts().to_string())

print('\n' + '='*80)

# Identificar lugares extranjeros
departamentos_peru = ['Lima', 'Ica', 'Callao', 'Cusco', 'Piura', 'Arequipa', 'La Libertad', 
                     'Lambayeque', 'Junín', 'Puno', 'Cajamarca', 'Ancash', 'Apurímac', 
                     'Huánuco', 'San Martín', 'Ayacucho', 'Loreto', 'Ucayali', 'Amazonas',
                     'Huancavelica', 'Pasco', 'Tumbes', 'Tacna', 'Madre de Dios', 'Moquegua']

lugares_extranjeros = df[~df['Lugar'].isin(departamentos_peru)]

print(f'🌎 ESTUDIOS EN EL EXTRANJERO: {len(lugares_extranjeros)} becarios ({len(lugares_extranjeros)/len(df)*100:.1f}%)')
print(f'\n🌍 PAÍSES DESTINO:')
if len(lugares_extranjeros) > 0:
    print(lugares_extranjeros['Lugar'].value_counts().to_string())
else:
    print('   (ninguno)')

print('\n' + '='*80)
print('📄 VISTA PREVIA DE REGISTROS CON ESTUDIOS EN EL EXTRANJERO:')
print('='*80)
if len(lugares_extranjeros) > 0:
    print(lugares_extranjeros[['NombreBeca', 'Lugar', 'CategoriaDeBecas', 'Carrera']].head(10).to_string(index=False))
else:
    print('   (ninguno)')

print('\n' + '='*80)
print('✅ ARCHIVO GENERADO: PRONABEC_2024_DATASET_ACTUALIZADO.xlsx')
print('📋 Hojas del archivo:')
print('   1. Datos_Becarios - 727 registros con 9 campos')
print('   2. Reporte_Datos_Inventados - Desglose de datos reales vs inventados')
print('   3. Estadisticas - Resumen estadístico del dataset')
print('='*80)
