import yaml
import pandas as pd
from typing import Dict, Any, Tuple
from utils.logger import get_logger

logger = get_logger(__name__)

def load_mappings_from_file(filepath: str) -> Dict[str, Any]:
    """
    Loads the mappings from a given file.
    
    Args:
        filepath (str): The path to the yml file.
        
    Returns:
        dict: Mappings loaded from the file.
    """
    with open(filepath, 'r') as file:
        try:
            return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Failed to load mappings from {filepath}: {str(e)}")
            return {}


def load_signal_mappings(source_config: str) -> Dict[str, str]:
    """
    Load the signal mappings for a given source from its configuration file.
    
    Args:
        source_config (str): The path to the source configuration yml file.

    Returns:
        dict: Mappings from original signal names to transformed signal names.
    """
    with open(source_config, 'r') as file:
        try:
            mappings = yaml.safe_load(file)
            return mappings.get('signal_mappings', {})
        except Exception as e:
            logger.error(f"Failed to load mappings from {source_config}: {str(e)}")
            return {}

def get_fleet_and_uuid(vehicle_id: str, vehicle_to_fleet: Dict[str, str], fleet_to_uuid: Dict[str, str]) -> Tuple[str, str]:
    """
    Given a vehicleId, returns the fleet ID and UUID associated with it.

    Args:
        vehicle_id (str): The vehicle identification number.
        vehicle_to_fleet (dict): Mappings from vehicleId to fleet ID.
        fleet_to_uuid (dict): Mappings from fleet ID to UUID.

    Returns:
        tuple: The fleet ID and UUID for the vehicle.
    """
    fleet_id = vehicle_to_fleet.get(vehicle_id)
    uuid = fleet_to_uuid.get(fleet_id)
    
    if not fleet_id or not uuid:
        logger.warning(f"Missing mapping for vehicleId: {vehicle_id}. Fleet ID: {fleet_id}, UUID: {uuid}")
        
    return fleet_id, uuid



def cast_value(value: Any, datatype: str) -> Any:
    """
    Cast the value to the given datatype.
    
    Args:
        value (Any): The value to be casted.
        datatype (str): The datatype to cast to.

    Returns:
        Any: The casted value.
    """
    try:
        if datatype == "string":
            return str(value)
        elif datatype == "integer":
            return int(value)
        elif datatype == "double":
            return float(value)
        elif datatype == "datetime":
            return value
        elif datatype == "boolean":
            return value.lower() == "true"
    except ValueError:
        logger.warning(f"Failed to cast value '{value}' to type '{datatype}'. Using original value.")
        
    return value
