from plotnine import (
    ggplot, aes, geom_line, geom_point, scale_color_manual,
    labs, theme_minimal, theme
)

def plot_spain_vs_eu(df_plot):
    """Create a line plot comparing Spain and the EU average HPI.

    The function generates a line chart with points showing the evolution
    of the house price index (HPI) over time for Spain and the EU average.

    Args:
        df_plot: Long-format DataFrame containing at least the columns
            ``year``, ``hpi``, and ``geo``. The ``geo`` column is expected
            to include the values 'ES' (Spain) and 'EU Avg'.

    Returns:
        A plotnine ``ggplot`` object representing the comparison between
        Spain and the EU average over time.
    """
    p = (
        ggplot(df_plot, aes(x='year', y='hpi', color='geo'))
        + geom_line(size=1.2)
        + geom_point(size=2)
        + scale_color_manual(values={'ES': '#c0392b', 'EU Avg': '#2980b9'})
        + labs(
            title='House Price Index: Spain vs EU Average',
            subtitle='All dwellings | Base year 2010 = 100 | Source: Eurostat (prc_hpi_a)',
            x='Year',
            y='HPI (2010 = 100)',
            color=''
        )
        + theme_minimal()
        + theme(figure_size=(10, 5))
    )
    return p