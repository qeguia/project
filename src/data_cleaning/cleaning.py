import eurostat
import pandas as pd
from ineapy import INEConsultor

DATASET = "prc_hpi_a"


def load_eurostat_data(dataset: str = DATASET) -> pd.DataFrame:
    """Load raw house price index data from Eurostat.

    Args:
        dataset: Eurostat dataset code to retrieve. Defaults to the house
            price index dataset defined in ``DATASET``.

    Returns:
        A raw pandas DataFrame returned by the Eurostat API, containing
        the original columns and values without additional cleaning.
    """
    print(f"Fetching '{dataset}' from Eurostat ...")
    raw = eurostat.get_data_df(dataset)
    return raw


def clean_eurostat_data(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardize the raw Eurostat dataset.

    This function removes columns that are not needed for the analysis
    and renames the geographic identifier column to a simpler name.

    Args:
        raw: Raw Eurostat DataFrame as returned by ``load_eurostat_data``.

    Returns:
        A cleaned DataFrame without the ``freq`` column and with the
        column ``geo\\TIME_PERIOD`` renamed to ``geo``.
    """
    df = raw.drop(columns=['freq'])
    df = df.rename(columns={'geo\\TIME_PERIOD': 'geo'})
    return df


def prepare_hpi_long(df: pd.DataFrame) -> pd.DataFrame:
    """Filter and reshape Eurostat HPI data into long format.

    The function keeps only observations for total dwellings and for the
    annual index with base year 2010 average. It then converts the data
    from wide format, where years are stored as columns, into long format
    with one row per geographic unit and year.

    Args:
        df: Cleaned Eurostat DataFrame containing at least the columns
            ``geo``, ``purchase``, ``unit``, and yearly HPI values.

    Returns:
        A long-format DataFrame with columns ``geo``, ``year``, and
        ``hpi``, where ``year`` is numeric and invalid HPI values have
        been removed.
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
    """Load raw house price index data from the INE API.

    Args:
        table_id: Identifier of the INE table to retrieve.

    Returns:
        A pandas DataFrame containing the raw table data returned by the
        INE API.
    """
    consultor = INEConsultor()
    data = consultor.get_table_data(id_table=table_id)
    return pd.DataFrame(data)


def clean_ine_data(df_ine: pd.DataFrame) -> pd.DataFrame:
    """Clean and filter the INE house price index dataset.

    This function standardizes the table labels, splits the composite
    ``name_table`` field into separate descriptive columns, keeps only
    annual index values, and selects the variables needed for analysis.

    Args:
        df_ine: Raw INE DataFrame returned by ``load_ine_data``.

    Returns:
        A cleaned DataFrame containing the columns ``region``,
        ``dwelling``, ``year``, and ``value``, filtered to annual index
        observations only.
    """
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