import json
import base64
import os
from utils.logger import get_logger

logger = get_logger(__name__)

def load_vin_config():
    """
    Load VIN numbers from the config list
    """
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sources_config = os.path.join(current_dir, 'vins', 'vin.txt')

    with open(sources_config) as file:
        lines = [line.rstrip() for line in file]

    return lines

def lambda_handler(event, context):
    """
    AWS Lambda function to check if VIN Numbers are valid from a Kinesis stream.

    Args:
        event (dict): The input event from the Kinesis stream.
        context (object): The Lambda context object (not used in this function).

    Returns:

        A response with statusCode and results from this check
    """
    
    # Load VIN numbers from the configuration file
    valid_vins = load_vin_config()

    for record in event['Records']:
        # Decode Kinesis record payload from base64
        base64_encoded_payload = record['kinesis']['data']
        decoded_bytes = base64.b64decode(base64_encoded_payload)
        raw_payload = decoded_bytes.decode('utf-8')
        decoded_payload = json.loads(raw_payload)

        vin = decoded_payload.get('vin', '')

        if vin in valid_vins:
            response = {
                'statusCode': 200,
                'body': json.dumps(decoded_payload)
            }
        else:
            response = {
                'statusCode': 400,
                'body': "The VIN number is not valid"
            }

        logger.info(response)
        return response
