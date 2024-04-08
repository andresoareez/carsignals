import os
from typing import Dict, Any
from utils.logger import get_logger
from utils.utils import load_mappings_from_file, load_signal_mappings, get_fleet_and_uuid, cast_value

# Directory Path Constants
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DIR = os.path.dirname(CURRENT_FILE_DIR)
SOURCES_CONFIG = os.path.join(MAIN_DIR, 'config', 'sources', 'bmw.yml')

# Constants for the fleet and vehicle mappings
VEHICLE_TO_FLEET_CONFIG = os.path.join(MAIN_DIR, 'config', 'vehicle_to_fleet.yml')
FLEET_TO_UUID_CONFIG = os.path.join(MAIN_DIR, 'config', 'fleet_to_uuid.yml')
        
# Load the mappings when the module is imported.
VEHICLE_TO_FLEET_MAPPINGS = load_mappings_from_file(VEHICLE_TO_FLEET_CONFIG)
FLEET_TO_UUID_MAPPINGS = load_mappings_from_file(FLEET_TO_UUID_CONFIG)

# Initialize logger
logger = get_logger(__name__)

# Load the mappings when the module is imported.
SIGNAL_MAPPINGS = load_signal_mappings(SOURCES_CONFIG)

def transform_bmw(data, vin):
    """
    Transform the data from BMW based on predefined mappings.
    
    Args:
        data (dict): Raw data from BMW to be transformed.
        
    Returns:
        dict: Transformed data.
    """
    transformed_data = {}

    
    for item in data:
        print(data)
        if 'key' in item and item['key'] in SIGNAL_MAPPINGS:
            metadata = SIGNAL_MAPPINGS[item['key']]
            if item['value'] is not None:
                transformed_data[metadata['transformed_name']] = cast_value(item['value'], metadata['type'])
    
    transformed_data['vin'] = vin

    # Get fleet_id and UUID using VIN
    fleet_id, uuid = get_fleet_and_uuid(vin, VEHICLE_TO_FLEET_MAPPINGS, FLEET_TO_UUID_MAPPINGS)
    transformed_data['fleet_id'] = fleet_id
    transformed_data['uuid'] = uuid
    return transformed_data

