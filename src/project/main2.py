import pandas as pd
from ineapy import INEConsultor
import re

consultor = INEConsultor()

# Table 25173: IPV by Autonomous Community, annual, base 2015=100
data = consultor.get_table_data(id_table=25173)

df_ine = pd.DataFrame(data)

df_ine['name_table'] = df_ine['name_table'].str.strip()

# Split on '. ' only when followed by a capital letter, max 2 splits
df_ine[['region', 'metric', 'dwelling']] = df_ine['name_table'].str.split(r'\. (?=[A-ZÁÉÍÓÚÜ])', n=2, expand=True)
df_ine['dwelling'] = df_ine['dwelling'].str.rstrip('. ')

# Filter
df_ine = df_ine[df_ine['unidad'] == 'Índice']
df_ine = df_ine[df_ine['metric'] == 'Media anual']

# Keep relevant columns
df_ine = df_ine[['region', 'dwelling', 'year', 'value']]

print(df_ine)