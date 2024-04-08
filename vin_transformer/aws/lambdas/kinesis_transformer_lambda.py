import json
import base64
from transformers.mercedes_transformer import transform_mercedes
from transformers.bmw_transformer import transform_bmw


def lambda_handler(event, context):
    """
    AWS Lambda function to transform data ingested from a Kinesis stream based on the data source.

    Args:
        event (dict): The input event from the Kinesis stream. Should contain the 'source' key to identify data source.
        context (object): The Lambda context object (not used in this function).

    Returns:
        dict: A dictionary containing transformed records, structured for Kinesis Firehose delivery to an S3 bucket.
    """
    
    transformed_records = []
    
    for record in event['records']:
        
        # Extract Kinesis record payload
        kinesis_record = record['kinesis']

        # Decode Kinesis record payload from base64
        base64_encoded_payload = kinesis_record['data']
        decoded_bytes = base64.b64decode(base64_encoded_payload)

        # Convert the bytes back to a string and parse as JSON
        raw_payload = decoded_bytes.decode('utf-8')
        decoded_payload = json.loads(raw_payload)

        # Extract source from the event
        # Defaulting to 'source_A' if no source is specified
        source = decoded_payload.get('source', 'source_A')  
        service = 'all'
        
        # Special handling for 'mercedes' source
        if source == 'mercedes':
            service = decoded_payload['data'].get('serviceId', 'all')

        # Map sources to their transformation functions
        transformation_map = {
            'source_A': transform_mercedes,
            'bmw': transform_bmw
        }

        # Get the appropriate transformation function
        transform_function = transformation_map.get(source, transform_mercedes)  # Default to transform_source_A

        # Apply the transformation function based on the source
        transformed_data = transform_function(decoded_payload)

        # Additional handling for 'bmw' source
        if source == 'bmw':
            date = decoded_payload.get('date', '')
            transformed_data['timestamp'] = date

        # Define partition keys for the output record
        partition_keys = {
            "uuid": transformed_data.get('uuid', "unknown"),
            "brand": source,
            "service": service
        }

        # Build the output record
        output_record = {
            'recordId': decoded_payload['messageId'],
            'result': 'Ok',
            'data': base64.b64encode(json.dumps(transformed_data).encode('utf-8') + b'\n').decode('utf-8'),
            'metadata': {'partitionKeys': partition_keys}
        }

        transformed_records.append(output_record)
    
    # Return transformed records to Kinesis Firehose for delivery to S3
    return {'records': transformed_records}
