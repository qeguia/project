import pyfiglet

def print_banner():
    # Get the version from the file
    version = "1.1.1"
    # Create the banner text
    banner = pyfiglet.figlet_format(f"Housing Affordability v{version}", font="small")

    # Print the header with a border of special characters
    print("#" * 75)
    print(banner) # ASCII art for the program name and version
    print("#" * 75)

print_banner()