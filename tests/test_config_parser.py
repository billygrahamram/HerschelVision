
from src.utils.config_parser import *

def test_config_parser():
    """Test the add function."""
    properties = parse_properties('../src/resources/config/default_config.property')
    print(properties)