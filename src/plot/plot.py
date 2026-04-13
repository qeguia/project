from plotnine import (
    ggplot,
    aes,
    geom_line,
    geom_point,
    labs,
    theme_minimal,
    theme,
)

def plot_spain_vs_eu(df_plot):
    """Create a line plot comparing Spain and the EU average HPI.

    Args:
        df_plot: Long-format DataFrame with columns ``year``, ``hpi``, and
            ``geo``.

    Returns:
        A plotnine ``ggplot`` object.
    """
    return (
        ggplot(df_plot, aes(x='year', y='hpi', color='geo'))
        + geom_line(size=1.2)
        + geom_point(size=2)
        + labs(
            title='House Price Index: Spain vs EU Average',
            subtitle='All dwellings | Base year 2010 = 100 | Source: Eurostat (prc_hpi_a)',
            x='Year',
            y='HPI (2010 = 100)',
            color='Series'
        )
        + theme_minimal()
        + theme(figure_size=(10, 5))
    )

def plot_country_comparison(df_plot, country_1: str, country_2: str):
    """Create a ggplot line chart comparing two countries.

    Args:
        df_plot: Long-format DataFrame with columns ``year``, ``hpi``, and
            ``geo``.
        country_1: First country code.
        country_2: Second country code.

    Returns:
        A plotnine ``ggplot`` object.
    """
    country_1 = country_1.upper()
    country_2 = country_2.upper()

    return (
        ggplot(df_plot, aes(x='year', y='hpi', color='geo'))
        + geom_line(size=1.2)
        + geom_point(size=2)
        + labs(
            title=f'House Price Index Comparison: {country_1} vs {country_2}',
            subtitle='All dwellings | Base year 2010 = 100 | Source: Eurostat (prc_hpi_a)',
            x='Year',
            y='HPI (2010 = 100)',
            color='Country'
        )
        + theme_minimal()
        + theme(figure_size=(10, 5))
    )