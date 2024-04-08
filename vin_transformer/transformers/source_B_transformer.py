# src/transformers/source_B_transformer.py

import yaml
import os
import time
from typing import Dict, Any
from datetime import datetime

# logger.py module provides get_logger function
from src.utils.logger import get_logger

from src.utils.utils import load_mappings_from_file, load_signal_mappings, get_fleet_and_uuid, cast_value


# Directory Path Constants
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(CURRENT_FILE_DIR)
PROJECT_ROOT = os.path.dirname(SRC_DIR)
SOURCES_CONFIG = os.path.join(PROJECT_ROOT, 'config', 'sources', 'source_B.yml')

# Constants for the fleet and vehicle mappings
VEHICLE_TO_FLEET_CONFIG = os.path.join(PROJECT_ROOT, 'config', 'vehicle_to_fleet.csv')
FLEET_TO_UUID_CONFIG = os.path.join(PROJECT_ROOT, 'config', 'fleet_to_uuid.csv')
        
# Load the mappings when the module is imported.
VEHICLE_TO_FLEET_MAPPINGS = load_mappings_from_file(VEHICLE_TO_FLEET_CONFIG)
FLEET_TO_UUID_MAPPINGS = load_mappings_from_file(FLEET_TO_UUID_CONFIG)

# Initialize logger
logger = get_logger(__name__)

# Load the mappings when the module is imported.
SIGNAL_MAPPINGS = load_signal_mappings(SOURCES_CONFIG)

def transform_source_B(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transform the data from source_B based on predefined mappings.
    
    Args:
        data (dict): Raw data from source_B to be transformed.
        
    Returns:
        dict: Transformed data.
    """
    transformed_data = {}

    signals = data.get('data', {})

    last_known_location = signals.get("vehicle.location.lastKnown", {})
    if last_known_location:
        timestamp_str = last_known_location.get("recordedAt")
        if timestamp_str:
            try:
                utc_datetime = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                transformed_data['timestamp'] = utc_datetime.strftime('%Y-%m-%d %H:%M:%S+00:00')
            except ValueError:
                logger.warning("Invalid 'recordedAt' timestamp format in input data.")

        # Convert 'long' and 'lat' to float
        longitude = last_known_location.get('long')
        latitude = last_known_location.get('lat')
        
        transformed_data['long'] = cast_value(longitude, "double") if longitude else None
        transformed_data['lat'] = cast_value(latitude, "double") if latitude else None

    odometer_data = signals.get("vehicle.odometer", {})
    if odometer_data:
        odometer_value = odometer_data.get('value')
        transformed_data['odometer_value'] = cast_value(odometer_value, "integer") if odometer_value is not None else None
        # transformed_data['odometer_recordedAt'] = odometer_data.get('recordedAt')  # commented out as it's not used

    # Extracting vehicleId
    vin = data.get('vehicleId')
    transformed_data['vehicleId'] = vin

    # Get fleet_id and UUID using vehicleId
    fleet_id, uuid = get_fleet_and_uuid(vin, VEHICLE_TO_FLEET_MAPPINGS, FLEET_TO_UUID_MAPPINGS)
    transformed_data['fleet_id'] = fleet_id
    transformed_data['uuid'] = uuid

    
    return transformed_data



# For testing or debugging
# if __name__ == '__main__':
#     sample_data = {
#         "fleetId": "string",
#         "vehicleId": "string",
#         "data": {
#             "vehicle.odometer": {
#             "recordedAt": "2023-08-21T10:02:55.668Z",
#             "value": 10000,
#             "unit": "km"
#             }
#         }
#         }
    #     "fleetId": "string",
    #     "vehicleId": "string",
    #     "data": {
    #         "vehicle.location.lastKnown": {
    #             "recordedAt": "2023-08-21T10:02:55.656Z",
    #             "long": "55.613306",
    #             "lat": "12.976209",
    #             "unit": "degrees"
    #         }
    #     }
    # }
#     print(transform_source_B(sample_data))







