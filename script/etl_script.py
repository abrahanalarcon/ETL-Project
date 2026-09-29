import pandas as pd
from sqlalchemy import create_engine
import urllib

# Parámetros de conexión
params = urllib.parse.quote_plus(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=MSI;"
    "DATABASE=EnergiaDB;"
    "Trusted_Connection=yes;"
)

# Crear engine
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)

# Cargar dataset
df = pd.read_csv('data/World Energy Consumption.csv')

print("Columnas disponibles:", df.columns)
print("Primeras filas:")
print(df.head())

# Energías que queremos transformar
energy_sources = ['biofuel', 'coal', 'gas', 'hydro', 'nuclear', 'oil', 'other_renewables', 'solar', 'wind']

# Crear DataFrame normalizado
data = []
for energy in energy_sources:
    consumption_col = f"{energy}_consumption"
    production_col = f"{energy}_electricity"
    
    if consumption_col in df.columns or production_col in df.columns:
        temp_df = df[['country', 'year']].copy()
        temp_df['energy_type'] = energy
        temp_df['consumption'] = df.get(consumption_col)
        temp_df['production'] = df.get(production_col)
        data.append(temp_df)

df_energy = pd.concat(data, ignore_index=True).dropna(subset=['consumption', 'production'])

# Renombrar columnas
df_energy.rename(columns={
    'country': 'country_name',
}, inplace=True)

# Crear dimensión de países
countries = df_energy[['country_name']].drop_duplicates().reset_index(drop=True)
countries['country_id'] = countries.index + 1

# Crear dimensión de tipo de energía
energy_types = df_energy[['energy_type']].drop_duplicates().reset_index(drop=True)
energy_types['energy_type_id'] = energy_types.index + 1

# Asociar IDs
df_energy = df_energy.merge(countries, on='country_name')
df_energy = df_energy.merge(energy_types, on='energy_type')

# Crear tabla de hechos
fact = df_energy[['country_id', 'energy_type_id', 'year', 'consumption', 'production']]

# Cargar a SQL Server
countries.to_sql('countries', engine, if_exists='replace', index=False)
energy_types.to_sql('energy_types', engine, if_exists='replace', index=False)
fact.to_sql('energy_consumption', engine, if_exists='replace', index=False)

print("Datos cargados correctamente a SQL Server.")
