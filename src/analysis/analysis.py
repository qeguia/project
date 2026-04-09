import pandas as pd


def get_spain_series(df_long: pd.DataFrame) -> pd.DataFrame:
    """Extract Spain series from long-format HPI dataframe."""
    return df_long[df_long['geo'] == 'ES'].copy()


def get_eu_average(df_long: pd.DataFrame) -> pd.DataFrame:
    """
    Compute EU average using only real country codes
    (2-letter codes), excluding aggregates.
    """
    df_countries = df_long[df_long['geo'].str.len() == 2].copy()

    df_eu_avg = (
        df_countries
        .groupby('year', as_index=False)['hpi']
        .mean()
        .assign(geo='EU Avg')
    )
    return df_eu_avg


def build_spain_vs_eu_dataset(df_long: pd.DataFrame) -> pd.DataFrame:
    """Combine Spain series with EU average for plotting."""
    df_spain = get_spain_series(df_long)
    df_eu_avg = get_eu_average(df_long)

    df_plot = pd.concat([df_spain, df_eu_avg], ignore_index=True)
    return df_plot