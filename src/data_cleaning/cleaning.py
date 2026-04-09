import eurostat
import pandas as pd
from ineapy import INEConsultor

DATASET = "prc_hpi_a"


def load_eurostat_data(dataset: str = DATASET) -> pd.DataFrame:
    """Fetch raw Eurostat house price index data."""
    print(f"Fetching '{dataset}' from Eurostat ...")
    raw = eurostat.get_data_df(dataset)
    return raw


def clean_eurostat_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning and normalization of Eurostat dataframe."""
    df = raw.drop(columns=['freq'])
    df = df.rename(columns={'geo\\TIME_PERIOD': 'geo'})
    return df


def prepare_hpi_long(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter to all dwellings, base 2010 average,
    and reshape from wide to long format.
    """
    df = df[
        (df['purchase'] == 'TOTAL') &
        (df['unit'] == 'I10_A_AVG')
    ].drop(columns=['purchase', 'unit'])

    df_long = df.melt(id_vars='geo', var_name='year', value_name='hpi')
    df_long['year'] = pd.to_numeric(df_long['year'])
    df_long['hpi'] = pd.to_numeric(df_long['hpi'], errors='coerce')
    df_long = df_long.dropna(subset=['hpi'])

    return df_long


def load_ine_data(table_id: int = 25173) -> pd.DataFrame:
    """Fetch raw INE table data."""
    consultor = INEConsultor()
    data = consultor.get_table_data(id_table=table_id)
    return pd.DataFrame(data)


def clean_ine_data(df_ine: pd.DataFrame) -> pd.DataFrame:
    """Clean INE house price index data."""
    df_ine = df_ine.copy()

    df_ine['name_table'] = df_ine['name_table'].str.strip()

    df_ine[['region', 'metric', 'dwelling']] = df_ine['name_table'].str.split(
        r'\. (?=[A-ZÁÉÍÓÚÜ])',
        n=2,
        expand=True
    )
    df_ine['dwelling'] = df_ine['dwelling'].str.rstrip('. ')

    df_ine = df_ine[df_ine['unidad'] == 'Índice']
    df_ine = df_ine[df_ine['metric'] == 'Media anual']

    df_ine = df_ine[['region', 'dwelling', 'year', 'value']]

    return df_ine