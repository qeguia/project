import pandas as pd


def get_spain_series(df_long: pd.DataFrame) -> pd.DataFrame:
    """Filter the dataset to include only Spain observations.

    Args:
        df_long: Long-format DataFrame containing at least a 'geo' column
            with country codes.

    Returns:
        A DataFrame containing only rows where the country code is 'ES'
        (Spain), preserving the original structure.
    """
    return df_long[df_long['geo'] == 'ES'].copy()


def get_eu_average(df_long: pd.DataFrame) -> pd.DataFrame:
    """Compute the average HPI across EU countries for each year.

    Only rows with two-letter country codes are considered, excluding
    aggregated regions or non-country entries.

    Args:
        df_long: Long-format DataFrame containing columns 'geo', 'year',
            and 'hpi'.

    Returns:
        A DataFrame with one row per year containing the mean HPI across
        all countries, with an added 'geo' value set to 'EU Avg'.
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
    """Create a dataset comparing Spain with the EU average.

    This function combines the Spain-specific series with the computed
    EU average into a single DataFrame suitable for visualization.

    Args:
        df_long: Long-format DataFrame containing HPI data with columns
            such as 'geo', 'year', and 'hpi'.

    Returns:
        A DataFrame containing both Spain ('ES') and EU average ('EU Avg')
        observations, concatenated into a single dataset.
    """
    df_spain = get_spain_series(df_long)
    df_eu_avg = get_eu_average(df_long)

    df_plot = pd.concat([df_spain, df_eu_avg], ignore_index=True)
    return df_plot