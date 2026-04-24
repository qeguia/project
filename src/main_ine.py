from data_cleaning.cleaning import load_ine_data, clean_ine_data
from plotnine import ggplot, aes, geom_bar, theme, element_text, labs, position_dodge
import pandas as pd


def main():
    """Run the INE data retrieval and cleaning pipeline.

    This function fetches house price index data from the Spanish
    National Statistics Institute (INE), applies cleaning and filtering
    steps, and prints a preview of the resulting dataset.

    We are not generating plots from INE here because the cleaned output
    is being used only as a supporting dataset in the project, while the
    main visual analysis is done with Eurostat data.

    Returns:
        None
    """
    raw_ine = load_ine_data()
    clean_ine = clean_ine_data(raw_ine)

    plot = (
        ggplot(clean_ine, aes(x='region', y='value', fill='dwelling'))
        + geom_bar(stat='identity', position=position_dodge())
        + labs(
            title='Housing Price Index by Region (2025)',
            x='Region',
            y='Value',
            fill='Dwelling Type'
        )
        + theme(
            axis_text_x=element_text(rotation=90, hjust=1),
            figure_size=(12, 6)
        )
    ).show()

    if __name__ == "__main__":
        main()
