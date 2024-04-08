# src/transformers/source_A_transformer.py
import os
from typing import Dict, Any
from datetime import datetime
from utils.utils import load_mappings_from_file, load_signal_mappings, get_fleet_and_uuid, cast_value
from utils.logger import get_logger

# Directory Path Constants
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DIR = os.path.dirname(CURRENT_FILE_DIR)
SOURCES_CONFIG = os.path.join(MAIN_DIR, 'config', 'sources', 'source_A.yml')


# # Constants for the fleet and vehicle mappings
VEHICLE_TO_FLEET_CONFIG = os.path.join(MAIN_DIR, 'config', 'vehicle_to_fleet.yml')
FLEET_TO_UUID_CONFIG = os.path.join(MAIN_DIR, 'config', 'fleet_to_uuid.yml')
        
# # Load the mappings when the module is imported.
VEHICLE_TO_FLEET_MAPPINGS = load_mappings_from_file(VEHICLE_TO_FLEET_CONFIG)

FLEET_TO_UUID_MAPPINGS = load_mappings_from_file(FLEET_TO_UUID_CONFIG)


# Initialize logger
logger = get_logger(__name__)

# # logger.debug("This is a test debug message.")

# Load the mappings when the module is imported.
SIGNAL_MAPPINGS = load_signal_mappings(SOURCES_CONFIG)
def transform_mercedes(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform the data from source_A based on predefined mappings.
    
    Args:
        data (dict): Raw data from source_A to be transformed.
        
    Returns:
        dict: Transformed data.
    """
    transformed_data = {}
    
    # Ensure the required keys exist in the input data to avoid KeyErrors
    if 'data' not in data or 'signals' not in data['data']:
        logger.error("Missing key 'data' or 'signals' in input data.")
        return {}

    # Extract signals from data
    signals = {item['name']: (item['value'], item['type']) for item in data['data']['signals']}

    for original_signal, metadata in SIGNAL_MAPPINGS.items():
        if original_signal in signals:
            value, signal_type = signals[original_signal]
            transformed_data[metadata['transformed_name']] = cast_value(value, signal_type)

    
    # Extracting and processing the timestamp, ensuring it's present and is in milliseconds
    if 'timestamp' in data and isinstance(data['timestamp'], (int, float)):
        timestamp_in_seconds = data['timestamp'] / 1000  # Convert from milliseconds to seconds
        utc_datetime = datetime.utcfromtimestamp(timestamp_in_seconds)
        formatted_utc = utc_datetime.strftime('%Y-%m-%d %H:%M:%S+00:00')
        transformed_data['timestamp'] = formatted_utc
    else:
        logger.warning("Invalid or missing 'timestamp' in input data.")
    
    # TODO add handling for lack of VIN number
    # Extracting VIN
    vin = data.get('vin')
    transformed_data['vin'] = vin

    # Get fleet_id and UUID using VIN
    fleet_id, uuid = get_fleet_and_uuid(vin, VEHICLE_TO_FLEET_MAPPINGS, FLEET_TO_UUID_MAPPINGS)
    transformed_data['fleet_id'] = fleet_id
    transformed_data['uuid'] = uuid

    return transformed_data

