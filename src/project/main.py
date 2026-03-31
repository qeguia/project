import eurostat
import pandas as pd
from plotnine import *

DATASET = "prc_hpi_a"

# Retrieving House pricing index from 2005-2024 across all european coutries // move this to init?
print(f"Fetching '{DATASET}' from Eurostat …")
raw = eurostat.get_data_df(DATASET)

# normalizing dataframe
raw = raw.drop(columns=['freq'])
raw = raw.rename(columns={'geo\\TIME_PERIOD': 'geo'})


#first plot

# Filter to existing dwellings + index base 2010 only
df = raw[
    (raw['purchase'] == 'TOTAL') &
    (raw['unit'] == 'I10_A_AVG')
].drop(columns=['purchase', 'unit'])

# Melt wide -> long // prepering for plot
df_long = df.melt(id_vars='geo', var_name='year', value_name='hpi')
df_long['year'] = pd.to_numeric(df_long['year'])
df_long['hpi']  = pd.to_numeric(df_long['hpi'], errors='coerce')
df_long = df_long.dropna(subset=['hpi'])

# Spain series
df_spain = df_long[df_long['geo'] == 'ES']

# EU average (only real country codes, length 2, excluding aggregates like EU, EA)
df_countries = df_long[df_long['geo'].str.len() == 2]
df_eu_avg = (
    df_countries
    .groupby('year', as_index=False)['hpi']
    .mean()
    .assign(geo='EU Avg')
)

# Combining both
df_plot = pd.concat([df_spain, df_eu_avg], ignore_index=True)

# Plot
(
    ggplot(df_plot, aes(x='year', y='hpi', color='geo'))
    + geom_line(size=1.2)
    + geom_point(size=2)
    + scale_color_manual(values={'ES': '#c0392b', 'EU Avg': '#2980b9'})
    + labs(
        title='House Price Index: Spain vs EU Average',
        subtitle='All dwellings | Base year 2010 = 100 | Source: Eurostat (prc_hpi_a)',
        x='Year',
        y='HPI (2010 = 100)',
        color='',
    )
    + theme_minimal()
    + theme(figure_size=(10, 5))
).show()