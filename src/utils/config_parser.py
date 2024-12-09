import configparser


def parse_properties(filepath):
    """Parses a .properties file and returns a dictionary of key-value pairs."""
    properties = {}
    
    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()
            # Ignore empty lines and comments
            if line and not line.startswith('#'):
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Convert to integer if value is a digit
                    if value.isdigit():
                        properties[key] = int(value)
                    else:
                        properties[key] = value  # Keep as string for non-numeric values
                        
    return properties