import sys

from main_eurostat import main as run_eurostat
from main_ine import main as run_ine
from mainstats import main as run_stats
from banner import print_banner


def main():
    """Run the project from the command line.

    Usage:
        python main.py [eurostat|ine] [extra options]

    Examples:
        python main.py eurostat
        python main.py eurostat --country1 ES --country2 PT
        python main.py ine
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py [eurostat|ine]")
        sys.exit(1)

    source = sys.argv[1].lower()

    # Remove the selected source from sys.argv before delegating
    # so that submodules can parse only their own arguments.
    sys.argv = [sys.argv[0]] + sys.argv[2:]

    if source == "eurostat":
        run_eurostat()
    elif source == "ine":
        run_ine()
    elif source == "stats":              
        run_stats()
    else:
        print("Invalid option. Use 'eurostat' or 'ine'.")
        sys.exit(1)


if __name__ == "__main__":
    main()