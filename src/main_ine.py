from data_cleaning.cleaning import load_ine_data, clean_ine_data


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

    print("Cleaned INE dataset preview:")
    print(clean_ine.head())
    print("\nRows:", len(clean_ine))
    print("Columns:", list(clean_ine.columns))


if __name__ == "__main__":
    main()