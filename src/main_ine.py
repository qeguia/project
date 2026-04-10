from data_cleaning.cleaning import load_ine_data, clean_ine_data


def main():
    raw_ine = load_ine_data()
    clean_ine = clean_ine_data(raw_ine)
    print(clean_ine.head())


if __name__ == "__main__":
    main()