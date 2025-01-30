import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from utils.config_parser import *


def test_config_parser():
    """Test the add function."""
    properties = parse_properties("../src/resources/config/default_config.property")
    print(properties)
