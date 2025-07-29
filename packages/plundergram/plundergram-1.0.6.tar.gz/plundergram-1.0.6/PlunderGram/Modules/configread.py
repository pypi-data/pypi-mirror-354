#PlunderGram/Modules/configread.py
import configparser
import os

ansi= {
    "conversion": {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "default": "\033[39m",
        "bright_black": "\033[90m",
        "bright_red": "\033[91m",
        "bright_green": "\033[92m",
        "bright_yellow": "\033[93m",
        "bright_blue": "\033[94m",
        "bright_magenta": "\033[95m",
        "bright_cyan": "\033[96m",
        "bright_white": "\033[97m",
    }
}

def load(config_path):
    """
    Loads configuration settings from a specified file and retrieves ANSI color codes based on the configuration.

    Arguments:
        - config_path: A string representing the path to the configuration file.

    Returns:
        - A tuple containing:
            - config_data: A dictionary holding all configuration data organized by sections and options.
            - colors: A dictionary mapping color names to their corresponding ANSI color codes.

    Behavior:
        - Initializes a configuration parser to read the specified configuration file.
        - Checks if the configuration file exists:
            - If the file does not exist, prints an error message.
            - If the file exists, attempts to read the configuration.
                - If the file has no sections, prints a warning message and sets the config to None.
        - Retrieves color names from the 'Colors' section of the configuration file, using fallback values if the keys are not found.
        - Maps the color names to their corresponding ANSI color codes using a predefined conversion dictionary, with defaults for each color.
        - Creates a dictionary to hold all configuration data by iterating through the sections and options in the configuration file.
        - Returns the configuration data and the colors dictionary.
    """
    #initialize default
    defaultval = 0
    # Initialize the configuration parser
    config = configparser.ConfigParser()

    # Check if the config file exists before trying to read it
    if not os.path.exists(config_path):
        print("File not found:", config_path)
    else:
        try:
            # Load the configuration
            config.read(config_path)

            # Check if the configuration file has sections
            if not config.sections():
                print("No sections found in the configuration file. Please check the file content.")
                config = None  # Set config to None if no sections are found
        except IOError:
            print("Error reading the file:", config_path)
    # Fetch color names from the config file
    color = config.get('Colors', 'color', fallback='bright_blue')
 
    # Retrieve ANSI color codes based on the names from the config and load into dict
    colors = {
    'color_code' : ansi['conversion'].get(color, '\033[96m'),  # Default to bright cyan
    }
    # Create a dictionary to hold all configuration data
    # Iterate through sections and options
    config_data = {}
    for section in config.sections():
        config_data[section] = {option: config.get(section, option, fallback=defaultval) for option in config.options(section)}
    return config_data, colors
