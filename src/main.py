import sys

from main_eurostat import main as run_eurostat
from main_ine import main as run_ine


def main():
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