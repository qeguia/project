import argparse # Python's standard library module for handling command-line inputs. Used so the user can choose countries from the terminal instead of editing the code by hand.

from data_cleaning.cleaning import (
    load_eurostat_data,
    clean_eurostat_data,
    prepare_hpi_long,
)
from analysis.analysis import (
    build_spain_vs_eu_dataset,
    build_country_comparison_dataset,
)
from plot.plot import plot_spain_vs_eu, plot_country_comparison

def main():
    """Run the Eurostat data processing and visualization pipeline.

    By default, the function reproduces the Spain vs EU-average plot.
    Optionally, the user can pass two country codes to generate a direct
    comparison between any two European countries available in the
    Eurostat dataset.

    Example:
        python main.py eurostat --country1 ES --country2 PT
    """
    parser = argparse.ArgumentParser(
        description='Eurostat house price index analysis.'
    )
    parser.add_argument('--country1', type=str, default=None) # Optional first country code. Example: --country1 ES
    parser.add_argument('--country2', type=str, default=None) # Optional second country code. Example: --country2 PT
    args = parser.parse_args() # Read the arguments written in the command line.

    try:
        raw_eurostat = load_eurostat_data()
        clean_eurostat = clean_eurostat_data(raw_eurostat)
        eurostat_long = prepare_hpi_long(clean_eurostat)

        if args.country1 and args.country2:
            valid_countries = set(eurostat_long['geo'].unique())

            if args.country1 not in valid_countries:
                raise ValueError(f"Invalid country code: {args.country1}")

            if args.country2 not in valid_countries:
                raise ValueError(f"Invalid country code: {args.country2}")

            df_plot = build_country_comparison_dataset(
                eurostat_long,
                args.country1,
                args.country2,
            )
            p = plot_country_comparison(df_plot, args.country1, args.country2)

        else:
            df_plot = build_spain_vs_eu_dataset(eurostat_long)
            p = plot_spain_vs_eu(df_plot)

        print(p)
        p.show()

    except ValueError as e:
        print(f"Error: {e}")
        print("Tip: Use valid Eurostat country codes (e.g., ES, PT, FR).")

    except Exception as e:
        print("An unexpected error occurred.")
        print(e)


if __name__ == '__main__':
    main()