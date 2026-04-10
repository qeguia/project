from data_cleaning.cleaning import (
    load_eurostat_data,
    clean_eurostat_data,
    prepare_hpi_long,
    load_ine_data,
    clean_ine_data
)
from analysis.analysis import build_spain_vs_eu_dataset
from plot.plot import plot_spain_vs_eu


def main():
    # Eurostat pipeline
    raw_eurostat = load_eurostat_data()
    clean_eurostat = clean_eurostat_data(raw_eurostat)
    eurostat_long = prepare_hpi_long(clean_eurostat)

    df_plot = build_spain_vs_eu_dataset(eurostat_long)
    p = plot_spain_vs_eu(df_plot)
    print(p)
    p.show()

    # INE pipeline
    raw_ine = load_ine_data()
    clean_ine = clean_ine_data(raw_ine)
    print(clean_ine.head())


if __name__ == "__main__":
    main()