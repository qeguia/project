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

def get_country_series(df_long: pd.DataFrame, country_code: str) -> pd.DataFrame:
    """Filter the dataset for a single country code.

    Args:
        df_long: Long-format Eurostat DataFrame.
        country_code: Two-letter Eurostat country code such as 'ES' or 'PT'.

    Returns:
        A copy of the subset corresponding to the selected country.

    Raises:
        ValueError: If the provided country code is not present.
    """
    country_code = country_code.upper()
    df_country = df_long[df_long['geo'] == country_code].copy()

    if df_country.empty:
        raise ValueError(
            f"Country code '{country_code}' was not found in the Eurostat dataset."
        )

    return df_country

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

def build_country_comparison_dataset(df_long: pd.DataFrame, country_1: str, country_2: str) -> pd.DataFrame:
    """Create a dataset comparing two European countries.

    Args:
        df_long: Long-format Eurostat DataFrame with columns 'geo', 'year',
            and 'hpi'.
        country_1: First country code.
        country_2: Second country code.

    Returns:
        A DataFrame containing the selected countries only.

    Raises:
        ValueError: If both input countries are the same.
    """
    country_1 = country_1.upper()
    country_2 = country_2.upper()

    if country_1 == country_2:
        raise ValueError('Please choose two different country codes.')

    df_country_1 = get_country_series(df_long, country_1)
    df_country_2 = get_country_series(df_long, country_2)

    return pd.concat([df_country_1, df_country_2], ignore_index=True)

def get_ine_national_series(df_ine: pd.DataFrame) -> pd.DataFrame:
    """Extract the national INE time series when available.

    The INE dataset usually contains one aggregate row for the whole of
    Spain. Since its exact label may vary slightly, the function looks for
    region names containing 'Nacional' and falls back to the full dataset
    if no aggregate label is found.

    Args:
        df_ine: Cleaned INE DataFrame.

    Returns:
        A DataFrame suitable for national-level plotting.
    """
    mask_national = df_ine['region'].str.contains('Nacional', case=False, na=False)

    if mask_national.any():
        return df_ine[mask_national].copy()

    return df_ine.copy()