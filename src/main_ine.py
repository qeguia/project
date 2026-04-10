from data_cleaning.cleaning import load_ine_data, clean_ine_data


def main():
    """Run the INE data retrieval and cleaning pipeline.

    This function fetches house price index data from the Spanish
    National Statistics Institute (INE), applies cleaning and filtering
    steps, and prints a preview of the resulting dataset.

    Workflow:
        1. Load raw INE data from the API
        2. Clean and structure the dataset
        3. Display the first rows of the cleaned data

    Returns:
        None
    """
    raw_ine = load_ine_data()
    clean_ine = clean_ine_data(raw_ine)
    print(clean_ine.head())


if __name__ == "__main__":
    main()