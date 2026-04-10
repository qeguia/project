from data_cleaning.cleaning import (
    load_eurostat_data,
    clean_eurostat_data,
    prepare_hpi_long,
)
from analysis.analysis import build_spain_vs_eu_dataset
from plot.plot import plot_spain_vs_eu


def main():
    """Run the Eurostat data processing and visualization pipeline.

    This function executes the full workflow for Eurostat house price
    index (HPI) data, including data retrieval, cleaning, transformation
    to long format, and visualization.

    The resulting plot compares Spain's HPI with the EU average and is
    displayed using plotnine.

    Workflow:
        1. Load raw Eurostat data
        2. Clean and standardize the dataset
        3. Transform data to long format
        4. Build Spain vs EU comparison dataset
        5. Generate and display the plot

    Returns:
        None
    """
    raw_eurostat = load_eurostat_data()
    clean_eurostat = clean_eurostat_data(raw_eurostat)
    eurostat_long = prepare_hpi_long(clean_eurostat)

    df_plot = build_spain_vs_eu_dataset(eurostat_long)
    p = plot_spain_vs_eu(df_plot)
    print(p)
    p.show()


if __name__ == "__main__":
    main()