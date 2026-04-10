import sys

from main_eurostat import main as run_eurostat
from main_ine import main as run_ine


def main():
    """Run the project from the command line.

    This function acts as an entry point for executing different data
    pipelines based on a command-line argument.

    The user must specify the data source to process:

        - 'eurostat': runs the Eurostat pipeline
        - 'ine': runs the INE pipeline

    Usage:
        python main.py [eurostat|ine]

    Behavior:
        - Calls the corresponding pipeline function
        - Exits with an error message if the input is invalid

    Returns:
        None
    """
    if len(sys.argv) != 2:
        print("Usage: python main.py [eurostat|ine]")
        sys.exit(1)

    source = sys.argv[1].lower()

    if source == "eurostat":
        run_eurostat()
    elif source == "ine":
        run_ine()
    else:
        print("Invalid option. Use 'eurostat' or 'ine'.")
        sys.exit(1)


if __name__ == "__main__":
    main()